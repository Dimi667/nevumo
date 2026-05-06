from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        query = text("""
            INSERT INTO translations (lang, key, value)
            SELECT lang, 'category.price_on_request' as key, value
            FROM translations
            WHERE key = 'widget.price_on_request'
            ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
        """)
        result = db.execute(query)
        db.commit()
        print(f"Inserted/Updated {result.rowcount} category.price_on_request keys")
    finally:
        db.close()

if __name__ == "__main__":
    main()
