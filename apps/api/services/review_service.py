"""Review service layer for rating/review system."""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NevumoException
from models import Review, Lead, User, Provider, LeadMatch
from services.email_service import email_service
from services.provider_service import get_provider_rating


def get_eligible_leads_for_review(
    client_id: UUID,
    db: Session,
    limit: int = 50
) -> List[Dict[str, Any]]:
    """Get completed leads that are eligible for review by the client.

    A lead is eligible if:
    - It has the client's client_id populated
    - It has status 'done' (completed)
    - No review exists for this lead yet
    """
    # Get all completed leads for this client
    leads_query = (
        db.query(
            Lead,
            Provider.business_name.label('provider_business_name'),
            Review.id.label('existing_review_id')
        )
        .join(Provider, Lead.provider_id == Provider.id)
        .outerjoin(Review, Review.lead_id == Lead.id)
        .filter(
            Lead.client_id == client_id,
            Lead.status == "done"
        )
        .order_by(Lead.created_at.desc())
        .limit(limit)
    )

    results = leads_query.all()

    eligible_leads = []
    for row in results:
        lead = row[0]
        provider_name = row[1]
        existing_review_id = row[2]

        eligible_leads.append({
            "id": lead.id,
            "description": lead.description,
            "created_at": lead.created_at,
            "provider_id": lead.provider_id,
            "provider_business_name": provider_name,
            "has_review": existing_review_id is not None,
        })

    return eligible_leads


def create_review(
    client_id: UUID,
    lead_id: UUID,
    rating: int,
    comment: Optional[str],
    db: Session
) -> Review:
    """Create a new review for a completed lead.

    Raises:
        NevumoException: If lead not found, not completed, already reviewed,
                        or client doesn't own the lead.
    """
    # Validate lead exists and is completed
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise NevumoException(404, "LEAD_NOT_FOUND", "Lead not found")

    if lead.status != "done":
        raise NevumoException(
            400,
            "LEAD_NOT_COMPLETED",
            "Can only review completed jobs"
        )

    # Verify client owns this lead
    if lead.client_id != client_id:
        raise NevumoException(
            403,
            "NOT_YOUR_LEAD",
            "You can only review your own completed jobs"
        )

    # Check if lead has a provider
    if not lead.provider_id:
        raise NevumoException(
            400,
            "LEAD_NO_PROVIDER",
            "Cannot review a lead without an assigned provider"
        )

    # Check for existing review (one review per lead)
    existing = db.query(Review).filter(Review.lead_id == lead_id).first()
    if existing:
        raise NevumoException(
            409,
            "REVIEW_EXISTS",
            "You have already reviewed this job"
        )

    # Create the review
    review = Review(
        provider_id=lead.provider_id,
        client_id=client_id,
        lead_id=lead_id,
        rating=rating,
        comment=comment,
    )
    db.add(review)
    db.commit()
    db.refresh(review)

    # Update provider's aggregate rating
    _update_provider_rating(lead.provider_id, db)

    return review


def _update_provider_rating(provider_id: UUID, db: Session) -> None:
    """Recalculate and update provider's aggregate rating."""
    avg_rating = get_provider_rating(provider_id, db)
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if provider:
        provider.rating = avg_rating
        db.commit()


def get_provider_reviews(
    provider_id: UUID,
    db: Session,
    limit: int = 50,
    offset: int = 0,
    include_unreplied_only: bool = False
) -> Dict[str, Any]:
    """Get all review conversations for a provider.

    Returns reviews sorted by latest activity (reply_at or created_at).
    """
    query = db.query(
        Review,
        User.email.label('client_email')
    ).join(
        User, Review.client_id == User.id
    ).filter(
        Review.provider_id == provider_id
    )

    if include_unreplied_only:
        query = query.filter(Review.provider_reply == None)

    # Sort by most recent activity
    query = query.order_by(
        func.coalesce(Review.provider_reply_at, Review.created_at).desc()
    )

    total = query.count()
    reviews = query.offset(offset).limit(limit).all()

    items = []
    for row in reviews:
        review = row[0]
        client_email = row[1]

        items.append({
            "id": review.id,
            "provider_id": review.provider_id,
            "client_id": review.client_id,
            "client_name": client_email.split('@')[0] if client_email else "Client",
            "lead_id": review.lead_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "provider_reply": review.provider_reply,
            "provider_reply_at": review.provider_reply_at,
            "provider_reply_edited_at": review.provider_reply_edited_at,
            "provider_reply_edit_count": review.provider_reply_edit_count,
            "is_reply_edited": review.provider_reply_edit_count > 0,
        })

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_latest_review_preview(
    provider_id: UUID,
    db: Session
) -> Optional[Dict[str, Any]]:
    """Get the latest review conversation for dashboard preview."""
    result = db.query(
        Review,
        User.email.label('client_email')
    ).join(
        User, Review.client_id == User.id
    ).filter(
        Review.provider_id == provider_id
    ).order_by(
        func.coalesce(Review.provider_reply_at, Review.created_at).desc()
    ).first()

    if not result:
        return None

    review = result[0]
    client_email = result[1]

    # Count unreplied reviews
    unreplied_count = db.query(Review).filter(
        Review.provider_id == provider_id,
        Review.provider_reply == None
    ).count()

    return {
        "id": review.id,
        "client_name": client_email.split('@')[0] if client_email else "Client",
        "rating": review.rating,
        "comment_preview": _truncate_text(review.comment, 100),
        "has_reply": review.provider_reply is not None,
        "created_at": review.created_at,
        "unreplied_count": unreplied_count,
    }


