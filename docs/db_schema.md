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
    password_hash TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    role TEXT NOT NULL CHECK (role IN ('client', 'provider')),
    locale TEXT NOT NULL DEFAULT 'en',
    country_code CHAR(2),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);

---

## 2. Providers

CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    business_name TEXT NOT NULL,
    description TEXT,
    slug TEXT UNIQUE NOT NULL,                -- URL slug, auto-generated from business_name
    profile_image_url TEXT,                   -- served at /static/provider_images/
    rating NUMERIC(2,1) DEFAULT 0,
    verified BOOLEAN DEFAULT FALSE,
    availability_status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_providers_rating ON providers(rating);
CREATE INDEX idx_providers_status ON providers(availability_status);
CREATE INDEX idx_providers_slug ON providers(slug);

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

## 4. Categories

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    slug TEXT UNIQUE NOT NULL,
    parent_id INT REFERENCES categories(id)
);

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
    slug TEXT NOT NULL,
    lat NUMERIC,
    lng NUMERIC,
    UNIQUE(country_code, slug)
);

CREATE INDEX idx_locations_country ON locations(country_code);

---

## 7. Services

CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider_id UUID REFERENCES providers(id) ON DELETE CASCADE,
    category_id INT REFERENCES categories(id),
    title TEXT NOT NULL,
    description TEXT,
    price_type TEXT CHECK (price_type IN ('fixed', 'hourly', 'request')),
    base_price NUMERIC,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_services_category ON services(category_id);
CREATE INDEX idx_services_provider ON services(provider_id);

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

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_leads_category ON leads(category_id);
CREATE INDEX idx_leads_city ON leads(city_id);
CREATE INDEX idx_leads_provider ON leads(provider_id);
CREATE INDEX idx_leads_status ON leads(status);
CREATE INDEX idx_leads_created_at ON leads(created_at);

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

## 14. Auth Rate Limits

CREATE TABLE auth_rate_limits (
    id SERIAL PRIMARY KEY,
    ip TEXT NOT NULL,
    action TEXT NOT NULL,  -- 'register' | 'login' | 'forgot' | 'reset'
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_auth_rate_limits_ip_action ON auth_rate_limits(ip, action);
CREATE INDEX idx_auth_rate_limits_created ON auth_rate_limits(created_at);

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