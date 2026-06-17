import csv
import re
import time
import traceback
import warnings
from pathlib import Path
from ddgs import DDGS

# Suppress deprecation warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

CSV_PATH = Path("apps/scripts/warszawa_providers_with_websites.csv")
DELAY_SECONDS: float = 1.5
SAVE_EVERY: int = 50

SKIP_DOMAINS: set[str] = {
    "facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com",
    "youtube.com", "google.com", "google.pl", "duckduckgo.com", "bing.com",
    "allegro.pl", "olx.pl", "panoramafirm.pl", "fixly.pl",
    "oferteo.pl", "aleo.com", "infobel.com", "zumi.pl",
    "pkt.pl", "targeo.pl", "biznes.gov.pl", "ceidg.gov.pl",
    "wikipedia.org", "yelp.com",
    # Block all Wikipedia subdomains
    "ru.wikipedia.org", "en.wikipedia.org", "pl.wikipedia.org",
    # Block document sharing sites
    "yandex.com", "scribd.com", "issuu.com", "docplayer.pl",
    # Block directory/monitoring sites
    "monitorfirm.pb.pl", "gazeta.sgh.waw.pl",
    # Block job/review sites
    "gowork.pl",
    # Block cloud storage/attachment sites
    "s3.amazonaws.com", "attachments.infoisinfo.com.s3.amazonaws.com",
    # Block corporate support sites
    "support.sas.com",
    # Block messaging apps
    "web.whatsapp.com",
    # Block directory sites
    "cylex-polska.pl",
}

# Block international TLDs (keep only .pl)
BLOCKED_TLDS = {".sk", ".cz", ".il", ".de", ".hu", ".be", ".it", ".si", ".travel"}


def extract_search_name(business_name: str) -> str:
    if not business_name:
        return ""
    if not isinstance(business_name, str):
        business_name = str(business_name)
    name = business_name.strip()
    # Handle "1. Name, 2. Name" format
    match = re.match(r'^1\.\s*(.+?),\s*2\.', name)
    if match:
        return match.group(1).strip()
    # Handle "1) Name, 2) Name" format
    match = re.match(r'^1\)\s*(.+?),\s*2\)', name)
    if match:
        return match.group(1).strip()
    # Handle "1. Name" format (no second part)
    match = re.match(r'^\d+\.\s*(.+)$', name)
    if match:
        return match.group(1).strip()
    # Handle "1) Name" format (no second part)
    match = re.match(r'^\d+\)\s*(.+)$', name)
    if match:
        return match.group(1).strip()
    return name


def extract_domain(url: str) -> str:
    if not isinstance(url, str):
        url = str(url)
    domain = re.sub(r'^https?://', '', url)
    domain = re.sub(r'^www\.', '', domain)
    domain = domain.split('/')[0].lower()
    # Block all Wikipedia subdomains
    if 'wikipedia.org' in domain:
        return 'wikipedia.org'
    return domain


def search_ddg(query: str) -> str:
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=1))
            if results:
                href = results[0].get("href", "")
                if href:
                    return extract_domain(str(href))
    except Exception as e:
        print(f"  DDG error: {e}")
    return ""


def save_csv(rows: list[dict], fieldnames: list[str], path: Path) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    print("Starting to read CSV...", flush=True)
    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames: list[str] = list(reader.fieldnames or [])
        rows: list[dict] = list(reader)
    print(f"CSV read complete. {len(rows)} rows.", flush=True)

    targets: list[tuple[int, dict]] = [
        (i, row) for i, row in enumerate(rows)
        if not row.get("email", "").strip() and not row.get("website", "").strip()
    ]

    print(f"Total rows: {len(rows)}", flush=True)
    print(f"Targets (no email + no website): {len(targets)}", flush=True)
    print("-" * 60, flush=True)

    found = 0
    blocked = 0
    errors = 0

    for idx, (row_idx, row) in enumerate(targets):
        business_name = row.get("business_name", "")
        if not business_name:
            continue

        try:
            clean_name = extract_search_name(str(business_name))
            if not clean_name:
                continue
            query = f"{clean_name} Warszawa"
        except Exception as e:
            errors += 1
            print(f"[{idx+1}/{len(targets)}] ERROR in name extraction: {e} | business_name type: {type(business_name)} | value: {repr(business_name)}", flush=True)
            continue

        try:
            domain = search_ddg(query)
            if domain:
                # Check if domain or any parent domain is in blocklist
                is_blocked = False
                for blocked_domain in SKIP_DOMAINS:
                    if domain == blocked_domain or domain.endswith('.' + blocked_domain):
                        is_blocked = True
                        break
                # Check for blocked TLDs
                for tld in BLOCKED_TLDS:
                    if domain.endswith(tld):
                        is_blocked = True
                        break
                if is_blocked:
                    domain = ""
                    blocked += 1
                else:
                    rows[row_idx]["website"] = domain
                    found += 1
            print(f"[{idx+1}/{len(targets)}] {clean_name[:50]:50} → {domain or '—'}", flush=True)
        except Exception as e:
            errors += 1
            print(f"[{idx+1}/{len(targets)}] ERROR: {e}", flush=True)
            print(f"  Traceback: {traceback.format_exc()}", flush=True)

        if (idx + 1) % SAVE_EVERY == 0:
            save_csv(rows, fieldnames, CSV_PATH)
            print(f"  ✓ Checkpoint saved ({idx+1} processed)", flush=True)

        time.sleep(DELAY_SECONDS)

    save_csv(rows, fieldnames, CSV_PATH)

    print("\n" + "=" * 60, flush=True)
    print(f"Processed : {len(targets)}", flush=True)
    print(f"Found     : {found}", flush=True)
    print(f"Blocked   : {blocked}", flush=True)
    print(f"Errors    : {errors}", flush=True)


if __name__ == "__main__":
    main()
