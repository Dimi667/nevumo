#!/usr/bin/env python3.13
"""
CSV Cleaning Script for CEIDG Provider Data
Cleans warszawa_providers_ceidg.csv and generates a detailed report.
"""

import csv
import re
import os
from pathlib import Path
from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple


def read_csv_file(file_path: Path) -> List[Dict[str, str]]:
    """Read CSV file and return list of dictionaries."""
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_file(file_path: Path, rows: List[Dict[str, str]], fieldnames: List[str]) -> None:
    """Write CSV file with UTF-8-BOM encoding for Excel compatibility."""
    with open(file_path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_valid_email_format(email: str) -> bool:
    """Check if email has valid format using simple regex."""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_invalid_email_content(email: str) -> bool:
    """Check if email contains invalid content."""
    if not email:
        return False
    
    # Check for space
    if ' ' in email:
        return True
    
    # Check for invalid prefixes
    invalid_prefixes = ['test@', 'example@', 'noreply@', 'no-reply@', 'info@test', 'admin@test']
    for prefix in invalid_prefixes:
        if email.lower().startswith(prefix):
            return True
    
    return False


def normalize_phone(phone: str) -> Tuple[str, bool]:
    """
    Normalize phone number and return (normalized_phone, was_prefix_added).
    Returns ("", False) if invalid after normalization.
    """
    if not phone:
        return "", False
    
    # Remove spaces, dashes, parentheses, dots
    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)
    
    # If starts with "0048" -> replace with "+48"
    if cleaned.startswith('0048'):
        cleaned = '+48' + cleaned[4:]
    
    # If starts with "48" and has 11 digits total -> add "+" prefix
    elif cleaned.startswith('48') and len(cleaned) == 11:
        cleaned = '+' + cleaned
    
    # If doesn't start with "+" and is 9 digits -> add "+48" prefix
    elif not cleaned.startswith('+') and len(cleaned) == 9 and cleaned.isdigit():
        cleaned = '+48' + cleaned
        return cleaned, True
    
    # Validate final format: +48 followed by exactly 9 digits
    if re.match(r'^\+48\d{9}$', cleaned):
        return cleaned, False
    
    return "", False


def normalize_website(website: str) -> Tuple[str, bool]:
    """
    Normalize website URL and return (normalized_url, was_prefix_added).
    Returns ("", False) if invalid.
    """
    if not website:
        return "", False
    
    # Strip whitespace
    website = website.strip()
    
    if not website:
        return "", False
    
    # If doesn't start with http:// or https:// -> add https://
    if not website.startswith('http://') and not website.startswith('https://'):
        website = 'https://' + website
        return website, True
    
    # If it's just "http://" or "https://" without domain -> nullify
    if website in ('http://', 'https://'):
        return "", False
    
    return website, False


def generate_initial_report(rows: List[Dict[str, str]]) -> str:
    """Generate initial state report before cleaning."""
    total_rows = len(rows)
    
    # Count non-empty fields
    non_empty_email = sum(1 for row in rows if row.get('email', '').strip())
    non_empty_phone = sum(1 for row in rows if row.get('phone', '').strip())
    non_empty_website = sum(1 for row in rows if row.get('website', '').strip())
    
    # Category breakdown
    categories = Counter(row.get('category', 'other') for row in rows)
    
    # Count duplicates by NIP (only non-empty)
    nip_values = [row.get('nip', '').strip() for row in rows if row.get('nip', '').strip()]
    nip_counter = Counter(nip_values)
    duplicate_nips = sum(count - 1 for count in nip_counter.values() if count > 1)
    
    # Count duplicates by business_name (case-insensitive, strip whitespace)
    business_names = [row.get('business_name', '').strip().lower() for row in rows if row.get('business_name', '').strip()]
    name_counter = Counter(business_names)
    duplicate_names = sum(count - 1 for count in name_counter.values() if count > 1)
    
    # Count invalid business names
    empty_business_name = sum(1 for row in rows if not row.get('business_name', '').strip())
    digits_only_business_name = sum(1 for row in rows if row.get('business_name', '').strip() and re.match(r'^\d+$', row.get('business_name', '').strip()))
    short_business_name = sum(1 for row in rows if row.get('business_name', '').strip() and len(row.get('business_name', '').strip()) < 3)
    
    # Count invalid emails
    invalid_emails = sum(1 for row in rows if row.get('email', '').strip() and not is_valid_email_format(row.get('email', '').strip()))
    
    # Count invalid phones (after normalization)
    invalid_phones = sum(1 for row in rows if row.get('phone', '').strip() and normalize_phone(row.get('phone', '').strip())[0] == "")
    
    report = f"""
═══════════════════════════════════════════
СТЪПКА 1 — ДОКЛАД ЗА НАЧАЛНО СЪСТОЯНИЕ
═══════════════════════════════════════════

НАЧАЛНО СЪСТОЯНИЕ:
- Общо редове: {total_rows}
- Редове с непразен email: {non_empty_email}
- Редове с непразен phone: {non_empty_phone}
- Редове с непразен website: {non_empty_website}
- Разбивка по category:
"""
    for category, count in sorted(categories.items()):
        report += f"  * {category}: {count}\n"
    
    report += f"""
- Брой дубликати по nip (само редове с nip != ""): {duplicate_nips}
- Брой дубликати по business_name (case-insensitive, strip whitespace): {duplicate_names}
- Брой редове с празен или None business_name: {empty_business_name}
- Брой редове с business_name само от цифри: {digits_only_business_name}
- Брой редове с business_name по-кратко от 3 символа (след strip): {short_business_name}
- Брой имейли с невалиден формат: {invalid_emails}
- Брой телефони с невалиден формат (след нормализация): {invalid_phones}
"""
    return report


