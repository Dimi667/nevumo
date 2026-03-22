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
