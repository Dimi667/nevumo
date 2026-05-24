#!/usr/bin/env python3
"""
Restore qr_slogan_submit_request translations from backup.
"""

from sqlalchemy import text
from apps.api.database import engine

def main():
    print("Reading qr_slogan_submit_request translations from file...")
    
    # Read the extracted translations
    translations = []
    with open("/tmp/qr_slogan_raw.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 4:
                _, lang, key, value = parts[:4]
                translations.append((lang, key, value))
    
    print(f"Found {len(translations)} translation rows to restore")
    
    # Insert into database
    with engine.begin() as conn:
        for lang, key, value in translations:
            conn.execute(text("""
                INSERT INTO translations (lang, key, value)
                VALUES (:lang, :key, :value)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """), {"lang": lang, "key": key, "value": value})
        
        print(f"✅ Inserted/Updated {len(translations)} translation rows")

if __name__ == "__main__":
    main()
