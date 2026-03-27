"""Provider dashboard service layer."""

import base64
import io
import os
import re
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List
from uuid import UUID

if TYPE_CHECKING:
    from models import User

import qrcode
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.orm import Session

from exceptions import NevumoException
from constants import COUNTRY_CURRENCY_MAP, DEFAULT_CURRENCY
from models import (
    Category,
    CategoryTranslation,
    Lead,
    LeadMatch,
    Location,
    Provider,
    ProviderSlugHistory,
    ProviderCity,
    Review,
    Service,
    ServiceCity,
    UrlRedirect,
)

MAX_SLUG_CHANGES = 1

# ---------------------------------------------------------------------------
# Dynamic Stats Calculations
# ---------------------------------------------------------------------------


def get_provider_rating(provider_id: UUID, db: Session) -> float:
    """Calculate average rating from reviews. Returns 0.0 if no reviews."""
    avg_rating = (
        db.query(func.avg(Review.rating))
        .filter(Review.provider_id == provider_id)
        .scalar()
    )
    return round(float(avg_rating or 0), 1)


def get_provider_jobs_completed(provider_id: UUID, db: Session) -> int:
    """Calculate completed jobs from leads + lead_matches with status 'done'."""
    direct_done = (
        db.query(func.count(Lead.id))
        .filter(Lead.provider_id == provider_id, Lead.status == "done")
        .scalar()
        or 0
    )

    match_done = (
        db.query(func.count(LeadMatch.id))
        .filter(LeadMatch.provider_id == provider_id, LeadMatch.status == "done")
        .scalar()
        or 0
    )

    return int(direct_done + match_done)


def get_provider_review_count(provider_id: UUID, db: Session) -> int:
    """Get total number of reviews for provider."""
    count = (
        db.query(func.count(Review.id))
        .filter(Review.provider_id == provider_id)
        .scalar()
        or 0
    )
    return int(count)


# ---------------------------------------------------------------------------
# Storage
# ---------------------------------------------------------------------------

UPLOAD_BASE = Path("uploads/provider_images")


def get_static_files_base_url() -> str:
    """Get the base URL for static files, supporting both local and cloud storage."""
    return os.getenv("STATIC_FILES_BASE_URL", "http://localhost:8000")


def save_provider_image(provider_id: UUID, content: bytes, ext: str) -> str:
    """Save image to local filesystem. Returns full URL.
    TODO: Replace with S3/R2 upload when migrating cloud storage."""
    UPLOAD_BASE.mkdir(parents=True, exist_ok=True)
    filename = f"{provider_id}.{ext}"
    filepath = UPLOAD_BASE / filename
    filepath.write_bytes(content)
    
    # Return full URL for proper cross-origin loading
    base_url = get_static_files_base_url().rstrip('/')
    return f"{base_url}/static/provider_images/{filename}"


def get_image_url(provider_id: UUID, ext: str) -> str:
    """Get public URL for provider image.
    TODO: Replace with S3/R2 URL when migrating cloud storage."""
    base_url = get_static_files_base_url().rstrip('/')
    return f"{base_url}/static/provider_images/{provider_id}.{ext}"


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
    currency: Optional[str] = None,
) -> Service:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise NevumoException(404, "CATEGORY_NOT_FOUND", "Category not found")

    locations = _resolve_cities(db, city_ids)
    
    # Auto-detect currency from first city if not provided
    if currency is None:
        first_location = locations[0] if locations else None
        if first_location:
            currency = COUNTRY_CURRENCY_MAP.get(first_location.country_code, DEFAULT_CURRENCY)
        else:
            currency = DEFAULT_CURRENCY

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
        
        # Auto-detect currency from first city if currency is None and city_ids changed
        if currency is None:
            first_location = locations[0] if locations else None
            if first_location:
                service.currency = COUNTRY_CURRENCY_MAP.get(first_location.country_code, DEFAULT_CURRENCY)

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

def validate_slug(slug: str) -> tuple[bool, Optional[str]]:
    """Validate slug format. Returns (is_valid, error_message)."""
    if len(slug) < 2 or len(slug) > 50:
        return False, "Slug must be 2-50 characters"
    if re.search(r'-\d+$', slug):
        return False, "Numeric suffixes not allowed (e.g., devs-1)"
    if not re.match(r'^[a-z0-9]+(?:-[a-z0-9]+)*$', slug):
        return False, "Only lowercase letters, numbers, and hyphens allowed"
    return True, None


