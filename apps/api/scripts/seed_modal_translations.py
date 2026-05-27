#!/usr/bin/env python3
"""
Seed modal translations.
Namespace: modal
Keys: 1 | Languages: 34
Run: docker exec nevumo-api python -m apps.api.scripts.seed_modal_translations
"""

import os

from sqlalchemy import create_engine, text

NAMESPACE = "modal"

TRANSLATIONS = {
    "dismiss_button": {
        "en": "Got it",
        "bg": "Разбрах",
        "cs": "Rozumím",
        "da": "Forstået",
        "de": "Verstanden",
        "el": "Κατάλαβα",
        "es": "Entendido",
        "et": "Sain aru",
        "fi": "Selvä",
        "fr": "Compris",
        "ga": "Tuigim",
        "hr": "Razumijem",
        "hu": "Értettem",
        "is": "Skil",
        "it": "Capito",
        "lb": "Verstanen",
        "lt": "Supratau",
        "lv": "Sapratu",
        "mk": "Разбрав",
        "mt": "Ftahmt",
        "nl": "Begrepen",
        "no": "Skjønt",
        "pl": "Rozumiem",
        "pt": "Entendi",
        "pt-PT": "Percebi",
        "ro": "Înțeles",
        "ru": "Понятно",
        "sk": "Rozumiem",
        "sl": "Razumem",
        "sq": "Kuptova",
        "sr": "Схватио",
        "sv": "Förstått",
        "tr": "Anladım",
        "uk": "Зрозуміло",
    },
}


def get_database_url() -> str:
    """Get database URL from environment or use default."""
    return os.getenv("DATABASE_URL", "postgresql://nevumo:nevumo@localhost:5432/nevumo_leads")


def seed_translations() -> None:
    """Seed all modal translations into the database."""
    engine = create_engine(get_database_url())

    with engine.connect() as conn:
        count = 0
        for key_base, translations in TRANSLATIONS.items():
            full_key = f"{NAMESPACE}.{key_base}"
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (lang, key, value)
                        VALUES (:lang, :key, :value)
                        ON CONFLICT (lang, key)
                        DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"lang": lang, "key": full_key, "value": value}
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
