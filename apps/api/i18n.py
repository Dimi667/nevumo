from typing import Dict

from sqlalchemy.orm import Session

from models import Translation

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = (
    "bg",
    "cs",
    "da",
    "de",
    "el",
    "en",
    "es",
    "et",
    "fi",
    "fr",
    "ga",
    "hr",
    "hu",
    "is",
    "it",
    "lb",
    "lt",
    "lv",
    "mk",
    "mt",
    "nl",
    "no",
    "pl",
    "pt",
    "pt-PT",
    "ro",
    "ru",
    "sk",
    "sl",
    "sq",
    "sr",
    "sv",
    "tr",
    "uk",
)

DEFAULT_PROVIDER_CATEGORY_KEY = "provider_category_general"
MASSAGE_PROVIDER_CATEGORY_KEY = "provider_category_massage"

DEFAULT_PROVIDER_CATEGORY_TRANSLATIONS = {
    "bg": "Obshti uslugi",
    "cs": "Obecne sluzby",
    "da": "Generelle tjenester",
    "de": "Allgemeine Dienstleistungen",
    "el": "Genikes ypiresies",
    "en": "General Services",
    "es": "Servicios generales",
    "et": "Uldteenused",
    "fi": "Yleiset palvelut",
    "fr": "Services generaux",
    "ga": "Seirbhisi ginearalta",
    "hr": "Opce usluge",
    "hu": "Altalanos szolgaltatasok",
    "it": "Servizi generali",
    "lt": "Bendrosios paslaugos",
    "lv": "Visparejie pakalpojumi",
    "mk": "Opshti uslugi",
    "mt": "Servizzi generali",
    "nl": "Algemene diensten",
    "no": "Generelle tjenester",
    "pl": "Uslugi ogolne",
    "pt": "Servicos gerais",
    "pt-PT": "Servicos gerais",
    "ro": "Servicii generale",
    "sk": "Vseobecne sluzby",
    "sl": "Splosne storitve",
    "sq": "Sherbime te pergjithshme",
    "sr": "Opste usluge",
    "sv": "Allmanna tjanster",
    "tr": "Genel hizmetler",
}

MASSAGE_PROVIDER_CATEGORY_TRANSLATIONS = {
    "bg": "Masazh",
    "cs": "Masaze",
    "da": "Massage",
    "de": "Massage",
    "el": "Masaz",
    "en": "Massage",
    "es": "Masajes",
    "et": "Massaaz",
    "fi": "Hieronta",
    "fr": "Massage",
    "ga": "Suathaireacht",
    "hr": "Masaza",
    "hu": "Masszazs",
    "it": "Massaggi",
    "lt": "Masazas",
    "lv": "Masaza",
    "mk": "Masaza",
    "mt": "Massagg",
    "nl": "Massage",
    "no": "Massasje",
    "pl": "Masaz",
    "pt": "Massagem",
    "pt-PT": "Massagem",
    "ro": "Masaj",
    "sk": "Masaze",
    "sl": "Masaza",
    "sq": "Masazh",
    "sr": "Masaza",
    "sv": "Massage",
    "tr": "Masaj",
}


def fetch_translations(db: Session, lang: str) -> Dict[str, str]:
    lang = normalize_language(lang)
    en_translations = db.query(Translation).filter(Translation.lang == DEFAULT_LANGUAGE).all()
    target_translations = db.query(Translation).filter(Translation.lang == lang).all()

    translations_dict = {translation.key: translation.value for translation in en_translations}
    for translation in target_translations:
        translations_dict[translation.key] = translation.value

    return translations_dict


def resolve_translation(db: Session, key: str, lang: str) -> str:
    if not key:
        return ""

    lang = normalize_language(lang)
    translations = (
        db.query(Translation)
        .filter(Translation.key == key, Translation.lang.in_([DEFAULT_LANGUAGE, lang]))
        .all()
    )
    values = {translation.lang: translation.value for translation in translations}
    return values.get(lang) or values.get(DEFAULT_LANGUAGE) or key


def validate_multilingual_payload(translations: Dict[str, str]) -> None:
    missing_languages = [
        lang for lang in SUPPORTED_LANGUAGES if not translations.get(lang, "").strip()
    ]
    if missing_languages:
        missing = ", ".join(missing_languages)
        raise ValueError(f"Missing category translations for: {missing}")


def normalize_language(lang: str) -> str:
    return lang if lang in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def upsert_translation_values(db: Session, key: str, translations: Dict[str, str]) -> None:
    validate_multilingual_payload(translations)

    for lang, value in translations.items():
        existing = db.query(Translation).filter_by(lang=lang, key=key).first()
        if existing:
            existing.value = value.strip()
        else:
            db.add(Translation(lang=lang, key=key, value=value.strip()))


def provider_category_seed_data() -> Dict[str, Dict[str, str]]:
    seed_data: Dict[str, Dict[str, str]] = {}

    for lang in SUPPORTED_LANGUAGES:
        seed_data[lang] = {
            DEFAULT_PROVIDER_CATEGORY_KEY: DEFAULT_PROVIDER_CATEGORY_TRANSLATIONS[lang],
            MASSAGE_PROVIDER_CATEGORY_KEY: MASSAGE_PROVIDER_CATEGORY_TRANSLATIONS[lang],
        }

    return seed_data
