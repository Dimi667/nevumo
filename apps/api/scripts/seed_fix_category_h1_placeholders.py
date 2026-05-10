#!/usr/bin/env python3
"""
Fix category H1 placeholders in translations table.
Changes hardcoded city names (Warsaw/Варшава/Varsovia/...) to {city} placeholder.
Correct format: "[Category name] [preposition_base] {city}"
Example EN: "Massage in {city}", BG: "Масаж в {city}", PL: "Masaż w {city}"

Run: docker exec nevumo-api python -m apps.api.scripts.seed_fix_category_h1_placeholders
"""

import redis
from sqlalchemy import text
from apps.api.database import SessionLocal
from apps.api.i18n import SUPPORTED_LANGUAGES

CATEGORIES = ["massage", "cleaning", "plumbing"]

def main():
    db = SessionLocal()
    try:
        run_fix(db)
    finally:
        db.close()

def run_fix(db):
    print("🔧 Fixing category H1 placeholders...")
    
    # Get all languages from translations table
    result = db.execute(text("""
        SELECT DISTINCT lang FROM translations WHERE key = 'category.preposition_base'
    """))
    languages = [row[0] for row in result.fetchall()]
    
    print(f"📋 Found {len(languages)} languages with category.preposition_base")
    
    update_count = 0
    
    for lang in languages:
        # Get preposition_base for this language
        prep_result = db.execute(text("""
            SELECT value FROM translations 
            WHERE lang = :lang AND key = 'category.preposition_base'
        """), {"lang": lang})
        prep_row = prep_result.fetchone()
        
        if not prep_row:
            print(f"⚠️  No preposition_base found for {lang}, skipping")
            continue
        
        preposition_base = prep_row[0]
        
        # Process each category
        for category_slug in CATEGORIES:
            # Get category_id from categories table
            cat_result = db.execute(text("""
                SELECT id FROM categories WHERE slug = :slug
            """), {"slug": category_slug})
            cat_row = cat_result.fetchone()
            
            if not cat_row:
                print(f"⚠️  Category {category_slug} not found, skipping")
                continue
            
            category_id = cat_row[0]
            
            # Get category translation for this language
            trans_result = db.execute(text("""
                SELECT name FROM category_translations 
                WHERE category_id = :cat_id AND lang = :lang
            """), {"cat_id": category_id, "lang": lang})
            trans_row = trans_result.fetchone()
            
            if not trans_row:
                print(f"⚠️  No translation found for {category_slug} in {lang}, skipping")
                continue
            
            category_name = trans_row[0]
            
            # Build the H1 string with {city} placeholder
            h1_value = f"{category_name} {preposition_base} {{city}}"
            
            # Update the translations table
            h1_key = f"category.h1_{category_slug}"
            db.execute(text("""
                UPDATE translations 
                SET value = :value 
                WHERE lang = :lang AND key = :key
            """), {"value": h1_value, "lang": lang, "key": h1_key})
            
            update_count += 1
            print(f"✅ Updated {lang}: {h1_key} = '{h1_value}'")
    
    db.commit()
    print(f"\n📊 Updated {update_count} H1 translations")
    
    # Flush Redis cache for category namespace
    flush_cache()
    
    # Verify the changes
    verify(db)

def flush_cache():
    """Flush Redis cache for category translations."""
    print("\n🧹 Flushing Redis cache...")
    
    try:
        # Use nevumo-redis hostname when running in Docker container
        redis_client = redis.Redis(host='nevumo-redis', port=6379, db=0, decode_responses=True)
        redis_client.ping()
        
        # Flush all translation cache keys (pattern: translations:*)
        cache_keys = redis_client.keys("translations:*")
        
        if cache_keys:
            deleted_count = redis_client.delete(*cache_keys)
            print(f"🗑️  Cleared {deleted_count} translation cache keys")
        else:
            print("ℹ️  No translation cache keys found")
            
    except redis.ConnectionError:
        print("⚠️  Could not connect to Redis - cache not flushed")
    except Exception as e:
        print(f"⚠️  Error flushing cache: {e}")

def verify(db):
    """Verify the H1 translations now contain {city} placeholder."""
    print("\n🔍 Verifying H1 translations...")
    
    for category_slug in CATEGORIES:
        h1_key = f"category.h1_{category_slug}"
        result = db.execute(text("""
            SELECT lang, value FROM translations 
            WHERE key = :key ORDER BY lang
        """), {"key": h1_key})
        
        print(f"\n{h1_key}:")
        for row in result.fetchall():
            lang, value = row[0], row[1]
            has_placeholder = "{city}" in value
            status = "✅" if has_placeholder else "❌"
            print(f"  {status} {lang}: {value}")

if __name__ == "__main__":
    main()
