#!/usr/bin/env python3
"""
Generate row() format for the 13 missing keys from extracted data.
"""

# Read the extracted translations
translations_by_key = {}
with open("/tmp/keys_to_restore.txt", 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        parts = line.split('\t')
        if len(parts) >= 3:
            lang, key, value = parts[:3]
            # Extract key name without namespace
            key_name = key.replace('provider_dashboard.', '')
            if key_name not in translations_by_key:
                translations_by_key[key_name] = {}
            translations_by_key[key_name][lang] = value

# Language order from seed_provider_dashboard_translations.py
LANGS = [
    "en", "bg", "cs", "da", "de", "el", "es", "et", "fi", "fr", "ga", "hr",
    "hu", "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt",
    "pt-PT", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk",
]

# Generate row() format for each key
for key_name in sorted(translations_by_key.keys()):
    values = []
    for lang in LANGS:
        if lang in translations_by_key[key_name]:
            values.append(f'"{translations_by_key[key_name][lang]}"')
        else:
            values.append(f'""')
    
    print(f'    "{key_name}": row(')
    # Print in chunks of 8 per line for readability
    for i in range(0, len(values), 8):
        chunk = values[i:i+8]
        print(f'        {", ".join(chunk)},')
    print('    ),')
    print()
