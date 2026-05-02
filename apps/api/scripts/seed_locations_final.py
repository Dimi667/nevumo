#!/usr/bin/env python3
"""
Seed locations and translations for Oslo, Helsinki, and Berlin in all 34 languages.
Uses port 5433 for database connection.
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Custom connection to port 5433
DATABASE_URL = "postgresql://nevumo:nevumo@localhost:5433/nevumo_leads"

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# All 34 language codes
LANGUAGES = [
    "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr", "ga", "hr", "hu",
    "is", "it", "lb", "lt", "lv", "mk", "mt", "nl", "no", "pl", "pt", "pt-PT",
    "ro", "ru", "sk", "sl", "sq", "sr", "sv", "tr", "uk"
]

# Cities to add
CITIES = {
    "oslo": {
        "country_code": "NO",
        "lat": 59.9139,
        "lng": 10.7522,
        "city_en": "Oslo",
        "translations": {
            "bg": "Осло", "ru": "Осло", "uk": "Осло", "sr": "Осло", "mk": "Осло", "el": "Όσλο"
        }
    },
    "helsinki": {
        "country_code": "FI",
        "lat": 60.1695,
        "lng": 24.9354,
        "city_en": "Helsinki",
        "translations": {
            "bg": "Хелзинки", "ru": "Хельсинки", "uk": "Гельсінкі", "sr": "Хелсинки",
            "mk": "Хелсинки", "el": "Ελσίνκι", "cs": "Helsinky", "sk": "Helsinki"
        }
    },
    "berlin": {
        "country_code": "DE",
        "lat": 52.5200,
        "lng": 13.4050,
        "city_en": "Berlin",
        "translations": {
            "bg": "Берлин", "ru": "Берлин", "uk": "Берлін", "sr": "Берлин", "mk": "Берлин",
            "el": "Βερολίνο", "hu": "Berlin", "it": "Berlino", "es": "Berlín",
            "pt": "Berlim", "pt-PT": "Berlim", "tr": "Berlin"
        }
    }
}


def get_translation(slug: str, lang: str) -> str:
    """Get translation for a city and language, with fallback to default."""
    city_data = CITIES[slug]
    translations = city_data["translations"]
    
    if lang in translations:
        return translations[lang]
    return city_data["city_en"]  # Default to English name


def main():
    db = SessionLocal()
    
    try:
        print("=== Seed Locations Final Script ===\n")
        
        locations_added = 0
        translations_added = 0
        
        for slug, city_data in CITIES.items():
            # Insert location if not exists
            insert_location_sql = text("""
                INSERT INTO locations (country_code, city, city_en, slug, lat, lng)
                VALUES (:country_code, :city, :city_en, :slug, :lat, :lng)
                ON CONFLICT (country_code, slug) DO NOTHING
                RETURNING id
            """)
            
            result = db.execute(insert_location_sql, {
                "country_code": city_data["country_code"],
                "city": city_data["city_en"],
                "city_en": city_data["city_en"],
                "slug": slug,
                "lat": city_data["lat"],
                "lng": city_data["lng"]
            })
            
            if result.fetchone():
                locations_added += 1
                print(f"✓ Location added: {slug}")
            else:
                print(f"  Location already exists: {slug}")
            
            # Get location ID
            location_query = text("SELECT id FROM locations WHERE slug = :slug")
            location_result = db.execute(location_query, {"slug": slug}).fetchone()
            location_id = location_result.id
            
            # Insert translations for all languages
            for lang in LANGUAGES:
                city_name = get_translation(slug, lang)
                
                insert_translation_sql = text("""
                    INSERT INTO location_translations (location_id, lang, city_name)
                    VALUES (:location_id, :lang, :city_name)
                    ON CONFLICT (location_id, lang) DO NOTHING
                """)
                
                result = db.execute(insert_translation_sql, {
                    "location_id": location_id,
                    "lang": lang,
                    "city_name": city_name
                })
                
                if result.rowcount > 0:
                    translations_added += 1
            
            print(f"  Translations for {slug}: {len(LANGUAGES)} languages")
        
        db.commit()
        
        # Print summary
        print("\n=== Summary ===")
        print(f"Locations added: {locations_added}")
        print(f"Translations added: {translations_added}")
        print("\n=== Seed script completed ===")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
