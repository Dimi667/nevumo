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
        WHERE key = 'homepage.select_city_link'
        ORDER BY lang
    """))
    rows = result.fetchall()
    print("\nVerification:")
    for row in rows:
        print(f"  {row[0]}: {row[2]}")

TRANSLATIONS: dict[str, dict[str, str]] = {
    "bg": {"homepage.select_city_link": "Избери град"},
    "cs": {"homepage.select_city_link": "Vybrat město"},
    "da": {"homepage.select_city_link": "Vælg by"},
    "de": {"homepage.select_city_link": "Stadt auswählen"},
    "el": {"homepage.select_city_link": "Επιλογή πόλης"},
    "en": {"homepage.select_city_link": "Select city"},
    "es": {"homepage.select_city_link": "Seleccionar ciudad"},
    "et": {"homepage.select_city_link": "Vali linn"},
    "fi": {"homepage.select_city_link": "Valitse kaupunki"},
    "fr": {"homepage.select_city_link": "Choisir une ville"},
    "ga": {"homepage.select_city_link": "Roghnaigh cathair"},
    "hr": {"homepage.select_city_link": "Odaberi grad"},
    "hu": {"homepage.select_city_link": "Város kiválasztása"},
    "is": {"homepage.select_city_link": "Veldu borg"},
    "it": {"homepage.select_city_link": "Seleziona città"},
    "lb": {"homepage.select_city_link": "Stad auswielen"},
    "lt": {"homepage.select_city_link": "Pasirinkti miestą"},
    "lv": {"homepage.select_city_link": "Izvēlēties pilsētu"},
    "mk": {"homepage.select_city_link": "Избери град"},
    "mt": {"homepage.select_city_link": "Agħżel belt"},
    "nl": {"homepage.select_city_link": "Stad selecteren"},
    "no": {"homepage.select_city_link": "Velg by"},
    "pl": {"homepage.select_city_link": "Wybierz miasto"},
    "pt": {"homepage.select_city_link": "Selecionar cidade"},
    "pt-PT": {"homepage.select_city_link": "Selecionar cidade"},
    "ro": {"homepage.select_city_link": "Selectează orașul"},
    "ru": {"homepage.select_city_link": "Выбрать город"},
    "sk": {"homepage.select_city_link": "Vybrať mesto"},
    "sl": {"homepage.select_city_link": "Izberi mesto"},
    "sq": {"homepage.select_city_link": "Zgjidh qytetin"},
    "sr": {"homepage.select_city_link": "Izaberi grad"},
    "sv": {"homepage.select_city_link": "Välj stad"},
    "tr": {"homepage.select_city_link": "Şehir seç"},
    "uk": {"homepage.select_city_link": "Вибрати місто"},
}

if __name__ == "__main__":
    main()
