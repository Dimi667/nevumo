"""Provider dashboard service layer."""

import base64
import io
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional, TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from models import User

import qrcode
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NevumoException
from models import (
    Category,
    CategoryTranslation,
    Lead,
    LeadMatch,
    Location,
    Provider,
    ProviderCity,
    Service,
    ServiceCity,
)

# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

UPLOAD_BASE = Path("uploads/provider_images")


def save_provider_image(provider_id: UUID, content: bytes, ext: str) -> str:
    """Save image to local filesystem. Returns URL path.
    TODO: Replace with S3/R2 upload when migrating cloud storage."""
    UPLOAD_BASE.mkdir(parents=True, exist_ok=True)
    filename = f"{provider_id}.{ext}"
    filepath = UPLOAD_BASE / filename
    filepath.write_bytes(content)
    return f"/static/provider_images/{filename}"


def get_image_url(provider_id: UUID, ext: str) -> str:
    """Get public URL for provider image.
    TODO: Replace with S3/R2 URL when migrating cloud storage."""
    return f"/static/provider_images/{provider_id}.{ext}"


# ---------------------------------------------------------------------------
# Lead status state machine
# ---------------------------------------------------------------------------

VALID_TRANSITIONS: dict[str, list[str]] = {
    "new": ["contacted", "rejected"],
    "contacted": ["done", "rejected"],
    "done": [],       # terminal
    "rejected": [],   # terminal
}


def get_ui_status(lead: Lead, match: Optional[LeadMatch] = None) -> str:
    """Map DB status to UI status."""
    if match:
        if match.status in ("contacted", "done", "rejected"):
            return match.status
        return "new"  # "invited" → "new" in UI
    else:
        if lead.status in ("contacted", "done", "rejected"):
            return lead.status
        return "new"  # "created"/"pending_match"/"matched" → "new" in UI


def change_lead_status(
    db: Session,
    lead_id_str: str,
    provider_id: UUID,
    new_status: str,
) -> dict:
    """Apply state-machine-validated status transition to a lead."""
    # Try direct lead first (lead.provider_id == this provider)
    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id_str, Lead.provider_id == provider_id)
        .first()
    )
    match: Optional[LeadMatch] = None

    if not lead:
        # Try marketplace lead via lead_match
        match = (
            db.query(LeadMatch)
            .filter(
                LeadMatch.lead_id == lead_id_str,
                LeadMatch.provider_id == provider_id,
            )
            .first()
        )
        if match:
            lead = db.query(Lead).filter(Lead.id == lead_id_str).first()

    if not lead:
        raise NevumoException(404, "LEAD_NOT_FOUND", "Lead not found")

    current_status = get_ui_status(lead, match)
    allowed = VALID_TRANSITIONS.get(current_status, [])
    if new_status not in allowed:
        raise NevumoException(
            400,
            "INVALID_STATUS_TRANSITION",
            f"Cannot change from {current_status} to {new_status}",
        )

    if match:
        match.status = new_status
    else:
        lead.status = new_status

    db.commit()
    return {"lead_id": lead_id_str, "status": new_status}


# ---------------------------------------------------------------------------
# Onboarding completeness
# ---------------------------------------------------------------------------

def check_onboarding_complete(
    db: Session, provider_id: UUID
) -> tuple[bool, list[str]]:
    """Return (is_complete, missing_fields).
    business_name counts as missing when it is absent or still an email placeholder.
    A service is complete only when it has at least one associated city in service_cities.
    """
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    missing: list[str] = []
    if not provider or not provider.business_name or "@" in provider.business_name:
        missing.append("business_name")

    has_service = (
        db.query(Service).filter(Service.provider_id == provider_id).first()
    ) is not None
    if not has_service:
        missing.append("service")
        missing.append("city")
    else:
        has_city = (
            db.query(ServiceCity)
            .join(Service, Service.id == ServiceCity.service_id)
            .filter(Service.provider_id == provider_id)
            .first()
        ) is not None
        if not has_city:
            missing.append("city")

    return (len(missing) == 0, missing)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def _resolve_cities(
    db: Session,
    city_ids: list[int],
) -> list[Location]:
    """Validate and return Location records for the given city_ids.
    Raises NevumoException for any id not found in locations table.
    """
    locations: list[Location] = []
    for city_id in city_ids:
        loc = db.query(Location).filter(Location.id == city_id).first()
        if not loc:
            raise NevumoException(404, "CITY_NOT_FOUND", f"City {city_id} not found")
        locations.append(loc)
    return locations


