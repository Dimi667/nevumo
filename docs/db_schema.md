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
    city_id INTEGER REFERENCES locations(id),
    review_reply_email_enabled BOOLEAN NOT NULL DEFAULT TRUE,  -- Opt-in for review reply emails
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_review_reply_email ON users(review_reply_email_enabled);
CREATE INDEX idx_users_phone ON users(phone) WHERE phone IS NOT NULL;
CREATE INDEX idx_users_city_id ON users(city_id);

---

## 2. Providers

CREATE TABLE providers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE REFERENCES users(id) ON DELETE CASCADE,  -- NULL for unclaimed profiles
    business_name TEXT,
    description TEXT,
    slug TEXT UNIQUE NOT NULL,                -- URL slug, auto-generated from business_name
    slug_change_count INTEGER NOT NULL DEFAULT 0,
    profile_image_url TEXT,                   -- served at /api/v1/static/provider_images/
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
- **rating**: calculated as AVG(reviews.rating) - updated in real-time via get_provider_rating() (May 25, 2026: removed cached column updates, all ratings now calculated dynamically from Review table)
- **review_count**: calculated as COUNT(reviews) via get_provider_review_count() (May 25, 2026: added dynamic calculation)
- **jobs_completed**: calculated as COUNT(leads.status='done') + COUNT(lead_matches.status='done') via get_provider_jobs_completed()

### Промени в providers таблица (May 21, 2026)
- Добавена колона: `verification_level INTEGER NOT NULL DEFAULT 0`
- Index: `CREATE INDEX idx_providers_verification_level ON providers(verification_level);`
- Изчислява се автоматично от `calculate_verification_level()` при всяка промяна на профила

### Промени в providers таблица (June 23, 2026)
- Добавена колона: `scraped_email TEXT` — email от scraping за banner claim verification
- Добавена колона: `category_slug TEXT` — категория за scraped providers
- Notes:
  - Banner flow: verification created WITHOUT user_id (nullable) — user_id се попълва след като get_or_create_claim_user() създаде/намери потребителя в verify endpoint
  - Magic link tokens table: ще бъде добавена в Блокер 7Б

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

## 3c. Provider Images (Gallery)

CREATE TABLE provider_images (
    id          SERIAL PRIMARY KEY,
    provider_id UUID NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    url         TEXT NOT NULL,
    position    INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_provider_images_provider_id ON provider_images(provider_id);

Rules:
- Maximum 8 images per provider
- Position 0 = cover image (used in ProviderFullPage hero)
- Images stored at: uploads/provider_gallery/{provider_id}/{image_id}.webp
- Served via: /api/v1/static/provider_gallery/{provider_id}/{image_id}.webp

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
    locative_form TEXT,    -- grammatical locative case (e.g., Sofia → Sofii in PL)
    genitive_form TEXT,    -- grammatical genitive case (e.g., Sofia → Sofii in PL)
    UNIQUE(location_id, lang)
);

CREATE INDEX idx_location_translations_location ON location_translations(location_id);
CREATE INDEX idx_location_translations_lang ON location_translations(lang);

### Seeded Data (May 2026)
- 3 cities × 34 languages = 102 rows
- Sofia (BG), Belgrade (RS), Warszawa (PL)
- locative_form and genitive_form added May 2026 (Alembic: 20260510_add_locative_genitive_forms)
- Seed script: apps/api/scripts/seed_location_declension.py
- Славянски езици: хардкоднати форми; останалите: locative_form = genitive_form = city_name

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
    client_notes TEXT,    -- Client's private notes about the lead (added via migration r2s3t4u5v6w7)

    cancelled_by TEXT CHECK (cancelled_by IN ('client', 'provider')),
    status_changed_by TEXT NOT NULL DEFAULT 'system' CHECK (status_changed_by IN ('system', 'client', 'provider')),
    status_changed_at TIMESTAMP,

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
    status TEXT CHECK (status IN ('invited', 'accepted', 'rejected', 'contacted', 'done', 'cancelled')),
    -- Updated via migration cdf063316609 (April 24, 2026)
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(lead_id, provider_id)
);

