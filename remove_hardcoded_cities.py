#!/usr/bin/env python3
"""
Remove hardcoded city names from seed_ui_translations.py
Only affects the 7 category keys with hardcoded city names
"""

import re

# Keys to clear
KEYS_TO_CLEAR = [
    'category.h1_cleaning',
    'category.h1_plumbing',
    'category.h1_massage',
    'category.subtitle_cleaning',
    'category.subtitle_plumbing',
    'category.subtitle_massage',
    'category.provider_cta_suffix',
]

# Read the file
with open('/Users/dimitardimitrov/nevumo/apps/api/scripts/seed_ui_translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Count changes
changes = 0

# Replace each key's value with empty string
for key in KEYS_TO_CLEAR:
    # Pattern to match: "key": "value with city name"
    pattern = rf'"{re.escape(key)}":\s*"[^"]*"'
    replacement = f'"{key}": ""'
    
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, replacement, content)
        changes += len(matches)
        print(f"Cleared {len(matches)} occurrences of {key}")

# Write back
with open('/Users/dimitardimitrov/nevumo/apps/api/scripts/seed_ui_translations.py', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nTotal changes: {changes}")
print("Expected: 238 (7 keys × 34 languages)")