def _sync_provider_cities(
    db: Session,
    provider_id: UUID,
    locations: list[Location],
) -> None:
    """Ensure every location also exists in provider_cities (for lead matching)."""
    for loc in locations:
        existing = (
            db.query(ProviderCity)
            .filter(
                ProviderCity.provider_id == provider_id,
                ProviderCity.city_id == loc.id,
            )
            .first()
        )
        if not existing:
            db.add(ProviderCity(provider_id=provider_id, city_id=loc.id))


def _serialize_service(service: Service, db: Session) -> dict:
    """Return a ServiceResponse-compatible dict for a single Service."""
    category = db.query(Category).filter(Category.id == service.category_id).first()
    category_slug = category.slug if category else ""

    city_rows = (
        db.query(ServiceCity, Location)
        .join(Location, Location.id == ServiceCity.city_id)
        .filter(ServiceCity.service_id == service.id)
        .all()
    )
    cities = [
        {"id": loc.id, "slug": loc.slug, "city": loc.city}
        for _, loc in city_rows
    ]

    return {
        "id": str(service.id),
        "title": service.title,
        "category_id": service.category_id,
        "category_slug": category_slug,
        "cities": cities,
        "description": service.description,
        "price_type": service.price_type,
        "base_price": float(service.base_price) if service.base_price is not None else None,
        "currency": service.currency,
    }


def add_service(
    db: Session,
    provider_id: UUID,
    category_id: int,
    title: str,
    city_ids: list[int],
    description: Optional[str],
    price_type: str,
    base_price: Optional[Decimal],
    currency: str = "EUR",
) -> Service:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")

    locations = _resolve_cities(db, city_ids)

    service = Service(
        provider_id=provider_id,
        category_id=category_id,
        title=title,
        description=description,
        price_type=price_type,
        base_price=base_price,
        currency=currency,
    )
    db.add(service)
    db.flush()  # get service.id before adding service_cities

    for loc in locations:
        db.add(ServiceCity(service_id=service.id, city_id=loc.id))

    _sync_provider_cities(db, provider_id, locations)

    db.commit()
    db.refresh(service)
    return service


def update_service(
    db: Session,
    service_id: str,
    provider_id: UUID,
    title: Optional[str],
    category_id: Optional[int],
    city_ids: Optional[list[int]],
    description: Optional[str],
    price_type: Optional[str],
    base_price: Optional[Decimal],
    currency: Optional[str],
) -> Service:
    service = (
        db.query(Service)
        .filter(Service.id == service_id, Service.provider_id == provider_id)
        .first()
    )
    if not service:
        raise NevumoException(404, "SERVICE_NOT_FOUND", "Service not found")

    if title is not None:
        service.title = title
    if description is not None:
        service.description = description
    if price_type is not None:
        service.price_type = price_type
    if base_price is not None:
        service.base_price = base_price
    if currency is not None:
        service.currency = currency

    if category_id is not None:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")
        service.category_id = category_id

    if city_ids is not None:
        locations = _resolve_cities(db, city_ids)
        db.query(ServiceCity).filter(ServiceCity.service_id == service.id).delete()
        for loc in locations:
            db.add(ServiceCity(service_id=service.id, city_id=loc.id))
        _sync_provider_cities(db, provider_id, locations)

    db.commit()
    db.refresh(service)
    return service


def delete_service(db: Session, service_id: str, provider_id: UUID) -> None:
    service = (
        db.query(Service)
        .filter(Service.id == service_id, Service.provider_id == provider_id)
        .first()
    )
    if not service:
        raise NevumoException(404, "SERVICE_NOT_FOUND", "Service not found")
    db.delete(service)
    db.commit()


def get_provider_services(provider: Provider, db: Session) -> list:
    """Return services for the provider with cities and currency."""
    services = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .all()
    )
    return [_serialize_service(s, db) for s in services]


# ---------------------------------------------------------------------------
# Cities
# ---------------------------------------------------------------------------

