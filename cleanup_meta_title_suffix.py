#!/usr/bin/env python3
"""
Mass correction script for homepage.meta_title translations.
Removes ' | Nevumo' or ' - Nevumo' suffix from all languages.
"""

import psycopg2
import redis
import os
from typing import List, Tuple

# Database connection - use DATABASE_URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://nevumo:nevumo@nevumo-postgres:5432/nevumo_leads')

# Redis connection
REDIS_HOST = os.getenv('REDIS_HOST', 'nevumo-redis')
REDIS_PORT = int(os.getenv('REDIS_PORT', '6379'))

def cleanup_meta_title_suffixes() -> List[Tuple[str, str, str]]:
    """
    Remove ' | Nevumo' or ' - Nevumo' suffix from homepage.meta_title translations.
    Returns list of (lang, old_value, new_value) for corrected records.
    """
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()
    
    corrected = []
    
    try:
        # First, find all records with the key
        cursor.execute(
            "SELECT lang, value FROM translations WHERE key = %s",
            ('homepage.meta_title',)
        )
        records = cursor.fetchall()
        
        print(f"Found {len(records)} records for key 'homepage.meta_title'")
        
        for lang, value in records:
            if value is None:
                continue
                
            old_value = value
            new_value = value
            
            # Remove ' | Nevumo' suffix
            if new_value.endswith(' | Nevumo'):
                new_value = new_value[:-9]  # Remove ' | Nevumo' (9 chars)
            # Remove ' - Nevumo' suffix
            elif new_value.endswith(' - Nevumo'):
                new_value = new_value[:-9]  # Remove ' - Nevumo' (9 chars)
            
            # If value was changed, update the database
            if new_value != old_value:
                cursor.execute(
                    "UPDATE translations SET value = %s WHERE lang = %s AND key = %s",
                    (new_value, lang, 'homepage.meta_title')
                )
                corrected.append((lang, old_value, new_value))
                print(f"  [{lang}] Corrected: '{old_value}' -> '{new_value}'")
        
        conn.commit()
        print(f"\nTotal corrections made: {len(corrected)}")
        
    except Exception as e:
        conn.rollback()
        print(f"Error during database operation: {e}")
        raise
    finally:
        cursor.close()
        conn.close()
    
    return corrected

def flush_redis_cache():
    """Flush all Redis cache to clear old translations."""
    try:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
        r.flushall()
        print(f"\n✓ Redis cache flushed successfully")
    except Exception as e:
        print(f"\n✗ Error flushing Redis: {e}")
        raise

def main():
    print("=" * 60)
    print("Mass Correction: homepage.meta_title suffixes")
    print("=" * 60)
    
    # Step 1: Clean up database
    corrected = cleanup_meta_title_suffixes()
    
    # Step 2: Flush Redis cache
    flush_redis_cache()
    
    # Step 3: Validation report
    print("\n" + "=" * 60)
    print("VALIDATION REPORT")
    print("=" * 60)
    if corrected:
        print(f"\nLanguages corrected: {len(corrected)}")
        print("\nList of corrected languages:")
        for lang, old, new in corrected:
            print(f"  - {lang}")
    else:
        print("\nNo corrections were needed.")
    
    print("\n" + "=" * 60)
    print("Script completed successfully")
    print("=" * 60)

if __name__ == "__main__":
    main()
