import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, select
from sqlalchemy.exc import IntegrityError
import redis as redis_lib

from apps.api.config import settings
from apps.api.dependencies import get_db, get_redis, get_current_user, get_optional_current_user
from apps.api.exceptions import CATEGORY_NOT_FOUND, CITY_NOT_FOUND, PROVIDER_NOT_FOUND
from apps.api.models import Provider, Service, Category, Location, ProviderCity, CategoryTranslation, ProviderTranslation, LocationTranslation, Lead, Review, User, CitySearchVolume, PendingClaimVerification
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
    calculate_verification_level,
    get_city_leads_count,
    get_provider_leads_received,
    get_public_latest_lead_preview,
    get_provider_rating,
    get_provider_jobs_completed,
    get_provider_review_count,
    resolve_provider_slug_safe,
    get_provider_by_claim_token,
    get_provider_gallery,
    get_providers_ratings_batch,
    get_providers_review_counts_batch,
)
from apps.api.services.review_service import get_public_latest_review_preview, get_provider_reviews
from apps.api.services.email_service import email_service
from apps.api.services.auth_service import get_or_create_claim_user, create_jwt


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
    review_count = get_providers_review_counts_batch(provider_ids, db) if provider_ids else {}

    # Batch query for rating (calculated from reviews)
    ratings = get_providers_ratings_batch(provider_ids, db) if provider_ids else {}

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
                rating=ratings.get(p.id, 0.0),
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
    lang: str = Query(default="en"),
    db: Session = Depends(get_db),
) -> dict:
    """Get provider by claim token (public endpoint)."""
    provider = get_provider_by_claim_token(token, db)
    if not provider:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "Provider not found"}
        )

    # Get first city slug and localized city_name
    first_city_row = (
        db.query(ProviderCity)
        .filter(ProviderCity.provider_id == provider.id)
        .first()
    )
    city_slug = None
    city_name = None
    if first_city_row:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        if city:
            city_slug = city.slug
            # Try to get localized city_name
            city_translation = db.query(LocationTranslation).filter(
                LocationTranslation.location_id == city.id,
                LocationTranslation.lang == lang
            ).first()
            if city_translation:
                city_name = city_translation.city_name
            else:
                # Fallback to city_slug if translation not found
                city_name = city_slug

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

    # Get claimed_count in the same city (social proof)
    claimed_count = 0
    if first_city_row:
        try:
            claimed_count = db.query(func.count(Provider.id)).join(
                ProviderCity, Provider.id == ProviderCity.provider_id
            ).filter(
                ProviderCity.city_id == first_city_row.city_id,
                Provider.is_claimed == True
            ).scalar() or 0
        except Exception:
            claimed_count = 0

    return {
        "id": str(provider.id),
        "business_name": provider.business_name,
        "category_slug": category_slug,
        "city_slug": city_slug,
        "city_name": city_name,
        "claimed_count": claimed_count,
        "is_claimed": provider.is_claimed,
        "data_source": provider.data_source
    }


@router.get("/providers/claim/{token}")
async def get_claim_preview(
    token: str,
    db: Session = Depends(get_db),
) -> dict:
    """Public preview of an unclaimed provider profile (no auth required)."""
    provider = db.query(Provider).filter(
        Provider.claim_token == token,
        Provider.is_claimed == False
    ).first()
    
    if not provider:
        raise HTTPException(
            status_code=404,
            detail={"code": "TOKEN_NOT_FOUND", "message": "Claim token not found or already used"}
        )
    
    # Get first city name
    first_city_row = (
        db.query(ProviderCity)
        .filter(ProviderCity.provider_id == provider.id)
        .first()
    )
    city_name = None
    if first_city_row:
        city = db.query(Location).filter(Location.id == first_city_row.city_id).first()
        if city:
            city_name = city.city_en if city.city_en else city.city
    
    # Get first category name
    first_service = (
        db.query(Service)
        .filter(Service.provider_id == provider.id)
        .first()
    )
    category_name = None
    if first_service:
        category = db.query(Category).filter(Category.id == first_service.category_id).first()
        if category:
            category_name = category.name
    
    return {
        "success": True,
        "data": {
            "business_name": provider.business_name,
            "slug": provider.slug,
            "city": city_name,
            "category": category_name,
            "data_source": provider.data_source
        }
    }


