import csv
import re
import time
from pathlib import Path
import requests
from bs4 import BeautifulSoup

CSV_PATH = Path("apps/scripts/warszawa_providers_with_websites.csv")
DELAY_SECONDS: float = 1.0
SAVE_EVERY: int = 50

EMAIL_REGEX = re.compile(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}')
EMAIL_SKIP = {"example", "test", "noreply", "no-reply", "donotreply",
              "spam", "domain", ".png", ".jpg", ".gif", ".css", ".js"}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1)"}


def get_page(url: str) -> str:
    resp = requests.get(url, timeout=10, headers=HEADERS, allow_redirects=True)
    resp.raise_for_status()
    return resp.text


def find_email(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    emails = EMAIL_REGEX.findall(text)
    for email in emails:
        if not any(skip in email.lower() for skip in EMAIL_SKIP):
            return email.lower()
    return ""


def fetch_email_for_domain(domain: str) -> str:
    pages = [
        f"https://{domain}",
        f"https://{domain}/kontakt",
        f"https://{domain}/contact",
    ]
    for url in pages:
        try:
            html = get_page(url)
            email = find_email(html)
            if email:
                return email
        except Exception:
            try:
                http_url = url.replace("https://", "http://")
                html = get_page(http_url)
                email = find_email(html)
                if email:
                    return email
            except Exception:
                continue
    return ""


def save_csv(rows: list[dict], fieldnames: list[str], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames: list[str] = list(reader.fieldnames or [])
        rows: list[dict] = list(reader)

    targets: list[tuple[int, dict]] = [
        (i, row) for i, row in enumerate(rows)
        if row.get("website", "").strip() and not row.get("email", "").strip()
    ]

    print(f"Total rows: {len(rows)}")
    print(f"Targets (website present, no email): {len(targets)}")
    print("-" * 60)

    found = 0
    errors = 0

    for idx, (row_idx, row) in enumerate(targets):
        domain = row.get("website", "").strip()

        try:
            email = fetch_email_for_domain(domain)
            if email:
                rows[row_idx]["email"] = email
                found += 1
            print(f"[{idx+1}/{len(targets)}] {domain[:40]:40} → {email or '—'}")
        except Exception as e:
            errors += 1
            print(f"[{idx+1}/{len(targets)}] ERROR: {domain} — {e}")

        if (idx + 1) % SAVE_EVERY == 0:
            save_csv(rows, fieldnames, CSV_PATH)
            print(f"  ✓ Checkpoint saved ({idx+1} processed)")

        time.sleep(DELAY_SECONDS)

    save_csv(rows, fieldnames, CSV_PATH)

    print("\n" + "=" * 60)
    print(f"Processed : {len(targets)}")
    print(f"Found     : {found}")
    print(f"Errors    : {errors}")


if __name__ == "__main__":
    main()
