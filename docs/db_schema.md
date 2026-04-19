# Nevumo Database Schema (PostgreSQL)

## Core Principles

- Normalize critical data (locations, categories)
- Use indexes for all matching/filtering fields
- Prepare for multi-country scaling
- Avoid premature complexity

---

## 1. Users

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT,                               -- Canonical display name (optional, never derived from email)
    phone TEXT,                              -- optional, E.164 format, persisted for UX convenience
    password_hash TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role TEXT NOT NULL CHECK (role IN ('client', 'provider')),
    locale TEXT NOT NULL DEFAULT 'en',
    country_code CHAR(2),
    review_reply_email_enabled BOOLEAN NOT NULL DEFAULT TRUE,  -- Opt-in for review reply emails
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_review_reply_email ON users(review_reply_email_enabled);
CREATE INDEX idx_users_phone ON users(phone) WHERE phone IS NOT NULL;

---

## 2. Providers

CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,  -- NULL for unclaimed profiles
    business_name TEXT,
    description TEXT,
    slug TEXT UNIQUE NOT NULL,                -- URL slug, auto-generated from business_name
    slug_change_count INTEGER NOT NULL DEFAULT 0,
    profile_image_url TEXT,                   -- served at /static/provider_images/
    rating NUMERIC(2,1) DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    availability_status TEXT DEFAULT 'active',
    is_claimed BOOLEAN NOT NULL DEFAULT TRUE, -- FALSE for unclaimed (scraped/auto-created) profiles
    claim_token TEXT UNIQUE,                  -- Magic token for claiming unclaimed profiles
    data_source TEXT NOT NULL DEFAULT 'manual', -- 'manual', 'scraped', 'imported', etc.
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_providers_rating ON providers(rating);
CREATE INDEX idx_providers_status ON providers(availability_status);
CREATE INDEX idx_providers_is_claimed ON providers(is_claimed);
CREATE UNIQUE INDEX idx_providers_claim_token ON providers(claim_token) WHERE claim_token IS NOT NULL;

