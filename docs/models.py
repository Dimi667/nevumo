from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import (
    String, Text, ForeignKey, Integer, Boolean,
    Numeric, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# -------------------------
# Base
# -------------------------

class Base(DeclarativeBase):
    pass


# -------------------------
# Users
# -------------------------

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    locale: Mapped[str] = mapped_column(String, default="en")
    country_code: Mapped[Optional[str]] = mapped_column(String(2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    provider: Mapped["Provider"] = relationship(back_populates="user", uselist=False)


# -------------------------
# Providers
# -------------------------

class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    business_name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    rating: Mapped[float] = mapped_column(Numeric(2, 1), default=0)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    availability_status: Mapped[str] = mapped_column(String, default="active")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="provider")

    services: Mapped[List["Service"]] = relationship(back_populates="provider")
    cities: Mapped[List["ProviderCity"]] = relationship(back_populates="provider")


# -------------------------
# Locations
# -------------------------

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_code: Mapped[str] = mapped_column(String(2), nullable=False)
    city: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)

    lat: Mapped[Optional[float]] = mapped_column(Numeric)
    lng: Mapped[Optional[float]] = mapped_column(Numeric)

    __table_args__ = (
        UniqueConstraint("country_code", "slug"),
        Index("idx_locations_country", "country_code"),
    )


# -------------------------
# Provider Cities
# -------------------------

class ProviderCity(Base):
    __tablename__ = "provider_cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"))
    city_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    provider: Mapped["Provider"] = relationship(back_populates="cities")

    __table_args__ = (
        UniqueConstraint("provider_id", "city_id"),
        Index("idx_provider_cities_city", "city_id"),
    )


# -------------------------
# Categories
# -------------------------

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))

    translations: Mapped[List["CategoryTranslation"]] = relationship(back_populates="category")


class CategoryTranslation(Base):
    __tablename__ = "category_translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    lang: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)

    category: Mapped["Category"] = relationship(back_populates="translations")

    __table_args__ = (
        UniqueConstraint("category_id", "lang"),
    )


# -------------------------
# Services
# -------------------------

class Service(Base):
    __tablename__ = "services"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)

    price_type: Mapped[str] = mapped_column(String)
    base_price: Mapped[Optional[float]] = mapped_column(Numeric)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    provider: Mapped["Provider"] = relationship(back_populates="services")

    __table_args__ = (
        Index("idx_services_category", "category_id"),
        Index("idx_services_provider", "provider_id"),
    )


# -------------------------
# Leads (CORE)
# -------------------------

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    client_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("users.id"))
    provider_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("providers.id"))

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    city_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    phone: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    budget: Mapped[Optional[float]] = mapped_column(Numeric)

    source: Mapped[Optional[str]] = mapped_column(String)
    utm_source: Mapped[Optional[str]] = mapped_column(String)
    utm_campaign: Mapped[Optional[str]] = mapped_column(String)
    landing_page: Mapped[Optional[str]] = mapped_column(String)

    status: Mapped[str] = mapped_column(String, default="created")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_leads_category", "category_id"),
        Index("idx_leads_city", "city_id"),
        Index("idx_leads_provider", "provider_id"),
        Index("idx_leads_status", "status"),
        Index("idx_leads_created_at", "created_at"),
    )


# -------------------------
# Lead Matches
# -------------------------

class LeadMatch(Base):
    __tablename__ = "lead_matches"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)

    lead_id: Mapped[UUID] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id"))

    status: Mapped[str] = mapped_column(String)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("lead_id", "provider_id"),
        Index("idx_lead_matches_lead", "lead_id"),
    )


# -------------------------
# Messages (Future)
# -------------------------

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    lead_id: Mapped[UUID] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))
    sender_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))

    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_messages_lead", "lead_id"),
    )


# -------------------------
# Lead Events (Tracking)
# -------------------------

class LeadEvent(Base):
    __tablename__ = "lead_events"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    lead_id: Mapped[UUID] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"))

    event_type: Mapped[Optional[str]] = mapped_column(String)
    metadata: Mapped[Optional[dict]] = mapped_column(JSONB)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_lead_events_lead", "lead_id"),
    )


# -------------------------
# Rate Limit (Anti-Spam)
# -------------------------

class LeadRateLimit(Base):
    __tablename__ = "lead_rate_limits"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_rate_limits_ip", "ip"),
    )


# -------------------------
# Password Reset Tokens (Auth)
# -------------------------

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    # SHA-256 of the raw token. Raw token is sent in email; only hash is stored.
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    # None = unused; set to datetime on first use (one-time token)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_reset_tokens_hash", "token_hash"),
        Index("idx_reset_tokens_user", "user_id"),
    )


# -------------------------
# Auth Rate Limits
# -------------------------

class AuthRateLimit(Base):
    __tablename__ = "auth_rate_limits"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    # action: 'register' | 'login' | 'forgot' | 'reset'
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_auth_rate_limits_ip_action", "ip", "action"),
        Index("idx_auth_rate_limits_created", "created_at"),
    )