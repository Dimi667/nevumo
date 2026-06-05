# -*- coding: utf-8 -*-
"""
seed_privacy_last_url.py — namespace 'privacy', key 't4_purpose_pwa_redirect'
Adds 't4_purpose_pwa_redirect' translation for EN, BG, PL only (others fallback to EN)
Run: railway run python -m apps.api.scripts.seed_privacy_last_url
After: flush Redis translations cache
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "privacy.t4_purpose_pwa_redirect": {
        "en": "Last visited page for PWA smart redirect",
        "bg": "Последно посетена страница за PWA пренасочване",
        "pl": "Ostatnio odwiedzona strona dla przekierowania PWA",
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
    print(f"Seeded {len(TRANSLATIONS)} keys x {sum(len(v) for v in TRANSLATIONS.values())} languages")


if __name__ == "__main__":
    seed()
