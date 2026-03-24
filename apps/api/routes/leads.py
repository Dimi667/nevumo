from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from dependencies import get_db
from exceptions import (
    INVALID_PHONE,
    CATEGORY_NOT_FOUND,
    CITY_NOT_FOUND,
    PROVIDER_NOT_FOUND,
    RATE_LIMIT_EXCEEDED,
)
from models import (
    Lead,
    LeadMatch,
    LeadRateLimit,
    Category,
    Location,
    Provider,
    Service,
    ProviderCity,
)
from schemas import (
    LeadCreate,
    LeadCreatedResponse,
)

router = APIRouter(prefix="/api/v1", tags=["leads"])


@router.post("/leads", response_model=LeadCreatedResponse)
async def create_lead(
    payload: LeadCreate,
    request: Request,
    db: Session = Depends(get_db),
) -> LeadCreatedResponse:
    phone = payload.phone.strip()
    if not phone:
        raise INVALID_PHONE

    category = db.query(Category).filter(Category.slug == payload.category_slug).first()
    if not category:
        raise CATEGORY_NOT_FOUND

    location = db.query(Location).filter(Location.slug == payload.city_slug).first()
    if not location:
        raise CITY_NOT_FOUND

    provider_id = None
    if payload.provider_slug:
        provider = db.query(Provider).filter(Provider.slug == payload.provider_slug).first()
        if not provider:
            raise PROVIDER_NOT_FOUND
        provider_id = provider.id

    client_ip = request.client.host if request.client else "unknown"
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_count = (
        db.query(LeadRateLimit)
        .filter(LeadRateLimit.ip == client_ip, LeadRateLimit.created_at >= one_hour_ago)
        .count()
    )
    if recent_count >= 5:
        raise RATE_LIMIT_EXCEEDED

    lead = Lead(
        category_id=category.id,
        city_id=location.id,
        provider_id=provider_id,
        phone=phone,
        description=payload.description,
        budget=payload.budget,
        source=payload.source,
        utm_source=payload.utm_source,
        utm_campaign=payload.utm_campaign,
        landing_page=payload.landing_page,
    )
    db.add(lead)
    db.flush()

    db.add(LeadRateLimit(ip=client_ip))

    if provider_id:
        # Direct assignment: create a single LeadMatch so the PATCH endpoint can update it
        db.add(LeadMatch(lead_id=lead.id, provider_id=provider_id, status="invited"))
    else:
        matching_providers = (
            db.query(Provider)
            .join(Service, Provider.id == Service.provider_id)
            .join(ProviderCity, Provider.id == ProviderCity.provider_id)
            .filter(
                Service.category_id == category.id,
                ProviderCity.city_id == location.id,
                Provider.availability_status == "active",
            )
            .distinct()
            .all()
        )
        for p in matching_providers:
            db.add(LeadMatch(lead_id=lead.id, provider_id=p.id, status="invited"))

    db.commit()
    db.refresh(lead)

    return LeadCreatedResponse(data={"lead_id": str(lead.id)})
