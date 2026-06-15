#!/usr/bin/env python3.13
"""
CEIDG Website Re-Scraper
Reads warszawa_providers_clean.csv, visits each provider's CEIDG profile
and fills in the missing "website" column.

Strategy (mirrors working collect_ceidg_providers.py exactly):
- sync_playwright, headless=False, real Chrome UA (same as original)
- Search by NIP + PKD code (two criteria → no CAPTCHA, no "min 1" error)
- Navigate to result via a[href*='SearchDetails.aspx'] (same as original)
- Extract "Strona" field via section.block → dt/dd (same get_dl_value logic)
"""

import csv
import sys
import time
import random
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# File paths
INPUT_CSV  = Path("apps/scripts/warszawa_providers_clean.csv")
OUTPUT_CSV = Path("apps/scripts/warszawa_providers_with_websites.csv")
LOG_FILE   = Path("apps/scripts/website_scrape_log.txt")

# CEIDG — exact same URL as working original script
CEIDG_SEARCH_URL = "https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/Search.aspx"

# Exact same UA and viewport as working original script
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
VIEWPORT = {"width": 1920, "height": 1080}

# Rate limiting
MIN_DELAY        = 2.0
MAX_DELAY        = 4.0
CHECKPOINT_EVERY = 50


# ──────────────────────────────────────────────────────────
# Logging
# ──────────────────────────────────────────────────────────

def log(message: str) -> None:
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} - {message}\n")


# ──────────────────────────────────────────────────────────
# Exact copy of get_dl_value from collect_ceidg_providers.py
# ──────────────────────────────────────────────────────────

def get_dl_value(page, label_text: str) -> str:
    """Extract dd value for a given dt label inside section.block elements."""
    try:
        sections = page.query_selector_all("section.block")
        for section in sections:
            dts = section.query_selector_all("dt")
            for dt in dts:
                if label_text.lower() in dt.inner_text().lower():
                    dd = dt.evaluate_handle("el => el.nextElementSibling")
                    if dd:
                        el = dd.as_element()
                        if el:
                            return el.inner_text().strip()
    except Exception:
        pass
    return ""


# ──────────────────────────────────────────────────────────
# Core scrape function
# ──────────────────────────────────────────────────────────

def fetch_website(page, nip: str, pkd_code: str) -> Optional[str]:
    """
    Search CEIDG by NIP + PKD code, navigate to profile, return website or None.
    Uses the same search flow as the working collect_ceidg_providers.py.
    """
    try:
        page.goto(CEIDG_SEARCH_URL, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)

        # Fill NIP field (exact selector from diagnostic output)
        page.fill("#MainContentForm_txtNip", nip)

        # Fill PKD code — second criterion so we avoid "min 1 criterion" error
        page.fill("#MainContentForm_txtPkd", pkd_code)

        # Click search — same button as original script
        page.click("#MainContentForm_btnInputSearch")
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(1)

        # Find first result link — same selector as original script
        result_link = page.query_selector("a[href*='SearchDetails.aspx']")
        if not result_link:
            log(f"No results for NIP {nip} / PKD {pkd_code}")
            return None

        href = result_link.get_attribute("href") or ""
        href = urljoin(page.url, href)  # same as working collect_ceidg_providers.py

        # Navigate to profile page
        page.goto(href, timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)

        # Extract website — same label as original script
        website = get_dl_value(page, "Adres strony internetowej")
        return website if website else None

    except PlaywrightTimeoutError as e:
        log(f"Timeout for NIP {nip}: {e}")
        return None
    except Exception as e:
        log(f"Error for NIP {nip}: {e}")
        return None


# ──────────────────────────────────────────────────────────
# URL normalisation
# ──────────────────────────────────────────────────────────

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url or len(url) < 4 or "." not in url:
        return ""
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return f"https://{url}"


# ──────────────────────────────────────────────────────────
# Checkpoint
# ──────────────────────────────────────────────────────────

def save_checkpoint(rows: list[dict], processed: int) -> None:
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    log(f"Checkpoint saved: {processed} rows processed")


# ──────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────

def main() -> None:
    log("Starting CEIDG website re-scraper")

    # --test N flag
    test_limit: Optional[int] = None
    if "--test" in sys.argv:
        idx = sys.argv.index("--test")
        if idx + 1 < len(sys.argv):
            test_limit = int(sys.argv[idx + 1])
            print(f"TEST MODE: processing only first {test_limit} rows")

    # Read input CSV
    with open(INPUT_CSV, "r", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    total_rows = len(rows)
    log(f"Total rows: {total_rows}")
    print(f"Loaded {total_rows} rows from {INPUT_CSV}")

    rows_to_process = rows[:test_limit] if test_limit else rows

    processed = found = skipped = errors = 0

    with sync_playwright() as p:
        # Exact same browser setup as working collect_ceidg_providers.py
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport=VIEWPORT, user_agent=USER_AGENT)
        page = context.new_page()

        for i, row in enumerate(rows_to_process):
            nip             = row.get("nip", "").strip()
            pkd_code        = row.get("pkd_code", "").strip()
            existing_site   = row.get("website", "").strip()

            # Skip rows with no NIP, no PKD, or already have a website
            if not nip or not pkd_code or existing_site:
                skipped += 1
                processed += 1
                continue

            try:
                website = fetch_website(page, nip, pkd_code)

                if website:
                    website = normalize_url(website)

                if website:
                    rows[i]["website"] = website
                    found += 1
                    print(f"  [{i+1}] ✓ {nip} → {website}")
                    log(f"Found: NIP={nip} website={website}")
                else:
                    print(f"  [{i+1}] – {nip} → no website")

                processed += 1

                # Checkpoint every N rows (not in test mode)
                if not test_limit and processed % CHECKPOINT_EVERY == 0:
                    save_checkpoint(rows, processed)
                    print(f">>> Checkpoint: {processed}/{total_rows}")

            except Exception as e:
                errors += 1
                processed += 1
                log(f"Unhandled error row {i} NIP={nip}: {e}")
                print(f"  [{i+1}] ERROR: {e}")

            # Rate limiting
            time.sleep(random.uniform(MIN_DELAY, MAX_DELAY))

        browser.close()

    # Final save (not in test mode)
    if not test_limit:
        save_checkpoint(rows, processed)

    print("\n" + "=" * 50)
    print("TEST COMPLETE" if test_limit else "SCRAPING COMPLETE")
    print("=" * 50)
    print(f"Rows processed:  {processed}")
    print(f"Websites found:  {found}")
    print(f"Rows skipped:    {skipped}")
    print(f"Errors:          {errors}")
    if not test_limit:
        print(f"Output file:     {OUTPUT_CSV}")
    print(f"Log file:        {LOG_FILE}")
    print("=" * 50)

    log(f"Complete: processed={processed} found={found} skipped={skipped} errors={errors}")


if __name__ == "__main__":
    main()