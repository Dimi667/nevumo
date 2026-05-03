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
        WHERE key IN ('category.preposition_base', 'category.preposition_modified')
        ORDER BY lang, key
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} = {row[2]}")

TRANSLATIONS: dict[str, dict[str, str]] = {
    "bg": {
        "category.preposition_base": "в",
        "category.preposition_modified": "във",
    },
    "cs": {
        "category.preposition_base": "v",
        "category.preposition_modified": "ve",
    },
    "da": {
        "category.preposition_base": "i",
        "category.preposition_modified": "i",
    },
    "de": {
        "category.preposition_base": "in",
        "category.preposition_modified": "in",
    },
    "el": {
        "category.preposition_base": "στο",
        "category.preposition_modified": "στο",
    },
    "en": {
        "category.preposition_base": "in",
        "category.preposition_modified": "in",
    },
    "es": {
        "category.preposition_base": "en",
        "category.preposition_modified": "en",
    },
    "et": {
        "category.preposition_base": "s",
        "category.preposition_modified": "s",
    },
    "fi": {
        "category.preposition_base": "ssä",
        "category.preposition_modified": "ssä",
    },
    "fr": {
        "category.preposition_base": "à",
        "category.preposition_modified": "à",
    },
    "ga": {
        "category.preposition_base": "i",
        "category.preposition_modified": "i",
    },
    "hr": {
        "category.preposition_base": "u",
        "category.preposition_modified": "u",
    },
    "hu": {
        "category.preposition_base": "-ban",
        "category.preposition_modified": "-ban",
    },
    "is": {
        "category.preposition_base": "í",
        "category.preposition_modified": "í",
    },
    "it": {
        "category.preposition_base": "in",
        "category.preposition_modified": "in",
    },
    "lb": {
        "category.preposition_base": "an",
        "category.preposition_modified": "an",
    },
    "lt": {
        "category.preposition_base": "viename",
        "category.preposition_modified": "viename",
    },
    "lv": {
        "category.preposition_base": "iekš",
        "category.preposition_modified": "iekš",
    },
    "mk": {
        "category.preposition_base": "во",
        "category.preposition_modified": "во",
    },
    "mt": {
        "category.preposition_base": "f",
        "category.preposition_modified": "f",
    },
    "nl": {
        "category.preposition_base": "in",
        "category.preposition_modified": "in",
    },
    "no": {
        "category.preposition_base": "i",
        "category.preposition_modified": "i",
    },
    "pl": {
        "category.preposition_base": "w",
        "category.preposition_modified": "we",
    },
    "pt": {
        "category.preposition_base": "em",
        "category.preposition_modified": "em",
    },
    "pt-PT": {
        "category.preposition_base": "em",
        "category.preposition_modified": "em",
    },
    "ro": {
        "category.preposition_base": "în",
        "category.preposition_modified": "în",
    },
    "ru": {
        "category.preposition_base": "в",
        "category.preposition_modified": "во",
    },
    "sk": {
        "category.preposition_base": "v",
        "category.preposition_modified": "ve",
    },
    "sl": {
        "category.preposition_base": "v",
        "category.preposition_modified": "v",
    },
    "sq": {
        "category.preposition_base": "në",
        "category.preposition_modified": "në",
    },
    "sr": {
        "category.preposition_base": "у",
        "category.preposition_modified": "у",
    },
    "sv": {
        "category.preposition_base": "i",
        "category.preposition_modified": "i",
    },
    "tr": {
        "category.preposition_base": "de",
        "category.preposition_modified": "de",
    },
    "uk": {
        "category.preposition_base": "в",
        "category.preposition_modified": "во",
    },
}

if __name__ == "__main__":
    main()
