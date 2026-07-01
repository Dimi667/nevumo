from __future__ import annotations

import hashlib
import hmac
import logging
from datetime import datetime, timezone
from urllib.parse import unquote

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from apps.api.database import get_db
from apps.api.models import OutreachUnsubscribe, Provider
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


# ---------------------------------------------------------------------------
# GDPR Art.21 objection endpoints
#
# These endpoints implement the data-objection flow for scraped providers.
# The objection_token is generated and persisted separately (see Б14 seed
# script); here we only consume it. GET never mutates data — it only inspects
# state and redirects. The actual erasure happens in POST.
# ---------------------------------------------------------------------------


@router.get("/api/v1/outreach/objection")
def outreach_objection_check(
    token: str = Query(..., description="Objection token issued to the provider"),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """
    Public endpoint — no auth required.
    Inspects the objection state for a provider and redirects to the
    confirmation page. NEVER mutates data.
    """
    provider = (
        db.query(Provider).filter(Provider.objection_token == token).first()
    )

    if provider is None:
        logger.warning("Objection GET: token not found")
        return RedirectResponse(
            url="/pl/outreach/objection?status=invalid",
            status_code=302,
        )

    if provider.objected_at is not None:
        logger.info("Objection GET: already processed provider_id=%s", provider.id)
        return RedirectResponse(
            url="/pl/outreach/objection?status=already_done",
            status_code=302,
        )

    return RedirectResponse(
        url=f"/pl/outreach/objection?status=confirm&token={token}",
        status_code=302,
    )


@router.post("/api/v1/outreach/objection")
def outreach_objection_submit(
    token: str = Query(..., description="Objection token issued to the provider"),
    db: Session = Depends(get_db),
) -> RedirectResponse:
    """
    Public endpoint — no auth required.
    Performs the GDPR Art.21 objection: erases identifying fields, hides the
    provider, and records the objection timestamp. Idempotency guarded — a
    second call for an already-processed provider returns 409.
    """
    provider = (
        db.query(Provider).filter(Provider.objection_token == token).first()
    )

    if provider is None:
        logger.warning("Objection POST: token not found")
        raise HTTPException(status_code=404, detail="invalid_token")

    if provider.objected_at is not None:
        logger.info(
            "Objection POST: already processed provider_id=%s", provider.id
        )
        raise HTTPException(status_code=409, detail="already_objected")

    # Erase identifying data and hide the provider.
    provider.business_name = None
    provider.scraped_email = None
    provider.scraped_phone = None
    provider.is_hidden = True
    provider.objected_at = datetime.now(timezone.utc)
    # objection_token is intentionally preserved for audit trail.
    db.commit()

    logger.info("Objection POST: completed provider_id=%s", provider.id)

    return RedirectResponse(
        url="/pl/outreach/objection?status=success",
        status_code=302,
    )
