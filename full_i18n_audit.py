#!/usr/bin/env python3
"""
Full i18n Audit Script for Nevumo Project
Scans all files in apps/web/app/ and apps/web/components/ for t() calls
and compares with PostgreSQL translations table for bg and en.
"""

import os
import re
import csv
import psycopg2
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

# Database connection settings (matching docker-compose.yml)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'nevumo_leads')
DB_USER = os.getenv('DB_USER', 'nevumo')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'nevumo')

# Directories to scan
SCAN_DIRS = [
    '/Users/dimitardimitrov/nevumo/apps/web/app',
    '/Users/dimitardimitrov/nevumo/apps/web/components'
]

# Output file
OUTPUT_FILE = '/Users/dimitardimitrov/nevumo/full_project_audit.csv'


def get_db_connection():
    """Connect to PostgreSQL database."""
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


def fetch_translations_from_db() -> Tuple[Dict[str, str], Dict[str, str]]:
    """
    Fetch all translations from database for bg and en.
    Returns tuple of (en_translations, bg_translations) as dict[key] = text
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Fetch English translations
    cursor.execute("""
        SELECT key, value 
        FROM translations 
        WHERE lang = 'en'
    """)
    en_translations = {row[0]: row[1] for row in cursor.fetchall()}
    
    # Fetch Bulgarian translations
    cursor.execute("""
        SELECT key, value 
        FROM translations 
        WHERE lang = 'bg'
    """)
    bg_translations = {row[0]: row[1] for row in cursor.fetchall()}
    
    cursor.close()
    conn.close()
    
    return en_translations, bg_translations


def extract_t_calls(file_path: str) -> List[Dict[str, str]]:
    """
    Extract all t() calls from a file.
    Returns list of dicts with: key, default, dict_var (if detectable)
    """
    t_calls = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return t_calls
    
    # Pattern to match t(dict, 'key', 'default') or t(dict, "key", "default")
    # Also matches t(dict, 'key') without default
    patterns = [
        r't\s*\(\s*([^,]+)\s*,\s*[\'"]([^\'"]+)[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\s*\)',
        r't\s*\(\s*([^,]+)\s*,\s*[\'"]([^\'"]+)[\'"]\s*,\s*([^\)]+)\)',
        r't\s*\(\s*([^,]+)\s*,\s*[\'"]([^\'"]+)[\'"]\s*\)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, content, re.MULTILINE)
        for match in matches:
            dict_var = match.group(1).strip()
            key = match.group(2)
            default = match.group(3) if len(match.groups()) >= 3 else ''
            
            # Clean up the variables
            dict_var = dict_var.strip()
            key = key.strip()
            default = default.strip()
            
            # Skip if default is another variable or expression
            if default and (default.startswith('{') or default.startswith('$') or default in dict_var):
                default = ''
            
            t_calls.append({
                'key': key,
                'default': default,
                'dict_var': dict_var
            })
    
    return t_calls


def scan_directory(directory: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Scan directory for .tsx, .ts files and extract t() calls.
    Returns dict mapping file_path to list of t_calls.
    """
    results = {}
    
    for root, dirs, files in os.walk(directory):
        # Skip node_modules and other common ignore dirs
        dirs[:] = [d for d in dirs if d not in ['node_modules', '.next', '.git']]
        
        for file in files:
            if file.endswith(('.tsx', '.ts')):
                file_path = os.path.join(root, file)
                t_calls = extract_t_calls(file_path)
                
                if t_calls:
                    results[file_path] = t_calls
    
    return results


