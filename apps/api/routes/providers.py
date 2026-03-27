import json
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import redis as redis_lib

from dependencies import get_db, get_redis
from exceptions import CATEGORY_NOT_FOUND, CITY_NOT_FOUND, PROVIDER_NOT_FOUND
from i18n import fetch_translations
from models import Provider, Service, Category, Location, ProviderCity
from schemas import (
    ProviderListItem,
    ProviderListResponse,
    ProviderDetail,
    ProviderDetailResponse,
    ServiceOut,
)
from services.provider_service import (
    get_provider_rating,
    get_provider_jobs_completed,
    get_provider_review_count,
)

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


@router.get("/providers/{provider_slug}", response_model=ProviderDetailResponse)
async def get_provider(
    provider_slug: str,
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
) -> ProviderDetailResponse:
    provider = db.query(Provider).filter(Provider.slug == provider_slug).first()
    if not provider:
        raise PROVIDER_NOT_FOUND

    # Calculate dynamic stats
    rating = get_provider_rating(provider.id, db)
    jobs_completed = get_provider_jobs_completed(provider.id, db)
    review_count = get_provider_review_count(provider.id, db)

    # Get widget translations
    all_translations = fetch_translations(db, lang)
    widget_keys = [
        'verified_label', 'rating_label', 'jobs_label', 'phone_label',
        'phone_placeholder', 'notes_label', 'notes_placeholder',
        'response_time', 'button_text', 'disclaimer', 'success_title',
        'success_message', 'new_request_button'
    ]
    translations = {k: all_translations.get(k, k) for k in widget_keys}

    services = db.query(Service).filter(Service.provider_id == provider.id).all()

    service_items = []
    for s in services:
        cat = db.query(Category).filter(Category.id == s.category_id).first()
        service_items.append(
            ServiceOut(
                id=s.id,
                title=s.title,
                description=s.description,
                price_type=s.price_type,
                base_price=s.base_price,
                category_slug=cat.slug if cat else None,
            )
        )

    detail = ProviderDetail(
        id=provider.id,
        business_name=provider.business_name,
        description=provider.description,
        slug=provider.slug,
        profile_image_url=provider.profile_image_url,
        rating=rating,
        verified=provider.verified,
        availability_status=provider.availability_status,
        created_at=provider.created_at,
        services=service_items,
        jobs_completed=jobs_completed,
        review_count=review_count,
        translations=translations,
    )

    return ProviderDetailResponse(data=detail)