@router.post("/providers/claim/{token}")
async def claim_provider(
    token: str,
    lang: str = Query(default="pl"),
    source: str = Query(default="email"),
    optional_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """
    Claim a provider profile via magic-link flow.
    No JWT required — the claim token IS the proof of identity.
    Auto-authenticates the provider and returns a JWT.

    Also handles returning providers (already claimed):
    re-authenticates the owner and returns a fresh JWT.
    """
    logger = logging.getLogger(__name__)

    # Find provider by claim token (regardless of is_claimed status)
    provider = db.query(Provider).filter(
        Provider.claim_token == token
    ).first()

    if not provider:
        raise HTTPException(
            status_code=404,
            detail={"code": "NOT_FOUND", "message": "Provider not found"}
        )

    # ── BANNER FLOW: public token, must verify business ownership ─────────────
    if source == "banner":
        if not provider.scraped_email:
            raise HTTPException(
                status_code=422,
                detail={"code": "NO_EMAIL", "message": "No scraped email for verification"}
            )
        if provider.is_claimed:
            raise HTTPException(
                status_code=409,
                detail={"code": "ALREADY_CLAIMED", "message": "Provider already claimed"}
            )

        # Generate 6-digit code and send to scraped_email
        import secrets
        code = str(secrets.randbelow(1000000)).zfill(6)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=24)

        # Invalidate any previous pending verifications for this token (user_id=None for banner flow)
        db.query(PendingClaimVerification).filter(
            PendingClaimVerification.claim_token == token,
            PendingClaimVerification.user_id == None,
            PendingClaimVerification.used == False,
        ).delete()

        pending = PendingClaimVerification(
            claim_token=token,
            user_id=None,
            code=code,
            expires_at=expires_at,
        )
        db.add(pending)
        db.commit()

        email_service.send_claim_verification_email(
            to_email=provider.scraped_email,
            business_name=provider.business_name,
            code=code,
        )

        # Mask the email for display (e.g. business@firm.pl → b****@firm.pl)
        local, domain = provider.scraped_email.rsplit('@', 1)
        mask_len = min(len(local) - 1, 4)
        masked_email = local[0] + ('*' * mask_len) + '@' + domain

        return JSONResponse(
            status_code=202,
            content={
                "status": "verification_required",
                "message": "Verification code sent to business email",
                "sent_to": masked_email
            }
        )

    # ── RETURNING PROVIDER: profile already claimed ──────────────────────
    # Re-authenticate the owner and return a fresh JWT.
    # No emails — they were already sent during the original claim.
    if provider.is_claimed:
        if not provider.user_id:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": "Provider owner not found"}
            )

        owner = db.query(User).filter(User.id == provider.user_id).first()
        if not owner:
            raise HTTPException(
                status_code=404,
                detail={"code": "NOT_FOUND", "message": "Provider owner not found"}
            )

        jwt_token = create_jwt(
            user_id=owner.id,
            email=owner.email,
            role=owner.role,
        )

        return {
            "success": True,
            "jwt_token": jwt_token,
            "user": {
                "id": str(owner.id),
                "email": owner.email,
                "role": owner.role,
            },
            "provider_slug": provider.slug,
            "is_returning": True,
            "is_onboarding_complete": bool(
                provider.description
                and provider.profile_image_url
                and provider.services
            ),
        }

    # ── NEW CLAIM: profile not yet claimed ───────────────────────────────

    # Determine the active user:
    # Use JWT user if present, otherwise auto-create from scraped_email
    if optional_user:
        active_user = optional_user
        jwt_token = create_jwt(
            user_id=active_user.id,
            email=active_user.email,
            role=active_user.role,
        )
    else:
        # scraped_email is guaranteed for email campaign providers
        if not provider.scraped_email:
            raise HTTPException(
                status_code=422,
                detail={"code": "NO_EMAIL", "message": "Cannot auto-authenticate: provider has no scraped email"}
            )
        active_user, jwt_token = get_or_create_claim_user(
            email=provider.scraped_email,
            lang=lang,
            db=db,
        )

    # Check if user already has a provider profile
    existing_provider = db.query(Provider).filter(
        Provider.user_id == active_user.id
    ).first()
    if existing_provider:
        is_draft = (
            existing_provider.slug.startswith("draft") and
            existing_provider.business_name == active_user.email
        )
        if is_draft:
            # Draft created by OAuth registration — delete and proceed with claim
            db.delete(existing_provider)
            db.flush()
        else:
            # User already has a real provider profile on Nevumo.
            # They clicked the outreach email — they're already registered.
            # Delete the scraped stub (it's a duplicate) and send them to
            # their existing real dashboard.
            db.delete(provider)
            db.commit()
            existing_jwt = create_jwt(
                user_id=active_user.id,
                email=active_user.email,
                role=active_user.role,
            )
            return {
                "success": True,
                "jwt_token": existing_jwt,
                "user": {
                    "id": str(active_user.id),
                    "email": active_user.email,
                    "role": active_user.role,
                },
                "provider_slug": existing_provider.slug,
                "is_returning": True,
                "is_onboarding_complete": bool(
                existing_provider.description
                and existing_provider.profile_image_url
                and existing_provider.services
            ),
            }

    # Claim the profile
    provider.is_claimed = True
    provider.user_id = active_user.id
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail={"code": "USER_ALREADY_HAS_PROVIDER", "message": "Your account already has a provider profile"}
        )

    # Send GDPR Art. 14 notification (non-blocking)
    try:
        CATEGORY_LABEL_PL = {
            "cleaning": "sprzątanie",
            "plumbing": "usługi hydrauliczne",
            "massage": "usługi masażu",
        }

        category_slug = None
        if provider.services:
            first_service = provider.services[0]
            category_slug = getattr(first_service, "category_slug", None) or \
                            getattr(getattr(first_service, "category", None), "slug", None)
        category_label = CATEGORY_LABEL_PL.get(category_slug or "", "usługi")

        email_service.send_article14_notification(
            to_email=active_user.email,
            business_name=provider.business_name or "",
            dashboard_link="https://nevumo.com/pl/dashboard",
            nip=None,
            provider_phone=None,
            scraped_email=provider.scraped_email,
            provider_website=None,
            category_label=category_label,
        )
    except Exception as e:
        print(f"[EMAIL_WARNING] {type(e).__name__}: {e}", flush=True)

    # Send welcome email (non-blocking)
    try:
        email_service.send_claim_welcome_email(
            provider_email=active_user.email,
            provider_name=provider.business_name
        )
    except Exception as e:
        logger.warning(
            f"[EMAIL_WARNING] Claim welcome email failed for provider {provider.id}: {e}"
        )

    return {
        "success": True,
        "jwt_token": jwt_token,
        "user": {
            "id": str(active_user.id),
            "email": active_user.email,
            "role": active_user.role,
        },
        "provider_slug": provider.slug,
        "is_returning": False,
        "is_onboarding_complete": False,
    }


