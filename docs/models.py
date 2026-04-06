from datetime import datetime
from typing import Optional, List
from uuid import UUID, uuid4

from sqlalchemy import (
    String, Text, ForeignKey, Integer, Boolean,
    Numeric, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB, INET
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
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    password_hash: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    role: Mapped[str] = mapped_column(String, nullable=False)
    locale: Mapped[str] = mapped_column(String, default="en")
    country_code: Mapped[Optional[str]] = mapped_column(String(2))
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Email notification preferences
    review_reply_email_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # Phone number (optional, E.164 format, persisted for UX convenience)
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    provider: Mapped["Provider"] = relationship(back_populates="user", uselist=False)

    __table_args__ = (
        CheckConstraint("role IN ('client', 'provider')", name="ck_users_role"),
        Index("idx_users_role", "role"),
        Index("idx_users_review_reply_email", "review_reply_email_enabled"),
        Index("idx_users_phone", "phone"),
    )


# -------------------------
# Providers
# -------------------------

class Provider(Base):
    __tablename__ = "providers"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)

    business_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    slug_change_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    profile_image_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    rating: Mapped[float] = mapped_column(Numeric(2, 1), default=0)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

    availability_status: Mapped[str] = mapped_column(String, default="active")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="provider")
    services: Mapped[List["Service"]] = relationship(back_populates="provider")
    cities: Mapped[List["ProviderCity"]] = relationship(back_populates="provider")
    slug_history: Mapped[List["ProviderSlugHistory"]] = relationship(
        back_populates="provider",
        cascade="all, delete-orphan",
        order_by="desc(ProviderSlugHistory.changed_at)",
    )
    redirects: Mapped[List["UrlRedirect"]] = relationship(
        back_populates="provider",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        Index("idx_providers_rating", "rating"),
        Index("idx_providers_status", "availability_status"),
    )


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
# Provider Slug History
# -------------------------

class ProviderSlugHistory(Base):
    __tablename__ = "provider_slug_history"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    old_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    new_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(INET, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    provider: Mapped["Provider"] = relationship(back_populates="slug_history")

    __table_args__ = (
        Index("idx_provider_slug_history_provider_changed", "provider_id", "changed_at"),
        Index("idx_provider_slug_history_old_slug", "old_slug"),
    )


# -------------------------
# URL Redirects
# -------------------------

class UrlRedirect(Base):
    __tablename__ = "url_redirects"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"), nullable=False)
    old_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    new_slug: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    provider: Mapped["Provider"] = relationship(back_populates="redirects")

    __table_args__ = (
        UniqueConstraint("provider_id", "old_slug", name="uq_url_redirects_provider_old_slug"),
        Index("idx_url_redirects_old_slug_active", "old_slug", "active"),
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
    currency: Mapped[str] = mapped_column(String, default="EUR")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    provider: Mapped["Provider"] = relationship(back_populates="services")
    cities: Mapped[List["ServiceCity"]] = relationship(back_populates="service", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_services_category", "category_id"),
        Index("idx_services_provider", "provider_id"),
    )


# -------------------------
# Service Cities
# -------------------------

class ServiceCity(Base):
    __tablename__ = "service_cities"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_id: Mapped[UUID] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"))
    city_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))

    service: Mapped["Service"] = relationship(back_populates="cities")

    __table_args__ = (
        UniqueConstraint("service_id", "city_id", name="uq_service_cities"),
        Index("idx_service_cities_service", "service_id"),
        Index("idx_service_cities_city", "city_id"),
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
        CheckConstraint("status IN ('invited', 'accepted', 'rejected')", name="ck_lead_matches_status"),
        UniqueConstraint("lead_id", "provider_id"),
        Index("idx_lead_matches_lead", "lead_id"),
    )


# -------------------------
# Reviews (Ratings)
# -------------------------

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    provider_id: Mapped[UUID] = mapped_column(ForeignKey("providers.id", ondelete="CASCADE"))
    client_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    lead_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), nullable=True)

    rating: Mapped[int] = mapped_column(Integer, nullable=False)  # 1-5 stars
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Provider reply fields (closed trust conversation model)
    provider_reply: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    provider_reply_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    provider_reply_edited_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    provider_reply_edit_count: Mapped[int] = mapped_column(Integer, default=0)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("rating >= 1 AND rating <= 5", name="ck_reviews_rating_range"),
        Index("idx_reviews_provider", "provider_id"),
        Index("idx_reviews_client", "client_id"),
        Index("idx_reviews_provider_reply_at", "provider_reply_at"),
        UniqueConstraint("lead_id", name="uq_reviews_lead"),
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
    event_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSONB)

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
# Translations (i18n)
# -------------------------

class Translation(Base):
    __tablename__ = "translations"

    id: Mapped[int] = mapped_column(primary_key=True)
    lang: Mapped[str] = mapped_column(String, nullable=False)
    key: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String)

    __table_args__ = (
        UniqueConstraint("lang", "key"),
        Index("idx_translations_lang", "lang"),
        Index("idx_translations_key", "key"),
    )


# -------------------------
# Page Events (Tracking)
# -------------------------

class PageEvent(Base):
    __tablename__ = "page_events"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    event_type: Mapped[str] = mapped_column(Text, nullable=False)
    page: Mapped[str] = mapped_column(Text, nullable=False)
    event_metadata: Mapped[Optional[dict]] = mapped_column("metadata", JSONB, default=dict)
    ip: Mapped[Optional[str]] = mapped_column(Text)
    user_agent: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_page_events_type", "event_type"),
        Index("idx_page_events_page", "page"),
        Index("idx_page_events_created", "created_at"),
    )


# -------------------------
# Password Reset Tokens
# -------------------------

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    token_hash: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_reset_tokens_hash", "token_hash"),
        Index("idx_reset_tokens_user", "user_id"),
    )


# -------------------------
# Pending Lead Claims
# -------------------------

class PendingLeadClaim(Base):
    __tablename__ = "pending_lead_claims"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    lead_id: Mapped[UUID] = mapped_column(ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    claimed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    claimed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    magic_link_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    magic_link_sent_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_pending_claims_lead", "lead_id"),
        Index("idx_pending_claims_email", "email"),
        Index("idx_pending_claims_claimed", "claimed"),
        Index("idx_pending_claims_expires", "expires_at"),
    )


# -------------------------
# Magic Link Tokens
# -------------------------

class MagicLinkToken(Base):
    __tablename__ = "magic_link_tokens"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    email: Mapped[str] = mapped_column(Text, nullable=False)
    lead_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("leads.id", ondelete="SET NULL"), nullable=True)
    token_hash: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("idx_magic_tokens_hash", "token_hash"),
        Index("idx_magic_tokens_email", "email"),
    )


# -------------------------
# Auth Rate Limits
# -------------------------

class AuthRateLimit(Base):
    __tablename__ = "auth_rate_limits"

    id: Mapped[int] = mapped_column(primary_key=True)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    action: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    __table_args__ = (
        Index("idx_auth_rate_limits_ip_action", "ip", "action"),
        Index("idx_auth_rate_limits_created", "created_at"),
    )