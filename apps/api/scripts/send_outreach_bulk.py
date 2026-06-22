"""
apps/api/scripts/send_outreach_bulk.py

Bulk outreach email sender — Task 5A, Nevumo Claimed Profiles Campaign.

Input CSV columns: email, business_name, claim_token
Template: apps/api/scripts/templates/outreach_email_pl.html
Sender: support@nevumo.com via Resend
Rate limit: 100 emails/hour (Resend free tier) → 37s delay between sends

Run (dry-run test):
  railway run python3.13 -m apps.api.scripts.send_outreach_bulk --dry-run --limit 3

Run (live):
  railway run python3.13 -m apps.api.scripts.send_outreach_bulk --limit 100
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
from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Template, TemplateError
from sqlalchemy import create_engine, text

TEMPLATE_PATH: Path = Path(__file__).parent / "templates" / "outreach_email_pl.html"
LOG_PATH: Path = Path(__file__).parent / "outreach_sent_log.csv"
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

_db_engine = None

def _get_db():
    global _db_engine
    if _db_engine is None:
        _db_engine = create_engine(os.environ["DATABASE_URL"], pool_pre_ping=True)
    return _db_engine

def _generate_unsubscribe_url(email: str, secret: str) -> str:
    """Generate HMAC-SHA256 signed unsubscribe URL."""
    token = hmac.new(secret.encode(), email.encode(), hashlib.sha256).hexdigest()
    encoded_email = urllib.parse.quote(email)
    return f"https://nevumo.com/pl/outreach/unsubscribe?email={encoded_email}&token={token}"


def load_template() -> Template:
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"Template not found: {TEMPLATE_PATH}")
    return Template(TEMPLATE_PATH.read_text(encoding="utf-8"))


def load_sent_emails() -> set[str]:
    """Return set of already-sent emails for idempotency."""
    if not LOG_PATH.exists():
        return set()
    sent: set[str] = set()
    with LOG_PATH.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("status") == "sent":
                sent.add(row["email"].strip().lower())
    return sent


def append_log(
    *,
    email: str,
    business_name: str,
    status: str,
    error: str = "",
) -> None:
    is_new = not LOG_PATH.exists()
    with LOG_PATH.open("a", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=["timestamp", "email", "business_name", "status", "error"],
        )
        if is_new:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "email": email,
                "business_name": business_name,
                "status": status,
                "error": error,
            }
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Bulk outreach email sender.")
    parser.add_argument("--csv-file", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    args = parser.parse_args()

    api_key: str = os.environ.get("RESEND_API_KEY", "")
    app_url: str = os.environ.get("APP_URL", "https://www.nevumo.com").rstrip("/")

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

    already_sent: set[str] = load_sent_emails()
    log.info("Previously sent (will skip): %d", len(already_sent))

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

    for i, row in enumerate(valid_rows, start=1):
        email: str = row["email"].strip().lower()
        business_name: str = (row.get("business_name") or email).strip()
        claim_token: str = row["claim_token"].strip()
        claim_link: str = f"{app_url}/pl/claim/{claim_token}"
        category: str = row.get("category", "").strip()
        subject: str = SUBJECT_BY_CATEGORY.get(category, DEFAULT_SUBJECT)

        log.info("Sending to %s | category: %s | subject: %s", email, category, subject)

        if email in already_sent:
            log.info("[%d/%d] SKIP already sent: %s", i, total, email)
            skipped += 1
            continue

        # Skip unsubscribed emails
        with _get_db().connect() as conn:
            unsub = conn.execute(
                text("SELECT 1 FROM outreach_unsubscribes WHERE email = :email"),
                {"email": email}
            ).fetchone()
        if unsub:
            log.info("UNSUBSCRIBED skip: %s", email)
            skipped += 1
            continue

        try:
            unsubscribe_url = _generate_unsubscribe_url(email, os.environ.get("OUTREACH_HMAC_SECRET", ""))
            html: str = template.render(
                business_name=business_name,
                claim_link=claim_link,
                unsubscribe_url=unsubscribe_url,
            )
        except TemplateError as exc:
            log.error("[%d/%d] Template error for %s: %s", i, total, email, exc)
            append_log(email=email, business_name=business_name, status="failed", error=str(exc))
            failed += 1
            continue

        if args.dry_run:
            log.info(
                "[DRY-RUN] [%d/%d] Would send to: %s | %s | claim_link: %s | html: %d chars",
                i, total, email, business_name, claim_link, len(html),
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
            log.info("[%d/%d] SENT: %s | id=%s", i, total, email, response.get("id", "?"))
            append_log(email=email, business_name=business_name, status="sent")
            already_sent.add(email)
            sent += 1
        except Exception as exc:  # noqa: BLE001
            log.error("[%d/%d] FAILED: %s | %s", i, total, email, exc)
            append_log(email=email, business_name=business_name, status="failed", error=str(exc))
            failed += 1

        if i < total:
            time.sleep(args.delay)

    mode = "DRY-RUN" if args.dry_run else "LIVE"
    log.info(
        "\n%s\n[%s] DONE  Sent: %d | Skipped: %d | Failed: %d | Log: %s\n%s",
        "=" * 60, mode, sent, skipped, failed, LOG_PATH, "=" * 60,
    )


if __name__ == "__main__":
    main()
