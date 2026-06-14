#!/usr/bin/env python3
"""
CEIDG Provider Data Collector

HTML STRUCTURE NOTES (based on CEIDG public search page):
- Base URL: https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/Search.aspx
- Technology: ASP.NET WebForms with ViewState (auto-handled by Playwright)
- Search form typically contains:
  * PKD code field (textbox or combobox)
  * City/Miejscowość field (textbox)
  * Status dropdown (combobox with options like "Aktywny", "Zawieszony", etc.)
  * Search button (input type="submit" or button)
- Results page:
  * Table or list of provider results
  * Each result has a clickable link to detailed profile
  * Pagination controls (typically "Next", "Previous", page numbers)
- Profile page:
  * Business name (nazwa firmy)
  * Owner name (imię i nazwisko)
  * Address (adres)
  * Phone (telefon)
  * Email (e-mail)
  * Website (strona www)
  * NIP (tax identification number)
  * PKD codes (PKD)

NOTE: Since this is a standalone script, it will use Playwright's sync API directly.
The script will need to be run with: python apps/scripts/collect_ceidg_providers.py
"""

import csv
import time
from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# Configuration
PKD_CODES = {
    "cleaning": ["81.21.Z", "81.22.Z", "81.29.Z"],
    "massage":  ["96.04.Z", "96.23.Z", "86.90.A", "86.99.D"],
    "plumbing": ["43.22.Z", "43.21.Z"],
}

BASE_URL = "https://aplikacja.ceidg.gov.pl/CEIDG/CEIDG.Public.UI/Search.aspx"
OUTPUT_FILE = Path("apps/scripts/warszawa_providers_ceidg.csv")
CITY = "Warszawa"
PROVINCE = "Mazowieckie"
STATUS = "Aktywny"
LETTERS = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
PROFILE_DELAY = 1.5  # seconds between profiles


def extract_text_safe(element, selector: str) -> str:
    """Safely extract text from an element, return empty string if not found."""
    try:
        el = element.query_selector(selector)
        if el:
            return el.inner_text().strip()
    except Exception:
        pass
    return ""


def extract_attribute_safe(element, selector: str, attr: str) -> str:
    """Safely extract attribute from an element, return empty string if not found."""
    try:
        el = element.query_selector(selector)
        if el:
            return el.get_attribute(attr).strip()
    except Exception:
        pass
    return ""


def process_profile_page(page, pkd_code: str, category: str) -> dict:
    """Extract data from a single provider profile page."""
    data = {
        "business_name": "",
        "owner_name": "",
        "address": "",
        "phone": "",
        "email": "",
        "website": "",
        "nip": "",
        "pkd_code": pkd_code,
        "category": category,
        "source": "ceidg",
    }

    try:
        # Wait for page to load
        page.wait_for_load_state("networkidle", timeout=10000)

        def get_dl_value(page, label_text: str) -> str:
            try:
                sections = page.query_selector_all("section.block")
                for section in sections:
                    dts = section.query_selector_all("dt")
                    for dt in dts:
                        if label_text.lower() in dt.inner_text().lower():
                            dd = dt.evaluate_handle(
                                "el => el.nextElementSibling"
                            )
                            if dd:
                                return dd.as_element().inner_text().strip()
            except Exception:
                pass
            return ""

        data["business_name"] = get_dl_value(page, "Firma przedsiębiorcy")
        first_name = get_dl_value(page, "Imię")
        last_name = get_dl_value(page, "Nazwisko")
        data["owner_name"] = f"{first_name} {last_name}".strip()
        data["nip"] = get_dl_value(page, "Numer NIP").replace(" ", "").replace("-", "")
        data["phone"] = get_dl_value(page, "Numer telefonu")
        data["email"] = get_dl_value(page, "Adres poczty elektronicznej")
        data["address"] = get_dl_value(page, "Adres")
        data["website"] = get_dl_value(page, "Strona")

    except Exception as e:
        print(f"[WARNING] Error extracting profile data: {e}")

    return data


def write_to_csv(data: dict, file_path: Path):
    """Append a single record to CSV file."""
    file_exists = file_path.exists()

    with open(file_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "business_name",
                "owner_name",
                "address",
                "phone",
                "email",
                "website",
                "nip",
                "pkd_code",
                "category",
                "source",
            ],
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)


