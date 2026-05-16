# -*- coding: utf-8 -*-
"""
seed_cookies_p12.py - namespace 'cookies'
cookies.s3_1_title, cookies.s3_2_title, cookies.s3_3_title, cookies.s3_4_title
NOTE: cookies.s3_text е намеренно изключен (грешен ключ, изтрит от DB)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_cookies_p12
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s3_1_title": {
        "en": "3.1 Strictly Necessary",
        "bg": "3.1 Задължително необходими",
        "cs": "3.1 Nezbytně nutné",
        "da": "3.1 Strengt nødvendige",
        "de": "3.1 Unbedingt erforderlich",
        "el": "3.1 Απολύτως απαραίτητα",
        "es": "3.1 Estrictamente necesarias",
        "et": "3.1 Rangelt vajalikud",
        "fi": "3.1 Ehdottoman välttämättömät",
        "fr": "3.1 Strictement nécessaires",
        "ga": "3.1 Riachtanach go Docht",
        "hr": "3.1 Strogo nužni",
        "hu": "3.1 Feltétlenül szükséges",
        "is": "3.1 Stranglega nauðsynlegar",
        "it": "3.1 Strettamente necessari",
        "lb": "3.1 Streng néideg",
        "lt": "3.1 Griežtai būtini",
        "lv": "3.1 Obligāti nepieciešamie",
        "mk": "3.1 Строго неопходни",
        "mt": "3.1 Strettament Neċessarji",
        "nl": "3.1 Strikt noodzakelijk",
        "no": "3.1 Strengt nødvendige",
        "pl": "3.1 Niezbędne",
        "pt": "3.1 Estritamente necessários",
        "pt-PT": "3.1 Estritamente necessários",
        "ro": "3.1 Strict necesare",
        "ru": "3.1 Строго необходимые",
        "sk": "3.1 Nevyhnutne potrebné",
        "sl": "3.1 Nujno potrebni",
        "sq": "3.1 Rreptësisht të nevojshme",
        "sr": "3.1 Строго неопходни",
        "sv": "3.1 Strikt nödvändiga",
        "tr": "3.1 Kesinlikle Gerekli",
        "uk": "3.1 Суворо необхідні",
    },
    "cookies.s3_2_title": {
        "en": "3.2 Functional",
        "bg": "3.2 Функционални",
        "cs": "3.2 Funkční",
        "da": "3.2 Funktionelle",
        "de": "3.2 Funktionale",
        "el": "3.2 Λειτουργικά",
        "es": "3.2 Funcionales",
        "et": "3.2 Funktsionaalsed",
        "fi": "3.2 Toiminnalliset",
        "fr": "3.2 Fonctionnels",
        "ga": "3.2 Feidhmiúil",
        "hr": "3.2 Funkcionalni",
        "hu": "3.2 Funkcionális",
        "is": "3.2 Virkni",
        "it": "3.2 Funzionali",
        "lb": "3.2 Funktional",
        "lt": "3.2 Funkciniai",
        "lv": "3.2 Funkcionālie",
        "mk": "3.2 Функционални",
        "mt": "3.2 Funzjonali",
        "nl": "3.2 Functioneel",
        "no": "3.2 Funksjonelle",
        "pl": "3.2 Funkcjonalne",
        "pt": "3.2 Funcionais",
        "pt-PT": "3.2 Funcionais",
        "ro": "3.2 Funcționale",
        "ru": "3.2 Функциональные",
        "sk": "3.2 Funkčné",
        "sl": "3.2 Funkcionalni",
        "sq": "3.2 Funksionale",
        "sr": "3.2 Функционални",
        "sv": "3.2 Funktionella",
        "tr": "3.2 İşlevsel",
        "uk": "3.2 Функціональні",
    },
    "cookies.s3_3_title": {
        "en": "3.3 Analytics",
        "bg": "3.3 Аналитични",
        "cs": "3.3 Analytické",
        "da": "3.3 Analytiske",
        "de": "3.3 Analyse",
        "el": "3.3 Αναλυτικά",
        "es": "3.3 Analíticas",
        "et": "3.3 Analüütilised",
        "fi": "3.3 Analytiikka",
        "fr": "3.3 Analytiques",
        "ga": "3.3 Anailísíochta",
        "hr": "3.3 Analitički",
        "hu": "3.3 Analitikai",
        "is": "3.3 Greining",
        "it": "3.3 Analitici",
        "lb": "3.3 Analytesch",
        "lt": "3.3 Analitiniai",
        "lv": "3.3 Analītiskie",
        "mk": "3.3 Аналитички",
        "mt": "3.3 Analitiċi",
        "nl": "3.3 Analytisch",
        "no": "3.3 Analytiske",
        "pl": "3.3 Analityczne",
        "pt": "3.3 Analíticos",
        "pt-PT": "3.3 Analíticos",
        "ro": "3.3 Analitice",
        "ru": "3.3 Аналитические",
        "sk": "3.3 Analytické",
        "sl": "3.3 Analitični",
        "sq": "3.3 Analitike",
        "sr": "3.3 Аналитички",
        "sv": "3.3 Analytiska",
        "tr": "3.3 Analitik",
        "uk": "3.3 Аналітичні",
    },
    "cookies.s3_4_title": {
        "en": "3.4 Marketing",
        "bg": "3.4 Маркетингови",
        "cs": "3.4 Marketingové",
        "da": "3.4 Marketing",
        "de": "3.4 Marketing",
        "el": "3.4 Μάρκετινγκ",
        "es": "3.4 Marketing",
        "et": "3.4 Turundus",
        "fi": "3.4 Markkinointi",
        "fr": "3.4 Marketing",
        "ga": "3.4 Margaíochta",
        "hr": "3.4 Marketinški",
        "hu": "3.4 Marketing",
        "is": "3.4 Markaðssetning",
        "it": "3.4 Marketing",
        "lb": "3.4 Marketing",
        "lt": "3.4 Rinkodaros",
        "lv": "3.4 Mārketinga",
        "mk": "3.4 Маркетиншки",
        "mt": "3.4 Marketing",
        "nl": "3.4 Marketing",
        "no": "3.4 Markedsføring",
        "pl": "3.4 Marketingowe",
        "pt": "3.4 Marketing",
        "pt-PT": "3.4 Marketing",
        "ro": "3.4 Marketing",
        "ru": "3.4 Маркетинговые",
        "sk": "3.4 Marketingové",
        "sl": "3.4 Trženjski",
        "sq": "3.4 Marketingu",
        "sr": "3.4 Маркетиншки",
        "sv": "3.4 Marknadsföring",
        "tr": "3.4 Pazarlama",
        "uk": "3.4 Маркетингові",
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