def _truncate_text(text: Optional[str], max_length: int) -> Optional[str]:
    """Truncate text to max_length with ellipsis."""
    if not text:
        return text
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def add_provider_reply(
    provider_id: UUID,
    review_id: UUID,
    reply: str,
    db: Session
) -> Review:
    """Add or update a provider's reply to a review.

    Rules:
    - Provider can only reply to their own reviews
    - First reply triggers email notification to client (unless opted out)
    - Subsequent edits do NOT trigger emails
    - Reply can be edited unlimited times

    Returns:
        Updated review

    Raises:
        NevumoException: If review not found or not owned by provider
    """
    review = db.query(Review).filter(
        Review.id == review_id,
        Review.provider_id == provider_id
    ).first()

    if not review:
        raise NevumoException(404, "REVIEW_NOT_FOUND", "Review not found")

    # Check if this is first reply or edit
    is_first_reply = review.provider_reply is None

    # Update reply
    review.provider_reply = reply.strip()

    if is_first_reply:
        review.provider_reply_at = datetime.utcnow()
        review.provider_reply_edit_count = 0
    else:
        # Editing existing reply
        review.provider_reply_edited_at = datetime.utcnow()
        review.provider_reply_edit_count += 1

    db.commit()
    db.refresh(review)

    # Send email notification on first reply only
    if is_first_reply:
        email_service.send_review_reply_notification(
            db=db,
            review=review,
            is_first_reply=True
        )

    return review


def get_client_reviews(
    client_id: UUID,
    db: Session,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, Any]:
    """Get all reviews created by a client with provider replies."""
    query = db.query(
        Review,
        Provider.business_name.label('provider_business_name'),
        Lead.description.label('lead_description')
    ).join(
        Provider, Review.provider_id == Provider.id
    ).outerjoin(
        Lead, Review.lead_id == Lead.id
    ).filter(
        Review.client_id == client_id
    ).order_by(
        func.coalesce(Review.provider_reply_at, Review.created_at).desc()
    )

    total = query.count()
    reviews = query.offset(offset).limit(limit).all()

    items = []
    for row in reviews:
        review = row[0]
        provider_name = row[1]
        lead_desc = row[2]

        items.append({
            "id": review.id,
            "provider_id": review.provider_id,
            "provider_business_name": provider_name,
            "lead_id": review.lead_id,
            "lead_description": lead_desc,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at,
            "provider_reply": review.provider_reply,
            "provider_reply_at": review.provider_reply_at,
            "provider_reply_edited_at": review.provider_reply_edited_at,
            "provider_reply_edit_count": review.provider_reply_edit_count,
            "is_reply_edited": review.provider_reply_edit_count > 0,
        })

    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_client_review_preferences(
    client_id: UUID,
    db: Session
) -> Dict[str, Any]:
    """Get client's email notification preferences for review replies."""
    user = db.query(User).filter(User.id == client_id).first()
    if not user:
        raise NevumoException(404, "USER_NOT_FOUND", "User not found")

    return {
        "review_reply_email_enabled": user.review_reply_email_enabled,
    }


def update_client_review_preferences(
    client_id: UUID,
    review_reply_email_enabled: bool,
    db: Session
) -> Dict[str, Any]:
    """Update client's email notification preferences."""
    user = db.query(User).filter(User.id == client_id).first()
    if not user:
        raise NevumoException(404, "USER_NOT_FOUND", "User not found")

    user.review_reply_email_enabled = review_reply_email_enabled
    db.commit()

    return {
        "review_reply_email_enabled": user.review_reply_email_enabled,
    }


def can_client_review_provider(
    client_id: UUID,
    provider_id: UUID,
    db: Session
) -> Dict[str, Any]:
    """Check if a client is eligible to review a specific provider.

    Eligibility requires:
    - At least one completed lead with this provider
    - No existing review for any lead with this provider
    """
    # Get completed leads with this provider
    completed_leads = db.query(Lead).filter(
        Lead.client_id == client_id,
        Lead.provider_id == provider_id,
        Lead.status == "done"
    ).all()

    if not completed_leads:
        return {
            "can_review": False,
            "reason": "no_completed_jobs",
            "message": "You can only review providers after completing a job with them",
        }

    # Check for existing reviews for any of these leads
    lead_ids = [lead.id for lead in completed_leads]
    existing_reviews = db.query(Review).filter(
        Review.client_id == client_id,
        Review.provider_id == provider_id
    ).count()

    if existing_reviews >= len(lead_ids):
        return {
            "can_review": False,
            "reason": "already_reviewed",
            "message": "You have already reviewed all completed jobs with this provider",
        }

    # Return eligible leads
    reviewed_lead_ids = {
        r[0] for r in db.query(Review.lead_id).filter(
            Review.client_id == client_id,
            Review.provider_id == provider_id
        ).all()
    }

    unreviewed_leads = [
        {"id": lead.id, "description": lead.description, "created_at": lead.created_at}
        for lead in completed_leads
        if lead.id not in reviewed_lead_ids
    ]

    return {
        "can_review": True,
        "eligible_leads": unreviewed_leads,
    }
