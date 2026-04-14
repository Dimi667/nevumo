"""Provider review endpoints (auth required)."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from apps.api.dependencies import get_current_provider, get_db
from apps.api.models import Provider
from apps.api.schemas import (
    ProviderReplyRequest,
    ProviderReplyResponse,
    ReviewLatestPreviewResponse,
    ReviewListResponse,
)
from apps.api.services.review_service import (
    get_provider_reviews,
    get_latest_review_preview,
    add_provider_reply,
)

router = APIRouter(prefix="/api/v1/provider", tags=["provider"])


@router.get("/reviews", response_model=ReviewListResponse)
def list_provider_reviews(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    unreplied_only: bool = Query(default=False),
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ReviewListResponse:
    """List all review conversations for the provider.

    - Sorted by latest activity (reply date or review date)
    - Optionally filter to show only unreplied reviews
    """
    result = get_provider_reviews(
        provider_id=provider.id,
        db=db,
        limit=limit,
        offset=offset,
        include_unreplied_only=unreplied_only
    )

    return ReviewListResponse(data=result)


@router.get("/reviews/latest-preview", response_model=ReviewLatestPreviewResponse)
def get_latest_review(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ReviewLatestPreviewResponse:
    """Get the latest review conversation for dashboard preview.

    Also returns count of unreplied reviews for the notification badge.
    """
    preview = get_latest_review_preview(provider.id, db)

    if not preview:
        return ReviewLatestPreviewResponse(data={
            "has_reviews": False,
            "unreplied_count": 0,
        })

    return ReviewLatestPreviewResponse(data={
        "has_reviews": True,
        "latest_review": preview,
        "unreplied_count": preview.get("unreplied_count", 0),
    })


@router.post("/reviews/{review_id}/reply", response_model=ProviderReplyResponse)
def reply_to_review(
    review_id: UUID,
    body: ProviderReplyRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderReplyResponse:
    """Reply to a client review.

    - First reply triggers email notification to client (if not opted out)
    - Can edit reply unlimited times
    - Edits do NOT trigger additional emails
    - Provider can only reply to reviews on their own profile
    """
    review = add_provider_reply(
        provider_id=provider.id,
        review_id=review_id,
        reply=body.reply,
        db=db
    )

    return ProviderReplyResponse(data={
        "id": review.id,
        "provider_reply": review.provider_reply,
        "provider_reply_at": review.provider_reply_at,
        "provider_reply_edited_at": review.provider_reply_edited_at,
        "provider_reply_edit_count": review.provider_reply_edit_count,
        "is_reply_edited": review.provider_reply_edit_count > 0,
    })


@router.patch("/reviews/{review_id}/reply", response_model=ProviderReplyResponse)
def edit_review_reply(
    review_id: UUID,
    body: ProviderReplyRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderReplyResponse:
    """Edit an existing reply to a client review.

    - Can edit unlimited times
    - Does NOT trigger email notification (only first reply sends email)
    - Provider can only edit replies on their own reviews
    """
    review = add_provider_reply(
        provider_id=provider.id,
        review_id=review_id,
        reply=body.reply,
        db=db
    )

    return ProviderReplyResponse(data={
        "id": review.id,
        "provider_reply": review.provider_reply,
        "provider_reply_at": review.provider_reply_at,
        "provider_reply_edited_at": review.provider_reply_edited_at,
        "provider_reply_edit_count": review.provider_reply_edit_count,
        "is_reply_edited": review.provider_reply_edit_count > 0,
    })
