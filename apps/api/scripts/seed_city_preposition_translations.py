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
        WHERE key IN ('city.preposition_base', 'city.preposition_modified')
        ORDER BY lang, key
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} = {row[2]}")

TRANSLATIONS: dict[str, dict[str, str]] = {
    "bg": {
        "city.preposition_base": "в",
        "city.preposition_modified": "във",
    },
    "cs": {
        "city.preposition_base": "v",
        "city.preposition_modified": "ve",
    },
    "da": {
        "city.preposition_base": "i",
        "city.preposition_modified": "i",
    },
    "de": {
        "city.preposition_base": "in",
        "city.preposition_modified": "in",
    },
    "el": {
        "city.preposition_base": "στο",
        "city.preposition_modified": "στο",
    },
    "en": {
        "city.preposition_base": "in",
        "city.preposition_modified": "in",
    },
    "es": {
        "city.preposition_base": "en",
        "city.preposition_modified": "en",
    },
    "et": {
        "city.preposition_base": "s",
        "city.preposition_modified": "s",
    },
    "fi": {
        "city.preposition_base": "ssä",
        "city.preposition_modified": "ssä",
    },
    "fr": {
        "city.preposition_base": "à",
        "city.preposition_modified": "à",
    },
    "ga": {
        "city.preposition_base": "i",
        "city.preposition_modified": "i",
    },
    "hr": {
        "city.preposition_base": "u",
        "city.preposition_modified": "u",
    },
    "hu": {
        "city.preposition_base": "-ban",
        "city.preposition_modified": "-ban",
    },
    "is": {
        "city.preposition_base": "í",
        "city.preposition_modified": "í",
    },
    "it": {
        "city.preposition_base": "in",
        "city.preposition_modified": "in",
    },
    "lb": {
        "city.preposition_base": "an",
        "city.preposition_modified": "an",
    },
    "lt": {
        "city.preposition_base": "viename",
        "city.preposition_modified": "viename",
    },
    "lv": {
        "city.preposition_base": "iekš",
        "city.preposition_modified": "iekš",
    },
    "mk": {
        "city.preposition_base": "во",
        "city.preposition_modified": "во",
    },
    "mt": {
        "city.preposition_base": "f",
        "city.preposition_modified": "f",
    },
    "nl": {
        "city.preposition_base": "in",
        "city.preposition_modified": "in",
    },
    "no": {
        "city.preposition_base": "i",
        "city.preposition_modified": "i",
    },
    "pl": {
        "city.preposition_base": "w",
        "city.preposition_modified": "we",
    },
    "pt": {
        "city.preposition_base": "em",
        "city.preposition_modified": "em",
    },
    "pt-PT": {
        "city.preposition_base": "em",
        "city.preposition_modified": "em",
    },
    "ro": {
        "city.preposition_base": "în",
        "city.preposition_modified": "în",
    },
    "ru": {
        "city.preposition_base": "в",
        "city.preposition_modified": "во",
    },
    "sk": {
        "city.preposition_base": "v",
        "city.preposition_modified": "ve",
    },
    "sl": {
        "city.preposition_base": "v",
        "city.preposition_modified": "v",
    },
    "sq": {
        "city.preposition_base": "në",
        "city.preposition_modified": "në",
    },
    "sr": {
        "city.preposition_base": "у",
        "city.preposition_modified": "у",
    },
    "sv": {
        "city.preposition_base": "i",
        "city.preposition_modified": "i",
    },
    "tr": {
        "city.preposition_base": "de",
        "city.preposition_modified": "de",
    },
    "uk": {
        "city.preposition_base": "в",
        "city.preposition_modified": "во",
    },
}

if __name__ == "__main__":
    main()