### Slug Validation Rules
- **Format**: 2-50 characters, lowercase letters, numbers, and hyphens only
- **Pattern**: `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- **Restrictions**: No numeric suffixes (e.g., `devs-1`, `provider-123`)
- **Uniqueness**: Must be unique across all providers
- **Auto-generation**: Created from business_name during registration if not provided

### Dynamic Fields (calculated, not stored)
- **rating**: calculated as AVG(reviews.rating) - updated in real-time via get_provider_rating()
- **jobs_completed**: calculated as COUNT(leads.status='done') + COUNT(lead_matches.status='done') via get_provider_jobs_completed()

---

## 3. Provider Availability (Cities)

CREATE TABLE provider_cities (
    id SERIAL PRIMARY KEY,
    provider_id UUID REFERENCES providers(id) ON DELETE CASCADE,
    city_id INT REFERENCES locations(id),
    UNIQUE(provider_id, city_id)
);

CREATE INDEX idx_provider_cities_city ON provider_cities(city_id);

---

## 3a. Provider Slug History

CREATE TABLE provider_slug_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    old_slug TEXT NOT NULL,
    new_slug TEXT NOT NULL,
    changed_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_provider_slug_history_provider_changed ON provider_slug_history(provider_id, changed_at);
CREATE INDEX idx_provider_slug_history_old_slug ON provider_slug_history(old_slug);

---

## 3b. URL Redirects

CREATE TABLE url_redirects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    old_slug TEXT NOT NULL,
    new_slug TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_url_redirects_provider_old_slug UNIQUE(provider_id, old_slug)
);

CREATE INDEX idx_url_redirects_old_slug_active ON url_redirects(old_slug, active);

---

## 4. Categories

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    parent_id INT REFERENCES categories(id)
);

-- Current seeded categories (April 4, 2026):
-- cleaning (34 translations)
-- plumbing (34 translations) 
-- massage (34 translations)

---

## 5. Category Translations

CREATE TABLE category_translations (
    id SERIAL PRIMARY KEY,
    category_id INT REFERENCES categories(id) ON DELETE CASCADE,
    lang TEXT NOT NULL,
    name TEXT NOT NULL,
    UNIQUE(category_id, lang)
);

---

## 6. Locations

CREATE TABLE locations (
    id SERIAL PRIMARY KEY,
    country_code CHAR(2) NOT NULL,
    city TEXT NOT NULL,
    city_en TEXT,                             -- English city name for multilingual support
    slug TEXT NOT NULL,
    lat NUMERIC,
    lng NUMERIC,
    UNIQUE(country_code, slug)
);

-- Current data includes:
-- BG (Bulgaria) - Sofia (EUR as of March 2026)
-- RS (Serbia) - Belgrade (RSD)
-- PL (Poland) - Warszawa (PLN) - seeded April 4, 2026 (slug=warszawa, lat=52.2297, lng=21.0122)

CREATE INDEX idx_locations_country ON locations(country_code);

---

## 6a. Location Translations

CREATE TABLE location_translations (
    id SERIAL PRIMARY KEY,
    location_id INT NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    lang TEXT NOT NULL,
    city_name TEXT NOT NULL,
    UNIQUE(location_id, lang)
);

CREATE INDEX idx_location_translations_location ON location_translations(location_id);
CREATE INDEX idx_location_translations_lang ON location_translations(lang);

### Seeded Data (April 2026)
- 3 cities × 34 languages = 102 rows
- Sofia (BG), Belgrade (RS), Warszawa (PL)
- Seed script: apps/api/scripts/seed_location_translations.py

---

## 7. Services

CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES providers(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id),
    title TEXT NOT NULL,
    description TEXT,
    price_type TEXT,           -- validated in Pydantic: fixed | hourly | request | per_sqm
    base_price NUMERIC,
    currency TEXT NOT NULL DEFAULT 'EUR',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_services_category ON services(category_id);
CREATE INDEX idx_services_provider ON services(provider_id);

---

## 7a. Service Cities

-- Many-to-many: which cities a specific service is offered in.
-- Separate from provider_cities (provider-level availability).

CREATE TABLE service_cities (
    id SERIAL PRIMARY KEY,
    service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
    city_id INT NOT NULL REFERENCES locations(id),
    UNIQUE(service_id, city_id)
);

CREATE INDEX idx_service_cities_service ON service_cities(service_id);
CREATE INDEX idx_service_cities_city ON service_cities(city_id);

---

## 8. Leads (CORE TABLE)

CREATE TABLE leads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES users(id),
    provider_id UUID REFERENCES providers(id),
    category_id INT REFERENCES categories(id),
    city_id INT REFERENCES locations(id),

    phone TEXT NOT NULL,
    description TEXT,
    budget NUMERIC,

    source TEXT,
    utm_source TEXT,
    utm_campaign TEXT,
    landing_page TEXT,

    status TEXT NOT NULL DEFAULT 'created',
    -- CHECK constraint (added via migration c3d4e5f6a7b8):
    -- CHECK (status IN ('created', 'pending_match', 'matched', 'contacted', 'done', 'expired', 'cancelled', 'rejected'))

    provider_notes TEXT,  -- Provider's private notes about the lead (added via migration q1r2s3t4u5v6)

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leads_category ON leads(category_id);
CREATE INDEX idx_leads_city ON leads(city_id);
CREATE INDEX idx_leads_provider ON leads(provider_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at);

### Runtime Semantics
- `client_id` is nullable because public lead creation supports anonymous requests
- When the same public endpoint is called with a valid authenticated JWT, `client_id` is populated with the current user id

---

## 9. Lead Matches

CREATE TABLE lead_matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    provider_id UUID REFERENCES providers(id),
    status TEXT CHECK (status IN ('invited', 'contacted', 'done', 'rejected')),
    -- Updated via migration c3d4e5f6a7b8 to support dashboard lead status flow
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(lead_id, provider_id)
);

CREATE INDEX idx_lead_matches_lead ON lead_matches(lead_id);

---

## 10. Messages (Future)

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    sender_id UUID REFERENCES users(id),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_lead ON messages(lead_id);

---

## 11. Tracking (Lead Events)

CREATE TABLE lead_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID REFERENCES leads(id) ON DELETE CASCADE,
    event_type TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_lead_events_lead ON lead_events(lead_id);

---

## 12. Anti-Spam (Basic Rate Limiting)

CREATE TABLE lead_rate_limits (
    id SERIAL PRIMARY KEY,
    ip TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_rate_limits_ip ON lead_rate_limits(ip);

---

## 13. Password Reset Tokens

CREATE TABLE password_reset_tokens (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash TEXT NOT NULL UNIQUE,  -- SHA-256 of raw token; raw token is sent in email
    expires_at TIMESTAMP NOT NULL,    -- 30 minutes from creation
    used_at TIMESTAMP,                -- set on first use; NULL = unused
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reset_tokens_hash ON password_reset_tokens(token_hash);
CREATE INDEX idx_reset_tokens_user ON password_reset_tokens(user_id);

---

## 14. Pending Lead Claims

CREATE TABLE pending_lead_claims (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lead_id UUID NOT NULL REFERENCES leads(id) ON DELETE CASCADE,
    email TEXT NOT NULL,
    phone TEXT,                               -- optional phone from lead claim form
    claimed BOOLEAN NOT NULL DEFAULT FALSE,
    claimed_at TIMESTAMP,                     -- set when user claims the lead
    magic_link_sent BOOLEAN NOT NULL DEFAULT FALSE,
    magic_link_sent_at TIMESTAMP,             -- set when delayed magic link is sent
    expires_at TIMESTAMP NOT NULL,           -- claim expiration (e.g., 7 days)
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pending_claims_lead ON pending_lead_claims(lead_id);
CREATE INDEX idx_pending_claims_email ON pending_lead_claims(email);
CREATE INDEX idx_pending_claims_claimed ON pending_lead_claims(claimed);
CREATE INDEX idx_pending_claims_expires ON pending_lead_claims(expires_at);

---

## 15. Magic Link Tokens

CREATE TABLE magic_link_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
    token_hash TEXT NOT NULL UNIQUE,          -- SHA-256 of raw token; raw token is sent in email
    expires_at TIMESTAMP NOT NULL,            -- token expiration (e.g., 48 hours)
    used_at TIMESTAMP,                        -- set when token is successfully used
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_magic_tokens_hash ON magic_link_tokens(token_hash);
CREATE INDEX idx_magic_tokens_email ON magic_link_tokens(email);

---

## 16. Auth Rate Limits

CREATE TABLE auth_rate_limits (
    id SERIAL PRIMARY KEY,
    ip TEXT NOT NULL,
    action TEXT NOT NULL,  -- 'register' | 'login' | 'forgot' | 'reset'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_auth_rate_limits_ip_action ON auth_rate_limits(ip, action);
CREATE INDEX idx_auth_rate_limits_created ON auth_rate_limits(created_at);

---

## 17. Translations (i18n)

CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    lang TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT,
    UNIQUE(lang, key)
);

CREATE INDEX idx_translations_lang ON translations(lang);
CREATE INDEX idx_translations_key ON translations(key);

### Storage Format
- **namespace.key pattern**: Keys are stored as `namespace.key` (e.g., `homepage.title`, `category.cleaning`).
- **Validation**: **Mandatory namespacing**. Keys must contain at least one dot and cannot start or end with a dot. Enforced at the ORM layer (SQLAlchemy `@validates`).
- **Namespace separation**: Different feature areas use different namespaces for organization.

### Current Seeded Data (April 4, 2026)
- **homepage namespace**: 45 keys × 34 languages = 1,530 rows
- **category namespace**: 42 UI keys × 34 languages + 18 SEO keys (pl/bg/en only) = 1,428 + 54 = 1,482 rows
- **category form keys (April 2026)**: 15 new keys × 34 languages = 510 rows
  Keys added: no_providers_title, no_providers_subtitle, form_subtext,
  how_it_works_label, how_step_1, how_step_2, how_step_3, what_need_label,
  chip_not_sure, details_label, details_placeholder, get_offers_btn,
  trust_multiple, trust_response, sticky_btn
- **widget namespace**: 23 keys × 34 languages = 782 rows
- **client_dashboard namespace**: Client dashboard UI strings
- **provider_dashboard namespace**: 168 keys × 34 languages = 5,712 rows (includes 8 onboarding hero keys added April 10, 2026)
  Keys include: nav_overview, nav_analytics, nav_leads, nav_qr_code, nav_reviews,
  nav_services, nav_settings, nav_profile, and all dashboard UI strings
- **Total rows**: 8,000+ translations across all namespaces

### Redis Caching
- **Cache key pattern**: `translations:{lang}:{namespace}`
- **Example**: `translations:en:homepage` caches all English homepage translations
- **TTL**: Configurable expiration for automatic refresh

---

## 16. Reviews (Closed Trust Conversation Model)

CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    client_id UUID NOT NULL REFERENCES users(id),
    lead_id UUID REFERENCES leads(id) ON DELETE SET NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,

    -- Provider reply fields (closed trust conversation model)
    provider_reply TEXT,                              -- Provider's single reply to review
    provider_reply_at TIMESTAMP,                      -- When first reply was posted
    provider_reply_edited_at TIMESTAMP,               -- Last edit timestamp
    provider_reply_edit_count INTEGER NOT NULL DEFAULT 0,  -- Number of edits

    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(lead_id)  -- one review per lead
);

CREATE INDEX idx_reviews_provider ON reviews(provider_id);
CREATE INDEX idx_reviews_client ON reviews(client_id);
CREATE INDEX idx_reviews_provider_reply_at ON reviews(provider_reply_at);

### Product Rules
- **Client review is the starting message** - Always the first message in conversation
- **Provider has exactly one reply per review** - Single reply, editable unlimited times
- **Edited indicator** - Shown when provider_reply_edit_count > 0
- **Conversation closes** - After provider reply, no further messages
- **Email notification** - Sent to client on first provider reply only (if opted in)
- **Canonical client display name** - Review surfaces use `users.name` when available, otherwise `Client`

### Constraints
- One review per lead (enforced by UNIQUE(lead_id))
- Rating must be 1-5 stars
- Only completed leads (status='done') can be reviewed
- Client must own the lead being reviewed
- Provider.user_id must differ from the reviewing client id (self-review is blocked at service layer)

### Dynamic Fields
- **provider.rating** calculated as AVG(reviews.rating)
- **provider review_count** calculated as COUNT(reviews)

---

## Performance Notes

- Indexes on category_id + city_id are critical for matching
- provider_id index is required for direct leads
- created_at index is required for sorting and analytics

---

## Scaling Strategy (Future)

- Partition leads table by country_code or created_at
- Add read replicas
- Use Redis for caching hot queries

---

## General Rules

- Use NUMERIC for all financial values (never FLOAT)
- Use UUID for distributed-safe IDs
- Use JSONB for flexible event tracking