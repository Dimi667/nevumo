import logging
import httpx
from typing import Optional
from sqlalchemy.orm import Session
from apps.api.models import ProviderTranslation
from uuid import UUID

logger = logging.getLogger(__name__)

LANGBLY_API_KEY = "WsgGdcDaTgFQMkk6gfqnpZ"
LANGBLY_URL = "https://api.langbly.com/language/translate/v2"

SUPPORTED_LANGS = [
    "bg", "cs", "da", "de", "el", "en", "es", "et", "fi", "fr",
    "ga", "hr", "hu", "is", "it", "lb", "lt", "lv", "mk", "mt",
    "nl", "no", "pl", "pt", "pt-PT", "ro", "ru", "sk", "sl",
    "sq", "sr", "sv", "tr", "uk"
]


def translate_text(text: str, target_lang: str) -> Optional[str]:
    """Translate text to target_lang via Langbly. Returns None on any error."""
    try:
        response = httpx.post(
            LANGBLY_URL,
            json={"q": text, "target": target_lang, "source": "auto"},
            headers={"Authorization": f"Bearer {LANGBLY_API_KEY}"},
            timeout=30.0
        )
        if response.status_code == 429:
            logger.warning("Langbly limit exhausted (429). Falling back to original text.")
            return None
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("translations", [{}])[0].get("translatedText")
    except Exception as e:
        logger.error(f"Translation error for lang={target_lang}: {e}")
        return None


def translate_and_store(
    provider_id: UUID,
    field: str,
    text: str,
    db: Session
) -> dict:
    """
    Translate text to all 34 languages and upsert into provider_translations.
    Fallback: on 429 or error, store original text with auto_translated=False.
    Returns {"translated": int, "fallback": int}
    """
    translated = 0
    fallback = 0
    limit_reached = False

    for lang in SUPPORTED_LANGS:
        if limit_reached:
            value = text
            auto_translated = False
            fallback += 1
        else:
            result = translate_text(text, lang)
            if result is None:
                limit_reached = True
                value = text
                auto_translated = False
                fallback += 1
            else:
                value = result
                auto_translated = True
                translated += 1

        existing = db.query(ProviderTranslation).filter_by(
            provider_id=provider_id, field=field, lang=lang
        ).first()
        if existing:
            existing.value = value
            existing.auto_translated = auto_translated
        else:
            db.add(ProviderTranslation(
                provider_id=provider_id,
                field=field,
                lang=lang,
                value=value,
                auto_translated=auto_translated
            ))

    db.commit()

    if limit_reached:
        logger.warning(
            f"Langbly limit reached: provider={provider_id} "
            f"translated={translated} fallback={fallback}"
        )

    return {"translated": translated, "fallback": fallback}