def add_city(db: Session, provider_id: UUID, city_id: int) -> ProviderCity:
    city = db.query(Location).filter(Location.id == city_id).first()
    if not city:
        raise NevumoException(404, "CITY_NOT_FOUND", "City not found")
    existing = (
        db.query(ProviderCity)
        .filter(
            ProviderCity.provider_id == provider_id,
            ProviderCity.city_id == city_id,
        )
        .first()
    )
    if existing:
        raise NevumoException(409, "CITY_ALREADY_ADDED", "City already added to your profile")
    pc = ProviderCity(provider_id=provider_id, city_id=city_id)
    db.add(pc)
    db.commit()
    return pc


# ---------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------

def generate_provider_slug(business_name: str, db: Session) -> str:
    """Generate a unique slug from business_name."""
    base = slugify(business_name, allow_unicode=False)
    slug = base
    counter = 1
    while db.query(Provider).filter(Provider.slug == slug).first():
        slug = f"{base}-{counter}"
        counter += 1
    return slug


def get_or_create_provider(user: "User", db: Session) -> Provider:
    """Return the Provider record for *user*, creating one if it does not exist."""
    provider = db.query(Provider).filter(Provider.user_id == user.id).first()
    if provider is None:
        slug = generate_provider_slug(user.email, db)
        provider = Provider(
            user_id=user.id,
            business_name=user.email,
            slug=slug,
            rating=0,
            verified=False,
            availability_status="active",
        )
        db.add(provider)
        db.commit()
        db.refresh(provider)
    return provider


def get_provider_profile(provider: Provider, db: Optional[Session] = None) -> dict:
    """Serialize provider profile for API response.
    When *db* is provided, also includes current_category and current_city.
    """
    data: dict = {
        "id": str(provider.id),
        "business_name": provider.business_name,
        "description": provider.description,
        "slug": provider.slug,
        "profile_image_url": provider.profile_image_url,
        "rating": float(provider.rating or 0),
        "verified": provider.verified,
        "availability_status": provider.availability_status,
        "created_at": provider.created_at.isoformat(),
    }

    if db is not None:
        # current_category: first service's category with English name
        first_service = (
            db.query(Service)
            .filter(Service.provider_id == provider.id)
            .first()
        )
        if first_service:
            translation = (
                db.query(CategoryTranslation)
                .filter(
                    CategoryTranslation.category_id == first_service.category_id,
                    CategoryTranslation.lang == "en",
                )
                .first()
            )
            category = db.query(Category).filter(Category.id == first_service.category_id).first()
            data["current_category"] = {
                "slug": category.slug if category else "",
                "name": translation.name if translation else (category.slug if category else ""),
            }
        else:
            data["current_category"] = None

        # current_city: first ProviderCity's Location
        first_pc = (
            db.query(ProviderCity)
            .filter(ProviderCity.provider_id == provider.id)
            .first()
        )
        if first_pc:
            loc = db.query(Location).filter(Location.id == first_pc.city_id).first()
            data["current_city"] = {
                "slug": loc.slug if loc else "",
                "name": loc.city if loc else "",
            }
        else:
            data["current_city"] = None

    return data


def update_provider_profile(
    provider: Provider,
    db: Session,
    business_name: Optional[str],
    description: Optional[str],
    availability_status: Optional[str],
    category_slug: Optional[str] = None,
    city_slug: Optional[str] = None,
) -> Provider:
    """Apply partial profile updates and commit."""
    if business_name is not None:
        provider.business_name = business_name
        new_slug = generate_provider_slug(business_name, db)
        provider.slug = new_slug
    if description is not None:
        provider.description = description
    if availability_status is not None:
        provider.availability_status = availability_status

    if category_slug is not None:
        category = db.query(Category).filter(Category.slug == category_slug).first()
        if not category:
            raise NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")
        existing_service = (
            db.query(Service)
            .filter(Service.provider_id == provider.id, Service.category_id == category.id)
            .first()
        )
        if not existing_service:
            translation = (
                db.query(CategoryTranslation)
                .filter(
                    CategoryTranslation.category_id == category.id,
                    CategoryTranslation.lang == "en",
                )
                .first()
            )
            title = translation.name if translation else category.slug
            db.add(Service(
                provider_id=provider.id,
                category_id=category.id,
                title=title,
                price_type="request",
            ))

    if city_slug is not None:
        loc = db.query(Location).filter(Location.slug == city_slug).first()
        if not loc:
            raise NevumoException(404, "CITY_NOT_FOUND", "City not found")
        existing_pc = (
            db.query(ProviderCity)
            .filter(ProviderCity.provider_id == provider.id, ProviderCity.city_id == loc.id)
            .first()
        )
        if not existing_pc:
            db.add(ProviderCity(provider_id=provider.id, city_id=loc.id))

    db.commit()
    db.refresh(provider)
    return provider


