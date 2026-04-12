#!/usr/bin/env python3
"""Check auth namespace translations in the database."""

import os
import psycopg2
from collections import defaultdict

# Database connection string
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")

# Specific keys to check for
REQUIRED_KEYS = [
    "auth.hero_title_client",
    "auth.hero_subtitle_client",
    "auth.hero_title_provider",
    "auth.back_btn",
    "auth.register_subtitle",
    "auth.forgot_password_link",
    "auth.login_btn",
    "auth.forgot_title",
    "auth.forgot_subtitle",
    "auth.forgot_send_btn",
]


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # Query all auth keys
    cur.execute(
        "SELECT key, lang, value FROM translations WHERE key LIKE 'auth.%' ORDER BY key, lang"
    )
    rows = cur.fetchall()

    # Organize by key
    key_langs = defaultdict(list)
    for key, lang, value in rows:
        key_langs[key].append(lang)

    print("=" * 70)
    print("AUTH TRANSLATIONS DIAGNOSTIC REPORT")
    print("=" * 70)

    # 1. Which auth keys exist
    print("\n📋 ALL AUTH KEYS FOUND (distinct key names):")
    print("-" * 50)
    all_keys = sorted(key_langs.keys())
    for key in all_keys:
        print(f"  • {key}")
    print(f"\n  Total: {len(all_keys)} unique keys")

    # 2. How many languages each key has
    print("\n🌐 LANGUAGE COUNT PER KEY:")
    print("-" * 50)
    for key in all_keys:
        lang_count = len(key_langs[key])
        langs_str = ", ".join(sorted(key_langs[key]))
        print(f"  {key}: {lang_count} languages")
        print(f"     └─ {langs_str}")

    # 3. Which required keys are MISSING
    print("\n🔍 REQUIRED KEYS CHECK:")
    print("-" * 50)
    existing_keys = set(all_keys)
    missing = []
    for required in REQUIRED_KEYS:
        if required in existing_keys:
            lang_count = len(key_langs[required])
            print(f"  ✅ {required} ({lang_count} languages)")
        else:
            print(f"  ❌ {required} - MISSING!")
            missing.append(required)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Total auth keys in DB: {len(all_keys)}")
    print(f"Required keys checked: {len(REQUIRED_KEYS)}")
    print(f"Missing required keys: {len(missing)}")

    if missing:
        print("\n⚠️  MISSING KEYS THAT NEED TO BE SEEDED:")
        for key in missing:
            print(f"   - {key}")
    else:
        print("\n✅ All required keys exist!")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
