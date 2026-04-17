"""Provider dashboard service layer."""

import base64
import html
import io
import os
import re
import secrets
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from typing import Optional, TYPE_CHECKING, List, Dict, Any
from uuid import UUID

if TYPE_CHECKING:
    from apps.api.models import User

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pillow_heif import register_heif_opener
from slugify import slugify
from sqlalchemy import func
from sqlalchemy.orm import Session

# Register HEIF opener to support HEIC/HEIF formats
register_heif_opener()

from apps.api.constants import COUNTRY_CURRENCY_MAP, DEFAULT_CURRENCY
from apps.api.exceptions import NevumoException
from apps.api.i18n import resolve_translation
from apps.api.models import (
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
    User,
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


def get_provider_leads_received(provider_id: UUID, db: Session) -> int:
    count = (
        db.query(func.count(Lead.id))
        .filter(Lead.provider_id == provider_id)
        .scalar()
        or 0
    )
    return int(count)


def get_city_leads_count(city_id: int, db: Session) -> int:
    count = (
        db.query(func.count(Lead.id))
        .filter(Lead.city_id == city_id)
        .scalar()
        or 0
    )
    return int(count)


def _get_public_client_name(client_name: Optional[str]) -> str:
    if client_name and client_name.strip():
        return client_name.strip()
    return "Client"


def get_public_latest_lead_preview(
    provider_id: UUID,
    db: Session,
) -> Optional[Dict[str, Any]]:
    result = (
        db.query(
            Lead,
            User.name.label("client_name"),
            Location.city.label("city_name"),
        )
        .outerjoin(User, Lead.client_id == User.id)
        .join(Location, Lead.city_id == Location.id)
        .filter(Lead.provider_id == provider_id)
        .order_by(Lead.created_at.desc())
        .first()
    )

    if not result:
        return None

    lead = result[0]
    client_name = result[1]
    city_name = result[2]

    return {
        "client_name": _get_public_client_name(client_name),
        "city_name": city_name,
        "created_at": lead.created_at,
        "client_image_url": None,
    }


from apps.api.config import settings
UPLOAD_BASE = Path(settings.UPLOADS_DIR) / "provider_images"


def get_static_files_base_url() -> str:
    """Get the base URL for static files, supporting both local and cloud storage."""
    from apps.api.config import settings
    return settings.STATIC_FILES_BASE_URL


def save_provider_image(provider_id: UUID, content: bytes, content_type: str, base_url: str | None = None) -> str:
    """Save and optimize image to local filesystem. Returns full URL.
    Converts all images to WebP format with max 1200px resolution and 85% quality.
    
    Args:
        provider_id: Provider UUID
        content: Image bytes
        content_type: MIME type from upload
        base_url: Optional base URL (defaults to settings.STATIC_FILES_BASE_URL)
    
    TODO: Replace with S3/R2 upload when migrating cloud storage."""
    UPLOAD_BASE.mkdir(parents=True, exist_ok=True)
    
    # Open image from bytes
    img = Image.open(io.BytesIO(content))
    
    # Convert RGBA to RGB if necessary (WebP supports RGBA but we want consistency)
    if img.mode in ('RGBA', 'LA', 'P'):
        img = img.convert('RGB')
    
    # Resize if larger than 1200px on the longest side (maintain aspect ratio)
    max_dimension = 1200
    width, height = img.size
    if max(width, height) > max_dimension:
        if width > height:
            new_width = max_dimension
            new_height = int(height * (max_dimension / width))
        else:
            new_height = max_dimension
            new_width = int(width * (max_dimension / height))
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Save as WebP with 85% quality
    filename = f"{provider_id}.webp"
    filepath = UPLOAD_BASE / filename
    img.save(filepath, 'WEBP', quality=85, method=6)
    
    # Use provided base_url, or fall back to settings
    if base_url is None:
        from apps.api.config import settings
        base_url = settings.STATIC_FILES_BASE_URL
    
    # Return full URL
    return f"{base_url.rstrip('/')}/static/provider_images/{filename}"


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
    from sqlalchemy import text
    
    for loc in locations:
        # Use ON CONFLICT DO NOTHING to handle race conditions gracefully
        # This handles both primary key conflicts and unique constraint conflicts
        db.execute(
            text("""
            INSERT INTO provider_cities (provider_id, city_id)
            VALUES (:provider_id, :city_id)
            ON CONFLICT DO NOTHING
            """),
            {"provider_id": str(provider_id), "city_id": loc.id}
        )


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

    from sqlalchemy import text
    
    for loc in locations:
        # Use ON CONFLICT (service_id, city_id) DO NOTHING to handle race conditions gracefully
        # This only skips duplicates of the unique constraint, not primary key sequence conflicts
        db.execute(
            text("""
            INSERT INTO service_cities (service_id, city_id)
            VALUES (:service_id, :city_id)
            ON CONFLICT (service_id, city_id) DO NOTHING
            """),
            {"service_id": str(service.id), "city_id": loc.id}
        )

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


def resolve_provider_slug_safe(
    provider_slug: str,
    db: Session,
    max_depth: int = 5
) -> tuple[Optional[Provider], Optional[str]]:
    """Resolve slug with loop prevention."""
    visited_slugs = set()
    current_slug = provider_slug
    original_redirect_slug = None
    
    for _ in range(max_depth):
        if current_slug in visited_slugs:
            return None, None  # Loop detected
        
        visited_slugs.add(current_slug)
        provider, redirect_slug = resolve_provider_slug(current_slug, db)
        
        if redirect_slug:
            if original_redirect_slug is None:
                original_redirect_slug = redirect_slug  # Store the original slug that redirected
            current_slug = provider.slug  # Use the new slug for next iteration
        else:
            return provider, original_redirect_slug
    
    return None, None  # Max depth reached


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
        # Автоматично проверяваме дали е в онбординг (игнорираме frontend параметъра)
        is_complete, _ = check_onboarding_complete(db, provider.id)
        is_actually_onboarding = not is_complete
        
        # Проверка за лимит САМО ако не е в онбординг
        if provider.slug_change_count >= MAX_SLUG_CHANGES and not is_actually_onboarding:
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
        
        # Увеличаваме брояча САМО ако не е в онбординг
        if old_slug and old_slug.strip() and not is_actually_onboarding:
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

    contacted_leads = (
        db.query(func.count(Lead.id))
        .filter(
            Lead.provider_id == provider.id,
            Lead.status == "contacted",
        )
        .scalar()
        or 0
    )

    return {
        "total_leads": total_leads,
        "new_leads": new_leads,
        "contacted_leads": contacted_leads,
        "rating": get_provider_rating(provider.id, db),
        "verified": provider.verified,
        "availability_status": provider.availability_status,
    }


# ---------------------------------------------------------------------------
# Leads list
# ---------------------------------------------------------------------------

def get_provider_leads(
    provider: Provider,
    db: Session,
    status: str = "all",
    period: str = "all",
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
) -> dict:
    """Return filtered leads for the provider with total count.

    Args:
        provider: The provider to fetch leads for
        db: Database session
        status: Filter by status (all, new, contacted, done, rejected)
              Note: 'new' maps to DB status 'created'
        period: Preset period filter (all, 7, 30, 90 days)
        date_from: Custom start date (YYYY-MM-DD), overrides period if set
        date_to: Custom end date (YYYY-MM-DD), overrides period if set
        search: Search query for case-insensitive partial match across
                client_name, client_email, client_phone, description, provider_notes
        limit: Maximum number of leads to return

    Returns:
        Dict with 'leads' list and 'total' count
    """
    from datetime import datetime, timedelta
    from sqlalchemy import or_

    query = db.query(Lead).outerjoin(User, Lead.client_id == User.id).filter(Lead.provider_id == provider.id)

    # Status filter
    if status == "new":
        query = query.filter(Lead.status == "created")
    elif status != "all" and status in ("contacted", "done", "rejected"):
        query = query.filter(Lead.status == status)

    # Date filter: custom range takes priority over period
    if date_from or date_to:
        if date_from:
            try:
                from_dt = datetime.strptime(date_from, "%Y-%m-%d")
                query = query.filter(Lead.created_at >= from_dt)
            except ValueError:
                pass  # Invalid date format, ignore
        if date_to:
            try:
                to_dt = datetime.strptime(date_to, "%Y-%m-%d")
                # Add one day to include the full end date
                to_dt = to_dt + timedelta(days=1)
                query = query.filter(Lead.created_at < to_dt)
            except ValueError:
                pass  # Invalid date format, ignore
    elif period != "all" and period in ("7", "30", "90"):
        days = int(period)
        since = datetime.utcnow() - timedelta(days=days)
        query = query.filter(Lead.created_at >= since)

    # Search filter: case-insensitive partial match across 5 fields
    if search and search.strip():
        search_pattern = f"%{search.strip()}%"
        query = query.filter(
            or_(
                User.name.ilike(search_pattern),
                User.email.ilike(search_pattern),
                User.phone.ilike(search_pattern),
                Lead.description.ilike(search_pattern),
                Lead.provider_notes.ilike(search_pattern),
            )
        )

    # Get total count before applying limit
    total = query.count()

    # Apply ordering and limit
    leads = query.order_by(Lead.created_at.desc()).limit(limit).all()

    result = []
    for lead in leads:
        result.append(
            {
                "id": str(lead.id),
                "phone": lead.phone,
                "description": lead.description,
                "status": lead.status,
                "source": lead.source,
                "provider_notes": lead.provider_notes,
                "created_at": lead.created_at.isoformat(),
            }
        )
    return {"leads": result, "total": total}


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


def load_nevumo_logo() -> Optional[Image.Image]:
    """Load Nevumo logo from web app public directory."""
    try:
        # Path to the logo in the web app public directory
        logo_path = Path(__file__).parent.parent / "web" / "public" / "Nevumo_logo.svg"
        
        # For now, we'll create a simple placeholder logo
        # In production, you might want to convert SVG to PNG beforehand
        logo_size = (60, 60)  # 15-20% of typical QR code size
        logo = Image.new('RGBA', logo_size, (255, 102, 0, 255))  # Orange background
        
        # Add a simple "N" text as placeholder
        draw = ImageDraw.Draw(logo)
        try:
            # Try to use an even bolder font for "N" - use Black font variant
            font = ImageFont.truetype("/System/Library/Fonts/Arial Black.ttf", 55)
            text_bbox = draw.textbbox((0, 0), "N", font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Perfect centering both horizontally and vertically in 60x60 square
            # Fix vertical centering by using the actual text bounds properly
            text_x = (logo_size[0] - text_width) // 2
            text_y = (logo_size[1] - text_height) // 2 - text_bbox[1]  # Adjust for proper vertical center
            
            draw.text((text_x, text_y), "N", fill="white", font=font)
        except:
            # Fallback to Bold if Black not available
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 55)
                text_bbox = draw.textbbox((0, 0), "N", font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                text_x = (logo_size[0] - text_width) // 2
                text_y = (logo_size[1] - text_height) // 2 - text_bbox[1]  # Adjust for proper vertical center
                draw.text((text_x, text_y), "N", fill="white", font=font)
            except:
                # Final fallback to default font
                try:
                    font = ImageFont.load_default()
                    text_bbox = draw.textbbox((0, 0), "N", font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]
                    text_x = (logo_size[0] - text_width) // 2
                    text_y = (logo_size[1] - text_height) // 2 - text_bbox[1]  # Adjust for proper vertical center
                    draw.text((text_x, text_y), "N", fill="white", font=font)
                except:
                    # If font loading fails, just use it orange square
                    pass
            
        return logo
    except Exception as e:
        print(f"Warning: Could not load Nevumo logo: {e}")
        return None


def add_logo_to_qr(qr_img: Image.Image, logo: Image.Image) -> Image.Image:
    """Add logo to center of QR code with white padding."""
    # Calculate logo size (15-20% of QR code size)
    qr_width, qr_height = qr_img.size
    logo_size = min(qr_width, qr_height) // 6  # ~16.7%
    
    # Resize logo
    logo_resized = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    # Create white padding around logo
    padding = logo_size // 10  # 10% padding
    padded_size = logo_size + 2 * padding
    padded_logo = Image.new('RGBA', (padded_size, padded_size), (255, 255, 255, 255))
    
    # Paste logo in center of white padding
    logo_x = (padded_size - logo_size) // 2
    logo_y = (padded_size - logo_size) // 2
    padded_logo.paste(logo_resized, (logo_x, logo_y))
    
    # Calculate position to center the logo on QR code
    logo_x = (qr_width - padded_size) // 2
    logo_y = (qr_height - padded_size) // 2
    
    # Create a copy of QR image and paste logo
    qr_with_logo = qr_img.convert('RGBA')
    qr_with_logo.paste(padded_logo, (logo_x, logo_y), padded_logo)
    
    return qr_with_logo.convert('RGB')


def add_text_to_qr(qr_img: Image.Image, business_name: str, service_name: str, slogan: str) -> Image.Image:
    """Add text below QR code."""
    # Create space for text and padding
    qr_width, qr_height = qr_img.size
    padding = 24  # 24px padding around QR
    text_height = 140  # Space for larger text (29px + 36px + spacing)
    new_width = qr_width + 2 * padding
    new_height = qr_height + text_height + padding
    
    # Create new image with space for text and padding
    result_img = Image.new('RGB', (new_width, new_height), 'white')
    
    # Paste QR image with padding
    result_img.paste(qr_img, (padding, padding))
    
    # Create drawing context
    draw = ImageDraw.Draw(result_img)
    
    try:
        # Try to load fonts with larger sizes
        font_business = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 29)
        font_slogan = ImageFont.truetype("/System/Library/Fonts/Arial Bold.ttf", 36)
    except:
        # Fallback to default font
        font_business = ImageFont.load_default()
        font_slogan = ImageFont.load_default()
    
    # Add business name and service name (50% larger)
    text_line = f'"{business_name}" - "{service_name}"'
    text_bbox = draw.textbbox((0, 0), text_line, font=font_business)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (new_width - text_width) // 2
    text_y = qr_height + padding + 15  # Position below QR with padding
    
    draw.text((text_x, text_y), text_line, fill="black", font=font_business)
    
    # Add slogan (even larger and bold)
    slogan_bbox = draw.textbbox((0, 0), slogan, font=font_slogan)
    slogan_width = slogan_bbox[2] - slogan_bbox[0]
    slogan_x = (new_width - slogan_width) // 2
    slogan_y = text_y + 55  # Space for 29px business text + padding
    
    draw.text((slogan_x, slogan_y), slogan, fill="black", font=font_slogan)
    
    return result_img


def generate_enhanced_qr_code_base64(
    url: str,
    business_name: str,
    service_name: str,
    language: str = "en",
    db: Optional[Session] = None
) -> str:
    """Generate enhanced QR code with logo and multilingual text."""
    
    # Get localized slogan
    slogan = "Send a request in 30 sec!"  # Default fallback
    if db:
        try:
            # The database key is namespaced
            slogan = resolve_translation(db, "provider_dashboard.qr_slogan_submit_request", language)
        except Exception as e:
            print(f"Warning: Could not resolve translation: {e}")
    
    # Generate QR code with high error correction for logo
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction for logo
        box_size=12,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Add logo if available
    logo = load_nevumo_logo()
    if logo:
        qr_img = add_logo_to_qr(qr_img, logo)
    
    # Add text
    final_img = add_text_to_qr(qr_img, business_name, service_name, slogan)
    
    # Convert to base64
    buffer = io.BytesIO()
    final_img.save(buffer, format="PNG", quality=95)
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def generate_enhanced_qr_code_svg(
    url: str,
    business_name: str,
    service_name: str,
    language: str = "en",
    db: Optional[Session] = None,
) -> str:
    """
    Генерира print & web-ready SVG QR код.
    - ECC Level H (30% корекция) — задължително при централно лого
    - border=4 (ISO 18004 тиха зона)
    - Оптимизиран SVG: хоризонтални runs → <rect> групи (5-10x по-малък файл)
    - Бяла подложка под логото
    - Слоган от превода (qr_slogan_submit_request)
    """
    import html
    import qrcode

    # --- Слоган от превода ---
    slogan = "Пусни заявка за 30 сек!"  # fallback
    if db:
        try:
            # The database key is namespaced
            slogan = resolve_translation(db, "provider_dashboard.qr_slogan_submit_request", language)
        except Exception:
            pass

    # --- Escape за XML ---
    safe_business = html.escape(business_name or "Business")
    safe_service  = html.escape(service_name or "")
    safe_slogan   = html.escape(slogan)

    # --- QR генериране ---
    # ECC_H = 30% корекция — задължително при лого в центъра
    # border=4 = ISO 18004 тиха зона (вградена в матрицата)
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # --- Матрица → оптимизирани <rect> (хоризонтални runs) ---
    matrix    = qr.get_matrix()           # list[list[bool]], включва border
    n_modules = len(matrix)               # брой редове = брой колони

    canvas_pad = 20
    qr_size    = 360
    module_px  = qr_size / n_modules      # размер на един модул в px

    rects: list[str] = []
    for row_idx, row in enumerate(matrix):
        y        = canvas_pad + row_idx * module_px
        h        = module_px
        run_start: Optional[int] = None
        run_len  = 0

        for col_idx, dark in enumerate(row):
            if dark:
                if run_start is None:
                    run_start = col_idx
                    run_len   = 1
                else:
                    run_len  += 1
            else:
                if run_start is not None:
                    x = canvas_pad + run_start * module_px
                    w = run_len * module_px
                    rects.append(
                        f'<rect x="{x:.3f}" y="{y:.3f}" '
                        f'width="{w:.3f}" height="{h:.3f}"/>'
                    )
                    run_start = None
                    run_len   = 0

        # Затвори последния run в реда
        if run_start is not None:
            x = canvas_pad + run_start * module_px
            w = run_len * module_px
            rects.append(
                f'<rect x="{x:.3f}" y="{y:.3f}" '
                f'width="{w:.3f}" height="{h:.3f}"/>'
            )

    qr_layer = f'<g fill="black">{"".join(rects)}</g>'

    # --- Logo (15% от QR + бяла подложка) ---
    cx       = canvas_pad + qr_size // 2   # 200
    cy       = canvas_pad + qr_size // 2   # 200
    logo_sz  = int(qr_size * 0.15)         # 54px
    logo_pad = 8
    white_sz = logo_sz + 2 * logo_pad      # 70px
    wx       = cx - white_sz // 2          # 165
    wy       = cy - white_sz // 2          # 165
    lx       = wx + logo_pad               # 173
    ly       = wy + logo_pad               # 173

    # --- Canvas ---
    svg_w   = qr_size + 2 * canvas_pad     # 400px
    text_y1 = canvas_pad + qr_size + 36    # 416px
    text_y2 = text_y1 + 50                 # 466px
    svg_h   = text_y2 + 52                 # 518px

    if safe_service:
        text_line1 = f'&quot;{safe_business}&quot; - &quot;{safe_service}&quot;'
    else:
        text_line1 = f'&quot;{safe_business}&quot;'

    return (
        f'<svg width="{svg_w}" height="{svg_h}" '
        f'viewBox="0 0 {svg_w} {svg_h}" '
        f'xmlns="http://www.w3.org/2000/svg">'

        # Бял фон
        f'<rect width="{svg_w}" height="{svg_h}" fill="white"/>'

        # QR слой — оптимизирани хоризонтални rect runs
        + qr_layer +

        # Бяла подложка зад логото
        f'<rect x="{wx}" y="{wy}" width="{white_sz}" height="{white_sz}" fill="white"/>'

        # Оранжев квадрат
        f'<rect x="{lx}" y="{ly}" width="{logo_sz}" height="{logo_sz}" '
        f'rx="9" fill="#FF6600"/>'

        # "N"
        f'<text x="{cx}" y="{cy}" '
        f'font-family="Arial Black, Arial, sans-serif" '
        f'font-size="{int(logo_sz * 0.65)}" font-weight="900" '
        f'fill="white" text-anchor="middle" dominant-baseline="central">N</text>'

        # Ред 1 — "business" - "service"
        f'<text x="{cx}" y="{text_y1}" '
        f'font-family="Arial, Helvetica, sans-serif" font-size="17" '
        f'fill="#333333" text-anchor="middle">{text_line1}</text>'

        # Ред 2 — слоган
        f'<text x="{cx}" y="{text_y2}" '
        f'font-family="Arial Black, Arial, sans-serif" font-size="26" '
        f'font-weight="900" fill="black" text-anchor="middle">{safe_slogan}</text>'

        f'</svg>'
    )

    # Сглобяваме всичко в един финален низ
    return header + qr_group + logo_group + text_group + footer


# ---------------------------------------------------------------------------
# Retro Matching
# ---------------------------------------------------------------------------


def retro_match_provider(
    provider_id: UUID,
    category_id: int,
    city_ids: List[int],
    db: Session
) -> int:
    """Create retroactive matches for a provider's first service.
    
    Finds existing leads that match the provider's new service category and cities,
    creates LeadMatch records, and updates lead statuses.
    
    Args:
        provider_id: Provider UUID to create matches for
        category_id: Service category ID to match against
        city_ids: List of city IDs where the provider offers the service
        db: Database session (must be the same session used by caller)
        
    Returns:
        Number of newly created matches (int)
    """
    from sqlalchemy import and_, not_, or_
    
    # Find matching leads that:
    # - Have the same category_id
    # - Are in one of the provider's cities
    # - Have status 'created' or 'pending_match'
    # - Are not already matched to this provider
    matching_leads = (
        db.query(Lead.id)
        .filter(
            and_(
                Lead.category_id == category_id,
                Lead.city_id.in_(city_ids),
                Lead.status.in_(["created", "pending_match"]),
                not_(
                    Lead.id.in_(
                        db.query(LeadMatch.lead_id)
                        .filter(LeadMatch.provider_id == provider_id)
                    )
                )
            )
        )
        .all()
    )
    
    if not matching_leads:
        return 0
    
    # Extract lead IDs
    lead_ids = [lead.id for lead in matching_leads]
    
    # Bulk insert LeadMatch records
    lead_matches_to_create = [
        {"lead_id": lead_id, "provider_id": provider_id, "status": "invited"}
        for lead_id in lead_ids
    ]
    
    db.bulk_insert_mappings(LeadMatch, lead_matches_to_create)
    
    # Update lead statuses to 'pending_match' if they are still 'created'
    (
        db.query(Lead)
        .filter(
            and_(
                Lead.id.in_(lead_ids),
                Lead.status == "created"
            )
        )
        .update({"status": "pending_match"}, synchronize_session=False)
    )
    
    db.commit()
    return len(lead_ids)


# ---------------------------------------------------------------------------
# Claim functionality
# ---------------------------------------------------------------------------


def generate_claim_token(db: Session) -> str:
    """Generate a unique claim token."""
    for attempt in range(5):
        token = secrets.token_urlsafe(32)
        existing = db.query(Provider).filter(Provider.claim_token == token).first()
        if not existing:
            return token
    raise RuntimeError("Failed to generate unique claim token after 5 attempts")


def claim_provider(claim_token: str, user: "User", db: Session) -> Provider:
    """Claim a provider using a claim token."""
    provider = db.query(Provider).filter(Provider.claim_token == claim_token).first()
    if not provider:
        from fastapi import HTTPException
        raise HTTPException(
            404, 
            detail={"code": "CLAIM_TOKEN_NOT_FOUND", "message": "Claim token not found"}
        )
    
    if provider.is_claimed:
        from fastapi import HTTPException
        raise HTTPException(
            409, 
            detail={"code": "ALREADY_CLAIMED", "message": "This profile has already been claimed"}
        )
    
    existing_user_provider = db.query(Provider).filter(Provider.user_id == user.id).first()
    if existing_user_provider:
        from fastapi import HTTPException
        raise HTTPException(
            409, 
            detail={"code": "USER_ALREADY_HAS_PROVIDER", "message": "Your account already has a provider profile"}
        )
    
    provider.user_id = user.id
    provider.is_claimed = True
    provider.claim_token = None
    db.commit()
    db.refresh(provider)
    return provider


def get_provider_by_claim_token(token: str, db: Session) -> Optional[Provider]:
    """Get provider by claim token if not claimed."""
    return db.query(Provider).filter(
        Provider.claim_token == token, 
        Provider.is_claimed == False
    ).first()