# ---------------------------------------------------------------------------
# Dashboard stats
# ---------------------------------------------------------------------------

def get_dashboard_stats(provider: Provider, db: Session) -> dict:
    """Return KPI stats for the provider dashboard."""
    total_leads = (
        db.query(func.count(Lead.id))
        .filter(Lead.provider_id == provider.id)
        .scalar()
        or 0
    )

    new_leads = (
        db.query(func.count(Lead.id))
        .filter(Lead.provider_id == provider.id, Lead.status == "created")
        .scalar()
        or 0
    )

    accepted_matches = (
        db.query(func.count(LeadMatch.id))
        .filter(
            LeadMatch.provider_id == provider.id,
            LeadMatch.status == "contacted",
        )
        .scalar()
        or 0
    )

    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "accepted_matches": accepted_matches,
        "rating": float(provider.rating or 0),
        "verified": provider.verified,
        "availability_status": provider.availability_status,
    }


# ---------------------------------------------------------------------------
# Leads list
# ---------------------------------------------------------------------------

def get_provider_leads(provider: Provider, db: Session, limit: int = 50) -> list:
    """Return recent leads for the provider."""
    leads = (
        db.query(Lead)
        .filter(Lead.provider_id == provider.id)
        .order_by(Lead.created_at.desc())
        .limit(limit)
        .all()
    )

    result = []
    for lead in leads:
        result.append(
            {
                "id": str(lead.id),
                "phone": lead.phone,
                "description": lead.description,
                "status": lead.status,
                "source": lead.source,
                "created_at": lead.created_at.isoformat(),
            }
        )
    return result


# ---------------------------------------------------------------------------
# Public URL + QR
# ---------------------------------------------------------------------------

def build_public_url(provider: Provider, db: Session, app_url: str) -> str:
    """Build the canonical public URL for the provider's page."""
    first_city_row = (
        db.query(ProviderCity)
        .filter(ProviderCity.provider_id == provider.id)
        .first()
    )
    first_service = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .first()
    )

    if first_city_row and first_service:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        category = db.query(Category).filter(Category.id == first_service.category_id).first()
        lang = provider.user.locale if provider.user else "en"
        if city and category:
            return f"{app_url}/{lang}/{city.slug}/{category.slug}/{provider.slug}"

    return f"{app_url}/provider/{provider.slug}"


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

_KNOWN_SOURCES = frozenset({"seo", "widget", "qr", "direct"})
_CONTACTED_STATUSES = frozenset({"contacted", "done", "accepted", "in_progress", "completed"})


def get_analytics(provider: Provider, db: Session, period_days: int = 30) -> dict:
    """Return analytics data for the provider over the last *period_days* days."""
    since = datetime.utcnow() - timedelta(days=period_days)

    leads = (
        db.query(Lead)
        .filter(Lead.provider_id == provider.id, Lead.created_at >= since)
        .all()
    )

    total = len(leads)
    contacted = sum(1 for lead in leads if lead.status in _CONTACTED_STATUSES)
    conversion_rate = round(contacted / total * 100, 1) if total > 0 else 0.0

    sources: dict[str, int] = {"seo": 0, "widget": 0, "qr": 0, "direct": 0, "other": 0}
    for lead in leads:
        src = (lead.source or "").lower().strip()
        if src in _KNOWN_SOURCES:
            sources[src] += 1
        else:
            sources["other"] += 1

    return {
        "period_days": period_days,
        "total_leads": total,
        "contacted_leads": contacted,
        "conversion_rate": conversion_rate,
        "sources": sources,
    }


def generate_qr_code_base64(url: str) -> str:
    """Generate a QR code PNG for the given URL and return as base64 data URI."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
