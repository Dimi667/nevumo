#!/usr/bin/env python3
"""
Panoramafirm.pl scraper - requests only, no Playwright.
Extracts business names, emails, and websites from cleaning, plumbing, and massage categories.
"""

import csv
import json
import random
import re
import time
from pathlib import Path

import requests

BASE_URL = "https://panoramafirm.pl"
BROWSER_RESTART_EVERY = 200  # For compatibility only

OUTPUT_FILE = Path("apps/scripts/panoramafirm_emails_final.csv")
CHECKPOINT_FILE = Path("apps/scripts/panoramafirm_requests_checkpoint.json")
CLEANING_SOURCE_FILE = Path("apps/scripts/warszawa_providers_panoramafirm.csv")

# Listing URL formats
PLUMBING_URL_TEMPLATE = f"{BASE_URL}/hydraulik/mazowieckie,,warszawa/firmy,{{page}}.html"
MASSAGE_URL_TEMPLATE = f"{BASE_URL}/masaz/mazowieckie,,warszawa/firmy,{{page}}.html"


def create_session() -> requests.Session:
    """Create a requests session with appropriate headers."""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'pl-PL,pl;q=0.9,en;q=0.8',
        'Referer': 'https://panoramafirm.pl',
    })
    try:
        session.get('https://panoramafirm.pl', timeout=15)
    except Exception:
        pass
    return session


def get_profile_data(profile_url: str, session: requests.Session) -> tuple[str, str, str]:
    """
    Extract email, website, and business name from a profile page.
    Returns (email, website, business_name).
    """
    try:
        r = session.get(profile_url, timeout=15)
        if r.status_code != 200:
            return "", "", ""

        email_match = re.search(r'data-popup-param-email="([^"@]+@[^"]+)"', r.text)
        email = email_match.group(1) if email_match else ""

        website = ""
        links = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>([^<]*strona www[^<]*)</a>', r.text, re.IGNORECASE)
        if links:
            website = links[0][0]

        name_match = re.search(r'<h1[^>]*>([^<]+)</h1>', r.text)
        business_name = name_match.group(1).strip() if name_match else ""

        return email, website, business_name
    except Exception as e:
        print(f"[WARNING] Profile error {profile_url}: {e}")
        return "", "", ""


def get_listing_profiles(listing_url: str, session: requests.Session) -> list[tuple[str, str]]:
    """
    Extract profile URLs from a listing page.
    Returns list of (business_name, profile_url) - business_name is empty here, extracted from profile later.
    """
    try:
        r = session.get(listing_url, timeout=15)
        if r.status_code != 200:
            return []

        profile_urls = re.findall(r'<h2[^>]*>\s*<a\s+href="(/[^"]+)"', r.text)
        results = []
        for url in profile_urls:
            full_url = BASE_URL + url
            results.append(("", full_url))
        return results
    except Exception as e:
        print(f"[WARNING] Listing error {listing_url}: {e}")
        return []


def load_checkpoint() -> dict:
    """Load checkpoint from JSON file."""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, 'r') as f:
            return json.load(f)
    return {
        "cleaning": {"last_index": 0, "done": False},
        "plumbing": {"listing_page": 1, "sub_index": 0, "done": False},
        "massage": {"listing_page": 1, "sub_index": 0, "done": False}
    }


def save_checkpoint(checkpoint: dict):
    """Save checkpoint to JSON file."""
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)


def write_csv_row(writer: csv.DictWriter, row: dict):
    """Write a single row to CSV."""
    writer.writerow(row)


