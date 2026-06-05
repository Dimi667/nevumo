# -*- coding: utf-8 -*-
"""
seed_cookies_last_url.py — namespace 'cookies', key 's5_p_last_url'
Adds 's5_p_last_url' translation for all 34 languages to cookies namespace
Run: railway run python -m apps.api.scripts.seed_cookies_last_url
After: flush Redis translations cache
"""

import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get("DATABASE_URL")
engine = create_engine(DATABASE_URL)

TRANSLATIONS = {
    "cookies.s5_p_last_url": {
        "bg": "Последно посетена страница за PWA пренасочване",
        "cs": "Naposledy navštívená stránka pro inteligentní přesměrování PWA",
        "da": "Sidst besøgte side til smart PWA-omdirigering",
        "de": "Zuletzt besuchte Seite für intelligente PWA-Weiterleitung",
        "el": "Τελευταία επισκεφθείσα σελίδα για έξυπνη ανακατεύθυνση PWA",
        "en": "Last visited page for PWA smart redirect",
        "es": "Última página visitada para redirección inteligente de PWA",
        "et": "Viimati külastatud leht PWA nutika ümbersuunamise jaoks",
        "fi": "Viimeksi vierailtu sivu PWA-älykkäätä uudelleenohjausta varten",
        "fr": "Dernière page visitée pour la redirection intelligente PWA",
        "ga": "Leathanach deireanach a tógadh d'atreorú cliste PWA",
        "hr": "Posljednja posjećena stranica za pametno preusmjeravanje PWA",
        "hu": "Utoljára meglátogatott oldal az intelligens PWA-átirányításhoz",
        "is": "Síðast heimsótta síða fyrir snjallt PWA-framsend",
        "it": "Ultima pagina visitata per il reindirizzamento intelligente PWA",
        "lb": "Zuletzt besuchte Säit fir intelligent PWA-Weiderleitung",
        "lt": "Paskiausiai aplankytas puslapis išmaniam PWA nukreipimui",
        "lv": "Pēdējā apmeklētā lapa viedai PWA pāradresācijai",
        "mk": "Последно посетена страница за паметно PWA пренасочување",
        "mt": "Paġna viżitata l-aħħar għar-ridirezzjoni intelliġenti tal-PWA",
        "nl": "Laatst bezochte pagina voor slimme PWA-omleiding",
        "no": "Sist besøkte side for smart PWA-omdirigering",
        "pl": "Ostatnio odwiedzona strona dla inteligentnego przekierowania PWA",
        "pt": "Última página visitada para redirecionamento inteligente do PWA",
        "pt-PT": "Última página visitada para redireccionamento inteligente da PWA",
        "ro": "Ultima pagină vizitată pentru redirecționare inteligentă PWA",
        "ru": "Последняя посещённая страница для умного перенаправления PWA",
        "sk": "Naposledy navštívená stránka pre inteligentné presmerovanie PWA",
        "sl": "Zadnja obiskana stran za pametno preusmeritev PWA",
        "sq": "Faqja e fundit e vizituar për ridrejtim të zgjuar PWA",
        "sr": "Последња посећена страница за паметно PWA преусмеравање",
        "sv": "Senast besökta sida för smart PWA-omdirigering",
        "tr": "PWA akıllı yönlendirmesi için son ziyaret edilen sayfa",
        "uk": "Остання відвідана сторінка для розумного перенаправлення PWA",
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
