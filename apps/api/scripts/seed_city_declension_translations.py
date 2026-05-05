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
        "city.locative_form": "Варшава",
        "city.genitive_form": "Варшава",
    },
    "cs": {
        "city.locative_form": "Varšavě",
        "city.genitive_form": "Varšavy",
    },
    "da": {
        "city.locative_form": "Warszawa",
        "city.genitive_form": "Warszawas",
    },
    "de": {
        "city.locative_form": "Warschau",
        "city.genitive_form": "Warschaus",
    },
    "el": {
        "city.locative_form": "Βαρσοβία",
        "city.genitive_form": "Βαρσοβίας",
    },
    "en": {
        "city.locative_form": "Warsaw",
        "city.genitive_form": "Warsaw",
    },
    "es": {
        "city.locative_form": "Varsovia",
        "city.genitive_form": "Varsovia",
    },
    "et": {
        "city.locative_form": "Varssavis",
        "city.genitive_form": "Varssavi",
    },
    "fi": {
        "city.locative_form": "Varsovassa",
        "city.genitive_form": "Varsovan",
    },
    "fr": {
        "city.locative_form": "Varsovie",
        "city.genitive_form": "Varsovie",
    },
    "ga": {
        "city.locative_form": "Vársá",
        "city.genitive_form": "Vársá",
    },
    "hr": {
        "city.locative_form": "Varšavi",
        "city.genitive_form": "Varšave",
    },
    "hu": {
        "city.locative_form": "Varsóban",
        "city.genitive_form": "Varsó",
    },
    "is": {
        "city.locative_form": "Varsjá",
        "city.genitive_form": "Varsjár",
    },
    "it": {
        "city.locative_form": "Varsavia",
        "city.genitive_form": "Varsavia",
    },
    "lb": {
        "city.locative_form": "Warschau",
        "city.genitive_form": "Warschau",
    },
    "lt": {
        "city.locative_form": "Varšuvoje",
        "city.genitive_form": "Varšuvos",
    },
    "lv": {
        "city.locative_form": "Varšavā",
        "city.genitive_form": "Varšavas",
    },
    "mk": {
        "city.locative_form": "Варшава",
        "city.genitive_form": "Варшава",
    },
    "mt": {
        "city.locative_form": "Varsavja",
        "city.genitive_form": "Varsavja",
    },
    "nl": {
        "city.locative_form": "Warschau",
        "city.genitive_form": "Warschau",
    },
    "no": {
        "city.locative_form": "Warszawa",
        "city.genitive_form": "Warszawas",
    },
    "pl": {
        "city.locative_form": "Warszawie",
        "city.genitive_form": "Warszawy",
    },
    "pt": {
        "city.locative_form": "Varsóvia",
        "city.genitive_form": "Varsóvia",
    },
    "pt-PT": {
        "city.locative_form": "Varsóvia",
        "city.genitive_form": "Varsóvia",
    },
    "ro": {
        "city.locative_form": "Varșovia",
        "city.genitive_form": "Varșoviei",
    },
    "ru": {
        "city.locative_form": "Варшаве",
        "city.genitive_form": "Варшавы",
    },
    "sk": {
        "city.locative_form": "Varšave",
        "city.genitive_form": "Varšavy",
    },
    "sl": {
        "city.locative_form": "Varšavi",
        "city.genitive_form": "Varšave",
    },
    "sq": {
        "city.locative_form": "Varshavë",
        "city.genitive_form": "Varshavës",
    },
    "sr": {
        "city.locative_form": "Варшави",
        "city.genitive_form": "Варшаве",
    },
    "sv": {
        "city.locative_form": "Warszawa",
        "city.genitive_form": "Warszawas",
    },
    "tr": {
        "city.locative_form": "Varşova'da",
        "city.genitive_form": "Varşova'nın",
    },
    "uk": {
        "city.locative_form": "Варшаві",
        "city.genitive_form": "Варшави",
    },
}

if __name__ == "__main__":
    main()
