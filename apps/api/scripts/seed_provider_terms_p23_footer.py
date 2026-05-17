"""
seed_provider_terms_p23_footer.py  —  Nevumo | namespace: provider_terms
Key: footer  (1 key x 34 langs = 34 rows)
Run: docker exec nevumo-api python -m apps.api.scripts.seed_provider_terms_p23_footer
"""
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "provider_terms"

TRANSLATIONS: dict[str, dict[str, str]] = {
    "footer": {
        "en": (
            "*Version 1.0 — Effective 1 June 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "bg": (
            "*Версия 1.0 — В сила от 1 юни 2026 г.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | ЕИК 175369610 | legal@nevumo.com*"
        ),
        "pl": (
            "*Wersja 1.0 — Obowiązuje od 1 czerwca 2026 r.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | NIP bułgarski (EIK): 175369610 | legal@nevumo.com*"
        ),
        "de": (
            "*Version 1.0 — Gültig ab 1. Juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "fr": (
            "*Version 1.0 — En vigueur à partir du 1er juin 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "es": (
            "*Versión 1.0 — En vigor desde el 1 de junio de 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "it": (
            "*Versione 1.0 — In vigore dal 1° giugno 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "nl": (
            "*Versie 1.0 — Van kracht vanaf 1 juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "pt": (
            "*Versão 1.0 — Em vigor a 1 de junho de 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "pt-PT": (
            "*Versão 1.0 — Em vigor a 1 de junho de 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "ro": (
            "*Versiunea 1.0 — În vigoare de la 1 iunie 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "ru": (
            "*Версия 1.0 — Вступает в силу 1 июня 2026 г.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | ЕИК 175369610 | legal@nevumo.com*"
        ),
        "uk": (
            "*Версія 1.0 — Набуває чинності 1 червня 2026 р.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "cs": (
            "*Verze 1.0 — Účinnost od 1. června 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "da": (
            "*Version 1.0 — Gældende fra 1. juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "sv": (
            "*Version 1.0 — Gäller från 1 juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "no": (
            "*Versjon 1.0 — Trer i kraft 1. juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "fi": (
            "*Versio 1.0 — Voimassa 1. kesäkuuta 2026 alkaen*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "et": (
            "*Versioon 1.0 — Jõustub 1. juunil 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "lt": (
            "*Versija 1.0 — Įsigalioja nuo 2026 m. birželio 1 d.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "lv": (
            "*Versija 1.0 — Spēkā no 2026. gada 1. jūnija*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "hu": (
            "*1.0 verzió — Hatályos: 2026. június 1-től*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "hr": (
            "*Verzija 1.0 — Stupa na snagu 1. lipnja 2026.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "sk": (
            "*Verzia 1.0 — Účinnosť od 1. júna 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "sl": (
            "*Različica 1.0 — Velja od 1. junija 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "el": (
            "*Έκδοση 1.0 — Σε ισχύ από 1 Ιουνίου 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "tr": (
            "*Sürüm 1.0 — Yürürlük Tarihi: 1 Haziran 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "ga": (
            "*Leagan 1.0 — I bhfeidhm ón 1 Meitheamh 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "is": (
            "*Útgáfa 1.0 — Gildir frá 1. júní 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "lb": (
            "*Versioun 1.0 — A Kraaft ab dem 1. Juni 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "mk": (
            "*Верзија 1.0 — Во сила од 1 јуни 2026 година*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | ЕИК 175369610 | legal@nevumo.com*"
        ),
        "mt": (
            "*Verżjoni 1.0 — Effettiva mill-1 ta' Ġunju 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "sq": (
            "*Versioni 1.0 — Në fuqi nga 1 Qershor 2026*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
        "sr": (
            "*Verzija 1.0 — Stupa na snagu 1. juna 2026.*\n"
            "*„ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ\" ООД | EIC 175369610 | legal@nevumo.com*"
        ),
    },
}

def seed() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            
            for lang, text_val in lang_values.items():
                query = text("""
                    INSERT INTO translations (key, lang, value)
                    VALUES (:k, :l, :v)
                    ON CONFLICT (key, lang)
                    DO UPDATE SET value = EXCLUDED.value
                """)
                session.execute(query, {"k": db_key, "l": lang, "v": text_val})
                count += 1

        session.commit()
        print(f"✅ Seeded {count} translations for {NAMESPACE}.footer")

if __name__ == "__main__":
    seed()