def clean_data(rows: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], Dict[str, int]]:
    """
    Clean data according to rules and return (cleaned_rows, stats).
    """
    print("Starting data cleaning...")
    
    stats = {
        'deleted_empty_business_name': 0,
        'deleted_digits_only_business_name': 0,
        'deleted_short_business_name': 0,
        'deleted_duplicate_nip': 0,
        'deleted_duplicate_business_name': 0,
        'nulled_invalid_emails': 0,
        'nulled_invalid_phones': 0,
        'normalized_phones_prefix_added': 0,
        'normalized_websites_prefix_added': 0,
        'duplicate_nips_list': [],
    }
    
    # STEP 2A: Delete rows based on business_name rules
    print("Step 2A: Deleting rows with invalid business_name...")
    
    filtered_rows = []
    for row in rows:
        business_name = row.get('business_name', '')
        stripped_name = business_name.strip() if business_name else ''
        
        # Delete if None, empty, or whitespace only
        if not stripped_name:
            stats['deleted_empty_business_name'] += 1
            continue
        
        # Delete if digits only
        if re.match(r'^\d+$', stripped_name):
            stats['deleted_digits_only_business_name'] += 1
            continue
        
        # Delete if shorter than 3 characters
        if len(stripped_name) < 3:
            stats['deleted_short_business_name'] += 1
            continue
        
        filtered_rows.append(row)
    
    print(f"  - Deleted {stats['deleted_empty_business_name']} rows with empty business_name")
    print(f"  - Deleted {stats['deleted_digits_only_business_name']} rows with digits-only business_name")
    print(f"  - Deleted {stats['deleted_short_business_name']} rows with short business_name")
    
    # Delete duplicates by NIP (keep first occurrence)
    print("Step 2A: Deleting duplicates by NIP...")
    seen_nips: Set[str] = set()
    rows_after_nip = []
    
    for row in filtered_rows:
        nip = row.get('nip', '').strip()
        if nip and nip in seen_nips:
            stats['deleted_duplicate_nip'] += 1
            stats['duplicate_nips_list'].append(nip)
        else:
            if nip:
                seen_nips.add(nip)
            rows_after_nip.append(row)
    
    print(f"  - Deleted {stats['deleted_duplicate_nip']} duplicate rows by NIP")
    
    # Delete duplicates by business_name (case-insensitive, keep first occurrence)
    print("Step 2A: Deleting duplicates by business_name...")
    seen_names: Set[str] = set()
    rows_after_name = []
    
    for row in rows_after_nip:
        business_name = row.get('business_name', '').strip().lower()
        if business_name in seen_names:
            stats['deleted_duplicate_business_name'] += 1
        else:
            seen_names.add(business_name)
            rows_after_name.append(row)
    
    print(f"  - Deleted {stats['deleted_duplicate_business_name']} duplicate rows by business_name")
    
    # STEP 2B: Clean fields
    print("Step 2B: Cleaning fields...")
    
    for row in rows_after_name:
        # EMAIL cleaning
        email = row.get('email', '').strip()
        if email:
            if is_invalid_email_content(email) or not is_valid_email_format(email):
                row['email'] = ''
                stats['nulled_invalid_emails'] += 1
        
        # PHONE normalization
        phone = row.get('phone', '').strip()
        if phone:
            normalized_phone, prefix_added = normalize_phone(phone)
            if normalized_phone:
                row['phone'] = normalized_phone
                if prefix_added:
                    stats['normalized_phones_prefix_added'] += 1
            else:
                row['phone'] = ''
                stats['nulled_invalid_phones'] += 1
        
        # WEBSITE normalization
        website = row.get('website', '').strip()
        if website:
            normalized_website, prefix_added = normalize_website(website)
            if normalized_website:
                row['website'] = normalized_website
                if prefix_added:
                    stats['normalized_websites_prefix_added'] += 1
            else:
                row['website'] = ''
        
        # ADDRESS - just strip whitespace
        address = row.get('address', '')
        if address:
            row['address'] = address.strip()
    
    print(f"  - Nulled {stats['nulled_invalid_emails']} invalid emails")
    print(f"  - Nulled {stats['nulled_invalid_phones']} invalid phones")
    print(f"  - Normalized {stats['normalized_phones_prefix_added']} phones with +48 prefix")
    print(f"  - Normalized {stats['normalized_websites_prefix_added']} websites with https:// prefix")
    
    return rows_after_name, stats


