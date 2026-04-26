import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

TRANSLATIONS = {
    "category.provider_on_request": {
        "bg": "По договаряне",
        "cs": "Na vyžádání",
        "da": "Efter aftale",
        "de": "Auf Anfrage",
        "el": "Κατόπιν συμφωνίας",
        "en": "On request",
        "es": "A consultar",
        "et": "Hinnapäringul",
        "fi": "Sopimuksen mukaan",
        "fr": "Sur demande",
        "ga": "Ar iarratas",
        "hr": "Na upit",
        "hu": "Megegyezés szerint",
        "is": "Á beiðni",
        "it": "Su richiesta",
        "lb": "Op Ufro",
        "lt": "Pagal susitarimą",
        "lv": "Pēc pieprasījuma",
        "mk": "По договор",
        "mt": "Fuq talba",
        "nl": "Op aanvraag",
        "no": "Etter avtale",
        "pl": "Na zapytanie",
        "pt": "Sob consulta",
        "pt-PT": "Sob consulta",
        "ro": "La cerere",
        "ru": "По запросу",
        "sk": "Na požiadanie",
        "sl": "Na povpraševanje",
        "sq": "Me kërkesë",
        "sr": "На упит",
        "sv": "På begäran",
        "tr": "Talep üzerine",
        "uk": "За запитом",
    }
}


def main() -> None:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    rows: list[tuple[str, str, str]] = []
    for key, langs in TRANSLATIONS.items():
        for lang, value in langs.items():
            rows.append((lang, key, value))

    query = """
        INSERT INTO translations (lang, key, value)
        VALUES (%s, %s, %s)
        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
    """

    cur.executemany(query, rows)
    conn.commit()
    cur.close()
    conn.close()

    print(f"Inserted/updated {len(rows)} translations.")


if __name__ == "__main__":
    main()
