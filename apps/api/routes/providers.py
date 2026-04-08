import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import redis as redis_lib

from config import settings
from dependencies import get_db, get_redis
from exceptions import CATEGORY_NOT_FOUND, CITY_NOT_FOUND, PROVIDER_NOT_FOUND
from models import Provider, Service, Category, Location, ProviderCity, CategoryTranslation, ProviderTranslation
from schemas import (
    ProviderListItem,
    ProviderListResponse,
    ProviderDetail,
    ProviderDetailResponse,
    ServiceOut,
    LatestLeadPreview,
    LatestReviewPreview,
)
from services.provider_service import (
    get_city_leads_count,
    get_provider_leads_received,
    get_public_latest_lead_preview,
    get_provider_rating,
    get_provider_jobs_completed,
    get_provider_review_count,
    resolve_provider_slug_safe,
    get_provider_by_claim_token,
)
from services.review_service import get_public_latest_review_preview


def get_widget_translations(lang: str, db: Session) -> dict:
    from models import Translation
    
    supported_langs = ["bg","cs","da","de","el","en","es","et","fi","fr","ga","hr","hu","is","it","lb","lt","lv","mk","mt","nl","no","pl","pt","pt-PT","ro","ru","sk","sl","sq","sr","sv","tr","uk"]
    
    # Normalize unsupported langs to 'en'
    if lang not in supported_langs:
        lang = "en"
    
    # Query DB for widget namespace
    rows = db.query(Translation).filter(
        Translation.lang == lang,
        Translation.key.like("widget.%")
    ).all()
    
    # If no rows found, fallback to English
    if not rows:
        rows = db.query(Translation).filter(
            Translation.lang == "en",
            Translation.key.like("widget.%")
        ).all()
    
    # Strip "widget." prefix from keys
    return {row.key.replace("widget.", "", 1): row.value for row in rows}


router = APIRouter(prefix="/api/v1", tags=["providers"])


