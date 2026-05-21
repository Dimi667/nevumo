import json
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
import redis as redis_lib

from apps.api.config import settings
from apps.api.dependencies import get_db, get_redis
from apps.api.exceptions import CATEGORY_NOT_FOUND, CITY_NOT_FOUND, PROVIDER_NOT_FOUND
from apps.api.models import Provider, Service, Category, Location, ProviderCity, CategoryTranslation, ProviderTranslation, LocationTranslation, Lead, Review, User
from apps.api.schemas import (
    ProviderListItem,
    ProviderListResponse,
    ProviderDetail,
    ProviderDetailResponse,
    ServiceOut,
    LatestLeadPreview,
    LatestReviewPreview,
    ProviderImageItem,
)
from apps.api.services.provider_service import (
    get_city_leads_count,
    get_provider_leads_received,
    get_public_latest_lead_preview,
    get_provider_rating,
    get_provider_jobs_completed,
    get_provider_review_count,
    resolve_provider_slug_safe,
    get_provider_by_claim_token,
    get_provider_gallery,
)
from apps.api.services.review_service import get_public_latest_review_preview


def get_widget_translations(lang: str, db: Session) -> dict:
    from apps.api.models import Translation
    from apps.api.i18n import get_widget_translation_defaults
    
    supported_langs = ["bg","cs","da","de","el","en","es","et","fi","fr","ga","hr","hu","is","it","lb","lt","lv","mk","mt","nl","no","pl","pt","pt-PT","ro","ru","sk","sl","sq","sr","sv","tr","uk"]
    
    # Normalize unsupported langs to 'en'
    if lang not in supported_langs:
        lang = "en"
    
    # 1. Start with English defaults from hardcoded i18n file
    result = get_widget_translation_defaults(lang)
    
    # 2. Layer 2: Fetch English from database (as base)
    en_rows = db.query(Translation).filter(
        Translation.lang == "en",
        Translation.key.like("widget.%")
    ).all()
    for row in en_rows:
        result[row.key.replace("widget.", "", 1)] = row.value
        
    # 3. Layer 3: Overwrite with target language from database (if not en)
    if lang != "en":
        lang_rows = db.query(Translation).filter(
            Translation.lang == lang,
            Translation.key.like("widget.%")
        ).all()
        for row in lang_rows:
            result[row.key.replace("widget.", "", 1)] = row.value
    
    return result


router = APIRouter(prefix="/api/v1", tags=["providers"])


