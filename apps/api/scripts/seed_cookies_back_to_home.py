# -*- coding: utf-8 -*-
"""
seed_cookies_back_to_home.py — namespace 'cookies', key 'back_to_home'
Adds missing 'back_to_home' translation for all 34 languages to cookies namespace
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_back_to_home
After: flush Redis — docker exec nevumo-redis redis-cli FLUSHALL
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.back_to_home": {
        "bg": "Начало",
        "cs": "Zpět na úvod",
        "da": "Tilbage til forsiden",
        "de": "Zurück zur Startseite",
        "el": "Επιστροφή στην αρχική",
        "en": "Back to home",
        "es": "Volver al inicio",
        "et": "Tagasi avalehele",
        "fi": "Takaisin alkuun",
        "fr": "Retour à l'accueil",
        "ga": "Ar ais go dtí an baile",
        "hr": "Povratak na početnu",
        "hu": "Vissza a főoldalra",
        "is": "Til baka á forsíðu",
        "it": "Torna alla home",
        "lb": "Zréck op d'Haaptsäit",
        "lt": "Grįžti į pradžią",
        "lv": "Atpakaļ uz sākumu",
        "mk": "Назад кон почетната",
        "mt": "Lura lejn il-home",
        "nl": "Terug naar home",
        "no": "Tilbake til forsiden",
        "pl": "Powrót do strony głównej",
        "pt": "Voltar ao início",
        "pt-PT": "Voltar ao início",
        "ro": "Înapoi la început",
        "ru": "На главную",
        "sk": "Späť na domov",
        "sl": "Nazaj na prvo stran",
        "sq": "Kthehu në kryefaqe",
        "sr": "Повратак на почетну",
        "sv": "Tillbaka till start",
        "tr": "Ana sayfaya dön",
        "uk": "На головну",
    },
}


def seed():
    with engine.begin() as conn:
        for key, translations in TRANSLATIONS.items():
            for lang, value in translations.items():
                conn.execute(
                    text("""
                        INSERT INTO translations (key, lang, value)
                        VALUES (:key, :lang, :value)
                        ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value
                    """),
                    {"key": key, "lang": lang, "value": value},
                )
    print(f"Seeded {len(TRANSLATIONS)} keys x 34 languages")


if __name__ == "__main__":
    seed()
