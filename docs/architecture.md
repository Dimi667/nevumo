# Nevumo Architecture Decisions

## Core Marketplace Model

Nevumo използва **Hybrid Marketplace Model**:

1. **Listing-based discovery (SEO-driven)**
2. **Lead-based conversion (primary monetization)**

---

## Why Hybrid?

### Listing only (Fiverr model) ❌
- Не работи добре за локални услуги
- Слаб SEO за long-tail
- Нисък conversion за сложни услуги

### Lead only (HomeAdvisor model) ❌
- Лош SEO
- Липса на trust (няма profiles/services)

### Hybrid ✅
- SEO pages (services + locations)
- Provider profiles (trust)
- Lead system (revenue engine)

---

## Core Entities

### 1. Users
- id
- email
- role: client | provider
- locale
- country

---

### 2. Providers
- id
- user_id
- business_name
- description
- languages[]
- countries[]
- rating
- verified

---

### Provider Availability (IMPORTANT)

Providers трябва да имат:

- available_cities[]
- service_radius (km, optional)
- availability_status (active | busy | offline)

Used for:
- filtering
- matching

---

### 3. Services
- id
- provider_id
- category_id
- title
- description
- price_type: fixed | hourly | request
- base_price (optional)

---

### 4. Categories
- id
- slug
- parent_id
- translations (32 languages)

---

### 5. Locations
- id
- country_code (ISO)
- city
- slug
- lat (optional)
- lng (optional)

---

### Location Strategy (CRITICAL)

Location трябва да бъде нормализирана:

- country_code (ISO)
- city_id (FK към locations)
- lat (optional)
- lng (optional)

НЕ използвай plain text location за matching.

---

### 6. Leads (🔥 CORE ENTITY)
- id
- client_id
- category_id
- city_id
- description
- budget (optional)
- provider_id (optional, for direct leads)
- source
- created_at

---

### Lead Status Lifecycle

- created
- pending_match
- matched
- contacted
- in_progress (future)
- completed (future)
- expired
- cancelled

---

### 7. LeadMatches
- id
- lead_id
- provider_id
- status: invited | accepted | rejected

---

### 8. Messages (future-ready)
- id
- lead_id
- sender_id
- content

---

## Core Flows

---

### 🔹 Flow 1: SEO → Provider (Listing Flow)

1. User lands on:
   /en/sofia/massage

2. Page shows:
   - providers
   - services
   - filters

3. User:
   → views provider profile  
   → contacts provider OR  
   → submits request (lead)

---

### 🔹 Flow 2: SEO → Lead (Primary Conversion)

1. User lands on SEO page  
2. Clicks "Request Service"  
3. Creates Lead  

System:
→ matches providers  
→ sends notifications  
→ providers respond  

---

### 🔹 Flow 3: Direct Provider Conversion

1. User opens provider profile  
2. Clicks "Contact"  
3. Creates lead linked to provider  

---

## Matching System (CRITICAL)

Initial version (simple & scalable):

Match by:
- category
- city_id
- language
- provider availability

Later upgrades:
- ranking by rating
- response time
- AI matching

---

## Lead Quality & Anti-Spam

- rate limiting per IP
- duplicate detection
- basic validation rules
- phone verification (future)

Goal:
- protect providers from spam
- maintain high lead quality

---

## Attribution Model

Track:

- source (seo | direct | widget | qr)
- utm_source
- utm_campaign
- provider_id
- landing_page
- country
- device_type

Used for:
- growth optimization
- provider analytics

---

## Database Design Strategy

### 🔹 PostgreSQL (Primary DB)
- relational data
- leads, users, providers

### 🔹 Redis
- translations cache
- session/cache layer
- hot queries

---

## Scaling Strategy

### Phase 1 (0–10k users)
- Single PostgreSQL instance
- Redis caching
- Basic indexing

---

### Phase 2 (10k–100k users)
- Read replicas
- Query optimization
- Background jobs (Celery / RQ)

---

### Phase 3 (100k+ users, multi-country)

#### 🔥 KEY DECISION: Region-aware architecture

Partition by:
- country
- or region

Options:
1. Single DB + partitioning  
2. Multi-DB per region (EU, US, etc.)

---

## API Design

- REST (FastAPI)

Future:
- GraphQL (optional)

---

## Frontend Architecture

- Next.js App Router
- Server Components for SEO pages
- Client components for interactions

---

## SEO Architecture (CRITICAL)

