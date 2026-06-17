import requests
from bs4 import BeautifulSoup
import csv
import re
import time
from urllib.parse import urlparse, urlunparse, unquote
from typing import Dict, List, Tuple, Optional

# Email regex pattern - with word boundary to avoid picking up adjacent text
EMAIL_RE = re.compile(
    r'\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b'
)

# Invalid email patterns to skip
INVALID_PATTERNS = [
    '.png', '.jpg', '.gif', '.svg', '.webp', '.js', '.css',
    'noreply', 'no-reply', 'example', 'sentry',
    'wixpress', 'panoramafirm', 'sampleemail'
]


def normalize_url(website: str) -> str:
    """Normalize URL: add https:// if missing, strip trailing slash"""
    website = website.strip()
    if not website.startswith(('http://', 'https://')):
        website = 'https://' + website
    if website.endswith('/'):
        website = website[:-1]
    return website


def get_normalized_domain(url: str) -> str:
    """Extract domain and strip www. for deduplication"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain


def is_valid_email(email: str) -> bool:
    """Check if email is valid (not in invalid patterns)"""
    email_lower = email.lower()
    
    # Must contain @
    if '@' not in email:
        return False
    
    # Check length constraints
    if len(email) > 100:
        return False
    
    local_part = email.split('@')[0]
    if len(local_part) > 60:
        return False
    
    # Check invalid patterns
    for pattern in INVALID_PATTERNS:
        if pattern in email_lower:
            return False
    
    # Check if domain ends with image/script extension
    domain = email.split('@')[1].lower()
    for ext in ['.png', '.jpg', '.gif', '.svg', '.webp', '.js', '.css']:
        if domain.endswith(ext):
            return False
    
    return True


def extract_emails_from_html(html: str) -> List[str]:
    """Extract emails from HTML using mailto links and regex"""
    soup = BeautifulSoup(html, 'html.parser')
    emails = set()
    
    # Method A: mailto links
    for tag in soup.find_all("a", href=True):
        href = tag["href"]
        if href.startswith("mailto:"):
            email = href[7:].split("?")[0].strip()
            # Clean up email
            email = clean_email(email)
            if is_valid_email(email):
                emails.add(email)
    
    # Method B: regex over full page text
    text_emails = EMAIL_RE.findall(soup.get_text())
    for email in text_emails:
        # Clean up regex matches
        email = clean_email(email)
        if is_valid_email(email):
            emails.add(email)
    
    return list(emails)


def clean_email(email: str) -> str:
    """Clean up email by removing leading/trailing invalid characters and URL encoding"""
    if '@' not in email:
        return email
    
    # Decode URL encoding (e.g., %20 -> space)
    try:
        email = unquote(email)
    except:
        pass
    
    local, domain = email.split('@', 1)
    
    # Clean local part: remove leading/trailing non-alphanumeric chars and digits
    local = re.sub(r'^[^a-zA-Z0-9._%+\-]+', '', local)
    local = re.sub(r'[^a-zA-Z0-9._%+\-]+$', '', local)
    
    # Clean domain: remove trailing non-alphanumeric chars aggressively
    # Stop at first invalid character after the TLD
    domain = re.sub(r'([a-zA-Z0-9.\-]+)[^a-zA-Z0-9.\-].*$', r'\1', domain)
    
    return f"{local}@{domain}"


def fetch_page(url: str, session: requests.Session) -> Optional[str]:
    """Fetch a page and return HTML, or None on error"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "pl-PL,pl;q=0.9,en;q=0.8"
    }
    
    try:
        response = session.get(url, headers=headers, timeout=10, allow_redirects=True)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def main():
    input_file = 'apps/scripts/panoramafirm_emails_final.csv'
    output_file = 'apps/scripts/panoramafirm_emails_final.csv'
    report_file = 'apps/scripts/panoramafirm_1z_report.csv'
    
    # STEP 1: Load and filter targets
    print("Loading CSV and filtering targets...")
    rows = []
    target_indices = []
    
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            rows.append(row)
            # Process all rows with websites (re-extract to fix malformed emails)
            if row['website'] and row['website'].strip():
                target_indices.append(idx)
    
    print(f"Total rows: {len(rows)}")
    print(f"Target rows (website != ''): {len(target_indices)}")
    
    # STEP 2: Deduplicate by normalized domain
    print("\nDeduplicating by domain...")
    domain_to_indices: Dict[str, List[int]] = {}
    
    for idx in target_indices:
        website = rows[idx]['website'].strip()
        normalized_url = normalize_url(website)
        domain = get_normalized_domain(normalized_url)
        
        if domain not in domain_to_indices:
            domain_to_indices[domain] = []
        domain_to_indices[domain].append(idx)
    
    print(f"Unique domains to visit: {len(domain_to_indices)}")
    
    # STEP 3: Fetch pages and extract emails
    print("\nStarting email extraction...")
    session = requests.Session()
    
    results = {}  # domain -> (email_found, pages_tried)
    emails_found_count = 0
    emails_not_found_count = 0
    
    for domain, indices in domain_to_indices.items():
        print(f"\nProcessing domain: {domain} ({len(indices)} business(es))")
        
        # Get the original URL from the first row
        original_url = normalize_url(rows[indices[0]]['website'])
        email_found = None
        pages_tried = []
        
        # Try homepage
        html = fetch_page(original_url, session)
        if html:
            pages_tried.append('homepage')
            emails = extract_emails_from_html(html)
            if emails:
                email_found = emails[0]
                print(f"  ✓ Email found on homepage: {email_found}")
        
        # Try /kontakt if no email found
        if not email_found:
            kontakt_url = original_url + '/kontakt'
            html = fetch_page(kontakt_url, session)
            if html:
                pages_tried.append('/kontakt')
                emails = extract_emails_from_html(html)
                if emails:
                    email_found = emails[0]
                    print(f"  ✓ Email found on /kontakt: {email_found}")
        
        # Try /contact if no email found
        if not email_found:
            contact_url = original_url + '/contact'
            html = fetch_page(contact_url, session)
            if html:
                pages_tried.append('/contact')
                emails = extract_emails_from_html(html)
                if emails:
                    email_found = emails[0]
                    print(f"  ✓ Email found on /contact: {email_found}")
        
        if not email_found:
            print(f"  ✗ No email found (tried: {', '.join(pages_tried) if pages_tried else 'none'})")
        
        results[domain] = (email_found or '', pages_tried)
        
        if email_found:
            emails_found_count += 1
        else:
            emails_not_found_count += 1
        
        # Delay between domains
        time.sleep(1.0)
    
    # STEP 4: Update CSV rows
    print("\nUpdating CSV rows...")
    for domain, (email, pages_tried) in results.items():
        for idx in domain_to_indices[domain]:
            # Clear existing email and set new one (or empty if not found)
            rows[idx]['email'] = email
    
    # STEP 5: Save outputs
    print("Saving updated CSV...")
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['business_name', 'website', 'category', 'source', 'profile_url', 'email']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    
    print("Saving report CSV...")
    with open(report_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['domain', 'email_found', 'pages_tried', 'business_names'])
        
        for domain, (email, pages_tried) in results.items():
            indices = domain_to_indices[domain]
            business_names = '; '.join([rows[idx]['business_name'] for idx in indices])
            pages_str = '; '.join(pages_tried)
            writer.writerow([domain, email, pages_str, business_names])
    
    # STEP 6: Print summary
    total_domains = len(domain_to_indices)
    success_rate = (emails_found_count / total_domains * 100) if total_domains > 0 else 0
    
    print("\n" + "="*60)
    print("EXTRACTION SUMMARY")
    print("="*60)
    print(f"Total unique domains visited: {total_domains}")
    print(f"Emails found: {emails_found_count}")
    print(f"Emails not found: {emails_not_found_count}")
    print(f"Success rate: {success_rate:.1f}%")
    print("="*60)


if __name__ == '__main__':
    main()
