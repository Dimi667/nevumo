#!/usr/bin/env python3
"""
Seed script to add prefixed FAQ keys for 22 languages
Run: python -m apps.api.scripts.seed_prefixed_faq_keys
"""
from sqlalchemy import text
from apps.api.database import SessionLocal


def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()


def run_seed(db):
    # Languages missing prefixed FAQ keys
    missing_languages = [
        "cs", "da", "el", "et", "fi", "ga", "hr", "hu", "is", "lb",
        "lt", "lv", "mk", "mt", "no", "pt", "pt-PT", "sk", "sl",
        "sq", "sr", "sv"
    ]
    
    # FAQ keys to copy
    faq_keys = [
        "faq_cleaning_q1",
        "faq_cleaning_q2",
        "faq_cleaning_q3",
        "faq_cleaning_a1",
        "faq_cleaning_a2",
        "faq_cleaning_a3"
    ]
    
    count = 0
    for lang in missing_languages:
        for key in faq_keys:
            # Query existing non-prefixed value
            result = db.execute(
                text("""
                    SELECT value FROM translations
                    WHERE lang = :lang AND key = :key
                """),
                {"lang": lang, "key": key}
            ).fetchone()
            
            if result and result[0]:
                # Insert with category. prefix
                prefixed_key = f"category.{key}"
                db.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": prefixed_key, "value": result[0]}
                )
                count += 1
                print(f"  {lang}: {key} -> {prefixed_key}")
            else:
                print(f"  {lang}: {key} NOT FOUND - skipping")
    
    db.commit()
    print(f"\nInserted/updated {count} prefixed FAQ translation rows")
    
    verify(db, missing_languages)


def verify(db, languages):
    print("\nPrefixed FAQ Translation Verification:")
    for lang in languages:
        result = db.execute(
            text("""
                SELECT COUNT(*) as keys
                FROM translations
                WHERE lang = :lang AND key LIKE 'category.faq_cleaning%'
            """),
            {"lang": lang}
        ).fetchone()
        print(f"  {lang}: {result[0]} prefixed keys")


if __name__ == "__main__":
    main()