### URL Structure (ACTUAL)

- /{lang}/{city}/{category}
- /{lang}/{city}/{category}/{providerSlug}

Examples:
- /en/sofia/massage
- /en/sofia/massage/maria-petrova

---

### Strategy:
- programmatic SEO
- localized content (32 languages)
- SSR for indexing

---

## Monetization Strategy

Primary:
- pay-per-lead

Future:
- subscriptions (providers)
- featured listings
- ads

---

## What NOT to build early

❌ Booking system  
❌ Payments  
❌ Complex chat  
❌ Advanced reviews system  

---

## Future Extensions

- AI lead matching
- Auto-translation
- Smart pricing suggestions
- Provider ranking algorithm

---

## Embedded Lead Widget (CRITICAL GROWTH COMPONENT)

Nevumo предоставя **embeddable lead widget**, който providers могат да използват извън платформата.

---

### Purpose

- Capture leads извън Nevumo (external traffic)
- Increase provider adoption
- Enable viral growth via providers

---

### Entry Points

#### 1. Direct URL (Primary)

/{lang}/{city}/{category}/{providerSlug}

---

#### 2. Embeddable Widget (iframe / script)

Example:

<iframe src="https://nevumo.com/en/sofia/massage/maria-petrova" />

---

#### 3. QR Code (Offline → Online)

QR → opens provider lead page

Used for:
- business cards
- flyers
- physical locations

---

### Provider Ownership

Each provider има:

- unique public URL
- embeddable widget URL

This URL acts as:

- lead entry point
- tracking identifier
- provider funnel

This is a core part of provider acquisition strategy.

---

### UX Flow

1. User opens widget / page  
2. Sees provider info + trust signals  
3. Submits request  

→ lead is created  
→ assigned to provider  

---

### Lead Handling Logic

If lead is created via provider page:

- lead.provider_id = конкретния provider  
- НЕ се изпраща към други providers (default)

Optional (future):
- fallback matching ако provider не отговори  

---

### Data Tracking (IMPORTANT)

Track:

- source: seo | direct | widget | qr
- provider_id
- conversion rate per provider
- external vs internal traffic

---

### Technical Notes

- SSR (ultra-fast)
- mobile-first (QR usage)
- minimal friction (2 fields max)

---

### Benefits

- Providers стават distribution channel
- Zero-cost growth loop
- Works in 30+ countries
- Not dependent only on SEO

---

### Future Enhancements

- White-label widget
- Custom branding
- Provider analytics dashboard

---

## Provider Dashboard (Phase 1 — Backend + Frontend Complete)

### Endpoints (all under /api/v1/provider/, JWT required)

| Method | Path | Purpose |
|--------|------|---------|
| GET | /dashboard | KPIs + profile completeness |
| GET | /leads | Leads inbox |
| PATCH | /leads/{id} | Update lead status (contacted/done/rejected) |
| GET | /profile | Full provider profile |
| PATCH | /profile | Update business_name, description, availability_status |
| POST | /profile/image | Upload profile image (multipart, max 5MB) |
| GET | /services | List provider's services |
| POST | /services | Add service (= choose category for onboarding) |
| POST | /cities | Add city to provider profile |
| GET | /qr-code | QR code as base64 data URI + public URL |

### Lead Status State Machine
- new → contacted, rejected
- contacted → done, rejected
- done → (terminal)
- rejected → (terminal)

UI status mapping: DB statuses "created"/"pending_match"/"matched"/"invited" all map to "new" in dashboard.

### Onboarding Completeness Check
Provider is complete when ALL are true:
- business_name exists
- At least 1 service (= category selected)
- At least 1 city

Returned in dashboard response as profile.is_complete + profile.missing_fields[].

### Image Storage
- Phase 1: Local filesystem at uploads/provider_images/{provider_id}.{ext}
- Served via FastAPI StaticFiles mount at /static/provider_images
- Storage abstraction (save_provider_image in provider_service.py) ready for S3/R2 migration

### QR Code Generation
- Generated on-the-fly as base64 PNG data URI (no file storage needed)
- Encodes provider's public SEO URL: {APP_URL}/{lang}/{city_slug}/{category_slug}/{provider_slug}
- Uses qrcode[pil] library

### JWT Auth Chain
get_current_user (HTTPBearer → JWT decode → User lookup) → get_current_provider (User → Provider)
Both in dependencies.py alongside existing get_db/get_redis.

