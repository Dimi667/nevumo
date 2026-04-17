"""Provider dashboard endpoints (auth required)."""

from typing import Union, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, UploadFile, status, Response
from sqlalchemy.orm import Session

from apps.api.config import settings
from apps.api.dependencies import get_current_provider, get_db, get_current_user
from apps.api.models import Provider, User
from apps.api.schemas import (
    AddCityRequest,
    ClaimProviderRequest,
    CreateServiceRequest,
    LeadStatusUpdateRequest,
    LeadStatusUpdateResponse,
    LeadProviderNotesUpdateRequest,
    LeadProviderNotesUpdateResponse,
    ProviderDashboardResponse,
    ProviderSlugHistoryResponse,
    ProviderLeadsResponse,
    ProviderProfileUpdateRequest,
    ProviderProfileUpdateResponse,
    QRCodeResponse,
    EnhancedQRCodeRequest,
    EnhancedQRCodeResponse,
    UpdateServiceRequest,
    ErrorResponse,
)
from apps.api.services import provider_service
from apps.api.services.provider_service import (
    add_city,
    add_service,
    build_public_url,
    build_qr_public_url,
    change_lead_status,
    check_onboarding_complete,
    claim_provider,
    delete_service,
    generate_qr_code_base64,
    generate_enhanced_qr_code_base64,
    generate_enhanced_qr_code_svg,
    generate_slug_suggestions,
    is_slug_taken,
    get_analytics,
    get_dashboard_stats,
    get_provider_leads,
    get_provider_profile,
    get_provider_services,
    get_slug_history,
    save_provider_image,
    update_provider_profile,
    update_service,
    validate_slug,
)

router = APIRouter(prefix="/api/v1/provider", tags=["provider"])


# -------------------------
# Dashboard overview
# -------------------------


