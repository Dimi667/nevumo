from playwright.sync_api import sync_playwright
import csv, json, time, random
import requests
import re
from pathlib import Path

CHECKPOINT_FILE = Path("apps/scripts/panoramafirm_emails_checkpoint.json")
INPUT_CSV = Path("apps/scripts/warszawa_providers_panoramafirm.csv")
OUTPUT_FILE = Path("apps/scripts/panoramafirm_emails_final.csv")
BROWSER_RESTART_EVERY = 200

CATEGORIES: dict[str, str] = {
    "plumbing": "https://panoramafirm.pl/hydraulik/warszawa",
    "massage": "https://panoramafirm.pl/masaz/warszawa",
}

def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {
        "cleaning": {"last_index": 0, "done": False},
        "plumbing": {"listing_page": 1, "done": False, "sub_index": 0},
        "massage": {"listing_page": 1, "done": False, "sub_index": 0},
    }

def save_checkpoint(cp: dict) -> None:
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(cp, f, indent=2)

def launch_browser(p):
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    return browser, page

def accept_cookies(page) -> None:
    page.goto("https://panoramafirm.pl", wait_until="domcontentloaded", timeout=60000)
    time.sleep(2)
    for sel in ["button:has-text('Akceptuj')", "button:has-text('Zaakceptuj')", "[id*='accept']"]:
        try:
            page.click(sel, timeout=3000)
            break
        except Exception:
            continue
    time.sleep(1)

def create_session() -> requests.Session:
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

def get_email_from_profile(profile_url: str, session: requests.Session) -> str:
    try:
        response = session.get(profile_url, timeout=15)
        if response.status_code != 200:
            return ""
        match = re.search(r'data-popup-param-email="([^"@]+@[^"]+)"', response.text)
        if match:
            return match.group(1)
        return ""
    except Exception as e:
        print(f"[WARNING] Profile error {profile_url}: {e}")
        return ""

def phase1_cleaning_enrichment(p, browser, page, checkpoint: dict, writer: csv.DictWriter, session: requests.Session) -> tuple:
    """Phase 1: Enrich existing cleaning data with emails"""
    print("\n=== PHASE 1: Cleaning enrichment ===")
    
    # Load and deduplicate input CSV
    records = []
    seen_urls = set()
    with open(INPUT_CSV) as f:
        reader = csv.DictReader(f)
        for row in reader:
            profile_url = row.get("profile_url", "")
            if profile_url and profile_url not in seen_urls:
                seen_urls.add(profile_url)
                records.append(row)
            elif not profile_url:
                records.append(row)
    
    total_records = len(records)
    start_index = checkpoint.get("cleaning", {}).get("last_index", 0)
    
    emails_found = 0
    
    for idx in range(start_index, total_records):
        record = records[idx]
        profile_url = record.get("profile_url", "")
        
        if profile_url:
            email = get_email_from_profile(profile_url, session)
            if email:
                emails_found += 1
        else:
            email = ""
        
        writer.writerow({
            "business_name": record.get("business_name", ""),
            "website": record.get("website", ""),
            "category": "cleaning",
            "source": "panoramafirm",
            "profile_url": profile_url,
            "email": email,
        })
        
        # Progress log every 100 records
        if (idx + 1) % 100 == 0:
            percentage = (emails_found / (idx + 1)) * 100
            print(f"[CLEANING {idx + 1}/{total_records}] Emails found: {emails_found} ({percentage:.1f}%)")
        
        # Checkpoint every 50 records
        if (idx + 1) % 50 == 0:
            checkpoint["cleaning"]["last_index"] = idx + 1
            save_checkpoint(checkpoint)
    
    # Final checkpoint
    checkpoint["cleaning"]["last_index"] = total_records
    checkpoint["cleaning"]["done"] = True
    save_checkpoint(checkpoint)
    print(f"[CLEANING COMPLETE] Total: {total_records} | Emails: {emails_found} ({(emails_found/total_records)*100:.1f}%)")
    
    return browser, page

