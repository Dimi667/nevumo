#!/usr/bin/env python3
"""
Generate missing_translations.json with all MISSING_IN_DB keys
Format: [{"Full_Key": "namespace.key", "Original_English_Text": "text"}]
"""
import csv
import json
from pathlib import Path

missing_entries = []

with open('full_project_audit.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['Status'] == 'MISSING_IN_DB':
            key_in_code = row['Key in Code']
            default_text = row['Default Text (Code)']
            detected_namespace = row['Detected Namespace']
            file_path = row['File Path']
            
            # Determine the namespace based on file path or detected namespace
            if detected_namespace and detected_namespace != 'unknown':
                namespace = detected_namespace
            else:
                # Infer namespace from file path
                if 'auth' in file_path:
                    namespace = 'auth'
                elif 'provider/dashboard' in file_path:
                    namespace = 'provider_dashboard'
                elif 'client/dashboard' in file_path:
                    namespace = 'client_dashboard'
                elif 'page.tsx' in file_path and file_path.endswith('/page.tsx'):
                    namespace = 'homepage'
                elif '[city]/[category]' in file_path:
                    namespace = 'category_page'
                else:
                    namespace = 'unknown'
            
            # Build full key
            if namespace != 'unknown':
                full_key = f"{namespace}.{key_in_code}"
            else:
                full_key = key_in_code
            
            # Clean up default text (remove quotes if present)
            clean_text = default_text.strip()
            if clean_text.startswith("'") and clean_text.endswith("'"):
                clean_text = clean_text[1:-1]
            elif clean_text.startswith('"') and clean_text.endswith('"'):
                clean_text = clean_text[1:-1]
            
            missing_entries.append({
                "Full_Key": full_key,
                "Original_English_Text": clean_text,
                "File_Path": file_path
            })

print(f"Total MISSING_IN_DB entries: {len(missing_entries)}")

# Remove duplicates based on Full_Key
unique_entries = {}
for entry in missing_entries:
    full_key = entry['Full_Key']
    if full_key not in unique_entries:
        unique_entries[full_key] = entry

print(f"Unique MISSING_IN_DB entries: {len(unique_entries)}")

# Export to JSON
output = []
for full_key, entry in sorted(unique_entries.items()):
    output.append({
        "Full_Key": entry['Full_Key'],
        "Original_English_Text": entry['Original_English_Text']
    })

with open('missing_translations.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Generated: missing_translations.json")
print(f"Total entries in JSON: {len(output)}")