def detect_namespace_pattern(file_path: str, dict_var: str) -> str:
    """
    Try to detect the namespace/translation dict being used.
    Returns the namespace name if detectable, otherwise 'unknown'.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 'unknown'
    
    # Look for fetchTranslations calls to determine namespace
    # Pattern: const xxx = await fetchTranslations(lang, 'namespace')
    pattern = r'fetchTranslations\s*\([^,]+,\s*[\'"]([^\'"]+)[\'"]\s*\)'
    matches = re.findall(pattern, content)
    
    if matches:
        # Return the last namespace found (most likely the one used)
        return matches[-1]
    
    # Look for prop names like authDict, categoryT, etc.
    if 'authDict' in dict_var:
        return 'auth'
    elif 'categoryT' in dict_var:
        return 'category'
    elif 'homepageT' in dict_var:
        return 'homepage'
    elif 'translations' in dict_var.lower():
        return 'general'
    
    return 'unknown'


def analyze_namespace_mismatch(code_key: str, db_keys: Set[str], namespace: str) -> str:
    """
    Check if there's a namespace mismatch between code and DB.
    Returns status message.
    """
    # Direct match
    if code_key in db_keys:
        return 'MATCH'
    
    # Check for namespace prefix variations
    # e.g., code has 'login' but DB has 'auth:login' or 'auth.login'
    possible_variations = [
        f"{namespace}:{code_key}",
        f"{namespace}.{code_key}",
        f"{namespace}_{code_key}",
    ]
    
    for variation in possible_variations:
        if variation in db_keys:
            return f'NAMESPACE_MISMATCH (code: {code_key}, db: {variation})'
    
    # Check reverse - code has prefix but DB doesn't
    if ':' in code_key:
        parts = code_key.split(':', 1)
        if parts[1] in db_keys:
            return f'NAMESPACE_MISMATCH (code: {code_key}, db: {parts[1]})'
    elif '.' in code_key:
        parts = code_key.split('.', 1)
        if parts[1] in db_keys:
            return f'NAMESPACE_MISMATCH (code: {code_key}, db: {parts[1]})'
    
    return 'MISSING_IN_DB'


def main():
    print("=" * 80)
    print("FULL I18N AUDIT FOR NEVUMO PROJECT")
    print("=" * 80)
    
    # Step 1: Fetch translations from database
    print("\n[1/5] Fetching translations from PostgreSQL...")
    try:
        en_translations, bg_translations = fetch_translations_from_db()
        print(f"   - Found {len(en_translations)} English translations")
        print(f"   - Found {len(bg_translations)} Bulgarian translations")
    except Exception as e:
        print(f"   ERROR: Failed to fetch translations: {e}")
        print("   Make sure PostgreSQL is running and credentials are correct.")
        return
    
    # Step 2: Scan directories for t() calls
    print("\n[2/5] Scanning directories for t() calls...")
    all_results = {}
    total_t_calls = 0
    
    for directory in SCAN_DIRS:
        print(f"   - Scanning {directory}...")
        results = scan_directory(directory)
        all_results.update(results)
        total_t_calls += sum(len(calls) for calls in results.values())
    
    print(f"   - Found {total_t_calls} t() calls in {len(all_results)} files")
    
    # Step 3: Analyze each t() call
    print("\n[3/5] Analyzing t() calls against database...")
    
    audit_data = []
    unique_keys_in_code = set()
    namespace_stats = defaultdict(int)
    
    for file_path, t_calls in all_results.items():
        for t_call in t_calls:
            key = t_call['key']
            default = t_call['default']
            dict_var = t_call['dict_var']
            
            unique_keys_in_code.add(key)
            
            # Detect namespace
            namespace = detect_namespace_pattern(file_path, dict_var)
            namespace_stats[namespace] += 1
            
            # Check against DB
            en_text = en_translations.get(key, '')
            bg_text = bg_translations.get(key, '')
            
            # Determine status
            if key in en_translations and key in bg_translations:
                status = 'MATCH'
            elif key in en_translations or key in bg_translations:
                status = 'PARTIAL_MATCH'
            else:
                # Check for namespace mismatch
                status = analyze_namespace_mismatch(key, set(en_translations.keys()) | set(bg_translations.keys()), namespace)
            
            audit_data.append({
                'File Path': file_path.replace('/Users/dimitardimitrov/nevumo/', ''),
                'Key in Code': key,
                'Default Text (Code)': default,
                'DB English': en_text,
                'DB Bulgarian': bg_text,
                'Status': status,
                'Detected Namespace': namespace,
                'Dict Variable': dict_var
            })
    
    print(f"   - Analyzed {len(audit_data)} t() calls")
    print(f"   - Found {len(unique_keys_in_code)} unique keys in code")
    
    # Step 4: Write CSV
    print("\n[4/5] Writing audit results to CSV...")
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'File Path', 'Key in Code', 'Default Text (Code)',
                'DB English', 'DB Bulgarian', 'Status',
                'Detected Namespace', 'Dict Variable'
            ])
            writer.writeheader()
            writer.writerows(audit_data)
        print(f"   - Written to {OUTPUT_FILE}")
    except Exception as e:
        print(f"   ERROR: Failed to write CSV: {e}")
        return
    
    # Step 5: Statistics
    print("\n[5/5] Generating statistics...")
    
    # Count statuses
    status_counts = defaultdict(int)
    for item in audit_data:
        status_counts[item['Status']] += 1
    
    # Count unique keys by status
    unique_key_status = {}
    for key in unique_keys_in_code:
        # Find first occurrence of this key to get status
        for item in audit_data:
            if item['Key in Code'] == key:
                unique_key_status[key] = item['Status']
                break
    
    unique_status_counts = defaultdict(int)
    for status in unique_key_status.values():
        unique_status_counts[status] += 1
    
    # Count missing in DB
    missing_in_db = sum(1 for status in unique_key_status.values() if status == 'MISSING_IN_DB')
    
    # Count namespace mismatches
    namespace_mismatches = sum(1 for status in unique_key_status.values() if 'NAMESPACE_MISMATCH' in status)
    
    print("\n" + "=" * 80)
    print("AUDIT STATISTICS")
    print("=" * 80)
    print(f"\nTotal unique keys in code: {len(unique_keys_in_code)}")
    print(f"Total t() calls found: {total_t_calls}")
    print(f"Files scanned: {len(all_results)}")
    print(f"\nKeys by status (unique):")
    for status, count in sorted(unique_status_counts.items()):
        print(f"  - {status}: {count}")
    
    print(f"\nKeys missing in database: {missing_in_db}")
    print(f"Keys with namespace mismatch: {namespace_mismatches}")
    
    print(f"\nDetected namespaces:")
    for namespace, count in sorted(namespace_stats.items()):
        print(f"  - {namespace}: {count} t() calls")
    
    print("\n" + "=" * 80)
    print("AUDIT COMPLETE")
    print("=" * 80)
    print(f"\nFull report saved to: {OUTPUT_FILE}")
    print("\nNext steps:")
    print("1. Review the CSV file for detailed information")
    print("2. Check keys with NAMESPACE_MISMATCH status")
    print("3. Add missing keys to the database")
    print("4. Standardize namespace usage across the codebase")


if __name__ == '__main__':
    main()
