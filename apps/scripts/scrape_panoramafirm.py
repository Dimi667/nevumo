from playwright.sync_api import sync_playwright
import csv, json, time, random
from pathlib import Path

CHECKPOINT_FILE = Path("apps/scripts/panoramafirm_checkpoint.json")
OUTPUT_FILE = Path("apps/scripts/warszawa_providers_panoramafirm.csv")
BROWSER_RESTART_EVERY = 200

CATEGORIES: dict[str, str] = {
    "cleaning": "https://panoramafirm.pl/sprzatanie/warszawa",
    "plumbing": "https://panoramafirm.pl/hydraulik/warszawa",
    "massage": "https://panoramafirm.pl/masaz/warszawa",
}

def load_checkpoint() -> dict:
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {cat: {"page": 1, "done": False} for cat in CATEGORIES}

def save_checkpoint(cp: dict) -> None:
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(cp, f, indent=2)

def launch_browser(p):
    browser = p.chromium.launch(headless=False)
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

def scrape_category(p, browser, page, base_url: str, category: str, start_page: int, writer: csv.DictWriter) -> int:
    total = 0
    current_page = start_page
    pages_scraped_since_restart = 0

    while True:
        # Build paginated URL - Panoramafirm uses: /category/mazowieckie,,warszawa/firmy,{page}.html
        if current_page == 1:
            url = base_url
        else:
            # Extract category from base URL
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

        # First collect all company data from listing page
        companies_data = []
        for h2 in company_h2s:
            try:
                # Business name
                name = h2.inner_text().strip()
                
                # Profile URL
                link_el = h2.query_selector("a")
                profile_url = link_el.get_attribute("href") if link_el else ""
                if profile_url and not profile_url.startswith("http"):
                    profile_url = "https://panoramafirm.pl" + profile_url
                
                companies_data.append({
                    "name": name,
                    "profile_url": profile_url
                })
            except Exception as e:
                print(f"  Error collecting company data: {e}")
                continue

        # Now visit each profile page to get phone and website
        for company in companies_data:
            try:
                phone = ""
                website = ""
                
                if company["profile_url"]:
                    try:
                        page.goto(company["profile_url"], wait_until="domcontentloaded", timeout=60000)
                        time.sleep(random.uniform(0.5, 1.0))
                        
                        # Get phone from tel: links
                        phone_elements = page.query_selector_all("a[href*='tel:']")
                        for phone_el in phone_elements:
                            phone_text = phone_el.get_attribute("href")
                            if phone_text and phone_text.startswith("tel:"):
                                phone = phone_text.replace("tel:", "").strip()
                                break
                        
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
                        print(f"  Error visiting profile {company['profile_url']}: {e}")

                if company["name"]:
                    writer.writerow({
                        "business_name": company["name"],
                        "phone": phone,
                        "website": website,
                        "category": category,
                        "source": "panoramafirm",
                        "profile_url": company["profile_url"],
                    })
                    total += 1
                    print(f"  [{total}] {company['name']} | Phone: {phone} | Website: {website}")
            except Exception as e:
                print(f"  Card error: {e}")
                continue

        print(f"[{category}] Page {current_page}: {len(company_h2s)} cards | Total so far: {total}")
        current_page += 1
        pages_scraped_since_restart += 1

        # Checkpoint after each page
        checkpoint_data = {"page": current_page, "total": total}
        yield checkpoint_data

        # Restart browser every N pages to prevent memory leak
        if pages_scraped_since_restart >= BROWSER_RESTART_EVERY:
            print(f"[RESTART] Restarting browser after {BROWSER_RESTART_EVERY} pages to prevent memory leak...")
            browser.close()
            browser, page = launch_browser(p)
            accept_cookies(page)
            pages_scraped_since_restart = 0

def main() -> None:
    checkpoint = load_checkpoint()

    fieldnames = ["business_name", "phone", "website", "category", "source", "profile_url"]
    file_exists = OUTPUT_FILE.exists()

    with sync_playwright() as p:
        browser, page = launch_browser(p)
        accept_cookies(page)

        try:
            with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

                for category, base_url in CATEGORIES.items():
                    if checkpoint.get(category, {}).get("done"):
                        print(f"[{category}] Already done, skipping.")
                        continue

                    start_page = checkpoint.get(category, {}).get("page", 1)
                    print(f"\n=== Scraping {category} from page {start_page} ===")

                    for checkpoint_data in scrape_category(p, browser, page, base_url, category, start_page, writer):
                        checkpoint[category]["page"] = checkpoint_data["page"]
                        checkpoint[category]["total"] = checkpoint_data.get("total", 0)
                        save_checkpoint(checkpoint)

                    checkpoint[category]["done"] = True
                    save_checkpoint(checkpoint)
                    print(f"[{category}] COMPLETE — {checkpoint[category].get('total', 0)} total records")
        finally:
            browser.close()

    print(f"\nDone. Output: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()