from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


# -------------------------
# Categories
# -------------------------

class CategoryOut(BaseModel):
    slug: str
    name: str


class CategoriesResponse(BaseModel):
    success: bool = True
    data: List[CategoryOut]


# -------------------------
# Cities
# -------------------------

class CityOut(BaseModel):
    slug: str
    name: str


class CitiesResponse(BaseModel):
    success: bool = True
    data: List[CityOut]


# -------------------------
# Services
# -------------------------

class ServiceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    description: Optional[str] = None
    price_type: Optional[str] = None
    base_price: Optional[float] = None
    category_slug: Optional[str] = None

    @field_validator("base_price", mode="before")
    @classmethod
    def convert_price(cls, v):
        if v is not None:
            return float(v)
        return None


# -------------------------
# Providers
# -------------------------

class ProviderListItem(BaseModel):
    id: UUID
    business_name: str
    rating: float
    verified: bool
    slug: str

    @field_validator("rating", mode="before")
    @classmethod
    def convert_rating(cls, v):
        if v is not None:
            return float(v)
        return 0.0


class ProviderListResponse(BaseModel):
    success: bool = True
    data: List[ProviderListItem]


class ProviderDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    business_name: str
    description: Optional[str] = None
    slug: str
    rating: float
    verified: bool
    availability_status: str
    created_at: datetime
    services: List[ServiceOut] = []

    @field_validator("rating", mode="before")
    @classmethod
    def convert_rating(cls, v):
        if v is not None:
            return float(v)
        return 0.0


class ProviderDetailResponse(BaseModel):
    success: bool = True
    data: ProviderDetail


# -------------------------
# Leads
# -------------------------

class LeadCreate(BaseModel):
    phone: str
    category_slug: str
    city_slug: str
    provider_slug: Optional[str] = None
    description: Optional[str] = None
    budget: Optional[Decimal] = None
    source: Optional[str] = None
    utm_source: Optional[str] = None
    utm_campaign: Optional[str] = None
    landing_page: Optional[str] = None


class LeadCreatedResponse(BaseModel):
    success: bool = True
    data: dict


class LeadOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    phone: str
    description: Optional[str] = None
    budget: Optional[Decimal] = None
    status: str
    created_at: datetime


class ProviderLeadsResponse(BaseModel):
    success: bool = True
    data: List[LeadOut]


class LeadMatchUpdate(BaseModel):
    status: str


class LeadMatchUpdateResponse(BaseModel):
    success: bool = True
    data: dict


# -------------------------
# Events
# -------------------------

class EventCreate(BaseModel):
    lead_id: UUID
    event_type: str
    metadata: Optional[dict] = None


class EventCreatedResponse(BaseModel):
    success: bool = True
    data: dict


# -------------------------
# Error
# -------------------------

class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    success: bool = False
    error: ErrorDetail


# -------------------------
# Page Events (Tracking)
# -------------------------

class PageEventCreate(BaseModel):
    event_type: str
    page: str
    metadata: dict = {}


# -------------------------
# Auth
# -------------------------

class CheckEmailRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class CheckEmailResponse(BaseModel):
    success: bool = True
    data: dict


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: str = "client"

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("role")
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ("client", "provider"):
            raise ValueError("Role must be client or provider")
        return v


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class AuthTokenResponse(BaseModel):
    success: bool = True
    data: dict


class ForgotPasswordRequest(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class ForgotPasswordResponse(BaseModel):
    success: bool = True
    data: dict


class ValidateResetTokenRequest(BaseModel):
    token: str


class ValidateResetTokenResponse(BaseModel):
    success: bool = True
    data: dict


class ResetPasswordRequest(BaseModel):
    token: str
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class ResetPasswordResponse(BaseModel):
    success: bool = True
    data: dict


# -------------------------
# Provider Dashboard Schemas
# -------------------------

class ProviderDashboardResponse(BaseModel):
    success: bool = True
    data: dict


class ProviderProfileUpdateRequest(BaseModel):
    business_name: Optional[str] = None
    description: Optional[str] = None
    availability_status: Optional[str] = None

    @field_validator("availability_status")
    @classmethod
    def validate_status(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v not in ("active", "busy", "offline"):
            raise ValueError("availability_status must be active, busy, or offline")
        return v


class ProviderProfileUpdateResponse(BaseModel):
    success: bool = True
    data: dict


class CreateServiceRequest(BaseModel):
    category_id: int
    title: str
    description: Optional[str] = None
    price_type: str
    base_price: Optional[Decimal] = None


class AddCityRequest(BaseModel):
    city_id: int


class LeadStatusUpdateRequest(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def validate_lead_status(cls, v: str) -> str:
        if v not in ("contacted", "done", "rejected"):
            raise ValueError("status must be contacted, done, or rejected")
        return v


class LeadStatusUpdateResponse(BaseModel):
    success: bool = True
    data: dict


class ProviderLeadsResponse(BaseModel):
    success: bool = True
    data: dict


class QRCodeResponse(BaseModel):
    success: bool = True
    data: dict
