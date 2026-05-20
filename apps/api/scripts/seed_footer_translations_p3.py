#!/usr/bin/env python3
"""
Seed footer translations (P3).
Namespace: footer
Keys: 1 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_footer_translations_p3
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "footer"

# Language dictionaries with full keys (including namespace)
TRANSLATIONS_BY_LANG = {
    "bg": {
        "footer.contact_dsa_link": "Точка за контакт по DSA",
    },
    "cs": {
        "footer.contact_dsa_link": "Kontaktní místo DSA",
    },
    "da": {
        "footer.contact_dsa_link": "DSA-kontaktpunkt",
    },
    "de": {
        "footer.contact_dsa_link": "DSA-Kontaktstelle",
    },
    "el": {
        "footer.contact_dsa_link": "Σημείο επαφής DSA",
    },
    "en": {
        "footer.contact_dsa_link": "DSA Contact Point",
    },
    "es": {
        "footer.contact_dsa_link": "Punto de contacto DSA",
    },
    "et": {
        "footer.contact_dsa_link": "DSA kontaktpunkt",
    },
    "fi": {
        "footer.contact_dsa_link": "DSA-yhteystaho",
    },
    "fr": {
        "footer.contact_dsa_link": "Point de contact DSA",
    },
    "ga": {
        "footer.contact_dsa_link": "Pointe Teagmhála DSA",
    },
    "hr": {
        "footer.contact_dsa_link": "DSA kontaktna točka",
    },
    "hu": {
        "footer.contact_dsa_link": "DSA kapcsolattartási pont",
    },
    "is": {
        "footer.contact_dsa_link": "DSA tengiliður",
    },
    "it": {
        "footer.contact_dsa_link": "Punto di contatto DSA",
    },
    "lb": {
        "footer.contact_dsa_link": "DSA Kontaktpunkt",
    },
    "lt": {
        "footer.contact_dsa_link": "DSA kontaktinis punktas",
    },
    "lv": {
        "footer.contact_dsa_link": "DSA kontaktpunkts",
    },
    "mk": {
        "footer.contact_dsa_link": "DSA контактна точка",
    },
    "mt": {
        "footer.contact_dsa_link": "Punt ta' kuntatt DSA",
    },
    "nl": {
        "footer.contact_dsa_link": "DSA-contactpunt",
    },
    "no": {
        "footer.contact_dsa_link": "DSA-kontaktpunkt",
    },
    "pl": {
        "footer.contact_dsa_link": "Punkt kontaktowy DSA",
    },
    "pt": {
        "footer.contact_dsa_link": "Ponto de Contato DSA",
    },
    "pt-PT": {
        "footer.contact_dsa_link": "Ponto de Contacto DSA",
    },
    "ro": {
        "footer.contact_dsa_link": "Punct de contact DSA",
    },
    "ru": {
        "footer.contact_dsa_link": "Контактная точка DSA",
    },
    "sk": {
        "footer.contact_dsa_link": "Kontaktné miesto DSA",
    },
    "sl": {
        "footer.contact_dsa_link": "Kontaktna točka DSA",
    },
    "sq": {
        "footer.contact_dsa_link": "Pika e kontaktit DSA",
    },
    "sr": {
        "footer.contact_dsa_link": "DSA kontaktna tačka",
    },
    "sv": {
        "footer.contact_dsa_link": "DSA-kontaktpunkt",
    },
    "tr": {
        "footer.contact_dsa_link": "DSA İletişim Noktası",
    },
    "uk": {
        "footer.contact_dsa_link": "Контактна точка DSA",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all footer translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for lang, translations in TRANSLATIONS_BY_LANG.items():
            for key, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": key, "value": value}
                )
                count += 1

        conn.commit()
        print(f"Inserted/updated {count} translation rows for namespace '{NAMESPACE}'")


def verify_translations() -> None:
    """Verify the translations were inserted correctly."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT lang, COUNT(*) as keys
                FROM translations
                WHERE key LIKE :pattern
                GROUP BY lang
                ORDER BY lang
            """),
            {"pattern": f"{NAMESPACE}.%"}
        )
        rows = result.fetchall()
        print(f"\nVerification for namespace '{NAMESPACE}':")
        for row in rows:
            print(f"  {row[0]}: {row[1]} keys")


if __name__ == "__main__":
    seed_translations()
    verify_translations()
