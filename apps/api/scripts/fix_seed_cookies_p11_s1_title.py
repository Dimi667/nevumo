# -*- coding: utf-8 -*-
"""
fix_seed_cookies_p11_s1_title.py — Remove "1. " prefix from cookies.s1_title values only
Run: python3 apps/api/scripts/fix_seed_cookies_p11_s1_title
"""

import os

def fix_seed_file():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "seed_cookies_p11.py")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    in_s1_title = False
    
    for i, line in enumerate(lines):
        if '"cookies.s1_title": {' in line:
            in_s1_title = True
            new_lines.append(line)
        elif in_s1_title and line.strip() == '},':
            in_s1_title = False
            new_lines.append(line)
        elif in_s1_title and '"1. ' in line:
            # Remove "1. " from the value only
            new_line = line.replace('"1. ', '"')
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print("Fixed seed_cookies_p11.py: removed '1. ' prefix from cookies.s1_title values")

if __name__ == "__main__":
    fix_seed_file()
