#!/usr/bin/env python3
"""
Translation audit script:
1. Extracts t() keys and defaults from apps/web/app/
2. Extracts translations from database (bg and en)
3. Compares and generates CSV audit table
"""

import os
import re
import csv
from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from apps.api.models import Translation

# Database connection
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads",
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Regex patterns
# Pattern for fetchTranslations(lang, 'namespace')
FETCH_PATTERN = re.compile(r'fetchTranslations\([^,]+,\s*[\'"]([^\'"]+)[\'"]\)')
# Pattern for t(namespaceVar, 'key', 'default')
T_PATTERN = re.compile(r't\(([^,]+),\s*[\'"]([^\'"]+)[\'"]\s*,\s*[\'"]([^\'"]*)[\'"]\)')
# Pattern for direct dict access: dict['key'] - only for translation variables
DICT_ACCESS_PATTERN = re.compile(r'(\w+[Tt]Dict|\w+[Tt])\[[\'"]([^\'"]+)[\'"]\]')


def extract_from_code():
    """Extract all t() keys and defaults from apps/web/ - key name only"""
    code_keys = {}
    web_path = Path("/Users/dimitardimitrov/nevumo/apps/web")
    
    # Scan each file for t() calls
    for file_path in web_path.rglob("*"):
        if file_path.suffix in {".tsx", ".ts", ".jsx", ".js"}:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                    # Find all t() calls and extract key and default
                    for match in T_PATTERN.finditer(content):
                        key = match.group(2)
                        default = match.group(3)
                        
                        # Filter out file paths and other non-translation keys
                        if "/" not in key and not key.startswith("["):
                            if key not in code_keys:
                                code_keys[key] = default
                    
                    # Find direct dict access for translation variables
                    for match in DICT_ACCESS_PATTERN.finditer(content):
                        key = match.group(2)
                        
                        # Filter out file paths and other non-translation keys
                        if "/" not in key and not key.startswith("["):
                            if key not in code_keys:
                                code_keys[key] = ""
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
    
    return code_keys


def extract_from_db():
    """Extract translations from database for bg and en"""
    db = SessionLocal()
    try:
        result = db.execute(
            select(Translation).where(Translation.lang.in_(["bg", "en"]))
        )
        translations = result.scalars().all()
        
        db_translations = {"bg": {}, "en": {}}
        for t in translations:
            db_translations[t.lang][t.key] = t.value
        
        return db_translations
    finally:
        db.close()


def compare_and_generate_audit(code_keys, db_translations):
    """Compare code keys with DB translations and generate audit data"""
    # Build a map of key name -> list of DB entries (namespace.key)
    db_key_map = {"en": {}, "bg": {}}
    for lang in ["en", "bg"]:
        for full_key, value in db_translations[lang].items():
            # Extract key part from namespace.key
            key_name = full_key.split(".")[-1] if "." in full_key else full_key
            if key_name not in db_key_map[lang]:
                db_key_map[lang][key_name] = []
            db_key_map[lang][key_name].append({"full_key": full_key, "value": value})
    
    # Get all unique key names
    all_key_names = set(code_keys.keys())
    for lang in ["en", "bg"]:
        all_key_names.update(db_key_map[lang].keys())
    
    audit_data = []
    for key_name in sorted(all_key_names):
        code_default = code_keys.get(key_name, "")
        
        # Get DB entries for this key name
        en_entries = db_key_map["en"].get(key_name, [])
        bg_entries = db_key_map["bg"].get(key_name, [])
        
        # Use first entry if multiple (shouldn't happen normally)
        db_en = en_entries[0]["value"] if en_entries else ""
        db_en_full = en_entries[0]["full_key"] if en_entries else ""
        db_bg = bg_entries[0]["value"] if bg_entries else ""
        db_bg_full = bg_entries[0]["full_key"] if bg_entries else ""
        
        # Determine status
        status = "OK"
        if key_name not in code_keys:
            status = "Not used in code"
        elif not en_entries:
            status = "Missing in DB (EN)"
        elif not bg_entries:
            status = "Missing in DB (BG)"
        elif db_bg == db_en:
            status = "English in BG column"
        elif not code_default:
            status = "No default in code"
        
        # Use the full DB key for display
        display_key = db_en_full or db_bg_full or key_name
        
        audit_data.append({
            "Key": display_key,
            "Source Code Default": code_default,
            "DB English": db_en,
            "DB Bulgarian": db_bg,
            "Status": status,
        })
    
    return audit_data


def main():
    print("Extracting translations from code...")
    code_keys = extract_from_code()
    print(f"Found {len(code_keys)} unique keys in code")
    
    print("Extracting translations from database...")
    db_translations = extract_from_db()
    print(f"Found {len(db_translations['en'])} EN translations in DB")
    print(f"Found {len(db_translations['bg'])} BG translations in DB")
    
    print("Comparing and generating audit...")
    audit_data = compare_and_generate_audit(code_keys, db_translations)
    
    # Write to CSV
    output_path = "/Users/dimitardimitrov/nevumo/translation_audit.csv"
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Key", "Source Code Default", "DB English", "DB Bulgarian", "Status"])
        writer.writeheader()
        writer.writerows(audit_data)
    
    print(f"Audit saved to {output_path}")
    
    # Show summary
    status_counts = {}
    for row in audit_data:
        status = row["Status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("\nStatus summary:")
    for status, count in sorted(status_counts.items()):
        print(f"  {status}: {count}")
    
    # Show first 30 rows
    print("\nFirst 30 rows:")
    print("-" * 200)
    for i, row in enumerate(audit_data[:30]):
        print(f"{i+1:3d}. Key: {row['Key'][:50]:50s} | Code Default: {row['Source Code Default'][:30]:30s} | DB EN: {row['DB English'][:30]:30s} | DB BG: {row['DB Bulgarian'][:30]:30s} | Status: {row['Status']}")


if __name__ == "__main__":
    main()
