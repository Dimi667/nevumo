from __future__ import annotations

import json
import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from apps.api.database import get_db
from apps.api.models import OutreachEvent, OutreachUnsubscribe
from apps.api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Events that should suppress future outreach
_SUPPRESSION_EVENTS = {"email.bounced", "email.complained"}

# Reason mapping for suppression events
_SUPPRESSION_REASON = {
    "email.bounced": "bounce",
    "email.complained": "complaint",
}


def _verify_resend_signature(body: bytes, headers: dict) -> bool:
    """
    Verify Resend webhook signature using svix.
    Returns True if valid, False if invalid or secret not configured.
    """
    if not settings.RESEND_WEBHOOK_SECRET:
        logger.error("RESEND_WEBHOOK_SECRET is not configured — rejecting webhook")
        return False

    try:
        from svix.webhooks import Webhook, WebhookVerificationError  # type: ignore
        wh = Webhook(settings.RESEND_WEBHOOK_SECRET)
        wh.verify(body, {
            "svix-id": headers.get("svix-id", ""),
            "svix-timestamp": headers.get("svix-timestamp", ""),
            "svix-signature": headers.get("svix-signature", ""),
        })
        return True
    except Exception as exc:
        logger.warning("Webhook signature verification failed: %s", exc)
        return False


@router.post("/api/v1/webhooks/resend", status_code=200)
async def resend_webhook(request: Request) -> dict:
    """
    Receives Resend webhook events.
    Verifies signature, logs to outreach_events, suppresses bounced/complained.
    Idempotent: duplicate events are safely ignored.
    """
    body = await request.body()

    if not _verify_resend_signature(body, dict(request.headers)):
        raise HTTPException(status_code=401, detail="invalid_signature")

    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="invalid_json")

    event_type: str = payload.get("type", "")
    data: dict = payload.get("data", {})
    resend_message_id: str = data.get("email_id", "")
    to_list: list = data.get("to", [])
    email: str = to_list[0].strip().lower() if to_list else ""

    if not event_type or not resend_message_id or not email:
        logger.warning(
            "Webhook missing required fields: type=%s email_id=%s to=%s",
            event_type, resend_message_id, to_list,
        )
        # Return 200 to prevent Resend from retrying malformed events
        return {"received": True}

    db: Session = next(get_db())
    try:
        # Log event to outreach_events (always)
        event = OutreachEvent(
            resend_message_id=resend_message_id,
            email=email,
            event_type=event_type,
            occurred_at=datetime.now(timezone.utc),
        )
        db.add(event)

        # Suppress bounced / complained
        if event_type in _SUPPRESSION_EVENTS:
            reason = _SUPPRESSION_REASON[event_type]
            existing = db.get(OutreachUnsubscribe, email)
            if existing is None:
                db.add(OutreachUnsubscribe(email=email, reason=reason))
                logger.info(
                    "Suppressed email=%s reason=%s resend_id=%s",
                    email, reason, resend_message_id,
                )
            else:
                logger.info(
                    "Already suppressed: email=%s existing_reason=%s",
                    email, existing.reason,
                )

        db.commit()

    except Exception as exc:
        db.rollback()
        logger.error("Webhook DB error: %s", exc)
        raise HTTPException(status_code=500, detail="db_error")
    finally:
        db.close()

    logger.info("Webhook processed: type=%s email=%s", event_type, email)
    return {"received": True}
