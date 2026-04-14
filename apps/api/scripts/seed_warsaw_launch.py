#!/usr/bin/env python3
"""
Warsaw Launch Seed Script
Inserts Warsaw city, categories, and translations into PostgreSQL.
Fully idempotent - safe to run multiple times.
"""

from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    
    try:
        print("=== Warsaw Launch Seed Script ===\n")
        
        # STEP 1: INSERT CITY
        print("STEP 1: Inserting Warsaw city...")
        # Check if Warsaw already exists
        check_city_sql = text("""
            SELECT COUNT(*) as count FROM locations 
            WHERE country_code = 'PL' AND slug = 'warszawa'
        """)
        city_exists = db.execute(check_city_sql).scalar()
        
        if not city_exists:
            city_sql = text("""
                INSERT INTO locations (country_code, city, slug, lat, lng)
                VALUES ('PL', 'Warszawa', 'warszawa', 52.2297, 21.0122)
            """)
            db.execute(city_sql)
            print("City inserted: Warszawa (PL)")
        else:
            print("City already exists: Warszawa (PL)")
        
        # STEP 2: INSERT 3 CATEGORIES
        print("\nSTEP 2: Inserting categories...")
        categories_sql = text("""
            INSERT INTO categories (slug, parent_id) VALUES
            ('cleaning', NULL),
            ('plumbing', NULL),
            ('massage', NULL)
            ON CONFLICT (slug) DO NOTHING;
        """)
        categories_result = db.execute(categories_sql)
        print("Categories inserted: cleaning, plumbing, massage")
        
        # STEP 3: INSERT ALL TRANSLATIONS
        print("\nSTEP 3: Inserting translations...")
        
        # Translation data
        translations = {
            'cleaning': {
                'bg': 'Почистване', 'cs': 'Úklid', 'da': 'Rengøring', 'de': 'Reinigung', 'el': 'Καθαριότητα',
                'en': 'Cleaning', 'es': 'Limpieza', 'et': 'Koristamine', 'fi': 'Siivous', 'fr': 'Nettoyage',
                'ga': 'Glanadh', 'hr': 'Čišćenje', 'hu': 'Takarítás', 'is': 'Þrif', 'it': 'Pulizie',
                'lb': 'Botzen', 'lt': 'Valymas', 'lv': 'Tīrīšana', 'mk': 'Чистење', 'mt': 'Tindif',
                'nl': 'Schoonmaak', 'no': 'Rengjøring', 'pl': 'Sprzątanie', 'pt': 'Limpeza', 'pt-PT': 'Limpeza',
                'ro': 'Curățenie', 'ru': 'Уборка', 'sk': 'Upratovanie', 'sl': 'Čiščenje', 'sq': 'Pastrim',
                'sr': 'Чишћење', 'sv': 'Städning', 'tr': 'Temizlik', 'uk': 'Прибирання'
            },
            'plumbing': {
                'bg': 'Водопроводчик', 'cs': 'Instalatér', 'da': 'VVS', 'de': 'Klempner', 'el': 'Υδραυλικός',
                'en': 'Plumbing', 'es': 'Fontanería', 'et': 'Torutööd', 'fi': 'Putkiasennus', 'fr': 'Plomberie',
                'ga': 'Pluiméireacht', 'hr': 'Vodoinstalater', 'hu': 'Vízvezeték-szerelés', 'is': 'Pípulagning', 'it': 'Idraulico',
                'lb': 'Klempner', 'lt': 'Santechnika', 'lv': 'Santehniķis', 'mk': 'Водовод', 'mt': 'Idrawlika',
                'nl': 'Loodgieter', 'no': 'Rørlegger', 'pl': 'Hydraulik', 'pt': 'Encanamento', 'pt-PT': 'Canalização',
                'ro': 'Instalații sanitare', 'ru': 'Сантехник', 'sk': 'Inštalatér', 'sl': 'Vodovodne napeljave', 'sq': 'Hidraulik',
                'sr': 'Водоинсталатер', 'sv': 'VVS', 'tr': 'Tesisatçı', 'uk': 'Сантехнік'
            },
            'massage': {
                'bg': 'Масаж', 'cs': 'Masáž', 'da': 'Massage', 'de': 'Massage', 'el': 'Μασάζ',
                'en': 'Massage', 'es': 'Masaje', 'et': 'Massaaž', 'fi': 'Hieronta', 'fr': 'Massage',
                'ga': 'Suathaireacht', 'hr': 'Masaža', 'hu': 'Masszázs', 'is': 'Nudd', 'it': 'Massaggio',
                'lb': 'Massage', 'lt': 'Masažas', 'lv': 'Masāža', 'mk': 'Масажа', 'mt': 'Massaġġ',
                'nl': 'Massage', 'no': 'Massasje', 'pl': 'Masaż', 'pt': 'Massagem', 'pt-PT': 'Massagem',
                'ro': 'Masaj', 'ru': 'Массаж', 'sk': 'Masáž', 'sl': 'Masaža', 'sq': 'Masazh',
                'sr': 'Масажа', 'sv': 'Massage', 'tr': 'Masaj', 'uk': 'Масаж'
            }
        }
        
        total_translations = 0
        for category_slug, names in translations.items():
            for lang, name in names.items():
                translation_sql = text("""
                    INSERT INTO category_translations (category_id, lang, name)
                    SELECT c.id, :lang, :name FROM categories c WHERE c.slug = :slug
                    ON CONFLICT (category_id, lang) DO NOTHING;
                """)
                result = db.execute(translation_sql, {
                    'slug': category_slug,
                    'lang': lang,
                    'name': name
                })
                total_translations += result.rowcount
        
        print(f"Translations inserted: {total_translations} rows")
        
        # Commit all changes
        db.commit()
        print("\n=== All changes committed ===")
        
        # STEP 4: VERIFICATION
        print("\nSTEP 4: Verification...")
        verification_sql = text("""
            SELECT c.slug, COUNT(ct.id) as translation_count
            FROM categories c
            LEFT JOIN category_translations ct ON ct.category_id = c.id
            WHERE c.slug IN ('cleaning', 'plumbing', 'massage')
            GROUP BY c.slug
            ORDER BY c.slug;
        """)
        verification_result = db.execute(verification_sql)
        
        print("\nVerification results:")
        for row in verification_result:
            print(f"  {row.slug}: {row.translation_count} translations")
        
        print("\n=== Warsaw Launch Seed Script Completed ===")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    main()
