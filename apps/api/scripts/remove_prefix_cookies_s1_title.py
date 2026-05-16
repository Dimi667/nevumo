# -*- coding: utf-8 -*-
"""
remove_prefix_cookies_s1_title.py — Remove "1. " prefix from cookies.s1_title in all languages
Run: docker exec nevumo-api python -m apps.api.scripts.remove_prefix_cookies_s1_title
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def remove_prefix():
    with engine.begin() as conn:
        # Get all translations for cookies.s1_title
        result = conn.execute(
            text("SELECT lang, value FROM translations WHERE key = 'cookies.s1_title'")
        )
        
        updated_count = 0
        for row in result:
            lang, value = row
            # Remove "1. " prefix if present
            if value.startswith("1. "):
                new_value = value[3:]  # Remove first 3 characters ("1. ")
                conn.execute(
                    text("""
                        UPDATE translations 
                        SET value = :new_value 
                        WHERE key = 'cookies.s1_title' AND lang = :lang
                    """),
                    {"new_value": new_value, "lang": lang}
                )
                updated_count += 1
                print(f"Updated {lang}: '{value}' -> '{new_value}'")
            else:
                print(f"Skipped {lang}: '{value}' (no prefix)")
    
    print(f"\nTotal updated: {updated_count} languages")

if __name__ == "__main__":
    remove_prefix()