def generate_slug_suggestions(
    base: str,
    city_slug: Optional[str],
    category_slug: Optional[str],
    db: Session
) -> List[str]:
    """Generate contextual slug suggestions, excluding taken ones."""
    normalized_base = slugify(base, allow_unicode=False)
    candidates: List[str] = []

    # Add contextual combinations
    if city_slug:
        candidates.append(f"{normalized_base}-{city_slug}")
    if category_slug:
        candidates.append(f"{normalized_base}-{category_slug}")
    if city_slug and category_slug:
        candidates.append(f"{normalized_base}-{city_slug}-{category_slug}")

    # Add generic alternatives
    candidates.extend([
        f"{normalized_base}-pro",
        f"{normalized_base}-studio",
        f"{normalized_base}-bg",
    ])

    # Filter out taken slugs
    taken = {p.slug for p in db.query(Provider.slug).all()}
    taken.update(old_slug for (old_slug,) in db.query(UrlRedirect.old_slug).all())
    available: List[str] = []
    for candidate in candidates:
        if candidate and candidate not in taken and candidate not in available:
            available.append(candidate)

    return available[:5]  # Return max 5 suggestions


def generate_provider_slug(business_name: str, db: Session) -> str:
    """Generate base slug from business_name without auto-increment."""
    return slugify(business_name, allow_unicode=False)


def is_slug_taken(slug: str, db: Session, provider_id: Optional[UUID] = None) -> bool:
    """Return whether a slug is already reserved by a provider or redirect."""
    provider_query = db.query(Provider).filter(Provider.slug == slug)
    if provider_id is not None:
        provider_query = provider_query.filter(Provider.id != provider_id)
    if provider_query.first():
        return True

    redirect_query = db.query(UrlRedirect).filter(UrlRedirect.old_slug == slug)
    if provider_id is not None:
        redirect_query = redirect_query.filter(UrlRedirect.provider_id != provider_id)
    return redirect_query.first() is not None


def _get_provider_public_context(
    provider: Provider,
    db: Session,
) -> tuple[Optional[str], Optional[str]]:
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

    city_slug: Optional[str] = None
    category_slug: Optional[str] = None

    if first_city_row:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        city_slug = city.slug if city else None

    if first_service:
        category = db.query(Category).filter(Category.id == first_service.category_id).first()
        category_slug = category.slug if category else None

    return city_slug, category_slug


def build_public_path(provider: Provider, db: Session, lang: Optional[str] = None) -> str:
    """Build the canonical public path for the provider."""
    city_slug, category_slug = _get_provider_public_context(provider, db)
    normalized_lang = lang or (provider.user.locale if provider.user else "en")
    if city_slug and category_slug:
        return f"/{normalized_lang}/{city_slug}/{category_slug}/{provider.slug}"
    return f"/provider/{provider.slug}"


def build_qr_public_path(provider: Provider, db: Session) -> str:
    """Build the stable QR path for the provider pointing to embedded widget."""
    city_slug, category_slug = _get_provider_public_context(provider, db)
    normalized_lang = provider.user.locale if provider.user else "en"
    
    if city_slug and category_slug:
        return f"/{normalized_lang}/{city_slug}/{category_slug}/{provider.slug}?embed=1"
    
    # Fallback to provider-only path if city/category missing
    return f"/provider/{provider.slug}?embed=1"


def _record_slug_change(
    provider: Provider,
    db: Session,
    old_slug: str,
    new_slug: str,
    request_ip: Optional[str],
    user_agent: Optional[str],
) -> None:
    db.add(
        ProviderSlugHistory(
            provider_id=provider.id,
            old_slug=old_slug,
            new_slug=new_slug,
            ip_address=request_ip,
            user_agent=user_agent,
        )
    )
    db.add(
        UrlRedirect(
            provider_id=provider.id,
            old_slug=old_slug,
            new_slug=new_slug,
            active=True,
        )
    )


def get_slug_history(provider: Provider, db: Session) -> list[dict]:
    """Return slug history for the provider."""
    entries = (
        db.query(ProviderSlugHistory)
        .filter(ProviderSlugHistory.provider_id == provider.id)
        .order_by(ProviderSlugHistory.changed_at.desc())
        .all()
    )
    return [
        {
            "id": str(entry.id),
            "old_slug": entry.old_slug,
            "new_slug": entry.new_slug,
            "changed_at": entry.changed_at.isoformat(),
            "ip_address": entry.ip_address,
            "user_agent": entry.user_agent,
        }
        for entry in entries
    ]


