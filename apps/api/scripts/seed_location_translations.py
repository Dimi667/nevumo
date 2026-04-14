#!/usr/bin/env python3
"""
Seed location translations for Sofia, Belgrade, and Warsaw in all 34 languages.
Uses INSERT ... ON CONFLICT for idempotent upserts.
"""

from sqlalchemy import text
from apps.api.database import SessionLocal

TRANSLATIONS = {
    "sofia": {
        "bg": "София", "cs": "Sofia", "da": "Sofia", "de": "Sofia",
        "el": "Σόφια", "en": "Sofia", "es": "Sofía", "et": "Sofia",
        "fi": "Sofia", "fr": "Sofia", "ga": "Sofia", "hr": "Sofija",
        "hu": "Szófia", "is": "Sofía", "it": "Sofia", "lb": "Sofia",
        "lt": "Sofija", "lv": "Sofija", "mk": "Софија", "mt": "Sofia",
        "nl": "Sofia", "no": "Sofia", "pl": "Sofia", "pt": "Sófia",
        "pt-PT": "Sófia", "ro": "Sofia", "ru": "София", "sk": "Sofia",
        "sl": "Sofija", "sq": "Sofia", "sr": "Софија", "sv": "Sofia",
        "tr": "Sofya", "uk": "Софія"
    },
    "belgrade": {
        "bg": "Белград", "cs": "Bělehrad", "da": "Beograd", "de": "Belgrad",
        "el": "Βελιγράδι", "en": "Belgrade", "es": "Belgrado", "et": "Belgrad",
        "fi": "Belgrad", "fr": "Belgrade", "ga": "Béalgrád", "hr": "Beograd",
        "hu": "Belgrád", "is": "Belgrad", "it": "Belgrado", "lb": "Beograd",
        "lt": "Belgradas", "lv": "Belgrada", "mk": "Белград", "mt": "Belgrad",
        "nl": "Belgrado", "no": "Beograd", "pl": "Belgrad", "pt": "Belgrado",
        "pt-PT": "Belgrado", "ro": "Belgrad", "ru": "Белград", "sk": "Belehrad",
        "sl": "Beograd", "sq": "Beogradi", "sr": "Београд", "sv": "Belgrad",
        "tr": "Belgrad", "uk": "Белград"
    },
    "warszawa": {
        "bg": "Варшава", "cs": "Varšava", "da": "Warszawa", "de": "Warschau",
        "el": "Βαρσοβία", "en": "Warsaw", "es": "Varsovia", "et": "Varssavi",
        "fi": "Varsova", "fr": "Varsovie", "ga": "Vársá", "hr": "Varšava",
        "hu": "Varsó", "is": "Varsjá", "it": "Varsavia", "lb": "Warschau",
        "lt": "Varšuva", "lv": "Varšava", "mk": "Варшава", "mt": "Varsavja",
        "nl": "Warschau", "no": "Warszawa", "pl": "Warszawa", "pt": "Varsóvia",
        "pt-PT": "Varsóvia", "ro": "Varșovia", "ru": "Варшава", "sk": "Varšava",
        "sl": "Varšava", "sq": "Varshavë", "sr": "Варшава", "sv": "Warszawa",
        "tr": "Varşova", "uk": "Варшава"
    }
}


def main():
    db = SessionLocal()
    
    try:
        print("=== Location Translations Seed Script ===\n")
        
        summary = {}
        
        for slug, translations in TRANSLATIONS.items():
            # Fetch location ID by slug
            location_query = text("SELECT id FROM locations WHERE slug = :slug")
            result = db.execute(location_query, {"slug": slug}).fetchone()
            
            if not result:
                print(f"⚠️  Location not found: {slug}")
                summary[slug] = 0
                continue
            
            location_id = result.id
            upsert_count = 0
            
            for lang, city_name in translations.items():
                upsert_sql = text("""
                    INSERT INTO location_translations (location_id, lang, city_name)
                    VALUES (:location_id, :lang, :city_name)
                    ON CONFLICT (location_id, lang) DO UPDATE
                    SET city_name = EXCLUDED.city_name
                """)
                
                result = db.execute(upsert_sql, {
                    "location_id": location_id,
                    "lang": lang,
                    "city_name": city_name
                })
                upsert_count += result.rowcount
            
            summary[slug] = upsert_count
            print(f"✓ {slug}: {upsert_count} rows upserted")
        
        db.commit()
        
        # Print summary
        print("\n=== Summary ===")
        total = 0
        for slug, count in summary.items():
            print(f"  {slug}: {count} rows")
            total += count
        print(f"  TOTAL: {total} rows")
        print("\n=== Seed script completed ===")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
