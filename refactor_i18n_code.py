#!/usr/bin/env python3
"""
Refactor i18n code to use full prefixed keys (e.g., 'homepage.meta_title' instead of 'meta_title')
Based on full_project_audit.csv
"""
import csv
import re
from pathlib import Path

# Build mapping: file -> list of (old_key, new_key, dict_var)
file_mappings = {}

with open('full_project_audit.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if 'NAMESPACE_MISMATCH' in row['Status']:
            file_path = row['File Path']
            old_key = row['Key in Code']
            
            # Extract namespace from status: "NAMESPACE_MISMATCH (code: meta_title, db: homepage.meta_title)"
            status = row['Status']
            if 'db:' in status:
                db_key = status.split('db:')[1].rstrip('")')
                new_key = db_key
                dict_var = row['Dict Variable']
                
                if file_path not in file_mappings:
                    file_mappings[file_path] = []
                file_mappings[file_path].append({
                    'old_key': old_key,
                    'new_key': new_key,
                    'dict_var': dict_var
                })

print(f"Files to refactor: {len(file_mappings)}")
for file_path, mappings in sorted(file_mappings.items()):
    print(f"  {file_path}: {len(mappings)} mappings")

# Perform refactoring
for file_path, mappings in file_mappings.items():
    full_path = Path(file_path)
    if not full_path.exists():
        print(f"SKIP: {file_path} not found")
        continue
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    for mapping in mappings:
        old_key = mapping['old_key']
        new_key = mapping['new_key']
        dict_var = mapping['dict_var']
        
        # Pattern: t(dictVar, 'key', 'default') -> t('namespace.key', 'default')
        if dict_var and dict_var != 'unknown' and dict_var != "'unknown'":
            # Replace t(dictVar, 'key', ...) with t('new_key', ...)
            pattern = rf't\({re.escape(dict_var)},\s*[\'"]{re.escape(old_key)}[\'"]'
            replacement = f"t('{new_key}'"
            content = re.sub(pattern, replacement, content)
        else:
            # For unknown dict_var, try direct key replacement
            pattern = rf't\([\'"]{re.escape(old_key)}[\'"]'
            replacement = f"t('{new_key}'"
            content = re.sub(pattern, replacement, content)
    
    if content != original_content:
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Refactored: {file_path}")
    else:
        print(f"  No changes: {file_path}")

print("\nRefactoring complete!")
