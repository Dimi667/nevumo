#!/usr/bin/env python3
"""
Seed script for provider card translations (1 key in category namespace)
Run: python scripts/seed_provider_card_translations.py
"""
import os
import psycopg2

def main():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    translations = {
        'category.provider_direct_contact': {
            'en': 'Direct contact', 'bg': 'Директен контакт', 'pl': 'Bezpośredni kontakt',
            'de': 'Direktkontakt', 'fr': 'Contact direct', 'es': 'Contacto directo',
            'it': 'Contatto diretto', 'nl': 'Direct contact', 'pt': 'Contato direto',
            'pt-PT': 'Contacto direto', 'ro': 'Contact direct', 'cs': 'Přímý kontakt',
            'sk': 'Priamy kontakt', 'hu': 'Közvetlen kapcsolat', 'hr': 'Izravni kontakt',
            'sl': 'Neposredni stik', 'sr': 'Direktan kontakt', 'mk': 'Директен контакт',
            'sq': 'Kontakt i drejtpërdrejtë', 'el': 'Άμεση επαφή', 'tr': 'Doğrudan iletişim',
            'ru': 'Прямой контакт', 'uk': 'Прямий контакт', 'lv': 'Tiešs kontakts',
            'lt': 'Tiesioginis kontaktas', 'et': 'Otsene kontakt', 'fi': 'Suora yhteys',
            'sv': 'Direkt kontakt', 'da': 'Direkte kontakt', 'no': 'Direkte kontakt',
            'is': 'Bein samskipti', 'lb': 'Direkten Kontakt', 'ga': 'Teagmháil dhíreach',
            'mt': 'Kuntatt dirett',
        }
    }

    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    count = 0
    for key, langs in translations.items():
        for lang, value in langs.items():
            cur.execute("""
                INSERT INTO translations (lang, key, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
            """, (lang, key, value))
            count += 1
    conn.commit()
    cur.close()
    conn.close()
    print(f"Seeded provider_direct_contact: {count} rows")

if __name__ == '__main__':
    main()
