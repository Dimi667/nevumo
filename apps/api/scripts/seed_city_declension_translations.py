from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, TRANSLATIONS)
    verify(db)

def insert_translations(db, data: dict[str, dict[str, str]]) -> None:
    count = 0
    for lang, keys in data.items():
        for key, value in keys.items():
            db.execute(
                text("""
                    INSERT INTO translations (lang, key, value)
                    VALUES (:lang, :key, :value)
                    ON CONFLICT (lang, key)
                    DO UPDATE SET value = EXCLUDED.value
                """),
                {"lang": lang, "key": key, "value": value}
            )
            count += 1
    db.commit()
    print(f"Inserted/updated {count} translation rows")

def verify(db) -> None:
    result = db.execute(text("""
        SELECT lang, key, value
        FROM translations
        WHERE key IN ('city.locative_form', 'city.genitive_form')
        ORDER BY lang, key
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} = {row[2]}")

TRANSLATIONS: dict[str, dict[str, str]] = {
    "bg": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "cs": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "da": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "de": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "el": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "en": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "es": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "et": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "fi": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "fr": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "ga": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "hr": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "hu": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "is": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "it": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "lb": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "lt": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "lv": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "mk": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "mt": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "nl": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "no": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "pl": {
        "city.locative_form": "Warszawie",
        "city.genitive_form": "Warszawy",
    },
    "pt": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "pt-PT": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "ro": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "ru": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "sk": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "sl": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "sq": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "sr": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "sv": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "tr": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
    "uk": {
        "city.locative_form": "",
        "city.genitive_form": "",
    },
}

if __name__ == "__main__":
    main()
