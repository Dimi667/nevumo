#!/usr/bin/env python3
"""Check widget namespace translations in the database."""

import os
import psycopg2
from collections import defaultdict

# Database connection string (Docker maps 5432 to 5433 on host)
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads")

# All 34 supported languages
ALL_LANGUAGES = [
    "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga", "hr", "hu", "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt", "pt-PT", "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk"
]

# Specific keys to check for
REQUIRED_KEYS = [
    "widget.services_label",
    "widget.price_on_request",
    "widget.jobs_label",
    "widget.rating_label",
    "widget.button_text",
]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Query all widget keys
    cur.execute(
        "SELECT key, lang, value FROM translations WHERE key LIKE 'widget.%' ORDER BY key, lang"
    )
    rows = cur.fetchall()

    # Organize by key and by language
    key_langs = defaultdict(list)
    lang_keys = defaultdict(list)
    for key, lang, value in rows:
        key_langs[key].append(lang)
        lang_keys[lang].append(key)

    print("=" * 70)
    print("WIDGET TRANSLATIONS DIAGNOSTIC REPORT")
    print("=" * 70)

    # 1. Which widget keys exist
    print("\n📋 ALL WIDGET KEYS FOUND (distinct key names):")
    print("-" * 50)
    all_keys = sorted(key_langs.keys())
    for key in all_keys:
        print(f"  • {key}")
    print(f"\n  Total: {len(all_keys)} unique keys")

    # 2. Language coverage per key
    print("\n🌐 LANGUAGE COUNT PER KEY:")
    print("-" * 50)
    for key in all_keys:
        lang_count = len(key_langs[key])
        langs_str = ", ".join(sorted(key_langs[key]))
        print(f"  {key}: {lang_count} languages")
        print(f"     └─ {langs_str}")

    # 3. Key count per language
    print("\n📊 KEY COUNT PER LANGUAGE:")
    print("-" * 50)
    for lang in sorted(ALL_LANGUAGES):
        key_count = len(lang_keys.get(lang, []))
        if key_count == 0:
            print(f"  {lang}: 0 keys (EMPTY)")
        else:
            print(f"  {lang}: {key_count} keys")

    # 4. Which required keys exist
    print("\n🔍 REQUIRED KEYS CHECK:")
    print("-" * 50)
    existing_keys = set(all_keys)
    missing = []
    for required in REQUIRED_KEYS:
        if required in existing_keys:
            lang_count = len(key_langs[required])
            langs_str = ", ".join(sorted(key_langs[required]))
            print(f"  ✅ {required} ({lang_count} languages)")
            print(f"     └─ {langs_str}")
        else:
            print(f"  ❌ {required} - MISSING!")
            missing.append(required)

    # 5. Empty languages
    print("\n⚠️  LANGUAGES WITH NO WIDGET TRANSLATIONS:")
    print("-" * 50)
    empty_langs = []
    for lang in ALL_LANGUAGES:
        if lang not in lang_keys or len(lang_keys[lang]) == 0:
            empty_langs.append(lang)
            print(f"  • {lang}")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total widget keys in DB: {len(all_keys)}")
    print(f"Languages with translations: {len(lang_keys)}")
    print(f"Languages completely empty: {len(empty_langs)}")
    print(f"Required keys checked: {len(REQUIRED_KEYS)}")
    print(f"Missing required keys: {len(missing)}")

    if missing:
        print("\n⚠️  MISSING REQUIRED KEYS:")
        for key in missing:
            print(f"   - {key}")

    if empty_langs:
        print("\n⚠️  EMPTY LANGUAGES (need all keys seeded):")
        for lang in empty_langs:
            print(f"   - {lang}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