### Provider Dashboard Frontend (COMPLETE)

Layout: Sidebar (logo + nav links + "НАМЕРИ УСЛУГА" CTA) + TopBar with user info.

#### Pages (all under /[lang]/provider/dashboard/)

**Overview** — Stats cards (total leads, new leads, accepted matches, rating, verified status, availability). "Last 30 days" analytics preview section. Auto-redirect to Profile page if is_complete === false (forces onboarding).

**Leads** — Table with lead data (phone, description, status, source, date). Filter tabs by status (All, New, Contacted, Done, Rejected). Empty state when no leads.

**Services** — Grid of service cards showing: title, category, cities (as badges), price + currency, price_type. "Add Service" button. Each card has Edit and Delete buttons. Delete triggers confirmation dialog → DELETE endpoint. Add → empty "New Service" form. Edit → pre-filled "Edit Service" form. Empty state when no services.

**Analytics** — KPI cards (Total Leads, Contacted, Conversion %). Period toggle: 7 days / 30 days. Source breakdown horizontal bars (seo, direct, widget, qr).

**QR Code** — Dedicated page. "Generate" button → displays QR code image + public provider URL.

**Profile** — Two modes:
- New provider (is_complete === false): 2-step onboarding wizard
  - Step 1: Profile photo upload + Business name + Description
  - Step 2: Add First Service — Title, Category (select), City (single-select), Price Type (fixed/hourly/request/per_sqm), Price, Currency (13 currencies)
- Existing provider (is_complete === true): Edit mode with all profile fields

**Settings** — Account info display, Availability status toggle (Active/Busy/Offline), Public URL slug display, "Switch to Client" button, Logout button.

#### Client Dashboard
Minimal dashboard with "ПРЕДЛАГАЙ УСЛУГИ" button that triggers role switch to provider.

#### Role Switching
Provider ↔ Client switching works. Updates user role via API and redirects to appropriate dashboard.

#### Service Form Architecture
- Service creation/edit includes: title, category_id, city_ids[], description, price_type, base_price, currency
- currency field supports 13 currencies: EUR, BGN, USD, GBP, CHF, CZK, DKK, HUF, PLN, RON, SEK, NOK, TRY, ALL, MKD, RSD, BAM, HRK
- price_type supports: fixed, hourly, request, per_sqm
- Creating a service auto-syncs provider_cities for lead matching

---

## Event Tracking (IMPORTANT)

### Двуслойна система
1. **Google Analytics 4 (GA4)** — глобално, автоматично на всички страници чрез GoogleAnalytics компонент в root layout.tsx
2. **Custom DB tracking** — per-page events записвани в page_events таблица чрез POST /api/v1/page-events

### Shared utility
import { trackPageEvent } from "@/lib/tracking";
trackPageEvent("event_name", "page_name", { key: "value" });

Изпраща и към DB (sendBeacon) и към GA4 (gtag event) автоматично.

### Правило за нови страници
Всяка страница с user actions (клик на бутон, submit на форма, избор) ТРЯБВА да извиква trackPageEvent(). GA4 pageview се записва автоматично.

### page_events таблица
- id UUID, event_type TEXT, page TEXT, metadata JSONB, ip TEXT, user_agent TEXT, created_at TIMESTAMP

### Intent Persistence
- При клик на login card: localStorage записва nevumo_intent ("client" | "provider") и nevumo_lang
- Utility: lib/intent.ts — getStoredIntent() и clearStoredIntent()
- Auth и onboarding pages трябва да извикат clearStoredIntent() след като прочетат intent-а

---

## Authentication (Phase 1 — Email-based)

### Frontend Pages (COMPLETE — connected to real API)

#### /[lang]/auth — Login/Register/Forgot Password
- File: `apps/web/app/[lang]/auth/LoginClient.tsx` 
- Single page, multi-step flow (state machine: initial → login | register | forgot)
- Intent-based headers: reads `nevumo_intent` from localStorage (client | provider)
- Social login buttons: Google + Facebook (UI only, placeholder — OAuth integration later)
- Email step: validation, sessionStorage persistence (key: nevumo_auth_email)
- Login step: password + "Забравена парола?" link
- Register step: password with show/hide toggle + built-in password generator (onClick on empty field)
- Forgot step: sends reset link → success toast "Провери имейла си"; catch also shows success (no enumeration)
- All buttons: orange active (bg-orange-500), gray disabled (bg-gray-300)
- Browser password save: hidden iframe technique (triggerPasswordSave)
- Post-auth: `saveAuth(token, user)` → localStorage; redirect by role (provider → /provider/dashboard, client → /)
- Events: auth_view, auth_email_entered, auth_password_shown, auth_success