def get_provider_by_id(provider_id: UUID, db: Session) -> Optional[Provider]:
    """Fetch provider by stable UUID identifier."""
    return db.query(Provider).filter(Provider.id == provider_id).first()


def resolve_provider_slug(
    provider_slug: str,
    db: Session,
) -> tuple[Optional[Provider], Optional[str]]:
    """Resolve a provider by current slug or active redirect."""
    provider = db.query(Provider).filter(Provider.slug == provider_slug).first()
    if provider:
        return provider, None

    redirect = (
        db.query(UrlRedirect)
        .filter(UrlRedirect.old_slug == provider_slug, UrlRedirect.active == True)  # noqa: E712
        .order_by(UrlRedirect.created_at.desc())
        .first()
    )
    if redirect:
        provider = db.query(Provider).filter(Provider.id == redirect.provider_id).first()
        if provider:
            return provider, redirect.old_slug

    return None, None


def get_or_create_provider(
    user: "User",
    db: Session,
    preferred_slug: Optional[str] = None,
    business_name: Optional[str] = None,
    city_slug: Optional[str] = None,
    category_slug: Optional[str] = None,
) -> Provider:
    """Return the Provider record for *user*, creating one if it does not exist.
    
    When creating a new provider, validates slug uniqueness and returns suggestions
    if the preferred slug is already taken.
    """
    provider = db.query(Provider).filter(Provider.user_id == user.id).first()
    if provider is None:
        # Validate required fields
        if not preferred_slug:
            raise NevumoException(400, "MISSING_SLUG", "Slug is required")
        if not business_name:
            raise NevumoException(400, "MISSING_BUSINESS_NAME", "Business name is required")
        
        base = preferred_slug
        
        # Validate format
        is_valid, error = validate_slug(base)
        if not is_valid:
            raise NevumoException(400, "INVALID_SLUG", error)
        
        # Check uniqueness
        if is_slug_taken(base, db):
            suggestions = generate_slug_suggestions(base, city_slug, category_slug, db)
            raise NevumoException(
                409,
                "SLUG_TAKEN",
                f"Slug '{base}' is already taken",
                extra_data={"suggestions": suggestions}
            )
        
        # Create provider with unique slug
        provider = Provider(
            user_id=user.id,
            business_name=business_name,
            slug=base,
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
        "slug_change_count": provider.slug_change_count,
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
    business_name: Optional[str] = None,
    description: Optional[str] = None,
    availability_status: Optional[str] = None,
    category_slug: Optional[str] = None,
    city_slug: Optional[str] = None,
    slug: Optional[str] = None,
    request_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    is_onboarding_setup: bool = False,
) -> Provider:
    """Apply partial profile updates and commit."""
    if business_name is not None:
        provider.business_name = business_name
    if description is not None:
        provider.description = description
    if availability_status is not None:
        provider.availability_status = availability_status

    if slug is not None and slug != provider.slug:
        if provider.slug_change_count >= MAX_SLUG_CHANGES:
            raise NevumoException(
                409,
                "SLUG_CHANGE_LIMIT_EXCEEDED",
                "URL can only be changed once. Contact support for assistance.",
            )

        # Validate slug format
        is_valid, error_msg = validate_slug(slug)
        if not is_valid:
            raise NevumoException(400, "INVALID_SLUG", error_msg)

        # Check uniqueness
        if is_slug_taken(slug, db, provider_id=provider.id):
            suggestions = generate_slug_suggestions(slug, city_slug, category_slug, db)
            raise NevumoException(
                409,
                "SLUG_TAKEN",
                "This URL is already taken",
                extra_data={"suggestions": suggestions}
            )

        old_slug = provider.slug
        provider.slug = slug
        
        # Only count as a change if this is not initial setup or onboarding
        # Initial setup: provider.slug was empty/None, this is not a "change"
        # Onboarding setup: first change during onboarding, not counted against limit
        # Actual change: provider.slug had a value and this is not onboarding, this is a real change
        if old_slug and old_slug.strip() and not is_onboarding_setup:
            provider.slug_change_count += 1
            _record_slug_change(provider, db, old_slug, slug, request_ip, user_agent)

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
    return f"{app_url.rstrip('/')}{build_public_path(provider, db)}"


def build_qr_public_url(provider: Provider, db: Session, app_url: str) -> str:
    """Build the stable QR URL for the provider."""
    return f"{app_url.rstrip('/')}{build_qr_public_path(provider, db)}"


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
