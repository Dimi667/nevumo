"""Provider dashboard service layer."""

import base64
import io
from decimal import Decimal
from pathlib import Path
from typing import Optional
from uuid import UUID

import qrcode
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NevumoException
from models import (
    Category,
    Lead,
    LeadMatch,
    Location,
    Provider,
    ProviderCity,
    Service,
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
    """Return (is_complete, missing_fields)."""
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    missing: list[str] = []
    if not provider or not provider.business_name:
        missing.append("business_name")
    if not db.query(Service).filter(Service.provider_id == provider_id).first():
        missing.append("service")
    if not db.query(ProviderCity).filter(ProviderCity.provider_id == provider_id).first():
        missing.append("city")
    return (len(missing) == 0, missing)


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

def add_service(
    db: Session,
    provider_id: UUID,
    category_id: int,
    title: str,
    description: Optional[str],
    price_type: str,
    base_price: Optional[Decimal],
) -> Service:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")
    if price_type not in ("fixed", "hourly", "request"):
        raise NevumoException(
            400,
            "INVALID_PRICE_TYPE",
            "price_type must be fixed, hourly, or request",
        )
    service = Service(
        provider_id=provider_id,
        category_id=category_id,
        title=title,
        description=description,
        price_type=price_type,
        base_price=base_price,
    )
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


def get_provider_services(provider: Provider, db: Session) -> list:
    """Return services for the provider."""
    services = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .all()
    )
    return [
        {
            "id": str(s.id),
            "title": s.title,
            "description": s.description,
            "price_type": s.price_type,
            "base_price": float(s.base_price) if s.base_price else None,
        }
        for s in services
    ]


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


def get_provider_profile(provider: Provider) -> dict:
    """Serialize provider profile for API response."""
    return {
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


def update_provider_profile(
    provider: Provider,
    db: Session,
    business_name: Optional[str],
    description: Optional[str],
    availability_status: Optional[str],
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