@router.get("/providers", response_model=ProviderListResponse)
async def list_providers(
    category_slug: str = Query(...),
    city_slug: str = Query(...),
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> ProviderListResponse:
    cache_key = f"providers:{category_slug}:{city_slug}"

    if redis_client:
        cached = redis_client.get(cache_key)
        if cached:
            items = json.loads(cached)
            return ProviderListResponse(data=[ProviderListItem(**i) for i in items])

    category = db.query(Category).filter(Category.slug == category_slug).first()
    if not category:
        raise CATEGORY_NOT_FOUND

    location = db.query(Location).filter(Location.slug == city_slug).first()
    if not location:
        raise CITY_NOT_FOUND

    providers = (
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

    data = [
        ProviderListItem(
            id=p.id,
            business_name=p.business_name,
            rating=p.rating,
            verified=p.verified,
            slug=p.slug,
        )
        for p in providers
    ]

    if redis_client and data:
        redis_client.setex(
            cache_key,
            600,
            json.dumps([d.model_dump(mode="json") for d in data]),
        )

    return ProviderListResponse(data=data)


@router.get("/providers/by-claim-token/{token}")
async def get_provider_by_claim_token_endpoint(
    token: str,
    db: Session = Depends(get_db),
) -> dict:
    """Get provider by claim token (public endpoint)."""
    provider = get_provider_by_claim_token(token, db)
    if not provider:
        return {
            "success": False,
            "error": {
                "code": "NOT_FOUND", 
                "message": "Token not found or already claimed"
            }
        }
    
    # Get first city name
    first_city_row = (
        db.query(ProviderCity)
        .filter(ProviderCity.provider_id == provider.id)
        .first()
    )
    city_name = None
    if first_city_row:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        city_name = city.city if city else None
    
    # Get first service category slug
    first_service = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .first()
    )
    category_slug = None
    if first_service:
        category = db.query(Category).filter(Category.id == first_service.category_id).first()
        category_slug = category.slug if category else None
    
    return {
        "success": True,
        "data": {
            "business_name": provider.business_name,
            "slug": provider.slug,
            "is_claimed": provider.is_claimed,
            "city_name": city_name,
            "category_slug": category_slug
        }
    }


@router.get("/providers/{provider_slug}", response_model=ProviderDetailResponse)
async def get_provider(
    provider_slug: str,
    lang: str = Query("en", min_length=2, max_length=5),
    city_slug: Optional[str] = Query(None),
    db: Session = Depends(get_db),
) -> ProviderDetailResponse:
    # Use safe resolution to prevent redirect loops
    provider, redirect_slug = resolve_provider_slug_safe(provider_slug, db)
    
    # If redirect found, return 301 redirect to new URL
    if redirect_slug:
        full_url = f"{settings.APP_URL.rstrip('/')}/providers/{provider.slug}"
        return RedirectResponse(url=full_url, status_code=301)
    
    # If no provider found, raise 404
    if not provider:
        raise PROVIDER_NOT_FOUND

    # Calculate dynamic stats
    rating = get_provider_rating(provider.id, db)
    jobs_completed = get_provider_jobs_completed(provider.id, db)
    review_count = get_provider_review_count(provider.id, db)
    leads_received = get_provider_leads_received(provider.id, db)
    latest_lead_preview_data = get_public_latest_lead_preview(provider.id, db)
    city_leads = 0
    if city_slug:
        location = db.query(Location).filter(Location.slug == city_slug).first()
        if location:
            city_leads = get_city_leads_count(location.id, db)

    # Get widget translations from DB
    translations = get_widget_translations(lang, db)

    services = db.query(Service).filter(Service.provider_id == provider.id).all()

    service_items = []
    for s in services:
        cat = db.query(Category).filter(Category.id == s.category_id).first()
        
        # For scraped providers, localize service title from CategoryTranslation
        service_title = s.title
        if provider.data_source == "scraped":
            # Try requested language first
            ct = db.query(CategoryTranslation).filter(
                CategoryTranslation.category_id == s.category_id,
                CategoryTranslation.lang == lang
            ).first()
            if ct:
                service_title = ct.name
            else:
                # Fall back to English
                ct_en = db.query(CategoryTranslation).filter(
                    CategoryTranslation.category_id == s.category_id,
                    CategoryTranslation.lang == "en"
                ).first()
                if ct_en:
                    service_title = ct_en.name
        
        service_items.append(
            ServiceOut(
                id=s.id,
                title=service_title,
                description=s.description,
                price_type=s.price_type,
                base_price=s.base_price,
                category_slug=cat.slug if cat else None,
                currency=s.currency,
            )
        )

    # Get latest review for social proof widget (optional, only if exists)
    latest_review_data = get_public_latest_review_preview(provider.id, db)
    latest_review = None
    if latest_review_data:
        latest_review = LatestReviewPreview(
            client_name=latest_review_data["client_name"],
            rating=latest_review_data["rating"],
            comment_preview=latest_review_data["comment_preview"],
            created_at=latest_review_data["created_at"],
        )

    latest_lead_preview = None
    if latest_lead_preview_data:
        latest_lead_preview = LatestLeadPreview(
            client_name=latest_lead_preview_data["client_name"],
            city_name=latest_lead_preview_data["city_name"],
            created_at=latest_lead_preview_data["created_at"],
            client_image_url=latest_lead_preview_data["client_image_url"],
        )

    # Get translated description if available
    translation = db.query(ProviderTranslation).filter_by(
        provider_id=provider.id,
        field="description",
        lang=lang
    ).first()

    if translation:
        description = translation.value
    else:
        description = provider.description

    detail = ProviderDetail(
        id=provider.id,
        business_name=provider.business_name,
        description=description,
        slug=provider.slug,
        slug_change_count=provider.slug_change_count,
        profile_image_url=provider.profile_image_url,
        rating=rating,
        verified=provider.verified,
        availability_status=provider.availability_status,
        created_at=provider.created_at,
        is_claimed=provider.is_claimed or False,
        services=service_items,
        jobs_completed=jobs_completed,
        review_count=review_count,
        leads_received=leads_received,
        city_leads=city_leads,
        translations=translations,
        latest_lead_preview=latest_lead_preview,
        latest_review=latest_review,
    )

    return ProviderDetailResponse(data=detail)


@router.get("/providers/resolve/{slug}")
async def resolve_slug(
    slug: str,
    db: Session = Depends(get_db),
) -> dict:
    """Resolve a slug and check if it redirects to another slug."""
    provider, redirect_slug = resolve_provider_slug_safe(slug, db)
    
    if provider and redirect_slug:
        return {"found": True, "slug": provider.slug, "redirected": True, "from_slug": redirect_slug}
    elif provider:
        return {"found": True, "slug": provider.slug, "redirected": False}
    else:
        return {"found": False, "slug": None, "redirected": False}
