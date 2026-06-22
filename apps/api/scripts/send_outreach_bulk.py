"""
apps/api/scripts/send_outreach_bulk.py

Bulk outreach email sender — Task 5A, Nevumo Claimed Profiles Campaign.

Input CSV columns: email, business_name, claim_token, category
Template: apps/api/scripts/templates/outreach_email_pl.html
Sender: support@nevumo.com via Resend
Rate limit: 100 emails/hour (Resend free tier) → 37s delay between sends
Idempotency: outreach_sequence_log DB table (UNIQUE email + sequence_step)

Run (dry-run test):
  railway run python3.13 -m apps.api.scripts.send_outreach_bulk --dry-run --limit 3

Run (live, step 1):
  railway run python3.13 -m apps.api.scripts.send_outreach_bulk --sequence-step 1 --limit 100
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import hmac
import logging
import os
import time
import urllib.parse
from pathlib import Path

from jinja2 import Template, TemplateError
from sqlalchemy import text

from apps.api.database import SessionLocal

TEMPLATE_PATH: Path = Path(__file__).parent / "templates" / "outreach_email_pl.html"
DEFAULT_CSV: Path = Path(__file__).parent / "outreach_ready.csv"

FROM_EMAIL: str = "Nevumo <support@nevumo.com>"
DEFAULT_DELAY: float = 37.0

SUBJECT_BY_CATEGORY: dict[str, str] = {
    "cleaning": "7 000 osób szuka sprzątania — ktoś inny je bierze",
    "plumbing": "5 400 osób szuka hydraulika — ktoś inny je bierze",
    "massage": "6 900 osób szuka masażu — ktoś inny je bierze",
}
DEFAULT_SUBJECT: str = "7 000 osób szuka sprzątania — ktoś inny je bierze"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def _generate_unsubscribe_url(email: str, secret: str) -> str:
    """Generate HMAC-SHA256 signed unsubscribe URL."""
    token = hmac.new(secret.encode(), email.encode(), hashlib.sha256).hexdigest()
    encoded_email = urllib.parse.quote(email)
    return f"https://nevumo.com/pl/outreach/unsubscribe?email={encoded_email}&token={token}"


def load_template() -> Template:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    return Template(TEMPLATE_PATH.read_text(encoding="utf-8"))


def _is_already_sent(db, email: str, sequence_step: int) -> bool:
    """Check outreach_sequence_log for existing sent record (DB idempotency)."""
    row = db.execute(
        text(
            "SELECT 1 FROM outreach_sequence_log "
            "WHERE email = :email AND sequence_step = :step AND status = 'sent'"
        ),
        {"email": email, "step": sequence_step},
    ).fetchone()
    return row is not None


def _is_unsubscribed(db, email: str) -> bool:
    """Check outreach_unsubscribes table."""
    row = db.execute(
        text("SELECT 1 FROM outreach_unsubscribes WHERE email = :email"),
        {"email": email},
    ).fetchone()
    return row is not None


def _log_to_db(
    db,
    *,
    email: str,
    business_name: str,
    category: str,
    sequence_step: int,
    resend_message_id: str | None,
    status: str,
) -> None:
    """Insert send record into outreach_sequence_log. ON CONFLICT DO NOTHING (idempotent)."""
    db.execute(
        text(
            """
            INSERT INTO outreach_sequence_log
                (email, business_name, category, sequence_step, resend_message_id, status)
            VALUES
                (:email, :business_name, :category, :step, :resend_id, :status)
            ON CONFLICT (email, sequence_step) DO NOTHING
            """
        ),
        {
            "email": email,
            "business_name": business_name,
            "category": category,
            "step": sequence_step,
            "resend_id": resend_message_id,
            "status": status,
        },
    )
    db.commit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk outreach email sender.")
    parser.add_argument("--csv-file", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--sequence-step", type=int, default=1,
                        help="Outreach sequence step (1-4). Default: 1")
    args = parser.parse_args()

    api_key: str = os.environ.get("RESEND_API_KEY", "")
    app_url: str = os.environ.get("APP_URL", "https://www.nevumo.com").rstrip("/")
    hmac_secret: str = os.environ.get("OUTREACH_HMAC_SECRET", "")
    sequence_step: int = args.sequence_step

    if not args.dry_run and not api_key:
        raise RuntimeError(
            "RESEND_API_KEY env var is required for live sends. "
            "Use --dry-run to test without it."
        )

    if not args.csv_file.exists():
        raise FileNotFoundError(
            f"Input CSV not found: {args.csv_file}\n"
            "Run Task 2A (seed_unclaimed_providers.py) first to generate outreach_ready.csv"
        )

    template = load_template()
    log.info("Template loaded: %s", TEMPLATE_PATH)
    log.info("Sequence step: %d", sequence_step)

    with args.csv_file.open(encoding="utf-8", newline="") as fh:
        all_rows: list[dict[str, str]] = list(csv.DictReader(fh))

    valid_rows = [
        r for r in all_rows
        if r.get("email", "").strip() and r.get("claim_token", "").strip()
    ]
    if args.limit is not None:
        valid_rows = valid_rows[: args.limit]

    total = len(valid_rows)
    log.info("Rows to process: %d", total)

    sent = skipped = failed = 0

    db = SessionLocal()
    try:
        for i, row in enumerate(valid_rows, start=1):
            email: str = row["email"].strip().lower()
            business_name: str = (row.get("business_name") or email).strip()
            claim_token: str = row["claim_token"].strip()
            claim_link: str = f"{app_url}/pl/claim/{claim_token}"
            category: str = row.get("category", "").strip()
            subject: str = SUBJECT_BY_CATEGORY.get(category, DEFAULT_SUBJECT)

            # Idempotency check — DB (replaces CSV)
            if not args.dry_run and _is_already_sent(db, email, sequence_step):
                log.info("[%d/%d] SKIP already sent (DB): %s step=%d", i, total, email, sequence_step)
                skipped += 1
                continue

            # Unsubscribe check — DB
            if not args.dry_run and _is_unsubscribed(db, email):
                log.info("[%d/%d] SKIP unsubscribed: %s", i, total, email)
                skipped += 1
                continue

            try:
                unsubscribe_url = _generate_unsubscribe_url(email, hmac_secret)
                html: str = template.render(
                    business_name=business_name,
                    claim_link=claim_link,
                    unsubscribe_url=unsubscribe_url,
                )
            except TemplateError as exc:
                log.error("[%d/%d] Template error for %s: %s", i, total, email, exc)
                if not args.dry_run:
                    _log_to_db(
                        db,
                        email=email,
                        business_name=business_name,
                        category=category,
                        sequence_step=sequence_step,
                        resend_message_id=None,
                        status="failed",
                    )
                failed += 1
                continue

            if args.dry_run:
                log.info(
                    "[DRY-RUN] [%d/%d] Would send: %s | step=%d | category=%s | html=%d chars",
                    i, total, email, sequence_step, category, len(html),
                )
                sent += 1
                continue

            try:
                import resend  # lazy import — dry-run works without resend installed
                resend.api_key = api_key
                response = resend.Emails.send(
                    {
                        "from": FROM_EMAIL,
                        "to": [email],
                        "subject": subject,
                        "html": html,
                    }
                )
                resend_message_id: str = response.get("id", "")
                log.info("[%d/%d] SENT: %s | step=%d | id=%s", i, total, email, sequence_step, resend_message_id)
                _log_to_db(
                    db,
                    email=email,
                    business_name=business_name,
                    category=category,
                    sequence_step=sequence_step,
                    resend_message_id=resend_message_id,
                    status="sent",
                )
                sent += 1
            except Exception as exc:  # noqa: BLE001
                log.error("[%d/%d] FAILED: %s | %s", i, total, email, exc)
                _log_to_db(
                    db,
                    email=email,
                    business_name=business_name,
                    category=category,
                    sequence_step=sequence_step,
                    resend_message_id=None,
                    status="failed",
                )
                failed += 1

            if i < total:
                time.sleep(args.delay)

    finally:
        db.close()

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    log.info(
        "\n%s\n[%s] DONE  Sent: %d | Skipped: %d | Failed: %d\n%s",
        "=" * 60, mode, sent, skipped, failed, "=" * 60,
    )


if __name__ == "__main__":
    main()