CREATE INDEX idx_lead_matches_lead ON lead_matches(lead_id);

### Review Eligibility
- Only leads with LeadMatch.status IN ('contacted', 'done') are eligible for review
- This allows clients to review each provider who contacted them for a given lead

### Status Synchronization (May 25, 2026)
- When a client changes lead status via `PATCH /api/v1/client/leads/{lead_id}/status`, the corresponding `LeadMatch` record is automatically synchronized
- Synchronization occurs when `lead.provider_id` exists and the new status is not `cancelled`
- This ensures review eligibility is correctly tracked after client status changes
- Implementation: `apps/api/routes/client.py` (lines 132-143)

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

-- Note: Sequences for this table were synchronized in April 2026 to fix 500 errors 
-- caused by ID mismatches during manual migrations.
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

-- Note: Sequences for this table were synchronized in April 2026 to fix 500 errors.
CREATE INDEX idx_auth_rate_limits_ip_action ON auth_rate_limits(ip, action);
CREATE INDEX idx_auth_rate_limits_created ON auth_rate_limits(created_at);

---

## 17. Consent Logs (GDPR Compliance)

CREATE TABLE consent_logs (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    session_hash VARCHAR(64) NOT NULL,
    ip_hash VARCHAR(64) NOT NULL,
    categories JSONB NOT NULL,
    policy_version VARCHAR(20) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX ix_consent_logs_user_id ON consent_logs(user_id);
CREATE INDEX ix_consent_logs_created_at ON consent_logs(created_at);

### Purpose
GDPR compliance tracking for cookie consent decisions. Records all user consent choices with anonymized session and IP hashes for audit purposes. Retention: 24 months.

### Categories Structure
JSONB field stores consent state:
```json
{
  "necessary": true,
  "functional": boolean,
  "analytics": boolean,
  "marketing": boolean
}
```

---

## 18. Translations (i18n)

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
- **Validation**: **Mandatory namespacing**. Keys must contain at least one dot and cannot start or end with a dot. Enforced at the ORM layer (SQLAlchemy `@validates`) to ensure cache consistency and avoid flat keys.
- **Namespace separation**: Different feature areas use different namespaces for organization.

### Current Seeded Data (May 15, 2026)
- **homepage namespace**: 45 keys × 34 languages = 1,530 rows
- **category namespace**: 44 UI keys × 34 languages + 18 SEO keys × 34 languages = 1,496 + 612 = 2,108 rows
  SEO keys:
  - Cleaning: seo_cleaning_h2, seo_cleaning_h3_1, seo_cleaning_h3_2, seo_cleaning_p1, seo_cleaning_p2, seo_cleaning_p3 (6 keys)
  - Massage: seo_massage_h2, seo_massage_h3_1, seo_massage_h3_2, seo_massage_p1, seo_massage_p2, seo_massage_p3 (6 keys)
  - Plumbing: seo_plumbing_h2, seo_plumbing_h3_1, seo_plumbing_h3_2, seo_plumbing_p1, seo_plumbing_p2, seo_plumbing_p3 (6 keys)
- **category form keys (April 2026)**: 15 new keys × 34 languages = 510 rows
  Keys added: no_providers_title, no_providers_subtitle, form_subtext,
  how_it_works_label, how_step_1, how_step_2, how_step_3, what_need_label,
  chip_not_sure, details_label, details_placeholder, get_offers_btn,
  trust_multiple, trust_response, sticky_btn
- **category preposition keys (May 2026)**: 2 new keys × 34 languages = 68 rows
  Keys added: preposition_base, preposition_modified (for dynamic preposition logic)
- **category FAQ keys (May 2026)**: 7 new keys × 34 languages = 238 rows
  Keys added: faq_title, faq_cleaning_q1, faq_cleaning_q2, faq_cleaning_q3, faq_cleaning_a1, faq_cleaning_a2, faq_cleaning_a3
- **category price_on_request key (May 2026)**: 1 key × 34 languages = 34 rows
- **city namespace**: 39 keys × 34 languages = 1,326 rows (includes 10 hero keys added April 21, 2026; full 34-language support added June 1, 2026 - previously only EN, BG, PL)
- **city preposition keys (May 2026)**: 3 new keys × 34 languages = 102 rows
  Keys added: preposition_base, preposition_modified, footer_in (for dynamic preposition logic)
- **city declension keys (May 2026)**: 2 new keys × 34 languages = 68 rows
  Keys added: locative_form, genitive_form (for Polish grammatical declension)
  - locative_form: Used for "in {city}" context (e.g., Warszawa → Warszawie)
  - genitive_form: Used for "from {city}" context (e.g., Warszawa → Warszawy)
  - Currently seeded only for Warsaw (Warszawa) - other cities require separate seed script execution
  - Seed script: apps/api/scripts/seed_city_declension_translations.py
- **widget namespace**: 23 keys × 34 languages = 782 rows
- **auth namespace (May 27, 2026)**: Authentication-related translations
  - Keys: dismiss_button (added May 27, 2026 for LegalModal close button)
  - Total: 1 key × 34 languages = 34 rows
  - Seed script: seed_auth_translations.py (dismiss_button seeded from pwa.dismiss_button)
- **client_dashboard namespace**: Client dashboard UI strings
- **provider_dashboard namespace**: 168 keys × 34 languages = 5,712 rows (includes 8 onboarding hero keys added April 10, 2026)
  Keys include: nav_overview, nav_analytics, nav_leads, nav_qr_code, nav_reviews,
  nav_services, nav_settings, nav_profile, and all dashboard UI strings
- **terms namespace (May 15, 2026)**: Terms & Conditions page translations
  - Keys: page_title, meta_description, effective_date, version, pl_notice, art1_title through art15_title, art1_body through art15_body, annex1_title, annex1_body, download_pdf, online_form, back_to_home
  - Total: 20+ keys × 34 languages = 680+ rows
  - Seed scripts: seed_terms_p1.py, seed_terms_p1_bodies.py through seed_terms_p15_bodies.py, seed_terms_annex_bodies.py, seed_terms_buttons.py
- **withdrawal namespace (May 15, 2026)**: Withdrawal form page translations
  - Keys: page_title, page_description, label_service_description, label_contract_date, label_consumer_name, label_consumer_address, label_account_id, label_email, label_submission_date, optional, cancel, submit, submitting, error_service_description_required, error_contract_date_required, error_consumer_name_required, error_consumer_address_required, error_email_required, error_submission_date_required, success_title, success_message, back_to_home
  - Total: 19 keys × 34 languages = 646 rows
  - Seed script: seed_withdrawal_translations_4.py
- **cookies namespace (May 16, 2026)**: Cookie Policy page translations
  - Keys: s1_title, s1_text, s2_title, s2_text, s3_title, s3_text, s4_title, s4_text, s5_title, s5_text, s5_p_consent, s5_p_lang, s5_p_ga, s5_p_ga_id, s5_p_stripe_mid, s5_p_stripe_sid, s5_p_auth_token, s5_p_auth_user, s5_p_phone, s5_p_intent, s5_p_city, s5_p_auth_email, s5_type_cookie_1p, s5_type_cookie_3p, s5_type_localstorage, s5_type_sessionstorage, s5_ret_12mo, s5_ret_13mo, s5_ret_1y, s5_ret_30d, s5_ret_30min, s5_ret_sess_30d, s5_ret_cleared, s5_ret_session, s5_ret_session_tab, s6_chrome_path, s6_firefox_path, s6_safari_path, s6_edge_path, s7_role_google, s7_role_stripe, s7_role_vercel, s7_role_railway, s7_role_neon, s7_role_upstash, s7_role_cloudflare, s8_safeguard_sccs_dpf, s8_safeguard_sccs, s8_country_usa, s9_title, s9_text, s10_title, s10_text, s11_title, s11_authority_bg, s11_authority_pl, last_updated, back_to_home
  - Total: 41 keys × 34 languages + 12 keys (EN only table data) + 4 keys × 34 languages (browser paths) = 1,394 + 12 + 136 = 1,542 rows
  - Seed scripts: seed_cookies_p21.py (374 rows), seed_cookies_p22.py (306 rows), seed_cookies_p23.py (272 rows), seed_cookies_p24.py (408 rows), seed_cookies_table_data_p1.py (23 rows), seed_cookies_browser_paths_p2.py (68 rows), seed_cookies_browser_paths_p3.py (68 rows), seed_cookies_back_to_home.py (34 rows)
- **provider_terms namespace (May 17, 2026)**: Terms & Conditions for Service Providers page translations
  - Keys: page_title, meta_description, effective_date, version, pl_notice, art1_title through art18_title, art1_body through art18_body, annex1_title, annex1_body, annex2_title, annex2_body, footer
  - Total: 50+ keys × 34 languages = 1,700+ rows
  - Seed scripts: 23 scripts (seed_provider_terms_p1_meta.py through seed_provider_terms_p23_footer.py)
    - p1_meta: page_title, meta_description, effective_date, version (4 keys × 34 langs = 136 rows)
    - p2_ui: pl_notice (1 key × 34 langs = 34 rows)
    - p3_titles1: art1_title through art5_title (5 keys × 34 langs = 170 rows)
    - p4_titles2: art6_title through art10_title (5 keys × 34 langs = 170 rows)
    - p5_titles3: art11_title through art15_title (5 keys × 34 langs = 170 rows)
    - p6_titles4: art16_title through art18_title (3 keys × 34 langs = 102 rows)
    - p7_titles5: annex1_title, annex2_title (2 keys × 34 langs = 68 rows)
    - p8_art1_body: art1_body (1 key × 34 langs = 34 rows)
    - p9_art2_body: art2_body (1 key × 34 langs = 34 rows)
    - p10_art3_body: art3_body (1 key × 34 langs = 34 rows)
    - p11_art4_body: art4_body (1 key × 34 langs = 34 rows)
    - p12_art5_body: art5_body (1 key × 34 langs = 34 rows)
    - p13_art6_body: art6_body (1 key × 34 langs = 34 rows)
    - p14_art7_body: art7_body (1 key × 34 langs = 34 rows)
    - p15_art8_body: art8_body (1 key × 34 langs = 34 rows)
    - p16_art9_body: art9_body (1 key × 34 langs = 34 rows)
    - p17_art10_body: art10_body (1 key × 34 langs = 34 rows)
    - p18_art11_body: art11_body (1 key × 34 langs = 34 rows)
    - p19_art12_body: art12_body (1 key × 34 langs = 34 rows)
    - p20_art13_14_body: art13_body, art14_body (2 keys × 34 langs = 68 rows)
    - p21_art15_16_body: art15_body, art16_body (2 keys × 34 langs = 68 rows)
    - p22_art17_18_body: art17_body, art18_body (2 keys × 34 langs = 68 rows)
    - p23_footer: annex1_body, annex2_body, footer (3 keys × 34 langs = 102 rows)
  - Documentation: Full legal content in docs/terms_conditions_providers_nevumo.md (EN + BG + PL versions)
- **city nav CTA keys (May 20, 2026)**: 2 new keys × 34 languages = 68 rows
  Keys added: nav_cta_line1, nav_cta_line2 (for city page "Become a Specialist" CTA link)
  Seed script: apps/api/scripts/seed_city_nav_cta_translations.py
- **contact_dsa namespace (May 21, 2026)**: 9 keys × 34 languages = 306 rows
  Keys added: s3_title, s3_what_to_include_title, s4_title, s5_title, back_to_home, s3_body, s3_what_to_include_body, s4_body, s5_body
  Purpose: DSA (Digital Services Act) Contact Point page - Article 11 compliance
  Seed scripts: seed_contact_dsa_p1.py, seed_contact_dsa_p2.py
- **provider_page namespace (May 23, 2026)**: 6 keys × 34 languages = 204 rows
  Keys added: price_per_hour, price_on_request, request_service, select_this_service, service_selected_confirm, service_deselect
  Purpose: Provider page pricing display, service card button text, and service selection toggle UI
  Seed scripts: seed_provider_page_price_units.py, seed_provider_page_translations_p2.py, seed_provider_page_service_select.py
- **Total rows**: 12,500+ translations across all namespaces

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
    UNIQUE(lead_id, provider_id)  -- one review per lead per provider
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
- One review per lead/provider combination (enforced by UNIQUE(lead_id, provider_id))
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

---

## Outreach Unsubscribes

CREATE TABLE outreach_unsubscribes (
    email TEXT PRIMARY KEY,
    unsubscribed_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    reason TEXT CHECK (reason IN ('user_request', 'bounce', 'complaint'))
);

### Notes
- Added: June 22, 2026 — Blocker 3 (GDPR/RODO unsubscribe mechanism)
- Alembic migration: u1v2w3x4y5z6_add_outreach_unsubscribes.py

---

## Outreach Events

CREATE TABLE outreach_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resend_message_id TEXT NOT NULL,
    email TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ DEFAULT NOW() NOT NULL
);
CREATE INDEX idx_outreach_events_email ON outreach_events(email);
CREATE INDEX idx_outreach_events_type ON outreach_events(event_type);
CREATE INDEX idx_outreach_events_occurred ON outreach_events(occurred_at);