@router.get("/providers", response_model=ProviderListResponse)
async def list_providers(
    category_slug: str = Query(...),
    city_slug: str = Query(...),
    lang: str = Query("en", min_length=2, max_length=5),
    db: Session = Depends(get_db),
    redis_client: Optional[redis_lib.Redis] = Depends(get_redis),
) -> ProviderListResponse:
    cache_key = f"providers:{category_slug}:{city_slug}:{lang}"

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

    if not providers:
        return ProviderListResponse(data=[])

    provider_ids: list[UUID] = [p.id for p in providers]

    # Batch query for descriptions (from provider_translations)
    descriptions: dict[UUID, str] = {}
    if provider_ids:
        # Try requested language first
        pt_rows = db.query(ProviderTranslation).filter(
            ProviderTranslation.provider_id.in_(provider_ids),
            ProviderTranslation.field == "description",
            ProviderTranslation.lang == lang
        ).all()
        for pt in pt_rows:
            descriptions[pt.provider_id] = pt.value

        # Fallback to English for missing ones
        missing_ids = [pid for pid in provider_ids if pid not in descriptions]
        if missing_ids and lang != "en":
            pt_en_rows = db.query(ProviderTranslation).filter(
                ProviderTranslation.provider_id.in_(missing_ids),
                ProviderTranslation.field == "description",
                ProviderTranslation.lang == "en"
            ).all()
            for pt in pt_en_rows:
                descriptions[pt.provider_id] = pt.value

    # Batch query for jobs_completed (leads with status='done')
    jobs_completed: dict[UUID, int] = {}
    if provider_ids:
        jc_rows = db.query(Lead.provider_id, func.count(Lead.id)).filter(
            Lead.provider_id.in_(provider_ids),
            Lead.status == "done"
        ).group_by(Lead.provider_id).all()
        jobs_completed = {row[0]: row[1] for row in jc_rows}

    # Batch query for leads_received (total leads count)
    leads_received: dict[UUID, int] = {}
    if provider_ids:
        lr_rows = db.query(Lead.provider_id, func.count(Lead.id)).filter(
            Lead.provider_id.in_(provider_ids)
        ).group_by(Lead.provider_id).all()
        leads_received = {row[0]: row[1] for row in lr_rows}

    # Batch query for review_count
    review_count: dict[UUID, int] = {}
    if provider_ids:
        rc_rows = db.query(Review.provider_id, func.count(Review.id)).filter(
            Review.provider_id.in_(provider_ids)
        ).group_by(Review.provider_id).all()
        review_count = {row[0]: row[1] for row in rc_rows}

    # Batch query for latest_lead_preview
    latest_lead_previews: dict[UUID, dict] = {}
    if provider_ids:
        # Subquery to get latest lead created_at per provider
        subq = db.query(
            Lead.provider_id,
            func.max(Lead.created_at).label('max_created_at')
        ).filter(
            Lead.provider_id.in_(provider_ids)
        ).group_by(Lead.provider_id).subquery()

        llp_rows = db.query(
            Lead.provider_id,
            Lead.created_at,
            User.name.label('client_name'),
            Location.city.label('city_name')
        ).join(
            User, Lead.client_id == User.id, isouter=True
        ).join(
            Location, Lead.city_id == Location.id
        ).join(
            subq, and_(
                Lead.provider_id == subq.c.provider_id,
                Lead.created_at == subq.c.max_created_at
            )
        ).all()

        for row in llp_rows:
            latest_lead_previews[row.provider_id] = {
                'created_at': row.created_at,
                'client_name': row.client_name if row.client_name else "Client",
                'city_name': row.city_name
            }

    # Batch query for services (filtered by category_slug)
    services_by_provider: dict[UUID, list[ServiceOut]] = {}
    if provider_ids and category:
        service_rows = db.query(Service).filter(
            Service.provider_id.in_(provider_ids),
            Service.category_id == category.id
        ).all()

        for s in service_rows:
            if s.provider_id not in services_by_provider:
                services_by_provider[s.provider_id] = []

            # Localize service title for scraped providers
            service_title = s.title
            provider = next((p for p in providers if p.id == s.provider_id), None)
            if provider and provider.data_source == "scraped":
                ct = db.query(CategoryTranslation).filter(
                    CategoryTranslation.category_id == s.category_id,
                    CategoryTranslation.lang == lang
                ).first()
                if ct:
                    service_title = ct.name
                else:
                    ct_en = db.query(CategoryTranslation).filter(
                        CategoryTranslation.category_id == s.category_id,
                        CategoryTranslation.lang == "en"
                    ).first()
                    if ct_en:
                        service_title = ct_en.name

            services_by_provider[s.provider_id].append(
                ServiceOut(
                    id=s.id,
                    title=service_title,
                    description=s.description,
                    price_type=s.price_type,
                    base_price=s.base_price,
                    category_slug=category.slug,
                    currency=s.currency,
                )
            )

    # Build response with all batched data
    data = []
    for p in providers:
        latest_lead_preview_obj = None
        if p.id in latest_lead_previews:
            llp_data = latest_lead_previews[p.id]
            latest_lead_preview_obj = LatestLeadPreview(
                client_name=llp_data['client_name'],
                city_name=llp_data['city_name'],
                created_at=llp_data['created_at'],
                client_image_url=None
            )

        data.append(
            ProviderListItem(
                id=p.id,
                business_name=p.business_name,
                rating=p.rating,
                verified=p.verified,
                slug=p.slug,
                profile_image_url=p.profile_image_url,
                description=descriptions.get(p.id),
                jobs_completed=jobs_completed.get(p.id, 0),
                leads_received=leads_received.get(p.id, 0),
                review_count=review_count.get(p.id, 0),
                verification_level=p.verification_level,
                latest_lead_preview=latest_lead_preview_obj,
                services=services_by_provider.get(p.id, []),
            )
        )

    if redis_client and data:
        redis_client.setex(
            cache_key,
            3600,
            json.dumps([d.model_dump(mode="json") for d in data]),
        )

    return ProviderListResponse(data=data)


@router.get("/providers/by-claim-token/{token}")
async def get_provider_by_claim_token_endpoint(
    token: str,
    lang: str = Query("en", min_length=2, max_length=5),
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
    
    # Get first city name with lang-aware lookup
    first_city_row = (
        db.query(ProviderCity)
        .filter(ProviderCity.provider_id == provider.id)
        .first()
    )
    city_name = None
    if first_city_row:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        if city:
            # Get translated city name with fallback
            translation = db.query(LocationTranslation).filter(
                LocationTranslation.location_id == city.id,
                LocationTranslation.lang == lang
            ).first()
            # Fallback: translation -> city_en -> city
            city_name = translation.city_name if translation else (city.city_en if city.city_en else city.city)
    
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
        verification_level=provider.verification_level,
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
        gallery=[ProviderImageItem.model_validate(img) for img in get_provider_gallery(db, provider.id)],
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