#### /[lang]/auth/reset-password — Reset Password
- File: `apps/web/app/[lang]/auth/reset-password/ResetPasswordClient.tsx` 
- Token from URL param: ?token=XYZ
- 5 states: loading, valid (form), success, expired/invalid, already used
- Password + confirm password with match validation
- Success: saveAuth() → "Паролата е сменена успешно" + "Логваме те..." + auto-redirect 2s
- Redirect by role (from JWT user) or localStorage intent; provider → /provider/dashboard
- Events: password_reset_view, password_reset_success, password_reset_error, token_expired, token_used

### Frontend Auth Lib
- `apps/web/lib/api.ts` — `ApiError` class + `apiPost<T>()` generic fetch wrapper
- `apps/web/lib/auth-types.ts` — `UserInfo`, `AuthResult`, `CheckEmailResult`, `ValidateTokenResult`, `MessageResult` 
- `apps/web/lib/auth-api.ts` — 6 typed functions wrapping `apiPost` 
- `apps/web/lib/auth-store.ts` — `saveAuth`, `getAuthToken`, `getAuthUser`, `clearAuth`, `isAuthenticated` 

### Backend Endpoints (COMPLETE — Phase A)
- POST /api/v1/auth/check-email → { exists: boolean }
- POST /api/v1/auth/register → { token: JWT, user: {id, email, role} }
- POST /api/v1/auth/login → { token: JWT, user: {id, email, role} }
- POST /api/v1/auth/forgot-password → { message } (always same response, no email enumeration)
- POST /api/v1/auth/reset-password → { token: JWT, user: {id, email, role} } (auto-login)
- POST /api/v1/auth/validate-reset-token → { valid: boolean, error?: 'expired' | 'used' }

### Security Measures
- bcrypt password hashing (direct bcrypt library, not passlib)
- Reset tokens: raw token in email, SHA-256 hash stored in DB — never raw in DB
- Rate limiting: 5 attempts / 15 min per IP per action (register/login/forgot/reset)
- Email normalization: lowercased + stripped on every input
- Password policy: minimum 8 characters (enforced in both Pydantic schema and frontend)
- No email enumeration: forgot-password always returns same response; login returns INVALID_CREDENTIALS for both wrong email and wrong password (with timing protection via dummy bcrypt verify)
- Account disabled: separate 403 ACCOUNT_DISABLED error code

### Backend Files
- `apps/api/routes/auth.py` — 6 endpoints, all errors as `{ success: false, error: { code, message } }` 
- `apps/api/services/auth_service.py` — hash_password, verify_password, create_jwt, decode_jwt, generate_reset_token, hash_token, send_reset_email, check_rate_limit, record_rate_limit
- `apps/api/config.py` — Settings (JWT_SECRET, JWT_EXPIRY_HOURS=720, RESET_TOKEN_EXPIRY_MINUTES=30, AUTH_RATE_LIMIT_MAX=5, AUTH_RATE_LIMIT_WINDOW_MINUTES=15, APP_URL)
- `apps/api/alembic/versions/a1b2c3d4e5f6_add_auth_tables.py` — migration

### Tech Decisions
- Password hashing: bcrypt (direct, bcrypt==4.2.1)
- JWT: python-jose, HS256, 30-day expiry
- JWT storage: localStorage Phase 1 (key: nevumo_auth_token + nevumo_auth_user)
- Reset tokens: secrets.token_urlsafe(32), expire 30 min, one-time use, SHA-256 hash in DB
- Email sending Phase 1: console log only (send_reset_email logs to stdout)
- Email sending Phase 2: TBD (Resend, SendGrid, or SMTP)
- OAuth: Google + Facebook (future, UI placeholders exist)

### Intent System
- localStorage key: nevumo_intent ('client' | 'provider')
- Set on homepage/landing when user clicks role card
- Read on auth pages for header text + post-auth redirect
- Cleared after successful auth (clearStoredIntent)
- Cross-device limitation: intent not available if reset link opened on different device → fallback to role from JWT user object

---

## Key Principles

- Keep backend simple
- Optimize for SEO first
- Leads = core revenue
- Avoid over-engineering
- Build for scale, but start lean