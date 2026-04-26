import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

TRANSLATIONS = {
    "category.provider_more_services": {
        "bg": "и още {n} услуги",
        "cs": "a {n} dalších služeb",
        "da": "og {n} flere tjenester",
        "de": "und {n} weitere Leistungen",
        "el": "και {n} ακόμα υπηρεσίες",
        "en": "and {n} more services",
        "es": "y {n} servicios más",
        "et": "ja {n} teenust veel",
        "fi": "ja {n} palvelua lisää",
        "fr": "et {n} services supplémentaires",
        "ga": "agus {n} seirbhís eile",
        "hr": "i {n} više usluga",
        "hu": "és még {n} szolgáltatás",
        "is": "og {n} fleiri þjónustur",
        "it": "e altri {n} servizi",
        "lb": "an nach {n} Servicer",
        "lt": "ir dar {n} paslaugos",
        "lv": "un vēl {n} pakalpojumi",
        "mk": "и уште {n} услуги",
        "mt": "u {n} servizzi oħra",
        "nl": "en nog {n} diensten",
        "no": "og {n} flere tjenester",
        "pl": "i jeszcze {n} usług",
        "pt": "e mais {n} serviços",
        "pt-PT": "e mais {n} serviços",
        "ro": "și încă {n} servicii",
        "ru": "и ещё {n} услуги",
        "sk": "a ďalších {n} služieb",
        "sl": "in še {n} storitev",
        "sq": "dhe {n} shërbime të tjera",
        "sr": "и још {n} услуга",
        "sv": "och {n} fler tjänster",
        "tr": "ve {n} hizmet daha",
        "uk": "і ще {n} послуги",
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
