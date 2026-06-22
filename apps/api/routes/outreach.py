from __future__ import annotations

import hashlib
import hmac
import logging
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from apps.api.database import get_db
from apps.api.models import OutreachUnsubscribe
from apps.api.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def _verify_hmac_token(email: str, token: str) -> bool:
    """Verify HMAC-SHA256 token for unsubscribe link."""
    if not settings.OUTREACH_HMAC_SECRET:
        logger.error("OUTREACH_HMAC_SECRET is not configured")
        return False
    expected = hmac.new(
        settings.OUTREACH_HMAC_SECRET.encode(),
        email.encode(),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, token)


@router.get("/api/v1/outreach/unsubscribe")
def outreach_unsubscribe(
    token: str = Query(..., description="HMAC-SHA256 token"),
    email: str = Query(..., description="Email address to unsubscribe"),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """
    Public endpoint — no auth required.
    Verifies HMAC token, records unsubscribe, redirects to confirmation page.
    """
    email = unquote(email).strip().lower()

    if not _verify_hmac_token(email, token):
        logger.warning("Invalid unsubscribe token for email=%s", email)
        raise HTTPException(status_code=400, detail="invalid_token")

    existing = db.get(OutreachUnsubscribe, email)
    if existing is None:
        record = OutreachUnsubscribe(email=email, reason="user_request")
        db.add(record)
        db.commit()
        logger.info("Unsubscribed: %s", email)
    else:
        logger.info("Already unsubscribed: %s", email)

    return RedirectResponse(
        url="/pl/outreach/unsubscribe?confirmed=1",
        status_code=302,
    )
