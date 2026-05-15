"""
seed_terms_buttons.py  —  Nevumo | namespace: terms
Keys: download_pdf, online_form (34 езика)
Run : docker exec nevumo-api python -m apps.api.scripts.seed_terms_buttons
"""
import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nevumo:nevumo@postgres:5432/nevumo_leads",
)

NAMESPACE = "terms"

TRANSLATIONS: dict[str, dict[str, str]] = {

    "download_pdf": {
        "bg": "Изтегли PDF",
        "cs": "Stáhnout PDF",
        "da": "Download PDF",
        "de": "PDF herunterladen",
        "el": "Λήψη PDF",
        "en": "Download PDF",
        "es": "Descargar PDF",
        "et": "Laadi alla PDF",
        "fi": "Lataa PDF",
        "fr": "Télécharger le PDF",
        "ga": "Íoslódáil PDF",
        "hr": "Preuzmi PDF",
        "hu": "PDF letöltése",
        "is": "Sækja PDF",
        "it": "Scarica PDF",
        "lb": "PDF eroflueden",
        "lt": "Atsisiųsti PDF",
        "lv": "Lejupielādēt PDF",
        "mk": "Преземи PDF",
        "mt": "Niżżel il-PDF",
        "nl": "PDF downloaden",
        "no": "Last ned PDF",
        "pl": "Pobierz PDF",
        "pt": "Baixar PDF",
        "pt-PT": "Descarregar PDF",
        "ro": "Descarcă PDF",
        "ru": "Скачать PDF",
        "sk": "Stiahnuť PDF",
        "sl": "Prenesi PDF",
        "sq": "Shkarko PDF",
        "sr": "Preuzmi PDF",
        "sv": "Ladda ner PDF",
        "tr": "PDF İndir",
        "uk": "Завантажити PDF",
    },

    "online_form": {
        "bg": "Онлайн форма",
        "cs": "Online formulář",
        "da": "Online formular",
        "de": "Online-Formular",
        "el": "Online φόρμα",
        "en": "Online form",
        "es": "Formulario online",
        "et": "Veebivorm",
        "fi": "Verkkolomake",
        "fr": "Formulaire en ligne",
        "ga": "Foirm ar líne",
        "hr": "Online obrazac",
        "hu": "Online űrlap",
        "is": "Neteyðublað",
        "it": "Modulo online",
        "lb": "Online Formular",
        "lt": "Internetinė forma",
        "lv": "Tiešsaistes forma",
        "mk": "Онлајн форма",
        "mt": "Formola onlajn",
        "nl": "Online formulier",
        "no": "Online skjema",
        "pl": "Formularz online",
        "pt": "Formulário online",
        "pt-PT": "Formulário online",
        "ro": "Formular online",
        "ru": "Онлайн-форма",
        "sk": "Online formulár",
        "sl": "Spletni obrazac",
        "sq": "Formular online",
        "sr": "Onlajn formular",
        "sv": "Onlineformulär",
        "tr": "Çevrimiçi form",
        "uk": "Онлайн-форма",
    },
}


def seed() -> None:
    engine = create_engine(DATABASE_URL, echo=False)
    Session = sessionmaker(bind=engine)

    with Session() as session:
        count = 0
        for key, lang_values in TRANSLATIONS.items():
            db_key = f"{NAMESPACE}.{key}"
            for lang, value in lang_values.items():
                session.execute(
                    text(
                        "INSERT INTO translations (lang, key, value) "
                        "VALUES (:lang, :key, :value) "
                        "ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value"
                    ),
                    {"lang": lang, "key": db_key, "value": value},
                )
                count += 1
        session.commit()
        print(f"✅ seed_terms_buttons: {count} rows upserted ({NAMESPACE}, 2 keys × 34 langs)")

    engine.dispose()


if __name__ == "__main__":
    seed()
