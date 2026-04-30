from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        result = db.execute(
            text("DELETE FROM translations WHERE key IN ('price_text_range', 'price_meta_range', 'price_faq_range', 'price_text_none')")
        )
        db.commit()
        print(f"Deleted {result.rowcount} old price translation rows")
    finally:
        db.close()

if __name__ == "__main__":
    main()
