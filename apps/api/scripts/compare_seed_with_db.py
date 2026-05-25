#!/usr/bin/env python3
"""
Safe comparison script - only READS from database, no modifications
Compares seed_ui_translations.py values with current database values
Run: docker exec nevumo-api python -m apps.api.scripts.compare_seed_with_db
"""
import sys
import json
from sqlalchemy import text
from apps.api.database import SessionLocal

sys.path.insert(0, '/app')
from apps.api.scripts.seed_ui_translations import ALL_TRANSLATIONS

def main():
    db = SessionLocal()
    try:
        compare_translations(db, ALL_TRANSLATIONS)
    finally:
        db.close()

def compare_translations(db, seed_data):
    # Flatten seed data
    seed_flat = {}
    for lang, keys in seed_data.items():
        for key, value in keys.items():
            seed_flat[(lang, key)] = value
    
    # Get current values from database (READ ONLY)
    result = db.execute(text("""
        SELECT lang, key, value
        FROM translations
        WHERE key LIKE 'homepage.%' OR key LIKE 'category.%'
        ORDER BY lang, key
    """))
    
    db_values = {}
    for row in result.fetchall():
        db_values[(row[0], row[1])] = row[2]
    
    # Compare
    differences = []
    only_in_seed = []
    only_in_db = []
    
    for (lang, key), seed_value in seed_flat.items():
        if (lang, key) in db_values:
            db_value = db_values[(lang, key)]
            if seed_value != db_value:
                differences.append({"lang": lang, "key": key, "seed": seed_value, "db": db_value})
        else:
            only_in_seed.append((lang, key))
    
    for (lang, key) in db_values.keys():
        if (lang, key) not in seed_flat:
            only_in_db.append((lang, key))
    
    # Report
    print(f"\n=== SAFE COMPARISON REPORT ===")
    print(f"Total keys in seed: {len(seed_flat)}")
    print(f"Total keys in DB (homepage/category): {len(db_values)}")
    print(f"\nDifferences (seed != db): {len(differences)}")
    print(f"Keys only in seed: {len(only_in_seed)}")
    print(f"Keys only in DB: {len(only_in_db)}")
    
    if differences:
        print(f"\n=== DIFFERENCES ({len(differences)}) ===")
        for diff in differences[:30]:
            print(f"\n[{diff['lang']}] {diff['key']}")
            print(f"  Seed: {diff['seed']}")
            print(f"  DB:   {diff['db']}")
        if len(differences) > 30:
            print(f"\n... and {len(differences) - 30} more differences")
    else:
        print(f"\n✓ No differences found - seed and DB are in sync")
    
    if only_in_seed:
        print(f"\n=== KEYS ONLY IN SEED ({len(only_in_seed)}) ===")
        for lang, key in only_in_seed[:10]:
            print(f"[{lang}] {key}")
        if len(only_in_seed) > 10:
            print(f"... and {len(only_in_seed) - 10} more")
    
    if only_in_db:
        print(f"\n=== KEYS ONLY IN DB ({len(only_in_db)}) ===")
        for lang, key in only_in_db[:10]:
            print(f"[{lang}] {key}")
        if len(only_in_db) > 10:
            print(f"... and {len(only_in_db) - 10} more")

if __name__ == "__main__":
    main()