def generate_final_report(initial_rows: int, cleaned_rows: List[Dict[str, str]], stats: Dict[str, int]) -> str:
    """Generate final report after cleaning."""
    total_rows = len(cleaned_rows)
    
    # Count non-empty fields in cleaned data
    non_empty_email = sum(1 for row in cleaned_rows if row.get('email', '').strip())
    non_empty_phone = sum(1 for row in cleaned_rows if row.get('phone', '').strip())
    non_empty_website = sum(1 for row in cleaned_rows if row.get('website', '').strip())
    
    # Category breakdown
    categories = Counter(row.get('category', 'other') for row in cleaned_rows)
    
    # Total deleted rows
    total_deleted = initial_rows - total_rows
    
    report = f"""
═══════════════════════════════════════════
СТЪПКА 3 — ДОКЛАД ЗА КРАЕН РЕЗУЛТАТ
═══════════════════════════════════════════

ПРИЛОЖЕНИ ПРОМЕНИ:
- Изтрити поради празен/невалиден business_name: {stats['deleted_empty_business_name'] + stats['deleted_digits_only_business_name'] + stats['deleted_short_business_name']} реда
  * Празен business_name: {stats['deleted_empty_business_name']}
  * Само цифри: {stats['deleted_digits_only_business_name']}
  * По-кратко от 3 символа: {stats['deleted_short_business_name']}
- Изтрити дубликати по NIP: {stats['deleted_duplicate_nip']} реда
  * NIP-ове с дубликати: {', '.join(set(stats['duplicate_nips_list'])) if stats['duplicate_nips_list'] else 'няма'}
- Изтрити дубликати по business_name: {stats['deleted_duplicate_business_name']} реда
- Нулирани имейли (невалиден формат): {stats['nulled_invalid_emails']}
- Нулирани телефони (невалиден формат): {stats['nulled_invalid_phones']}
- Нормализирани телефони (добавен +48 префикс): {stats['normalized_phones_prefix_added']}
- Нормализирани уебсайтове (добавен https://): {stats['normalized_websites_prefix_added']}

КРАЕН РЕЗУЛТАТ (след почистване):
- Общо редове: {total_rows}
- Редове с имейл: {non_empty_email}
- Редове с телефон: {non_empty_phone}
- Редове с уебсайт: {non_empty_website}
- Разбивка по category:
"""
    for category, count in sorted(categories.items()):
        report += f"  * {category}: {count}\n"
    
    report += f"""
- Общо изтрити редове (начало - край): {total_deleted}
"""
    return report


def main() -> None:
    """Main function to execute the CSV cleaning process."""
    # Define file paths
    script_dir = Path(__file__).parent
    input_file = script_dir / 'warszawa_providers_ceidg.csv'
    output_file = script_dir / 'warszawa_providers_clean.csv'
    report_file = script_dir / 'csv_cleaning_report.txt'
    
    # Check if input file exists
    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        exit(1)
    
    print(f"Reading input file: {input_file}")
    rows = read_csv_file(input_file)
    fieldnames = ['business_name', 'owner_name', 'address', 'phone', 'email', 'website', 'nip', 'pkd_code', 'category', 'source']
    
    print(f"Loaded {len(rows)} rows")
    
    # Generate initial report
    print("\nGenerating initial state report...")
    initial_report = generate_initial_report(rows)
    
    # Clean data
    print("\n" + "="*50)
    cleaned_rows, stats = clean_data(rows)
    print("="*50)
    
    # Generate final report
    print("\nGenerating final report...")
    final_report = generate_final_report(len(rows), cleaned_rows, stats)
    
    # Combine reports
    full_report = initial_report + final_report
    
    # Write cleaned CSV
    print(f"\nWriting cleaned data to: {output_file}")
    write_csv_file(output_file, cleaned_rows, fieldnames)
    
    # Write report to file
    print(f"Writing report to: {report_file}")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(full_report)
    
    # Print report to console
    print("\n" + "="*50)
    print("CLEANING REPORT")
    print("="*50)
    print(full_report)
    print("="*50)
    print(f"\n✓ Process completed successfully!")
    print(f"✓ Cleaned data saved to: {output_file}")
    print(f"✓ Report saved to: {report_file}")


if __name__ == '__main__':
    main()