def phase1_cleaning_enrichment(session: requests.Session, checkpoint: dict):
    """Phase 1: Enrich existing cleaning CSV with emails and websites."""
    print("\n=== PHASE 1: CLEANING ENRICHMENT ===")

    if not CLEANING_SOURCE_FILE.exists():
        print(f"[ERROR] Source file not found: {CLEANING_SOURCE_FILE}")
        checkpoint["cleaning"]["done"] = True
        save_checkpoint(checkpoint)
        return

    # Load and deduplicate by profile_url
    with open(CLEANING_SOURCE_FILE, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Deduplicate
    seen_urls = set()
    unique_rows = []
    for row in rows:
        url = row.get('profile_url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_rows.append(row)

    print(f"[CLEANING] Loaded {len(unique_rows)} unique records from source file")

    last_index = checkpoint["cleaning"]["last_index"]
    total = len(unique_rows)
    email_count = 0

    for i in range(last_index, total):
        row = unique_rows[i]
        profile_url = row.get('profile_url', '')

        if not profile_url:
            continue

        email, website, business_name = get_profile_data(profile_url, session)
        if email:
            email_count += 1

        # Write to output
        with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['business_name', 'website', 'category', 'source', 'profile_url', 'email'])
            writer.writerow({
                'business_name': business_name or row.get('business_name', ''),
                'website': website or row.get('website', ''),
                'category': 'cleaning',
                'source': 'panoramafirm',
                'profile_url': profile_url,
                'email': email
            })

        # Checkpoint every 10 records
        if (i + 1) % 10 == 0:
            checkpoint["cleaning"]["last_index"] = i + 1
            save_checkpoint(checkpoint)

        # Log every 100
        if (i + 1) % 100 == 0:
            print(f"[CLEANING {i+1}/{total}] Emails: {email_count} ({email_count/(i+1)*100:.1f}%)")

        # Delay
        time.sleep(random.uniform(0.5, 1.5))

    checkpoint["cleaning"]["last_index"] = total
    checkpoint["cleaning"]["done"] = True
    save_checkpoint(checkpoint)
    print(f"[CLEANING] Complete. Total: {total}, Emails: {email_count}")


def phase2_plumbing(session: requests.Session, checkpoint: dict):
    """Phase 2: Scrape plumbing category."""
    print("\n=== PHASE 2: PLUMBING ===")

    listing_page = checkpoint["plumbing"]["listing_page"]
    sub_index = checkpoint["plumbing"]["sub_index"]
    total_records = 0
    email_count = 0

    while True:
        listing_url = PLUMBING_URL_TEMPLATE.format(page=listing_page)
        print(f"[PLUMBING] Fetching page {listing_page}...")

        profiles = get_listing_profiles(listing_url, session)

        if not profiles:
            print(f"[PLUMBING] No profiles on page {listing_page} - end of category")
            break

        # Skip already processed profiles from this page
        profiles_to_process = profiles[sub_index:]
        page_emails = 0

        for i, (name, profile_url) in enumerate(profiles_to_process):
            email, website, business_name = get_profile_data(profile_url, session)

            if email:
                email_count += 1
                page_emails += 1

            # Write to output
            with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['business_name', 'website', 'category', 'source', 'profile_url', 'email'])
                writer.writerow({
                    'business_name': business_name,
                    'website': website,
                    'category': 'plumbing',
                    'source': 'panoramafirm',
                    'profile_url': profile_url,
                    'email': email
                })

            total_records += 1

            # Checkpoint after every profile
            current_sub_index = sub_index + i + 1
            checkpoint["plumbing"]["listing_page"] = listing_page
            checkpoint["plumbing"]["sub_index"] = current_sub_index
            save_checkpoint(checkpoint)

            # Delay
            time.sleep(random.uniform(0.5, 1.5))

        print(f"[PLUMBING page {listing_page}] Records: {len(profiles_to_process)} | Emails: {page_emails}")

        # Reset sub_index for next page
        sub_index = 0
        checkpoint["plumbing"]["sub_index"] = 0
        listing_page += 1
        checkpoint["plumbing"]["listing_page"] = listing_page
        save_checkpoint(checkpoint)

    checkpoint["plumbing"]["done"] = True
    save_checkpoint(checkpoint)
    print(f"[PLUMBING] Complete. Total: {total_records}, Emails: {email_count}")


def phase3_massage(session: requests.Session, checkpoint: dict):
    """Phase 3: Scrape massage category."""
    print("\n=== PHASE 3: MASSAGE ===")

    listing_page = checkpoint["massage"]["listing_page"]
    sub_index = checkpoint["massage"]["sub_index"]
    total_records = 0
    email_count = 0

    while True:
        listing_url = MASSAGE_URL_TEMPLATE.format(page=listing_page)
        print(f"[MASSAGE] Fetching page {listing_page}...")

        profiles = get_listing_profiles(listing_url, session)

        if not profiles:
            print(f"[MASSAGE] No profiles on page {listing_page} - end of category")
            break

        # Skip already processed profiles from this page
        profiles_to_process = profiles[sub_index:]
        page_emails = 0

        for i, (name, profile_url) in enumerate(profiles_to_process):
            email, website, business_name = get_profile_data(profile_url, session)

            if email:
                email_count += 1
                page_emails += 1

            # Write to output
            with open(OUTPUT_FILE, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['business_name', 'website', 'category', 'source', 'profile_url', 'email'])
                writer.writerow({
                    'business_name': business_name,
                    'website': website,
                    'category': 'massage',
                    'source': 'panoramafirm',
                    'profile_url': profile_url,
                    'email': email
                })

            total_records += 1

            # Checkpoint after every profile
            current_sub_index = sub_index + i + 1
            checkpoint["massage"]["listing_page"] = listing_page
            checkpoint["massage"]["sub_index"] = current_sub_index
            save_checkpoint(checkpoint)

            # Delay
            time.sleep(random.uniform(0.5, 1.5))

        print(f"[MASSAGE page {listing_page}] Records: {len(profiles_to_process)} | Emails: {page_emails}")

        # Reset sub_index for next page
        sub_index = 0
        checkpoint["massage"]["sub_index"] = 0
        listing_page += 1
        checkpoint["massage"]["listing_page"] = listing_page
        save_checkpoint(checkpoint)

    checkpoint["massage"]["done"] = True
    save_checkpoint(checkpoint)
    print(f"[MASSAGE] Complete. Total: {total_records}, Emails: {email_count}")


def main():
    """Main execution function."""
    print("=== PANORAMAFIRM REQUESTS-ONLY SCRAPER ===")

    # Initialize CSV with header
    if not OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['business_name', 'website', 'category', 'source', 'profile_url', 'email'])
            writer.writeheader()

    # Load checkpoint
    checkpoint = load_checkpoint()

    # Create session
    session = create_session()

    try:
        # Phase 1: Cleaning enrichment
        if not checkpoint["cleaning"]["done"]:
            phase1_cleaning_enrichment(session, checkpoint)
        else:
            print("[CLEANING] Already completed, skipping")

        # Phase 2: Plumbing
        if not checkpoint["plumbing"]["done"]:
            phase2_plumbing(session, checkpoint)
        else:
            print("[PLUMBING] Already completed, skipping")

        # Phase 3: Massage
        if not checkpoint["massage"]["done"]:
            phase3_massage(session, checkpoint)
        else:
            print("[MASSAGE] Already completed, skipping")

        print("\n=== ALL PHASES COMPLETE ===")

    except KeyboardInterrupt:
        print("\n[INTERRUPT] Gracefully stopping...")
        save_checkpoint(checkpoint)
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        save_checkpoint(checkpoint)
    finally:
        session.close()


if __name__ == "__main__":
    main()
