from typing import Any
from uuid import UUID

from sqlalchemy import and_, func
from sqlalchemy.orm import Session, aliased

from apps.api.exceptions import NevumoException
from apps.api.models import Category, CategoryTranslation, Lead, LeadMatch, Location, Provider, Review, Service, ServiceCity, User

ACTIVE_LEAD_STATUSES: tuple[str, ...] = ("created", "pending_match", "matched", "contacted")
REJECTED_LEAD_STATUSES: tuple[str, ...] = ("rejected", "expired", "cancelled")


def require_client_user(current_user: User) -> User:
    """Ensure current user is an active user (can be client or provider)."""
    return current_user


def _apply_status_filter(query: Any, status: str) -> Any:
    if status == "active":
        return query.filter(Lead.status.in_(ACTIVE_LEAD_STATUSES))
    if status == "done":
        return query.filter(Lead.status == "done")
    if status == "rejected":
        return query.filter(Lead.status.in_(REJECTED_LEAD_STATUSES))
    return query


def get_client_dashboard(client_id: UUID, db: Session, lang: str = 'en') -> dict[str, Any]:
    active_leads = int(
        db.query(func.count(Lead.id))
        .filter(Lead.client_id == client_id, Lead.status.in_(ACTIVE_LEAD_STATUSES))
        .scalar()
        or 0
    )
    completed_leads = int(
        db.query(func.count(Lead.id))
        .filter(Lead.client_id == client_id, Lead.status == "done")
        .scalar()
        or 0
    )
    reviews_written = int(
        db.query(func.count(Review.id))
        .filter(Review.client_id == client_id)
        .scalar()
        or 0
    )

    provider_user = aliased(User)
    ct_req = aliased(CategoryTranslation)
    ct_en = aliased(CategoryTranslation)
    recent_rows = (
        db.query(
            Lead.id.label("id"),
            Category.slug.label("category_slug"),
            func.coalesce(ct_req.name, ct_en.name, Category.slug).label("category_name"),
            Location.city.label("city"),
            Location.slug.label("city_slug"),
            Provider.business_name.label("provider_business_name"),
            Lead.status.label("status"),
            Lead.created_at.label("created_at"),
        )
        .join(Category, Lead.category_id == Category.id)
        .outerjoin(
            ct_req,
            and_(ct_req.category_id == Category.id, ct_req.lang == lang),
        )
        .outerjoin(
            ct_en,
            and_(ct_en.category_id == Category.id, ct_en.lang == "en"),
        )
        .join(Location, Lead.city_id == Location.id)
        .outerjoin(Provider, Lead.provider_id == Provider.id)
        .outerjoin(provider_user, Provider.user_id == provider_user.id)
        .filter(Lead.client_id == client_id)
        .order_by(Lead.created_at.desc())
        .limit(3)
        .all()
    )

    recent_leads = [
        {
            "id": row.id,
            "category_slug": row.category_slug,
            "category_name": row.category_name,
            "city": row.city,
            "city_slug": row.city_slug,
            "provider_business_name": row.provider_business_name,
            "status": row.status,
            "created_at": row.created_at,
        }
        for row in recent_rows
    ]

    # Priority 1: user.city_id
    user = db.query(User).filter(User.id == client_id).first()
    last_city_slug = None
    if user and user.city_id:
        last_city_slug = db.query(Location.slug).filter(Location.id == user.city_id).scalar()

    # Priority 2: Last client lead (fallback)
    if not last_city_slug:
        if recent_leads:
            last_city_slug = recent_leads[0]["city_slug"]
        else:
            last_city_slug = (
                db.query(Location.slug)
                .join(Lead, Lead.city_id == Location.id)
                .filter(Lead.client_id == client_id)
                .order_by(Lead.created_at.desc())
                .limit(1)
                .scalar()
            )

    # Priority 3: Provider service city (fallback)
    if not last_city_slug:
        last_city_slug = (
            db.query(Location.slug)
            .join(ServiceCity, ServiceCity.city_id == Location.id)
            .join(Service, Service.id == ServiceCity.service_id)
            .join(Provider, Provider.id == Service.provider_id)
            .filter(Provider.user_id == client_id)
            .order_by(Service.created_at.desc())
            .limit(1)
            .scalar()
        )

    return {
        "stats": {
            "active_leads": active_leads,
            "completed_leads": completed_leads,
            "reviews_written": reviews_written,
        },
        "recent_leads": recent_leads,
        "last_city_slug": last_city_slug,
    }