### Notes
- Added: June 22, 2026 — Blocker 4 (Resend Webhooks)
- Alembic migration: v1w2x3y4z5a6_add_outreach_events.py
- Populated by POST /api/v1/webhooks/resend (svix signature verification)
- event_type values: email.sent, email.delivered, email.opened, email.clicked, email.bounced, email.complained
- email.bounced → also writes to outreach_unsubscribes (reason='bounce')
- email.complained → also writes to outreach_unsubscribes (reason='complaint')
- Used for 30-day campaign analytics (Section 7 of claimed_profiles_plan_2.md)
- email is PRIMARY KEY (one record per address, idempotent)
- reason='user_request' — set when user clicks unsubscribe link in email
- reason='bounce' — reserved for Resend webhook (Blocker 4)
- reason='complaint' — reserved for Resend webhook (Blocker 4)
- Checked by send_outreach_bulk.py before every send (DB query, not CSV)

---

## Outreach Sequence Log

CREATE TABLE outreach_sequence_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    business_name TEXT,
    category TEXT,
    sequence_step INTEGER NOT NULL,
    resend_message_id TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW() NOT NULL,
    status TEXT NOT NULL DEFAULT 'sent',
    UNIQUE(email, sequence_step)
);
CREATE INDEX idx_outreach_seq_email ON outreach_sequence_log(email);

### Notes
- Added: June 22, 2026 — Blocker 5 (replaces outreach_sent_log.csv)
- Alembic migration: w1x2y3z4a5b6_add_outreach_sequence_log.py
- Commits: 4cbdb17 (implementation), d70616d (alembic merge migrations)
- Replaces local CSV file `outreach_sent_log.csv` — reliable with Railway scheduler + multi-instance
- UNIQUE(email, sequence_step) provides built-in idempotency
- status values: 'sent', 'failed'
- category values: 'cleaning', 'plumbing', 'massage'
- sequence_step values: 1, 2, 3, 4 (one per outreach email)
- Written by send_outreach_bulk.py via ON CONFLICT DO NOTHING (idempotent inserts)
- Dry-run mode: NO DB writes (read-only behavior preserved)
- Used by Railway scheduler (run_outreach_sequence.py — Blocker 8) to track sequence state
- Used for 30-day campaign analytics query (Section 7 of claimed_profiles_plan_2.md)