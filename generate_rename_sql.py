#!/usr/bin/env python3
"""
Generate SQL script to rename keys in translations table
Based on full_project_audit.csv - rename old keys (without prefix) to new keys (with prefix)
"""
import csv

# Build mapping: old_key -> new_key for keys that exist in DB without prefix
rename_mappings = []

with open('full_project_audit.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'NAMESPACE_MISMATCH' in row['Status']:
            old_key = row['Key in Code']
            # Extract namespace from status: "NAMESPACE_MISMATCH (code: meta_title, db: homepage.meta_title)"
            status = row['Status']
            if 'db:' in status:
                db_key = status.split('db:')[1].rstrip('")')
                new_key = db_key
                
                # Only add if the keys are different
                if old_key != new_key:
                    rename_mappings.append({
                        'old_key': old_key,
                        'new_key': new_key
                    })

print(f"Total rename mappings: {len(rename_mappings)}")

# Remove duplicates
unique_mappings = {}
for mapping in rename_mappings:
    unique_mappings[mapping['old_key']] = mapping['new_key']

print(f"Unique rename mappings: {len(unique_mappings)}")

# Generate SQL script
with open('rename_translation_keys.sql', 'w', encoding='utf-8') as f:
    f.write("-- Rename translation keys to include namespace prefix\n")
    f.write("-- Generated from full_project_audit.csv\n\n")
    
    for old_key, new_key in sorted(unique_mappings.items()):
        # Remove any leading/trailing spaces from keys
        clean_new_key = new_key.strip()
        clean_old_key = old_key.strip()
        f.write(f"UPDATE translations SET key = '{clean_new_key}' WHERE key = '{clean_old_key}';\n")

print("SQL script generated: rename_translation_keys.sql")
