# -*- coding: utf-8 -*-
"""
seed_cookies_p12.py — namespace 'cookies', keys s3_1_title..s3_4_title
NOTE: cookies.s3_text is intentionally excluded (wrong key, deleted from DB)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p12
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s3_1_title": {
        "en": "3.1 Strictly Necessary",
        "bg": "3.1 Zadulzhitelno neobhodimi",
        "cs": "3.1 Nezbytne nutne",
        "da": "3.1 Strengt nodvendige",
        "de": "3.1 Unbedingt erforderlich",
        "el": "3.1 Apolytos aparaitita",
        "es": "3.1 Estrictamente necesarias",
        "et": "3.1 Rangelt vajalikud",
        "fi": "3.1 Ehdottoman valttamattomat",
        "fr": "3.1 Strictement necessaires",
        "ga": "3.1 Riachtanach go Docht",
        "hr": "3.1 Strogo nuzni",
        "hu": "3.1 Feltetlenul szukseges",
        "is": "3.1 Stranglega nauosynlegar",
        "it": "3.1 Strettamente necessari",
        "lb": "3.1 Streng neideg",
        "lt": "3.1 Grieztai butini",
        "lv": "3.1 Obligati nepieciesamie",
        "mk": "3.1 Strogo neophodni",
        "mt": "3.1 Strettament Necessarji",
        "nl": "3.1 Strikt noodzakelijk",
        "no": "3.1 Strengt nodvendige",
        "pl": "3.1 Niezbedne",
        "pt": "3.1 Estritamente necessarios",
        "pt-PT": "3.1 Estritamente necessarios",
        "ro": "3.1 Strict necesare",
        "ru": "3.1 Strogo neobkhodimye",
        "sk": "3.1 Nevyhnutne potrebne",
        "sl": "3.1 Nujno potrebni",
        "sq": "3.1 Rreptesisht te nevojshme",
        "sr": "3.1 Strogo neophodni",
        "sv": "3.1 Strikt nodvandiga",
        "tr": "3.1 Kesinlikle Gerekli",
        "uk": "3.1 Suvoroho neobkhidni",
    },
    "cookies.s3_2_title": {
        "en": "3.2 Functional",
        "bg": "3.2 Funktsionalni",
        "cs": "3.2 Funkcni",
        "da": "3.2 Funktionelle",
        "de": "3.2 Funktionale",
        "el": "3.2 Leitourgika",
        "es": "3.2 Funcionales",
        "et": "3.2 Funktsionaalsed",
        "fi": "3.2 Toiminnalliset",
        "fr": "3.2 Fonctionnels",
        "ga": "3.2 Feidhmiul",
        "hr": "3.2 Funkcionalni",
        "hu": "3.2 Funkcionalis",
        "is": "3.2 Virkni",
        "it": "3.2 Funzionali",
        "lb": "3.2 Funktional",
        "lt": "3.2 Funkciniai",
        "lv": "3.2 Funkcionalie",
        "mk": "3.2 Funkcionalni",
        "mt": "3.2 Funzjonali",
        "nl": "3.2 Functioneel",
        "no": "3.2 Funksjonelle",
        "pl": "3.2 Funkcjonalne",
        "pt": "3.2 Funcionais",
        "pt-PT": "3.2 Funcionais",
        "ro": "3.2 Functionale",
        "ru": "3.2 Funktsionalnyye",
        "sk": "3.2 Funkcne",
        "sl": "3.2 Funkcionalni",
        "sq": "3.2 Funksionale",
        "sr": "3.2 Funkcionalni",
        "sv": "3.2 Funktionella",
        "tr": "3.2 Islevsel",
        "uk": "3.2 Funktsionalni",
    },
    "cookies.s3_3_title": {
        "en": "3.3 Analytics",
        "bg": "3.3 Analitichni",
        "cs": "3.3 Analyticke",
        "da": "3.3 Analytiske",
        "de": "3.3 Analyse",
        "el": "3.3 Analytika",
        "es": "3.3 Analiticas",
        "et": "3.3 Analyytilised",
        "fi": "3.3 Analytiikka",
        "fr": "3.3 Analytiques",
        "ga": "3.3 Anailisiochta",
        "hr": "3.3 Analiticki",
        "hu": "3.3 Analitikai",
        "is": "3.3 Greining",
        "it": "3.3 Analitici",
        "lb": "3.3 Analytesch",
        "lt": "3.3 Analitiniai",
        "lv": "3.3 Analitiskie",
        "mk": "3.3 Analiticski",
        "mt": "3.3 Analitici",
        "nl": "3.3 Analytisch",
        "no": "3.3 Analytiske",
        "pl": "3.3 Analityczne",
        "pt": "3.3 Analiticos",
        "pt-PT": "3.3 Analiticos",
        "ro": "3.3 Analitice",
        "ru": "3.3 Analiticheskiye",
        "sk": "3.3 Analyticke",
        "sl": "3.3 Analiticni",
        "sq": "3.3 Analitike",
        "sr": "3.3 Analiticski",
        "sv": "3.3 Analytiska",
        "tr": "3.3 Analitik",
        "uk": "3.3 Analitychni",
    },
    "cookies.s3_4_title": {
        "en": "3.4 Marketing",
        "bg": "3.4 Marketingovi",
        "cs": "3.4 Marketingove",
        "da": "3.4 Marketing",
        "de": "3.4 Marketing",
        "el": "3.4 Marketing",
        "es": "3.4 Marketing",
        "et": "3.4 Turundus",
        "fi": "3.4 Markkinointi",
        "fr": "3.4 Marketing",
        "ga": "3.4 Margaiochta",
        "hr": "3.4 Marketinski",
        "hu": "3.4 Marketing",
        "is": "3.4 Markadssetning",
        "it": "3.4 Marketing",
        "lb": "3.4 Marketing",
        "lt": "3.4 Rinkodaros",
        "lv": "3.4 Marketinga",
        "mk": "3.4 Marketinski",
        "mt": "3.4 Marketing",
        "nl": "3.4 Marketing",
        "no": "3.4 Markedsforing",
        "pl": "3.4 Marketingowe",
        "pt": "3.4 Marketing",
        "pt-PT": "3.4 Marketing",
        "ro": "3.4 Marketing",
        "ru": "3.4 Marketingovyye",
        "sk": "3.4 Marketingove",
        "sl": "3.4 Trzenjski",
        "sq": "3.4 Marketingu",
        "sr": "3.4 Marketinski",
        "sv": "3.4 Marknadsforing",
        "tr": "3.4 Pazarlama",
        "uk": "3.4 Marketynhovi",
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