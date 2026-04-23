"""Client review endpoints (auth required)."""

from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from apps.api.dependencies import get_current_user, get_db
from apps.api.models import User
from apps.api.schemas import (
    ClientDashboardResponse,
    ClientLeadNotesUpdate,
    ClientLeadNotesUpdateResponse,
    ClientLeadsQueryParams,
    ClientLeadsResponse,
    ReviewCreateRequest,
    ReviewCreateResponse,
    ReviewEligibleLeadsResponse,
    ReviewEmailPreferenceResponse,
    ReviewListResponse,
)
from apps.api.services.client_service import get_client_dashboard, get_client_leads, require_client_user
from apps.api.services.review_service import (
    get_eligible_leads_for_review,
    create_review,
    get_client_reviews,
    get_client_review_preferences,
    update_client_review_preferences,
    can_client_review_provider,
)

router = APIRouter(prefix="/api/v1/client", tags=["client"])


def _require_client_role(current_user: User) -> User:
    """Ensure current user is an active user (can be client or provider)."""
    return current_user


@router.get("/dashboard", response_model=ClientDashboardResponse)
def get_dashboard(
    lang: str = Query(default='en'),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClientDashboardResponse:
    user = require_client_user(current_user)
    result = get_client_dashboard(user.id, db, lang=lang)
    return ClientDashboardResponse(data=result)


@router.get("/leads", response_model=ClientLeadsResponse)
def list_client_leads(
    params: Annotated[ClientLeadsQueryParams, Query()],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClientLeadsResponse:
    user = require_client_user(current_user)
    result = get_client_leads(
        user.id,
        db,
        status=params.status,
        limit=params.limit,
        offset=params.offset,
        lang=params.lang,
    )
    return ClientLeadsResponse(data=result)


@router.patch("/leads/{lead_id}/notes", response_model=ClientLeadNotesUpdateResponse)
def update_lead_client_notes(
    lead_id: UUID,
    body: ClientLeadNotesUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ClientLeadNotesUpdateResponse:
    """Update private notes for a lead (client view)."""
    from apps.api.models import Lead
    user = require_client_user(current_user)

    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id, Lead.client_id == user.id)
        .first()
    )

    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found or you don't have access to this lead"
        )

    lead.client_notes = body.client_notes
    db.commit()

    return ClientLeadNotesUpdateResponse(data={"lead_id": lead_id, "client_notes": body.client_notes})


@router.get("/reviews/eligible-leads", response_model=ReviewEligibleLeadsResponse)
def list_eligible_leads(
    limit: int = Query(default=50, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewEligibleLeadsResponse:
    """List completed leads that are eligible for review.

    Returns leads with status 'done' that haven't been reviewed yet.
    """
    user = _require_client_role(current_user)
    leads = get_eligible_leads_for_review(user.id, db, limit=limit)

    return ReviewEligibleLeadsResponse(data={
        "leads": leads,
        "count": len(leads),
    })


@router.post("/reviews", response_model=ReviewCreateResponse, status_code=201)
def create_client_review(
    body: ReviewCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewCreateResponse:
    """Create a review for a completed lead.

    - Client must own the lead
    - Lead must have status 'done'
    - One review per lead only
    - Rating must be 1-5
    """
    user = _require_client_role(current_user)

    review = create_review(
        client_id=user.id,
        lead_id=body.lead_id,
        rating=body.rating,
        comment=body.comment,
        db=db
    )

    return ReviewCreateResponse(data={
        "id": review.id,
        "provider_id": review.provider_id,
        "lead_id": review.lead_id,
        "rating": review.rating,
        "comment": review.comment,
        "created_at": review.created_at,
    })


@router.get("/reviews", response_model=ReviewListResponse)
def list_client_reviews(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewListResponse:
    """List all reviews created by the client with provider replies."""
    user = _require_client_role(current_user)

    result = get_client_reviews(user.id, db, limit=limit, offset=offset)

    return ReviewListResponse(data=result)


@router.get("/reviews/preferences", response_model=ReviewEmailPreferenceResponse)
def get_email_preferences(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewEmailPreferenceResponse:
    """Get email notification preferences for review replies.

    Default is enabled (True) - client will receive emails when providers reply.
    """
    user = _require_client_role(current_user)

    prefs = get_client_review_preferences(user.id, db)

    return ReviewEmailPreferenceResponse(data={
        "review_reply_email_enabled": prefs["review_reply_email_enabled"],
        "description": "Receive email notifications when providers reply to your reviews",
    })


@router.patch("/reviews/preferences", response_model=ReviewEmailPreferenceResponse)
def update_email_preferences(
    review_reply_email_enabled: bool,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> ReviewEmailPreferenceResponse:
    """Update email notification preferences for review replies.

    Set to False to opt-out of review reply emails.
    """
    user = _require_client_role(current_user)

    prefs = update_client_review_preferences(
        client_id=user.id,
        review_reply_email_enabled=review_reply_email_enabled,
        db=db
    )

    return ReviewEmailPreferenceResponse(data={
        "review_reply_email_enabled": prefs["review_reply_email_enabled"],
        "description": "Receive email notifications when providers reply to your reviews",
    })


@router.get("/reviews/can-review-provider/{provider_id}")
def check_can_review_provider(
    provider_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Check if the client is eligible to review a specific provider.

    Eligibility requires at least one completed job with the provider
    that hasn't been reviewed yet.
    """
    user = _require_client_role(current_user)

    result = can_client_review_provider(user.id, provider_id, db)

    return {"success": True, "data": result}