def scrape_category_with_emails(p, browser, page, base_url: str, category: str, start_page: int, sub_index: int, writer: csv.DictWriter, session: requests.Session):
    """Phase 2 & 3: Scrape listing pages and extract emails in one pass"""
    total = 0
    current_page = start_page
    pages_scraped_since_restart = 0
    emails_found = 0
    
    while True:
        # Build paginated URL
        if current_page == 1:
            url = base_url
        else:
            category_slug = base_url.split('/')[3]
            url = f"https://panoramafirm.pl/{category_slug}/mazowieckie,,warszawa/firmy,{current_page}.html"
        
        max_retries = 3
        page_loaded = False
        for attempt in range(max_retries):
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                page_loaded = True
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"[WARNING] Skipping {url} after {max_retries} attempts: {e}")
                else:
                    print(f"[RETRY {attempt + 1}] {url}")
                    time.sleep(random.uniform(2.0, 4.0))
        
        if not page_loaded:
            print(f"[{category}] Page {current_page}: Failed to load, skipping.")
            current_page += 1
            continue
        
        pages_scraped_since_restart += 1
        time.sleep(random.uniform(1.5, 3.0))
        
        # Check for company cards using h2 elements
        h2_elements = page.query_selector_all("h2")
        if not h2_elements:
            print(f"[{category}] Page {current_page}: No more results. Done.")
            break
        
        # Filter h2 elements that contain company links
        company_h2s = [h2 for h2 in h2_elements if h2.query_selector("a[href*='/mazowieckie,,warszawa']")]
        
        if not company_h2s:
            print(f"[{category}] Page {current_page}: No company cards found. Done.")
            break
        
        # Process each company card
        for h2 in company_h2s:
            # Skip already processed records on resume
            if total < sub_index:
                total += 1
                continue
            try:
                # Business name
                name = h2.inner_text().strip()
                
                # Profile URL
                link_el = h2.query_selector("a")
                profile_url = link_el.get_attribute("href") if link_el else ""
                if profile_url and not profile_url.startswith("http"):
                    profile_url = "https://panoramafirm.pl" + profile_url
                
                # Visit profile page to get website and email
                website = ""
                email = ""
                
                if profile_url:
                    try:
                        # Get email using requests (no memory leak)
                        email = get_email_from_profile(profile_url, session)
                        if email:
                            emails_found += 1
                        
                        # Get website using Playwright (still needed for dynamic content)
                        page.goto(profile_url, wait_until="domcontentloaded", timeout=60000)
                        time.sleep(random.uniform(1.5, 2.5))
                        
                        # Get website - look for links with "strona www" text
                        all_links = page.query_selector_all("a")
                        for link in all_links:
                            href = link.get_attribute("href")
                            text = link.inner_text().lower()
                            if href and "strona www" in text:
                                if not any(x in href for x in ["panoramafirm", "youtube", "openstreetmap", "google", "facebook", "linkedin"]):
                                    website = href
                                    break
                        
                    except Exception as e:
                        print(f"  Error visiting profile {profile_url}: {e}")
                
                writer.writerow({
                    "business_name": name,
                    "website": website,
                    "category": category,
                    "source": "panoramafirm",
                    "profile_url": profile_url,
                    "email": email,
                })
                total += 1
                
                # Checkpoint after each profile
                yield {"listing_page": current_page, "total": total, "emails_found": emails_found}
                
            except Exception as e:
                print(f"  Card error: {e}")
                continue
        
        percentage = (emails_found / total) * 100 if total > 0 else 0
        print(f"[{category} page {current_page}] Records: {total} | Emails: {emails_found} ({percentage:.1f}%)")
        current_page += 1
        
        # Browser restart
        if pages_scraped_since_restart >= BROWSER_RESTART_EVERY:
            print(f"[RESTART] Restarting browser after {BROWSER_RESTART_EVERY} pages...")
            browser.close()
            browser, page = launch_browser(p)
            accept_cookies(page)
            pages_scraped_since_restart = 0

def main() -> None:
    checkpoint = load_checkpoint()
    
    fieldnames = ["business_name", "website", "category", "source", "profile_url", "email"]
    file_exists = OUTPUT_FILE.exists()
    
    with sync_playwright() as p:
        browser, page = launch_browser(p)
        accept_cookies(page)
        session = create_session()
        
        try:
            with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                
                # Phase 1: Cleaning enrichment
                if not checkpoint.get("cleaning", {}).get("done"):
                    browser, page = phase1_cleaning_enrichment(p, browser, page, checkpoint, writer, session)
                else:
                    print("[CLEANING] Already done, skipping.")
                
                # Phase 2: Plumbing
                if not checkpoint.get("plumbing", {}).get("done"):
                    print("\n=== PHASE 2: Plumbing ===")
                    start_page = checkpoint.get("plumbing", {}).get("listing_page", 1)
                    sub_index = checkpoint.get("plumbing", {}).get("sub_index", 0)
                    base_url = CATEGORIES["plumbing"]
                    
                    for checkpoint_data in scrape_category_with_emails(p, browser, page, base_url, "plumbing", start_page, sub_index, writer, session):
                        checkpoint["plumbing"]["listing_page"] = checkpoint_data["listing_page"]
                        checkpoint["plumbing"]["sub_index"] = checkpoint_data.get("total", 0)
                        save_checkpoint(checkpoint)
                    
                    checkpoint["plumbing"]["done"] = True
                    save_checkpoint(checkpoint)
                    print(f"[PLUMBING COMPLETE] Total records: {checkpoint_data['total']} | Emails: {checkpoint_data['emails_found']}")
                else:
                    print("[PLUMBING] Already done, skipping.")
                
                # Phase 3: Massage
                if not checkpoint.get("massage", {}).get("done"):
                    print("\n=== PHASE 3: Massage ===")
                    start_page = checkpoint.get("massage", {}).get("listing_page", 1)
                    sub_index = checkpoint.get("massage", {}).get("sub_index", 0)
                    base_url = CATEGORIES["massage"]
                    
                    for checkpoint_data in scrape_category_with_emails(p, browser, page, base_url, "massage", start_page, sub_index, writer, session):
                        checkpoint["massage"]["listing_page"] = checkpoint_data["listing_page"]
                        checkpoint["massage"]["sub_index"] = checkpoint_data.get("total", 0)
                        save_checkpoint(checkpoint)
                    
                    checkpoint["massage"]["done"] = True
                    save_checkpoint(checkpoint)
                    print(f"[MASSAGE COMPLETE] Total records: {checkpoint_data['total']} | Emails: {checkpoint_data['emails_found']}")
                else:
                    print("[MASSAGE] Already done, skipping.")
        
        finally:
            browser.close()
    
    print(f"\nDone. Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
