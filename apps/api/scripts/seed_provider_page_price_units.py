from sqlalchemy import text
from apps.api.database import SessionLocal

def main():
    db = SessionLocal()
    try:
        run_seed(db)
    finally:
        db.close()

def run_seed(db):
    insert_translations(db, ALL_TRANSLATIONS)
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
        SELECT lang, COUNT(*) as keys
        FROM translations
        WHERE key LIKE 'provider_page.%'
        GROUP BY lang
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[1]} keys")

ALL_TRANSLATIONS: dict[str, dict[str, str]] = {
  "bg": {
    "provider_page.price_per_hour": "/ч",
    "provider_page.price_on_request": "По запитване",
  },
  "cs": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Na dotaz",
  },
  "da": {
    "provider_page.price_per_hour": "/t",
    "provider_page.price_on_request": "Efter aftale",
  },
  "de": {
    "provider_page.price_per_hour": "/Std.",
    "provider_page.price_on_request": "Auf Anfrage",
  },
  "el": {
    "provider_page.price_per_hour": "/ώρα",
    "provider_page.price_on_request": "Κατόπιν αιτήματος",
  },
  "en": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "On request",
  },
  "es": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "A consultar",
  },
  "et": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Päringul",
  },
  "fi": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Pyydettäessä",
  },
  "fr": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Sur demande",
  },
  "ga": {
    "provider_page.price_per_hour": "/u",
    "provider_page.price_on_request": "Ar iarratas",
  },
  "hr": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Na upit",
  },
  "hu": {
    "provider_page.price_per_hour": "/ó",
    "provider_page.price_on_request": "Érdeklődjön",
  },
  "is": {
    "provider_page.price_per_hour": "/klst",
    "provider_page.price_on_request": "Að beiðni",
  },
  "it": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Su richiesta",
  },
  "lb": {
    "provider_page.price_per_hour": "/St.",
    "provider_page.price_on_request": "Op Ufro",
  },
  "lt": {
    "provider_page.price_per_hour": "/val.",
    "provider_page.price_on_request": "Pagal užklausą",
  },
  "lv": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Pēc pieprasījuma",
  },
  "mk": {
    "provider_page.price_per_hour": "/ч",
    "provider_page.price_on_request": "По барање",
  },
  "mt": {
    "provider_page.price_per_hour": "/siegħa",
    "provider_page.price_on_request": "Fuq talba",
  },
  "nl": {
    "provider_page.price_per_hour": "/u",
    "provider_page.price_on_request": "Op aanvraag",
  },
  "no": {
    "provider_page.price_per_hour": "/t",
    "provider_page.price_on_request": "Etter avtale",
  },
  "pl": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Na zapytanie",
  },
  "pt": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Sob consulta",
  },
  "pt-PT": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Sob consulta",
  },
  "ro": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "La cerere",
  },
  "ru": {
    "provider_page.price_per_hour": "/ч",
    "provider_page.price_on_request": "По запросу",
  },
  "sk": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Na požiadanie",
  },
  "sl": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "Na povpraševanje",
  },
  "sq": {
    "provider_page.price_per_hour": "/orë",
    "provider_page.price_on_request": "Me kërkesë",
  },
  "sr": {
    "provider_page.price_per_hour": "/ч",
    "provider_page.price_on_request": "По захтеву",
  },
  "sv": {
    "provider_page.price_per_hour": "/h",
    "provider_page.price_on_request": "På begäran",
  },
  "tr": {
    "provider_page.price_per_hour": "/sa",
    "provider_page.price_on_request": "Talep üzerine",
  },
  "uk": {
    "provider_page.price_per_hour": "/год",
    "provider_page.price_on_request": "На запит",
  },
}

if __name__ == "__main__":
    main()
