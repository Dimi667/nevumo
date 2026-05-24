#!/usr/bin/env python3
"""
Restore 11 missing translation keys from backup that were overwritten by seed_provider_dashboard_translations.py.
Keys: msg_saving, placeholder_private_notes, msg_notes_saved, msg_notes_save_failed, msg_no_description, 
      lead_detail_title, label_private_notes, label_client_message, btn_save_notes, btn_close, aria_close
"""

from sqlalchemy import text
from apps.api.database import engine

def main():
    print("Reading translations from file...")
    
    # Read the extracted translations
    translations = []
    with open("/tmp/keys_to_restore.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) >= 3:
                lang, key, value = parts[:3]
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