@router.get("/dashboard", response_model=ProviderDashboardResponse)
def get_dashboard(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderDashboardResponse:
    stats = get_dashboard_stats(provider, db)
    profile = get_provider_profile(provider, db)
    is_complete, missing = check_onboarding_complete(db, provider.id)
    profile["is_complete"] = is_complete
    profile["missing_fields"] = missing
    analytics = get_analytics(provider, db, period_days=30)
    analytics_summary = {
        "period_days": analytics["period_days"],
        "total_leads": analytics["total_leads"],
        "contacted_leads": analytics["contacted_leads"],
        "sources": {k: v for k, v in analytics["sources"].items() if k != "other"},
    }
    return ProviderDashboardResponse(data={
        "stats": stats,
        "profile": profile,
        "analytics_summary": analytics_summary,
    })


# -------------------------
# Profile
# -------------------------


@router.get("/profile", response_model=ProviderProfileUpdateResponse)
def get_profile(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderProfileUpdateResponse:
    return ProviderProfileUpdateResponse(data=get_provider_profile(provider, db))


@router.patch("/profile", response_model=ProviderProfileUpdateResponse)
def update_profile(
    body: ProviderProfileUpdateRequest,
    request: Request,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderProfileUpdateResponse:
    print("=" * 50)
    print("BACKEND: Profile update request started")
    print(f"BACKEND: Request body: {body}")
    print(f"BACKEND: Provider ID: {provider.id}")
    print(f"BACKEND: Provider current state: slug={provider.slug}, slug_change_count={provider.slug_change_count}")
    
    try:
        print("BACKEND: Calling update_provider_profile function...")
        updated = update_provider_profile(
            provider,
            db,
            business_name=body.business_name,
            description=body.description,
            availability_status=body.availability_status,
            category_slug=body.category_slug,
            city_slug=body.city_slug,
            slug=body.slug,
            request_ip=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
            is_onboarding_setup=body.is_onboarding_setup,
        )
        print(f"BACKEND: Update successful: new_slug={updated.slug}, new_count={updated.slug_change_count}")
        print("BACKEND: Building response data...")
        response_data = get_provider_profile(updated, db)
        print(f"BACKEND: Response data built successfully")
        
        # Trigger translation for description if updated
        try:
            if getattr(body, 'description', None) and body.description.strip():
                from apps.api.services.translation_service import translate_and_store
                translate_and_store(
                    provider_id=provider.id,
                    field="description",
                    text=body.description.strip(),
                    db=db
                )
        except Exception as e:
            import logging
            logging.getLogger(__name__).error(f"Translation failed silently: {e}")
        
        print("=" * 50)
        return ProviderProfileUpdateResponse(data=response_data)
    except Exception as e:
        print(f"BACKEND: ERROR: Profile update failed: {e}")
        print(f"BACKEND: ERROR: Exception type: {type(e)}")
        import traceback
        print("BACKEND: Full traceback:")
        traceback.print_exc()
        print("=" * 50)
        raise


@router.get("/slug-history", response_model=ProviderSlugHistoryResponse)
def get_profile_slug_history(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderSlugHistoryResponse:
    return ProviderSlugHistoryResponse(data={"items": get_slug_history(provider, db)})


@router.get("/slug/check")
def check_slug_availability(
    slug: str = Query(..., min_length=2, max_length=50),
    city_slug: Optional[str] = None,
    category_slug: Optional[str] = None,
    db: Session = Depends(get_db),
) -> dict:
    """Check if slug is available and return suggestions if taken."""
    # Validate slug format
    is_valid, error_msg = validate_slug(slug)
    if not is_valid:
        return {
            "success": False,
            "error": {"code": "INVALID_SLUG", "message": error_msg},
            "data": {"available": False, "suggestions": []},
        }

    # Check availability
    is_available = not is_slug_taken(slug, db)

    suggestions = []
    if not is_available:
        suggestions = generate_slug_suggestions(slug, city_slug, category_slug, db)

    return {
        "success": True,
        "data": {
            "available": is_available,
            "suggestions": suggestions if not is_available else None,
        },
    }


# -------------------------
# Profile image upload
# -------------------------


@router.post("/profile/image")
async def upload_profile_image(
    file: UploadFile,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
    request: Request = None,
):
    # Derive base URL for static files
    # Priority: STATIC_FILES_BASE_URL env var > X-Forwarded headers > Host header
    from apps.api.config import settings
    
    base_url = settings.STATIC_FILES_BASE_URL
    
    if not base_url and request:
        # Check for X-Forwarded headers (set by reverse proxy)
        forwarded_host = request.headers.get("X-Forwarded-Host")
        forwarded_proto = request.headers.get("X-Forwarded-Proto", "http")
        
        if forwarded_host:
            # Use forwarded headers (Docker/production with reverse proxy)
            base_url = f"{forwarded_proto}://{forwarded_host}"
        else:
            # Use Host header directly (local development without proxy)
            host = request.headers.get("Host", "localhost:8000")
            scheme = request.url.scheme if request.url else "http"
            base_url = f"{scheme}://{host}"
    
    allowed = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}
    # Also check by filename extension if content_type is missing or generic
    content = await file.read()
    
    if file.content_type not in allowed:
        filename_lower = (file.filename or "").lower()
        is_heic_by_ext = filename_lower.endswith('.heic') or filename_lower.endswith('.heif')
        if not is_heic_by_ext:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Only JPEG, PNG, WebP, HEIC, and HEIF images are allowed",
            )

    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File size must be under 5 MB",
        )

    url = save_provider_image(provider.id, content, file.content_type, base_url)

    provider.profile_image_url = url
    db.commit()

    return {"success": True, "data": {"image_url": url}}


# -------------------------
# Leads
# -------------------------


@router.get("/leads", response_model=ProviderLeadsResponse)
def list_leads(
    status: str = Query(default="all", pattern="^(all|new|contacted|done|rejected)$"),
    period: str = Query(default="all", pattern="^(all|7|30|90)$"),
    date_from: Optional[str] = Query(default=None, alias="date_from"),
    date_to: Optional[str] = Query(default=None, alias="date_to"),
    search: Optional[str] = Query(default=None),
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderLeadsResponse:
    result = get_provider_leads(
        provider,
        db,
        status=status,
        period=period,
        date_from=date_from,
        date_to=date_to,
        search=search,
    )
    return ProviderLeadsResponse(data=result)


@router.patch("/leads/{lead_id}", response_model=LeadStatusUpdateResponse)
def update_lead_status(
    lead_id: str,
    body: LeadStatusUpdateRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> LeadStatusUpdateResponse:
    result = change_lead_status(db, lead_id, provider.id, body.status)
    return LeadStatusUpdateResponse(data=result)


@router.patch("/leads/{lead_id}/notes", response_model=LeadProviderNotesUpdateResponse)
def update_lead_provider_notes(
    lead_id: str,
    body: LeadProviderNotesUpdateRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> LeadProviderNotesUpdateResponse:
    from apps.api.models import Lead
    
    lead = (
        db.query(Lead)
        .filter(Lead.id == lead_id, Lead.provider_id == provider.id)
        .first()
    )
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found or you don't have access to this lead"
        )
    
    lead.provider_notes = body.provider_notes
    db.commit()
    
    return LeadProviderNotesUpdateResponse(data={"lead_id": lead_id, "provider_notes": body.provider_notes})


# -------------------------
# Services
# -------------------------


@router.get("/services")
def list_services(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    services = get_provider_services(provider, db)
    return {"success": True, "data": {"services": services}}


@router.post("/services", status_code=201)
def create_service(
    body: CreateServiceRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    from apps.api.services.provider_service import _serialize_service, retro_match_provider
    
    service = add_service(
        db,
        provider.id,
        body.category_id,
        body.title,
        body.city_ids,
        body.description,
        body.price_type,
        body.base_price,
        body.currency,
    )
    
    # Perform retroactive matching for the new service
    retro_matched_leads = 0
    try:
        retro_matched_leads = retro_match_provider(
            provider.id, 
            service.category_id, 
            body.city_ids, 
            db
        )
    except Exception as e:
        # Log error but don't fail the service creation
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Retro matching failed for provider {provider.id}: {e}")
    
    response_data = _serialize_service(service, db)
    response_data["retro_matched_leads"] = retro_matched_leads
    
    return {"success": True, "data": response_data}


@router.put("/services/{service_id}")
def update_service_endpoint(
    service_id: str,
    body: UpdateServiceRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    from apps.api.services.provider_service import _serialize_service
    service = update_service(
        db,
        service_id,
        provider.id,
        body.title,
        body.category_id,
        body.city_ids,
        body.description,
        body.price_type,
        body.base_price,
        body.currency,
    )
    return {"success": True, "data": _serialize_service(service, db)}


@router.delete("/services/{service_id}")
def delete_service_endpoint(
    service_id: str,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    delete_service(db, service_id, provider.id)
    return {"success": True, "data": {"message": "Service deleted"}}


# -------------------------
# Cities
# -------------------------


@router.post("/cities", status_code=201)
def add_provider_city(
    body: AddCityRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    add_city(db, provider.id, body.city_id)
    return {"success": True, "data": {"message": "City added"}}


# -------------------------
# QR code / growth
# -------------------------


@router.get("/qr-code", response_model=QRCodeResponse)
def get_qr_code(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> QRCodeResponse:
    public_url = build_qr_public_url(provider, db, settings.APP_URL)
    canonical_url = build_public_url(provider, db, settings.APP_URL)
    qr_data_uri = generate_qr_code_base64(public_url)
    return QRCodeResponse(data={
        "public_url": public_url,
        "canonical_url": canonical_url,
        "qr_code": qr_data_uri,
    })


@router.post("/enhanced-qr-code", response_model=Union[EnhancedQRCodeResponse, ErrorResponse])
def get_enhanced_qr_code(
    request: EnhancedQRCodeRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> Union[EnhancedQRCodeResponse, ErrorResponse]:
    try:
        public_url = build_qr_public_url(provider, db, settings.APP_URL)
        canonical_url = build_public_url(provider, db, settings.APP_URL)
        
        # Get provider's primary service for QR code
        services = get_provider_services(provider, db)
        primary_service = services[0] if services else None
        service_name = primary_service.get('title') if primary_service else "General Service"
        
        # Generate enhanced QR code with logo and multilingual text
        qr_data_uri = generate_enhanced_qr_code_base64(
            url=public_url,
            business_name=provider.business_name,
            service_name=service_name,
            language=request.language,
            db=db
        )
        
        return EnhancedQRCodeResponse(data={
            "public_url": public_url,
            "canonical_url": canonical_url,
            "qr_code": qr_data_uri,
            "language": request.language,
            "business_name": provider.business_name,
            "service_name": service_name,
        })
    except Exception as e:
        return ErrorResponse(
            error={
                "code": "QR_GENERATION_FAILED",
                "message": f"Failed to generate QR code: {str(e)}"
            }
        )


@router.post("/enhanced-qr-code-svg")
def get_enhanced_qr_code_svg(
    request: EnhancedQRCodeRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> Response:
    """Generate enhanced QR code as SVG for download."""
    try:
        public_url = build_qr_public_url(provider, db, settings.APP_URL)
        
        # Get provider's primary service for QR code
        services = get_provider_services(provider, db)
        primary_service = services[0] if services else None
        service_name = primary_service.get('title') if primary_service else "General Service"
        
        # Generate SVG QR code
        svg_content = generate_enhanced_qr_code_svg(
            url=public_url,
            business_name=provider.business_name,
            service_name=service_name,
            language=request.language,
            db=db
        )
        
        return Response(
            content=svg_content,
            media_type="image/svg+xml",
            headers={
                "Content-Disposition": f'attachment; filename="nevumo-qr-{request.language}.svg"'
            }
        )
    except Exception as e:
        return ErrorResponse(
            error={
                "code": "QR_GENERATION_FAILED",
                "message": f"Failed to generate QR code: {str(e)}"
            }
        )


# -------------------------
# Analytics
# -------------------------


@router.get("/analytics")
def get_provider_analytics(
    period: int = Query(default=30, ge=1, le=365),
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> dict:
    data = get_analytics(provider, db, period_days=period)
    return {"success": True, "data": data}


# -------------------------
# Claim functionality
# -------------------------


@router.post("/claim")
def claim_provider_endpoint(
    body: ClaimProviderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> dict:
    """Claim a provider profile using a claim token."""
    provider = claim_provider(body.claim_token, current_user, db)
    return {
        "success": True,
        "data": {
            "provider_id": str(provider.id),
            "slug": provider.slug,
            "message": "Profile claimed successfully"
        }
    }