def get_client_leads(
    client_id: UUID,
    db: Session,
    status: str = "all",
    limit: int = 50,
    offset: int = 0,
    lang: str = 'en',
) -> dict[str, Any]:
    total_query = db.query(func.count(Lead.id)).filter(Lead.client_id == client_id)
    total_query = _apply_status_filter(total_query, status)
    total = int(total_query.scalar() or 0)

    provider_user = aliased(User)
    has_review_subquery = db.query(Review.id).filter(Review.lead_id == Lead.id).exists()
    ct_req = aliased(CategoryTranslation)
    ct_en = aliased(CategoryTranslation)

    leads_query = (
        db.query(
            Lead.id.label("id"),
            Category.slug.label("category_slug"),
            func.coalesce(ct_req.name, ct_en.name, Category.slug).label("category_name"),
            Location.city.label("city"),
            Location.slug.label("city_slug"),
            Provider.id.label("provider_id"),
            Provider.business_name.label("provider_business_name"),
            Provider.slug.label("provider_slug"),
            Lead.status.label("status"),
            Lead.description.label("description"),
            Lead.source.label("source"),
            Lead.created_at.label("created_at"),
            Lead.client_notes.label("client_notes"),
            Lead.cancelled_by.label("cancelled_by"),
            Lead.status_changed_by.label("status_changed_by"),
            has_review_subquery.label("has_review"),
        )
        .join(Category, Lead.category_id == Category.id)
        .outerjoin(
            ct_req,
            and_(ct_req.category_id == Category.id, ct_req.lang == lang),
        )
        .outerjoin(
            ct_en,
            and_(ct_en.category_id == Category.id, ct_en.lang == "en"),
        )
        .join(Location, Lead.city_id == Location.id)
        .outerjoin(Provider, Lead.provider_id == Provider.id)
        .outerjoin(provider_user, Provider.user_id == provider_user.id)
        .filter(Lead.client_id == client_id)
    )
    leads_query = _apply_status_filter(leads_query, status)

    rows = (
        leads_query.order_by(Lead.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    items = []
    for row in rows:
        reviewable_providers = []
        if row.status == "done":
            # Find reviewable providers for this lead
            # Must have LeadMatch status in ('contacted', 'done')
            # AND no existing review for this lead/provider combo
            reviewable_providers_query = (
                db.query(
                    Provider.id,
                    Provider.business_name,
                    Provider.slug
                )
                .join(LeadMatch, LeadMatch.provider_id == Provider.id)
                .outerjoin(
                    Review,
                    (Review.lead_id == LeadMatch.lead_id) & (Review.provider_id == LeadMatch.provider_id)
                )
                .filter(
                    LeadMatch.lead_id == row.id,
                    LeadMatch.status.in_(["contacted", "done"]),
                    Review.id == None,  # No review yet
                    Provider.user_id != client_id  # Cannot review self
                )
            )
            providers = reviewable_providers_query.all()
            reviewable_providers = [
                {
                    "provider_id": p.id,
                    "provider_name": p.business_name,
                    "provider_slug": p.slug
                } for p in providers
            ]

        items.append({
            "id": row.id,
            "category_slug": row.category_slug,
            "category_name": row.category_name,
            "city": row.city,
            "city_slug": row.city_slug,
            "provider_id": row.provider_id,
            "provider_business_name": row.provider_business_name,
            "provider_slug": row.provider_slug,
            "status": row.status,
            "description": row.description,
            "source": row.source,
            "created_at": row.created_at,
            "has_review": bool(row.has_review),
            "reviewable_providers": reviewable_providers,
            "client_notes": row.client_notes,
            "cancelled_by": row.cancelled_by,
            "status_changed_by": row.status_changed_by,
        })

    return {"items": items, "total": total}
