"""Provider dashboard endpoints (auth required)."""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from config import settings
from dependencies import get_current_provider, get_db
from models import Provider
from schemas import (
    AddCityRequest,
    CreateServiceRequest,
    LeadStatusUpdateRequest,
    LeadStatusUpdateResponse,
    ProviderDashboardResponse,
    ProviderLeadsResponse,
    ProviderProfileUpdateRequest,
    ProviderProfileUpdateResponse,
    QRCodeResponse,
    UpdateServiceRequest,
)
from services import provider_service
from services.provider_service import (
    add_city,
    add_service,
    build_public_url,
    change_lead_status,
    check_onboarding_complete,
    delete_service,
    generate_qr_code_base64,
    get_analytics,
    get_dashboard_stats,
    get_provider_leads,
    get_provider_profile,
    get_provider_services,
    save_provider_image,
    update_provider_profile,
    update_service,
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
    profile = get_provider_profile(provider)
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
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderProfileUpdateResponse:
    updated = update_provider_profile(
        provider,
        db,
        business_name=body.business_name,
        description=body.description,
        availability_status=body.availability_status,
        category_slug=body.category_slug,
        city_slug=body.city_slug,
    )
    return ProviderProfileUpdateResponse(data=get_provider_profile(updated, db))


# -------------------------
# Profile image upload
# -------------------------


@router.post("/profile/image")
async def upload_profile_image(
    file: UploadFile,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    allowed = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Only JPEG, PNG, and WebP images are allowed",
        )

    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="File size must be under 5 MB",
        )

    ext_map = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}
    ext = ext_map[file.content_type]
    url = save_provider_image(provider.id, content, ext)

    provider.profile_image_url = url
    db.commit()

    return {"success": True, "data": {"image_url": url}}


# -------------------------
# Leads
# -------------------------


@router.get("/leads", response_model=ProviderLeadsResponse)
def list_leads(
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> ProviderLeadsResponse:
    leads = get_provider_leads(provider, db)
    return ProviderLeadsResponse(data={"leads": leads, "total": len(leads)})


@router.patch("/leads/{lead_id}", response_model=LeadStatusUpdateResponse)
def update_lead_status(
    lead_id: str,
    body: LeadStatusUpdateRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
) -> LeadStatusUpdateResponse:
    result = change_lead_status(db, lead_id, provider.id, body.status)
    return LeadStatusUpdateResponse(data=result)


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
    from services.provider_service import _serialize_service
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
    return {"success": True, "data": _serialize_service(service, db)}


@router.put("/services/{service_id}")
def update_service_endpoint(
    service_id: str,
    body: UpdateServiceRequest,
    provider: Provider = Depends(get_current_provider),
    db: Session = Depends(get_db),
):
    from services.provider_service import _serialize_service
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
    public_url = build_public_url(provider, db, settings.APP_URL)
    qr_data_uri = generate_qr_code_base64(public_url)
    return QRCodeResponse(data={"public_url": public_url, "qr_code": qr_data_uri})


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
