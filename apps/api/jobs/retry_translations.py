import logging
from sqlalchemy.orm import Session
from models import ProviderTranslation
from services.translation_service import translate_text, SUPPORTED_LANGS

logger = logging.getLogger(__name__)

def retry_failed_translations(db: Session) -> None:
    """
    Retry translating entries where auto_translated=False.
    Stops immediately if Langbly returns 429 again.
    """
    failed = db.query(ProviderTranslation).filter_by(auto_translated=False).all()

    if not failed:
        logger.info("Retry translations: nothing to retry.")
        return

    combos = {}
    for row in failed:
        key = (str(row.provider_id), row.field)
        if key not in combos:
            combos[key] = row.value

    retried = 0
    skipped = 0

    for (provider_id, field), original_text in combos.items():
        for lang in SUPPORTED_LANGS:
            result = translate_text(original_text, lang)
            if result is None:
                logger.warning(f"Retry aborted: Langbly still at limit. Retried={retried} Skipped={skipped}")
                return
            row = db.query(ProviderTranslation).filter_by(
                provider_id=provider_id, field=field, lang=lang
            ).first()
            if row:
                row.value = result
                row.auto_translated = True
        db.commit()
        retried += 1

    logger.info(f"Retry translations complete: {retried} providers retried, {skipped} skipped.")
