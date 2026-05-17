#!/usr/bin/env python3
"""
Remove "| Nevumo" from page_title translations in seed_provider_terms_p1_meta.py
Only modifies page_title key, nothing else.
"""

import re

def remove_nevumo_from_page_title():
    file_path = 'apps/api/scripts/seed_provider_terms_p1_meta.py'
    
    print(f"Reading file: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Total lines: {len(lines)}")
    
    modified_lines = []
    in_page_title = False
    modified_count = 0
    
    for i, line in enumerate(lines):
        # Start of page_title block
        if '"page_title":' in line:
            print(f"Line {i}: Found page_title start")
            in_page_title = True
            modified_lines.append(line)
        # End of page_title block - next key starts
        elif in_page_title and '"meta_description"' in line:
            print(f"Line {i}: Found meta_description - ending page_title block")
            in_page_title = False
            modified_lines.append(line)
        # Inside page_title block - remove "| Nevumo"
        elif in_page_title:
            if '| Nevumo' in line:
                print(f"Line {i}: Removing | Nevumo from: {line.strip()}")
                modified_count += 1
            modified_line = re.sub(r'\s*\|\s*Nevumo"', '"', line)
            modified_lines.append(modified_line)
        else:
            modified_lines.append(line)
    
    print(f"Modified {modified_count} lines")
    
    # Write back to file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)
    
    print(f"✅ Removed '| Nevumo' from page_title in {file_path}")
    return True

if __name__ == "__main__":
    remove_nevumo_from_page_title()