def search_and_collect(page, pkd_code: str, category: str, seen_nips: set, letter: str = "") -> int:
    """Search for providers with given PKD code and collect all data."""
    total_processed = 0
    page_num = 1

    prefix = f"[{letter}]" if letter else ""
    print(f"\n{prefix}[{category} / {pkd_code}] Starting search...")

    # Navigate to search page
    page.goto(BASE_URL)
    page.wait_for_load_state("networkidle", timeout=15000)

    try:
        # Fill PKD code field
        page.fill("#MainContentForm_txtPkd", pkd_code)

        # Fill city field
        page.fill("#MainContentForm_txtCity", CITY)
        page.fill("#MainContentForm_txtProvince", PROVINCE)

        if letter:
            page.fill("#MainContentForm_txtName", letter)

        # Click search button
        page.click("#MainContentForm_btnInputSearch")

        # Wait for results
        page.wait_for_load_state("networkidle", timeout=15000)
        time.sleep(2)

        # Handle CAPTCHA if present
        if page.query_selector("iframe[src*='recaptcha'], .g-recaptcha, #recaptcha"):
            print("\n⚠️  CAPTCHA DETECTED! Реши го ръчно в браузъра и натисни Enter тук...")
            input()
            page.wait_for_load_state("networkidle", timeout=15000)

    except Exception as e:
        print(f"[WARNING] Error during search form submission for {pkd_code}: {e}")
        return 0

    # Process all pages of results
    while True:
        print(f"{prefix}[{category} / {pkd_code}] Page {page_num} — processed {total_processed} profiles so far...")

        try:
            # Collect HREFs as strings first — NOT ElementHandles
            elements = page.query_selector_all("a[href*='SearchDetails.aspx']")
            result_hrefs = []
            for el in elements:
                href = el.get_attribute("href") or ""
                if href:
                    href = urljoin(page.url, href)
                    if href not in result_hrefs:
                        result_hrefs.append(href)

            if not result_hrefs:
                print(f"[{category} / {pkd_code}] No results found on page {page_num}")
                break

            # Store current list page URL
            list_url = page.url

            # Navigate to each profile by URL — no stale element issues
            for href in result_hrefs:
                try:
                    page.goto(href)
                    page.wait_for_load_state("networkidle", timeout=10000)

                    profile_data = process_profile_page(page, pkd_code, category)

                    if profile_data["nip"] and profile_data["nip"] in seen_nips:
                        print(f"[{category} / {pkd_code}] Skipping duplicate NIP: {profile_data['nip']}")
                    else:
                        if profile_data["nip"]:
                            seen_nips.add(profile_data["nip"])
                        write_to_csv(profile_data, OUTPUT_FILE)
                        total_processed += 1

                    time.sleep(PROFILE_DELAY)

                except Exception as e:
                    print(f"[WARNING] Error processing profile {href}: {e}")
                    continue

            # Go back to list and check for next page
            page.goto(list_url)
            page.wait_for_load_state("networkidle", timeout=10000)
            time.sleep(1)

            # Get next page href as string — NOT ElementHandle
            next_href = None
            next_el = page.query_selector("a:has-text('Następna'), a:has-text('Next'), a:has-text('>')")
            if next_el:
                next_href = next_el.get_attribute("href")
                if next_href and not next_href.startswith("http"):
                    next_href = "https://aplikacja.ceidg.gov.pl" + next_href

            if next_href:
                page.goto(next_href)
                page.wait_for_load_state("networkidle", timeout=10000)
                page_num += 1
            else:
                print(f"[{category} / {pkd_code}] No more pages available")
                break

        except Exception as e:
            print(f"[WARNING] Error processing page {page_num}: {e}")
            break

    print(f"[{category} / {pkd_code}] Completed. Total profiles: {total_processed}")
    return total_processed


def main():
    """Main execution function."""
    print("=" * 60)
    print("CEIDG Provider Data Collector")
    print("=" * 60)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"City: {CITY}")
    print(f"Status: {STATUS}")
    print(f"Letters: {len(LETTERS)} (A-Z + 0-9)")
    print(f"PKD codes: {sum(len(v) for v in PKD_CODES.values())}")
    print(f"Total searches: {len(LETTERS) * sum(len(v) for v in PKD_CODES.values())}")
    print("=" * 60)

    # Initialize CSV file with header
    if OUTPUT_FILE.exists():
        print(f"[INFO] Output file already exists. Appending to it.")
    else:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "business_name",
                    "owner_name",
                    "address",
                    "phone",
                    "email",
                    "website",
                    "nip",
                    "pkd_code",
                    "category",
                    "source",
                ],
            )
            writer.writeheader()

    seen_nips = set()
    total_grand = 0

    with sync_playwright() as p:
        # Launch browser in headless mode (set to False to see what's happening)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            for letter in LETTERS:
                for category, pkd_list in PKD_CODES.items():
                    for pkd_code in pkd_list:
                        try:
                            count = search_and_collect(page, pkd_code, category, seen_nips, letter)
                            total_grand += count
                        except Exception as e:
                            print(f"[ERROR] Fatal error for {category}/{pkd_code}: {e}")
                            continue

        finally:
            browser.close()

    print("=" * 60)
    print(f"Collection complete!")
    print(f"Total profiles collected: {total_grand}")
    print(f"Output file: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()