@router.post("/providers/claim/{token}/verify")
async def verify_claim_code(
    token: str,
    body: dict,
    lang: str = Query(default="pl"),
    optional_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Verify 6-digit code and complete the claim."""
    code: str = body.get("code", "").strip().replace(" ", "")

    if not code or not code.isdigit() or len(code) != 6:
        raise HTTPException(status_code=400, detail="invalid_code_format")

    # Find valid pending verification (support both user_id=None for banner flow and user_id for non-banner)
    query = db.query(PendingClaimVerification).filter(
        PendingClaimVerification.claim_token == token,
        PendingClaimVerification.code == code,
        PendingClaimVerification.used == False,
        PendingClaimVerification.expires_at > datetime.now(timezone.utc),
    )

    # If user is present, filter by user_id; otherwise look for user_id=None (banner flow)
    if optional_user:
        query = query.filter(PendingClaimVerification.user_id == optional_user.id)
    else:
        query = query.filter(PendingClaimVerification.user_id == None)

    pending = query.first()

    if not pending:
        raise HTTPException(status_code=400, detail="invalid_or_expired_code")

    # Find and claim the provider
    provider = (
        db.query(Provider)
        .filter(Provider.claim_token == token, Provider.is_claimed == False)
        .first()
    )
    if not provider:
        raise HTTPException(status_code=409, detail="already_claimed")

    if not provider.scraped_email:
        raise HTTPException(
            status_code=422,
            detail="NO_EMAIL_FOR_CLAIM"
        )

    # Get or create user from scraped_email
    user, jwt_token = get_or_create_claim_user(
        email=provider.scraped_email,
        lang=lang,
        db=db,
    )

    # Complete the claim
    provider.is_claimed = True
    provider.user_id = user.id
    provider.claim_token = None
    pending.used = True
    db.commit()

    # Send post-claim emails (non-blocking)
    try:
        email_service.send_article14_notification(
            to_email=user.email,
            business_name=provider.business_name or "",
            dashboard_link=f"https://nevumo.com/{lang}/provider/dashboard/profile",
            scraped_email=provider.scraped_email,
        )
    except Exception as exc:
        logger.error("[EMAIL_WARNING] Art.14 after verify failed: %s", exc)

    try:
        email_service.send_claim_welcome_email(
            provider_email=user.email,
            provider_name=provider.business_name or "",
        )
    except Exception as exc:
        logger.error("[EMAIL_WARNING] Welcome email after verify failed: %s", exc)

    return {
        "success": True,
        "token": jwt_token,
        "redirect": f"/{lang}/provider/dashboard/profile"
    }

    return {
        "success": True,
        "provider_slug": provider.slug,
        "business_name": provider.business_name,
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

    # Fetch search volume for the provider's city and category
    search_volume = None
    first_city = db.query(ProviderCity).filter(ProviderCity.provider_id == provider.id).first()
    first_service = db.query(Service).filter(Service.provider_id == provider.id).first()
    
    if first_city and first_service:
        city = db.query(Location).filter(Location.id == first_city.city_id).first()
        category = db.query(Category).filter(Category.id == first_service.category_id).first()
        
        if city and category:
            volume_row = db.execute(
                select(CitySearchVolume).where(
                    CitySearchVolume.city_slug == city.slug,
                    CitySearchVolume.category_slug == category.slug,
                )
            ).scalar_one_or_none()
            
            search_volume = volume_row.search_volume if volume_row else None

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

    # Get reviews for provider (limit to 10 most recent)
    reviews_data = get_provider_reviews(provider.id, db, limit=10)
    reviews = []
    for review_dict in reviews_data.get("items", []):
        reviews.append({
            "id": str(review_dict["id"]),
            "provider_id": str(review_dict["provider_id"]),
            "client_id": str(review_dict["client_id"]),
            "lead_id": str(review_dict["lead_id"]) if review_dict.get("lead_id") else None,
            "rating": review_dict["rating"],
            "comment": review_dict["comment"],
            "created_at": review_dict["created_at"],
            "provider_reply": review_dict.get("provider_reply"),
            "provider_reply_at": review_dict.get("provider_reply_at"),
            "client_name": review_dict.get("client_name"),
        })

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
        claim_token=provider.claim_token if not provider.is_claimed else None,
        search_volume=search_volume,
        services=service_items,
        jobs_completed=jobs_completed,
        review_count=review_count,
        leads_received=leads_received,
        city_leads=city_leads,
        translations=translations,
        latest_lead_preview=latest_lead_preview,
        latest_review=latest_review,
        reviews=reviews,
        gallery=[ProviderImageItem.model_validate(img) for img in get_provider_gallery(db, provider.id)],
        scraped_email=provider.scraped_email,
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
