# Nevumo Architecture Decisions

## 2026 Architectural Overhaul

This document reflects the major architectural optimization performed in April 2026, which unified the project into a high-performance monorepo.

### 1. New Monorepo Structure & Path Logic
- **Unified Root**: The project is now a clean monorepo managed by **Turborepo**.
- **Path Optimization**: `apps/api` and `apps/web` are decoupled but share a consistent environment. All shared logic is moved to `packages/*`.
- **Venv Relocation**: The backend virtual environment is strictly at `/Users/dimitardimitrov/nevumo/apps/api/.venv`. All local execution (scripts, uvicorn) should point there.

### 2. Docker & Containerization Strategy
- **Optimized Dockerfiles**: Implemented multi-stage builds (Build-stage + Run-stage) to minimize image size and maximize build speed.
- **Docker Compose Orchestration**: The root `docker-compose.yml` manages `nevumo-api`, `nevumo-web`, `nevumo-postgres`, and `nevumo-redis`.
- **Volume Mapping**: Local development uses volume mapping (`./:/workspace`) to ensure hot-reload works correctly across the monorepo.
- **Static File Routing (April 20, 2026)**: The static file mount point was changed from `/static/provider_images` to `/api/v1/static/provider_images` to bring it under the versioned API namespace. The `STATIC_FILES_BASE_URL` is now an empty string by default to support relative routing when served from the same domain/proxy.

### 3. SQLAlchemy & Models (The 'Base' Fix)
- **Centralized Base**: All SQLAlchemy models now inherit from a single `Base` defined in `apps/api/database.py`.
- **Explicit Imports**: To prevent 'table not found' errors during migrations or `docker exec` sessions, all models are explicitly imported into `database.py`.
- **SessionLocal Standardization**: `SessionLocal` usage is standardized for both the API and CLI commands to ensure consistent transaction management.

### 4. Networking & Environment
- **Centralized URL Management**: All internal and external URL addresses are managed through environment variables to ensure consistency across development, staging, and production environments.
- **Key Environment Variables**:
  - `APP_URL`: The public base URL of the frontend application (e.g., `http://localhost:3000` in dev). Used for generating magic links, reset emails, and QR codes.
  - `STATIC_FILES_BASE_URL`: The public base URL of the API server. Used for generating absolute URLs for uploaded images and other static assets.
  - `NEXT_PUBLIC_API_URL`: The URL used by the frontend to communicate with the backend. In SSR, this might be an internal Docker URL (e.g., `http://nevumo-api:8000`), while in the browser, it is the public API URL.
- **Inter-container Communication**: Containers in Docker Compose communicate using service names (e.g., `nevumo-api`, `nevumo-postgres`) rather than `localhost`.
- **CORS Configuration (April 2026)**: Added `CORSMiddleware` to `apps/api/main.py` using a configurable `CORS_ORIGINS` setting from `.env` (via `load_dotenv()`) to allow secure communication from the frontend domain.

### 5. Next.js & UI (Metadata + i18n)
- **Universal Slug Generation (April 30, 2026)**: Unified URL slug generation logic between Frontend and Backend to support all 34 languages.
  - **Frontend**: Removed the hardcoded 'bg' locale from `apps/web/lib/slug-utils.ts` and replaced the primitive implementation in `apps/web/lib/slugify.ts` with the robust `slugify` library.
  - **Backend**: Standardized `apps/api/services/provider_service.py` to use a consistent `slugify` wrapper with pre-defined Cyrillic replacements, ensuring identical output for special characters (Turkish İ/ı, German ü/ö, Icelandic ð/þ, etc.) across the entire stack.
- **PRODUCTION_READY_AUTH**: Implemented session checks and BFCache (Back-Forward Cache) handling in the authentication flow. Replaced legacy hidden iframe hacks with the modern **Credential Management API** (`navigator.credentials.store`) for robust password saving across all modern browsers including iOS Safari.
- **Client Dashboard Optimization (April 2026)**: Resolved issues where client data was not loading correctly after a role switch, implemented robust status tracking for leads and reviews, synchronized missing translation keys for the dashboard overview, and integrated `ClientLeadDetailModal` into the requests page.
- **Dynamic User Intent Navigation (April 30, 2026)**: Implemented "City-First" navigation logic for clients. The "Find Service" button in the dashboard (Overview, Sidebar, Requests, and Reviews) now dynamically links based on the `last_city_slug` returned by the API via a multi-layer fallback chain:
   - **Fallback Chain**: 
     1. user.city_id
     2. Last lead as client
     3. City from provider's last service (if user is a provider)
     4. null
   - **last_city_slug present** → Redirect to `/[lang]/[last_city_slug]` (returns user to their relevant local market).
   - **last_city_slug is null** → Redirect to `/[lang]/izberi-grad` (City Selection page).
   Maximizes conversion by returning users to their relevant context while providing a clear selection path if no history exists.
- **City Landing Page SEO Optimization (April 30, 2026)**:
  - **Canonical Tags**: Added absolute canonical URLs to `apps/web/app/[lang]/[city]/page.tsx` using `NEXT_PUBLIC_SITE_URL` environment variable.
  - **JSON-LD Implementation**:
    - Integrated `Organization` and `WebSite` schemas from `apps/web/lib/seo.ts`.
    - Added `LocalBusiness` schema using `generateLocalBusinessJsonLd`.
    - **I18n Compliance**: Schema data (name, description, services) is fully localized using the `lang` parameter and `city` namespace translations.
    - **Pseudo-Provider Pattern**: Since the city landing page does not have a single provider, a pseudo-provider object representing the platform's presence in the city is used to satisfy the `LocalBusiness` schema requirement.

### Automated SEO Infrastructure (April 30, 2026)
The system now implements a fully automated SEO strategy for City Landing pages, ensuring production-ready technical SEO across all 34 supported languages:

#### Canonical Tag Generation
- **Implementation**: `apps/web/app/[lang]/[city]/page.tsx` automatically generates absolute canonical URLs
- **Environment Variable**: Uses `NEXT_PUBLIC_SITE_URL` to construct canonical links
- **Purpose**: Prevents duplicate content issues by specifying the canonical version of each city landing page
- **Scope**: Applied to all city landing pages across all language variants

#### JSON-LD Structured Data
Three types of structured data schemas are automatically generated for each city landing page:

1. **Organization Schema** (`apps/web/lib/seo.ts`)
   - Describes Nevumo as a business entity
   - Includes: name, url, logo, contact information
   - Serves as the foundation for all city-specific business data

2. **WebSite Schema** (`apps/web/lib/seo.ts`)
   - Defines the website structure and search functionality
   - Includes: name, url, potentialAction (SearchAction)
   - Enables rich search results in Google

3. **LocalBusiness Schema** (`generateLocalBusinessJsonLd`)
   - **Purpose**: Represents Nevumo's presence in each specific city
   - **Pseudo-Provider Pattern**: Since city pages don't have a single provider, a pseudo-provider object represents the platform's local presence
   - **Fields Included**:
     - `@type`: LocalBusiness
     - `name`: Localized city name + "Nevumo"
     - `description`: Localized description from `city` namespace translations
     - `url`: Absolute URL to the city landing page
     - `areaServed`: City and country information
     - `priceRange`: Dynamic price range from `/api/v1/price-range` endpoint
     - `aggregateRating`: Platform-wide rating (if available)
   - **I18n Compliance**: All text fields (name, description, services) are fully localized using the `lang` parameter and `city` namespace translations

#### Universal Multi-Language Slug Logic
The slug generation system has been unified across the entire stack to support special characters from all 34 languages:

- **Frontend** (`apps/web/lib/slug-utils.ts`):
  - Removed hardcoded `locale: 'bg'` parameter
  - Replaced primitive implementation in `apps/web/lib/slugify.ts` with the robust `slugify` library
  - Dynamic locale handling based on the current language context

- **Backend** (`apps/api/services/provider_service.py`):
  - Standardized slug generation with a consistent `slugify` wrapper
  - Pre-defined character replacements for special characters across 34 languages:
    - Turkish: İ → i, ı → i
    - German: ü → u, ö → o, ä → a, ß → ss
    - Icelandic: ð → d, þ → th
    - Cyrillic: Full transliteration support for all Cyrillic-based languages
  - Ensures identical slug output between frontend and backend

- **Result**:
  - Consistent URL structure across all languages
  - No duplicate content issues from slug variations
  - SEO-friendly URLs that preserve language-specific character semantics
  - Scalable to 10,000+ locations without slug conflicts

#### Production Readiness
The automated SEO infrastructure is designed for:
- **Scalability**: Can handle 10,000+ city landing pages without manual intervention
- **Consistency**: All pages follow the same SEO pattern across all languages
- **Performance**: JSON-LD and canonical tags are generated server-side (SSR) for optimal page load speed
- **Compliance**: Follows Google's structured data guidelines and SEO best practices

### Docker Environment Variable Pattern (April 27, 2026)
Next.js in Docker requires two separate environment variables to handle server-side and client-side API communication correctly:

- **API_URL=http://nevumo-api:8000** — Used server-side (SSR, Next.js rewrites) for container-to-container communication within the Docker network
- **NEXT_PUBLIC_API_URL=http://localhost:8000** — Used client-side (browser) for API calls from the user's browser

This pattern is applied in:
- **docker-compose.yml**: Both `API_URL` and `NEXT_PUBLIC_API_URL` are defined in the web service environment section
- **apps/web/lib/api.ts**: `API_BASE` checks `process.env.API_URL` first, then falls back to `NEXT_PUBLIC_API_URL`
- **apps/web/lib/ui-translations.ts**: Same fallback pattern for translation fetching
- **apps/web/next.config.mjs**: Rewrites use `process.env.API_URL || process.env.NEXT_PUBLIC_API_URL`

This separation ensures that:
- Server-side rendering can reach the backend container via Docker network
- Client-side browser requests reach the backend via localhost port forwarding
- Development and production environments work consistently without hardcoded URLs
- **Client Notes Feature (April 21, 2026)** — COMPLETE:
  - **DB:** New column `leads.client_notes TEXT` (nullable) — migration r2s3t4u5v6w7
  - **Backend:**
    - New endpoint: `PATCH /api/v1/client/leads/{lead_id}/notes` (ownership check: lead.client_id == user.id)
    - `GET /api/v1/client/leads` and `GET /api/v1/client/dashboard` now accept `?lang=` param and return localized `category_name`
    - Schemas added: `ClientLeadNotesUpdate`, `ClientLeadNotesUpdateResponse`
    - `ClientLeadListItem` updated with `client_notes` field
  - **Frontend:**
    - New component: `apps/web/components/client/ClientLeadDetailModal.tsx`
      - Opens on card click in requests page
      - Shows: ДАТА, СПЕЦИАЛИСТ (provider link OR broadcast msg), STATUS, ВАШЕТО СЪОБЩЕНИЕ ДО СПЕЦИАЛИСТА
      - Private notes textarea: debounced 500ms autosave + blur save
      - Button: "Запази и затвори" (btn_save_and_close)
    - `RequestsClient.tsx`: cards clickable, description preview, note preview/CTA with SVG pencil icon, broadcast message instead of "Marketplace"
    - `OverviewClient.tsx`: recent lead cards clickable → navigate to /requests?open={lead_id} to auto-open modal; broadcast message instead of "Marketplace"
    - `client-api.ts`: ClientLead interface + updateClientLeadNotes() + lang param on getClientLeads() and getClientDashboard()
  - **Translations:** 10 keys in `client_dashboard` namespace × 34 languages = 340 rows
    - modal_title_request, label_specialist, label_your_message, msg_broadcast_lead
    - label_client_notes, placeholder_client_notes, btn_save_and_close, btn_add_note
    - (+ 2 existing reused: label_date, label_status)
    - Seed script: `apps/api/scripts/seed_client_notes_translations.py`
  - **Dual Role Architecture (April 2026)** — UPDATED:
  - **PROBLEM:** One user can be both provider and client simultaneously (two tabs open). However, a provider accidentally landing on the client dashboard and clicking "Become a provider" received an `ALREADY_IN_ROLE` error.
  - **SOLUTION:** 
    - Kept ownership-based security on the backend.
    - Added a frontend guard in `apps/web/app/[lang]/client/dashboard/layout.tsx` that decodes the JWT and redirects users with `role === 'provider'` to the provider dashboard.
    - Added a frontend check in `apps/web/components/dashboard/DashboardSidebar.tsx` that checks `user.role === 'client'` before calling `switchRole('client')`. If already a client, it redirects directly to the client dashboard.
  - **Result:** Providers are automatically steered to the correct dashboard, and clients in the provider dashboard can switch back without API errors.
- **Category Page Fix (April 2026)** — COMPLETE:
  - **PROBLEM:** CATEGORY_CONTENT keyed by Polish slugs (masaz, sprzatanie, hydraulik); URLs use English slugs (cleaning, massage, plumbing) → always showed cleaning content
  - **SOLUTION:** Re-keyed CATEGORY_CONTENT, CategoryKey type, relatedLinksByCategory from Polish to English slugs
  - Removed categorySlugMap and categoryKeyMap — getApiSlug() is now identity function
  - File: apps/web/app/[lang]/[city]/[category]/page.tsx
  - **Result:** /bg/warszawa/plumbing correctly shows plumbing content
- **Client Dashboard Localization (April 2026)** — COMPLETE:
  - GET /api/v1/client/leads: added lang query param, category_name now localized
  - GET /api/v1/client/dashboard: added lang query param, category_name in recent_leads now localized
  - ClientLeadsQueryParams schema: added lang field (was causing 422 without it)
  - Frontend passes lang to both API calls
- **Lead Rate Limiting UX (April 2026)**: The lead submission flow now gracefully handles rate limiting by returning the ID of the last successful lead. This allows users to "Claim" their request via email even if they hit the rate limit on a subsequent attempt, significantly improving UX for edge cases.
- **Client Components in Server Pages (April 2026)**: Interactive elements that require browser APIs (e.g., `IntersectionObserver`, DOM manipulation) must be extracted into dedicated `'use client'` components. Inline `<script>` tags with `dangerouslySetInnerHTML` that mutate DOM outside React cause hydration mismatches. Use `useRef`, `useEffect`, and an `isMounted` state pattern to ensure client-only behavior while preserving SSR output. Reference implementation: `apps/web/components/homepage/MobileStickyCTA.tsx`.
- **Namespaced Translations Validator**: Implemented a mandatory `namespace.key` pattern at the ORM layer to ensure all UI copy is properly organized and to avoid cache conflicts.
- **Redis Sync**: After updating translations in the database, Redis MUST be flushed (`FLUSHALL`) to clear the cache and reflect changes in the UI.

---

## Core Marketplace Model

Nevumo използва **Hybrid Marketplace Model**:

1. **Listing-based discovery (SEO-driven)**
2. **Lead-based conversion (primary monetization)**

---

## Backend
- FastAPI
- Python 3.13.12
- SQLAlchemy (ORM)
- Pydantic v2 + pydantic-settings (validation + config)
- bcrypt 4.2.1 (password hashing)
- python-jose (JWT — HS256, 30-day tokens)
- Alembic (migrations)
- python-slugify (URL slug generation)
- qrcode[pil] (QR code generation for provider growth tools)
- python-multipart (file upload support)
- apscheduler>=3.10.0 (background jobs for magic link delivery)
- tzlocal>=3.0 (timezone support for APScheduler)
- Backend packaging/runtime: absolute `apps.api.*` imports with module-based startup/scripts
- STATIC_FILES_BASE_URL: Environment variable for proper static file URL generation (images, etc.)
- Docker runtime must expose the monorepo root on `PYTHONPATH` so the top-level `apps` package is importable
- Current container alignment uses:
  - `PYTHONPATH=/workspace`
  - `working_dir=/workspace/apps/api`
  - `uvicorn apps.api.main:app`
  - repo-root bind mount (`./:/workspace`) in local compose development

---

## Frontend Workspace Runtime Layout

- Frontend Docker compose development now uses the monorepo root as the `web` build context, matching the `api` service pattern
- The `web` container installs dependencies from the root workspace so npm can resolve local packages from `packages/*` and sibling workspaces from `apps/*`
- **Next.js 16 Routing**: The application has migrated from `middleware.ts` to `proxy.ts` to comply with Next.js 16 requirements.
- **Proxy Interface**: The `proxy.ts` file must use a `default` export for the main interceptor function (previously `middleware`).
- Current container alignment uses:
  - `context: .`
  - `dockerfile: apps/web/Dockerfile`
  - `working_dir=/workspace/apps/web`
  - repo-root bind mount (`./:/workspace`) in local compose development
  - Next dev server bound to `0.0.0.0:3000` inside the container

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

### Location Display Name System
- `slug` — used for URL routing only, never changes (SEO-stable)
- `city` — local official name stored in locations table (e.g., "Warszawa", "Beograd")
- `city_en` — English name in locations.city_en, used as internal/admin fallback
- `city_name` — translated display name from location_translations for UI rendering
- GET /api/v1/cities?lang={lang}&country={country_code} returns translated city_name as `city` field
- GET /api/v1/cities/active?lang={lang} returns all cities with at least one active provider across all countries
- GET /api/v1/cities/{slug}?lang={lang} returns translated city_name as `city` field (IMPORTANT: this endpoint returns the object directly, not wrapped in `data`)
- Fallback chain: location_translations.city_name → locations.city_en → locations.city
- Adding a new city requires: 1) row in locations, 2) rows in location_translations for all 34 languages
- Backend: apps/api/routes/cities.py uses LEFT OUTER JOIN on LocationTranslation

### City Selection Page (April 30, 2026)
- **Route**: `/[lang]/izberi-grad`
- **Purpose**: A landing page for users to select their city before browsing services.
- **Fetch**: Uses `GET /api/v1/cities/active?lang={lang}` to list only cities with active providers.
- **UI**: Displayed as a grid of cards with city names and country codes.
- **SEO**: Indexed, with English metadata by default.
- **Persistence**: The slug `izberi-grad` is fixed across all languages to maintain SEO stability.

### Frontend City Data Fetching (Next.js SSR)
- **Problem**: Next.js SSR can cache `fetch()` calls aggressively. If a city name is updated in the DB, the frontend might still show the old name.
- **Problem**: The API endpoint `/api/v1/cities/{slug}` returns the city object directly (e.g., `{"id": 2, "city": "Варшава", ...}`), while most other endpoints return a wrapped success object (`{"success": true, "data": { ... }}`).
- **Solution**: Use `cache: 'no-store'` in `fetch()` calls for city data to ensure fresh translations.
- **Solution**: Correctly handle the unwrapped JSON response in `apps/web/lib/api.ts`'s `getCityBySlug` function.
- **Cache Invalidation**: After updating `location_translations`, always flush Redis: `docker exec nevumo-redis redis-cli FLUSHALL`.

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

`client_id` remains nullable for anonymous public submissions and is populated automatically when the same public flow is used with a valid authenticated JWT.

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

### Retro-Matching (Provider Registration)
When a provider adds their first service, the system automatically runs retro-matching:
- Queries all leads with status 'created' or 'pending_match' matching the service category + cities
- Bulk inserts LeadMatch rows (status: 'invited') for each unmatched lead
- Updates matched lead statuses from 'created' to 'pending_match'
- Triggered from POST /api/v1/provider/services after successful service creation
- Errors are caught and logged — service creation response is never blocked
- Returns retro_matched_leads count in service creation response

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
 
 ### Namespaced Translations Endpoint
 - Public endpoint: `GET /api/v1/translations?lang={lang}&namespace={namespace}`
 - Reads from the `translations` table where records are stored as `namespace.key`
 - Returns a flat JSON object without the namespace prefix so frontend consumers can access keys directly
 - Redis caches payloads by language and namespace for 1 hour using `translations:{lang}:{namespace}`
 - When a requested language is not `en`, the backend merges English rows with localized rows and returns localized keys first with per-key English fallback for anything missing

### Translation System Architecture
- **Source of truth**: PostgreSQL `translations` table
- **Translation Key Validation (Mandatory)**: All keys MUST follow the `namespace.key` pattern (e.g., `auth.login_title`). This is enforced at the **SQLAlchemy model level** (`@validates`) and the **Pydantic schema level**. Keys without at least one dot will trigger a validation error.
- Translation content is stored as `namespace.key` rows, for example `homepage.hero_title` and `category.form_btn`
- The database is the authoritative content layer for UI copy across homepage, category pages, reviews, and future market surfaces
- Backend translation reads are namespace-scoped, which keeps payloads small and frontend usage simple

### Redis Namespaced Translation Cache
- Cache key pattern: `translations:{lang}:{namespace}`
- TTL: 1 hour (`3600` seconds)
- Cache sits in front of DB reads for hot public UI namespaces
- Cache is language-aware and namespace-aware, so homepage/category payloads do not invalidate each other
- Current implementation caches non-empty payloads only

### Frontend Translation Fetching
- Shared utility: `apps/web/lib/ui-translations.ts`
- `fetchTranslations(lang, namespace)` is the single frontend entry point for public UI namespace translations
- Runs in SSR/server contexts for metadata generation and page rendering
- Normalizes unsupported languages to `en` before calling the API
- Uses environment-aware fetch caching:
  - development: `cache: 'no-store'`
  - production: Next.js `revalidate: 3600`
- Consumers use `t(dict, key, fallback)` to keep rendering resilient when keys are missing
- Provider dashboard now centralizes `provider_dashboard` loading in `apps/web/lib/provider-dashboard-i18n.tsx`, with `DashboardI18nProvider` mounted in the dashboard layout so pages and shared dashboard components read one shared dictionary and locale-aware date formatter

### Translation Fallback Chain
- Requested language is attempted first
- If the namespace has no rows for that language, backend falls back to `en`
- If English also has no rows, the endpoint returns an empty object
- Frontend can additionally supply local fallback strings through `t()` for critical UI rendering

### Market Scaling Principle
- New market launch should require **DB seeding only**, not new translation-fetching code paths
- Homepage/category/review pages consume the same namespaced translation endpoint regardless of market
- Operational rule: adding a new market means inserting translation rows for that locale and namespace set, with zero application logic changes

### SSR Absolute URL Rule (CRITICAL)

**Problem:** Next.js SSR runs `fetch()` calls on the server. Relative URLs like `/api/v1/...` fail silently server-side — the server has no base URL context. Result: all translation fetches return empty, page renders in English regardless of the URL language segment.

**Mandatory pattern for every file that fetches from the API:**
```typescript
const API_BASE = typeof window === 'undefined'
  ? (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000')
  : '';
```

**Files where this is applied:**
- `apps/web/lib/ui-translations.ts` 
- `apps/web/lib/api.ts` 
- `apps/web/lib/auth-api.ts` 
- `apps/web/lib/provider-api.ts` 
- `apps/web/lib/client-api.ts` 
- `apps/web/lib/tracking.ts` 
- `apps/web/lib/locales.ts` 

**Rule for new files:** Any new lib file or SSR page that calls `fetch('/api/v1/...')` MUST use this pattern. Client components (`'use client'`) are exempt.

**Production checklist:**
- `NEXT_PUBLIC_API_URL` must point to the real backend URL in production `.env` 
- Never hardcode `localhost` anywhere
- Test every new SSR page from a second device on the same network before deploying

### Widget Translation Namespace
- All provider widget UI strings are stored in the `widget` namespace of the `translations` table
- Keys follow the pattern `widget.key_name` (e.g., `widget.button_text`, `widget.phone_label`)
- Backend serves them via `get_widget_translations(lang, db)` in `apps/api/routes/providers.py`
- Frontend `ProviderWidget` receives them as `provider.translations` prop and accesses via `const t = provider.translations`
- Fallback: three-layer fallback chain — hardcoded defaults → English DB → target language DB
- Total keys: 24 per language (added `widget.send_request_to` in April 27, 2026)
- Seed script: apps/api/scripts/seed_widget_send_request_to.py for new keys

### Provider Dashboard i18n Architecture

#### Overview
The Provider Dashboard uses a dedicated `provider_dashboard` translation namespace with 339 keys across 34 languages. Translations are fetched once at the layout level via `DashboardI18nProvider` and shared across all dashboard pages and components.

#### Frontend Flow
1. Dashboard layout mounts `DashboardI18nProvider` from `apps/web/lib/provider-dashboard-i18n.tsx`
2. Provider fetches translations for namespace `provider_dashboard` on load using `useTranslation('provider_dashboard', lang)`
3. The hook returns a scoped `t` function that automatically prefixes keys with the namespace
4. All pages and components consume translations via `useDashboardI18n()` which provides `{ t, lang }`
5. Translation calls use pattern `t(key, fallback)` for resilient rendering (no dict parameter needed)
6. The scoped `t` function internally constructs the full key as `provider_dashboard.{key}`

#### Backend Source of Truth
Translation seed data lives in `apps/api/scripts/seed_provider_dashboard_translations.py`:
- `row(*values)` — full multilingual row with 34 language values
- `row_bg(en, bg)` — Bulgarian/English dual with English fallback for other locales
- `CLIENT_DASHBOARD_TRANSLATIONS` — alias reuse where client and provider share identical strings

#### Polish Translation Fix (April 2026)

**Failure Mode:**
Many keys were seeded via `row_bg(...)` which returns Bulgarian for `bg` and English for all other locales. This caused Polish (`pl`) translations to incorrectly display English text instead of Polish.

**Remediation Approach:**
1. **DB-driven audit** — Extracted all `t(dict, key, fallback)` keys from affected dashboard pages/components
2. **Comparison** — Queried `bg`, `pl`, and `en` values in the `translations` table
3. **Identification** — Found keys where `pl` was missing or equal to `en` (indicating fallback)
4. **Targeted fixes** applied in priority order:
   - Same-namespace aliases where provider dashboard already had equivalent keys
   - Client-dashboard alias reuse where appropriate (`CLIENT_DASHBOARD_TRANSLATIONS` import)
   - Explicit multilingual `row(...)` overrides for keys needing full 34-language support
   - Centralized `POLISH_OVERRIDES` block for remaining Polish-specific fixes

**Operational Workflow:**
```bash
# 1. Reseed translations
cd apps/api
python scripts/seed_provider_dashboard_translations.py

# 2. Clear Redis cache for provider_dashboard namespace
redis-cli DEL "translations:pl:provider_dashboard"
redis-cli KEYS "translations:*:provider_dashboard" | xargs redis-cli DEL

# 3. Validate DB values and UI pages
# - Check /pl/provider/dashboard
# - Check /pl/provider/dashboard/leads
# - Check /pl/provider/dashboard/services
# - Check /pl/provider/dashboard/analytics
# - Check /pl/provider/dashboard/reviews
# - Check /pl/provider/dashboard/qr-code
# - Check /pl/provider/dashboard/profile
```

**Branding Exception:**
The key `logo_pro` must remain untranslated as `"Pro"` in all 34 locales. This is an intentional branding exception, not a bug.

**Affected Sections:**
- Overview / Panel
- Leads
- Services
- Analytics
- Reviews
- QR Code
- Profile
- Settings / Sidebar (previously fixed and validated)

#### Onboarding Hero Banner i18n (April 10, 2026)
The onboarding hero banner on the dashboard overview page is now fully DB-backed. All 8 strings (titles, descriptions, CTAs, step labels) are stored in the `provider_dashboard` namespace and served via the standard translations endpoint. `getHeroContent()` and `CompactStepIndicator` in `apps/web/lib/onboarding-utils.tsx` accept a `dict` parameter and use `t()` for rendering. The dashboard page passes `dict` from `useDashboardI18n()` to both components.

#### Translation Loading Race Condition Fix (April 2026)
isLoading is now exposed via DashboardI18nContextValue. In provider dashboard page.tsx, isOnboardingComplete defaults to true while translationsLoading is true, preventing the onboarding banner from rendering with English fallback strings before the translation dict is populated.

Root cause: getHeroContent() was called on first render when dict was still empty ({}) — returning English fallback values. The fix delays banner rendering until translations are loaded.

Also fixed: provider_dashboard translation keys for onboarding hero banner were seeded with wrong key names. Correct keys are: setup_title, setup_subtitle, btn_complete_setup, setup_title_1step, setup_subtitle_1step, btn_add_service, step_profile, step_service (seed script: seed_onboarding_hero_v2.py)

#### Translation Key Standards (CRITICAL)
Translation keys used in `t()` calls must follow strict conventions to ensure consistency with the database namespace system:

1. **Clean Keys Only**: Keys must NOT contain colons (`:`) or prefixes in the `t()` function call itself
   - ✅ Correct: `t('msg_url_changes_remaining', 'URL changes remaining')`
   - ❌ Wrong: `t('msg_url_changes_remaining:', 'URL changes remaining')`

2. **Colons in JSX**: If UI requires a colon after a label, place it in the JSX text, not in the translation key or fallback
   - ✅ Correct: `{t('label_suggestions', 'Suggestions')}:`
   - ❌ Wrong: `t('label_suggestions:', 'Suggestions:')`

3. **Namespace Matching**: Keys must correspond exactly to namespaces defined in the database (`translations` table)
   - Provider dashboard: keys in `provider_dashboard` namespace
   - Client dashboard: keys in `client_dashboard` namespace
   - Public pages: keys in `homepage`, `category`, etc. namespaces

4. **No Manual Prefixing**: The `t()` function or hook handles namespace prefixing internally
   - ✅ Correct: `t('nav_dashboard', 'Dashboard')` (hook prefixes with `provider_dashboard.`)
   - ❌ Wrong: `t('provider_dashboard.nav_dashboard', 'Dashboard')`

**Operational Rule:** When adding new translation keys, always:
1. Add to the appropriate seed script (`seed_provider_dashboard_translations.py` or `seed_client_dashboard_translations.py`)
2. Use clean key names without colons or prefixes
3. Run the seed script to update the database
4. Flush Redis cache for the affected namespace

---

## Category Page Lead Form (Broadcast Model)

### LeadForm Component
- Location: apps/web/components/category/LeadForm.tsx
- Model: marketplace broadcast (one request → multiple providers)
- No provider pre-selected on category pages
- Chips sourced from existing provider service titles in the category
- "Not sure" chip always present as fallback
- Textarea hidden by default, expands after chip selection
- Chip value pre-fills textarea (user can edit freely)
- Submit includes selectedChip as description fallback if textarea empty
- Trust signals: Free, No obligation, Sent to multiple providers, Response 30min

### Pioneer Framing Banner
- Shown when: services prop is empty or undefined (no providers yet)
- Location: apps/web/app/[lang]/[city]/[category]/page.tsx
- Translation keys: category.no_providers_title, category.no_providers_subtitle
- Replaces old "Check back tomorrow" empty state text

### Mobile Sticky CTA Button
- Component: apps/web/components/category/StickyLeadFormButton.tsx
- Visibility: md:hidden (hidden on desktop, shown on mobile only)
- Logic: shows when form is NOT in viewport (above OR below)
- Uses isFormInView check: rect.top < window.innerHeight && rect.bottom > 0
- Targets: id="lead-form-anchor" on mobile form wrapper
- Scroll: smoothly scrolls to form on click
- Style: full-width orange button with white container and border-top

### CSS Fix: overflow-x:clip
- File: apps/web/app/globals.css
- Changed overflow-x:hidden to overflow-x:clip on html, body
- Reason: overflow-x:hidden causes browser to set overflow-y:auto on body
  making body a scroll container which breaks position:fixed on mobile

## Provider Description Auto-Translation

### Overview
Provider descriptions are automatically translated into all 34 supported languages when saved via PATCH /api/v1/provider/profile. Translations are stored in the provider_translations table and served by the public provider detail endpoint based on the lang query parameter.

### Translation Service
- Provider: Langbly API (https://api.langbly.com/language/translate/v2)
- Execution: Triggered via FastAPI **BackgroundTasks** to prevent request timeouts.
- API Key: stored in apps/api/services/translation_service.py
- Format: POST { "q": text, "target": lang } with Authorization: Bearer header
- Timeout: 30 seconds per request
- Fast Response: API returns success immediately (<1s) while translation proceeds in background.

### Fallback Strategy
- If Langbly returns 429 (monthly limit exhausted): stores original text with auto_translated=False
- If request times out or errors: same fallback behavior
- Daily retry job at 03:00 re-attempts all auto_translated=False rows
- Provider page always serves best available translation, falls back to original

### Database
Table: provider_translations
- provider_id + field + lang = unique constraint
- field = "description" (extensible to "business_name" etc.)
- auto_translated = False means original text stored as fallback, pending retry

---

## Global Phone Field System

### Overview
Phone is collected contextually at point of need, never during 
registration or onboarding. This preserves conversion rates.

### Storage Strategy
- Anonymous users: localStorage key `nevumo_phone` 
- Authenticated users: users.phone column in DB (source of truth)
- On login: if DB phone is null and localStorage has phone → 
  background sync to DB
- On submit: savePhone() writes to localStorage + DB (if logged in)

### Auto-prefix by Country
- PhoneInput auto-prefills with country code on mount
- Source: CITY_COUNTRY_MAP in page components
- User can freely edit/replace the prefix
- On blur: restores prefix if field is completely empty

### CITY_COUNTRY_MAP (current)
warszawa → PL (+48)
sofia → BG (+359)
belgrade → RS (+381)
prague → CZ (+420)
athens → GR (+30)
Adding new city: add entry to CITY_COUNTRY_MAP in:
  - apps/web/app/[lang]/[city]/[category]/page.tsx
  - apps/web/app/[lang]/[city]/[category]/[providerPage]/page.tsx

### Soft Validation
- Validates on blur and on submit only (never aggressive)
- Valid: total digits >= 7
- Error: simple message below input
- savePhone() only called when digits >= 7

### Components
- PhoneInput: apps/web/components/ui/PhoneInput.tsx
  - Fully controlled, no internal state
  - Props: value, onChange, countryCode, error, onValidChange, 
    errorMessage, label, placeholder, required
- usePhone hook: apps/web/hooks/usePhone.ts
  - Manages sync between localStorage and DB
  - Returns: { phone, savePhone, clearPhone, loading }

### Where Phone Appears
| Location | countryCode source | Required |
|----------|--------------------|----------|
| Category page LeadForm | CITY_COUNTRY_MAP | YES |
| Provider page LeadForm | CITY_COUNTRY_MAP | YES |
| ProviderWidget | prop + cityInfo | YES |
| Provider dashboard Settings | user.country_code | NO |
| Client dashboard Settings | user.country_code | NO |

### Privacy & GDPR
- Legal basis: Legitimate Interest (Art. 6(1)(f))
- Phone stored locally for user convenience, not for Nevumo's benefit
- Must be mentioned in Privacy Policy and Cookie/Storage Banner
- User can clear phone from Settings at any time

---

### City Landing Page Architecture (April 21, 2026)

- **Route**: `apps/web/app/[lang]/[city]/page.tsx`
- **Model**: SEO-focused entry point for users searching for services in a specific city.
- **Hero Logic (4 States)**:
  - **State 1: Full Data**: Shows count of providers, total requests, and average rating.
  - **State 2: No Ratings**: Shows provider and request counts, hides rating.
  - **State 3: Only Providers**: Shows "X professionals ready to help", hides requests/rating.

### SEO & Internationalization Infrastructure (April 2026)

#### 1. Source of Truth for Languages
- **File**: `apps/web/lib/locales.ts`
- **Definition**: The `SUPPORTED_LANGUAGES` array is the absolute Source of Truth (SoT) for the 34 supported locales across the entire project.
- **Automation**: `generateHreflangAlternates` (in `lib/seo.ts`) automatically generates `hreflang` tags for all 34 languages based on this array, ensuring global SEO consistency.

#### 2. Metadata Logic & Branding
- **Template**: Defined in `apps/web/app/layout.tsx` using the Next.js Metadata API: `%s | Nevumo`.
- **Database Rule**: SEO translations in the database (e.g., `meta_title`) MUST be "clean" — they should not include the brand name "Nevumo", as it is appended programmatically via the template.
- **Duplication Fix**: Mass correction performed on 2026-04-28 to strip hardcoded suffixes from database translations.

#### 3. Structured Data (JSON-LD)
- **Centralized Logic**: `apps/web/lib/seo.ts` contains dedicated functions for schema generation:
  - `generateOrganizationJsonLd()`: Standardized company schema.
  - `generateWebSiteJsonLd(lang)`: Dynamic site-search schema that adapts to the current page language.
- **Dynamic Adaptation**: The `WebSite` schema templates (like `urlTemplate`) are localized per language segment.

#### 4. SEO Validation & Diagnostics
- **Protocol**: SEO code quality is validated using a combination of **Playwright** (for crawler-like page loading) and **Phoenix** (for technical SEO auditing of the rendered HTML).
- **Scope**: Includes validation of `hreflang` alternates, canonical tags, and JSON-LD integrity.
  - **State 4: Pioneer (Empty)**: Shows "Be the first to request a service", hides all stats.
- **Core Components**:
  - `CityPageHero.tsx`: Main hero container handling the 4 states.
  - `CityHeroChips.tsx`: Category selector with inline `LeadForm` integration.
  - `CityLeadSection.tsx`: Contextual "How it works" and secondary CTA.
- **Data Fetching**:
  - Uses `getCityBySlug` for localized city details.
  - Fetches aggregate city statistics from `/api/v1/cities/{slug}/stats` (Redis cached, 1h).
  - Uses `getCategories` for category list.
  - Fetches translations from the `city` namespace.
- **LeadForm Integration**:
  - Integrated directly into the hero section for maximum conversion.
  - `showTextarea` defaults to true for better UX.
  - Removed "Not sure" chip to simplify the flow on city pages.

### Bug Fixes (April 19-20, 2026)

- **Onboarding Form Validation**: Added `noValidate` to onboarding forms to prevent browser-native validation from interfering with custom logic and causing cryptic frontend errors.
- **Cyrillic Slugification**: Improved `slugifyText` utility to properly support Bulgarian Cyrillic transliteration, ensuring valid SEO-friendly slugs for all providers.

### ScrollIntoView on Phone Validation Error (April 27, 2026)
When phone validation fails on form submit, the viewport smoothly scrolls to the phone field to improve UX. This pattern is applied in:
- **apps/web/components/provider/ProviderWidget.tsx**: On form submit, if phone validation fails, the form scrolls smoothly to the phone input field
- **apps/web/components/category/LeadForm.tsx**: Same behavior for category page lead forms

This ensures users immediately see the validation error and can correct it without having to manually scroll.
- **Sequence Synchronization**: Fixed critical 500 errors in lead submission by synchronizing PostgreSQL sequences (`lead_rate_limits`, `auth_rate_limits`) that were out of sync after Phase 3 migrations.

---

## SEO Architecture (CRITICAL)

### Strategy:
- programmatic SEO
- localized content (34 languages)
- SSR for indexing

## Embedded Lead Widget (CRITICAL GROWTH COMPONENT)

Nevumo предоставя **embeddable lead widget**, който providers могат да използват извън платформата.

### Recent Request Preview
- Source: latest direct lead where `lead.provider_id = provider.id`
- Fields exposed publicly: `client_name`, `city_name`, `created_at`, `client_image_url`
- `client_name` uses `users.name` or falls back to `Client`
- `client_image_url` is currently always `null` because the public client model has no avatar field

### City Demand Signal

- `city_leads` is computed from all leads in the requested `city_slug`
- This is city-wide demand, not category-filtered demand
- The frontend uses route city context so embed and full page fetch the same provider payload shape

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

## Smart Slug Generation

### Purpose

Replace automatic numeric suffix slug generation with user-controlled slug selection featuring smart suggestions and validation. Prevents auto-generated numeric suffix slugs. User-entered slugs with numbers (rio-22, studio-7) are allowed.

### Validation Rules

**Forbidden patterns:**
- `DevS` (uppercase)
- `devs_studio` (underscores)
- `devs@studio` (special chars)

**Allowed patterns (Manual Input):**
- `rio-22`, `studio-7` (numeric suffixes in user-entered slugs)
- `devs-sofia`
- `devs-massage`
- `devs-pro`
- `devs-studio-bg`

**Note:** Numeric suffix restriction applies ONLY to auto-generation (generate_provider_slug), NOT to user-entered slugs (validate_slug in provider_service.py and schemas.py).

### Implementation

**Backend (apps/api/services/provider_service.py):**
- `validate_slug(slug)` — returns (is_valid, error_message)
- `generate_slug_suggestions(base, city_slug, category_slug, db)` — generates contextual suggestions
- `generate_provider_slug(business_name, db)` — generates base slug without auto-increment
- `get_or_create_provider(user, db, preferred_slug?, city_slug?, category_slug?)` — creates provider with slug validation

**Backend (apps/api/routes/provider.py):**
- `GET /slug/check` — check availability + get suggestions (JWT required)

**Backend (apps/api/routes/auth.py):**
- `POST /register` — creates provider with draft slug, actual slug set during onboarding

**Frontend (apps/web/lib/slug-utils.ts):**
- `isValidSlugFormat(slug)` — client-side validation
- `sanitizeSlug(input)` — normalize user input
- `getSlugValidationError(slug)` — get specific error message
- `slugify(text)` — convert text to slug format

**Frontend (apps/web/lib/provider-api.ts):**
- `checkSlugAvailability(slug, citySlug?, categorySlug?)` — API call (JWT required)

**Frontend (apps/web/lib/auth-api.ts):**
- `registerWithEmail(email, password, role, locale)` — registration without slug

### Suggestion Logic

Suggestions generated in priority order:
1. `{slug}-{city_slug}` (if city provided)
2. `{slug}-{category_slug}` (if category provided)
3. `{slug}-{city_slug}-{category_slug}` (if both provided)
4. Generic: `{slug}-pro`, `{slug}-studio`, `{slug}-bg`

Taken slugs are filtered out. Maximum 5 suggestions returned.

### API Behavior

**Profile slug check endpoint (JWT required):**
- Returns `{ available: true }` if slug is free
- Returns `{ available: false, suggestions: [...] }` if taken
- Returns validation error for invalid formats

**Registration slug check endpoint (no auth required):**
- Same behavior as profile endpoint
- Used during registration flow before account creation

### Security Features

**Loop Prevention:**
- Tracks visited slugs to prevent infinite redirect chains
- Maximum depth of 5 redirects before aborting
- Returns 404 if loop detected

**Change Limit Enforcement:**
- `MAX_SLUG_CHANGES = 1` - Only one real change allowed after onboarding
- Backend automatically detects onboarding completion using `check_onboarding_complete()`
- Frontend parameter `is_onboarding_setup` is ignored for security

### Frontend Integration

**Provider Pages:**
- Automatic redirect detection via `resolveSlug()` API call
- Browser URL updates seamlessly using Next.js `redirect()`
- No user interruption - transparent redirect experience

**Settings Page:**
- Shows remaining changes allowed based on `slug_change_count`
- Displays "URL locked" when limit reached
- Provides support contact information

### User Experience

**Slug Change Flow:**
1. User changes slug in settings (if allowed)
2. Backend validates and creates redirect record
3. Old URLs immediately start redirecting to new URL
4. SEO value preserved with 301 redirects
5. Browser address bar updates automatically

**Error Handling:**
- 404 for non-existent slugs
- 409 for slug change limit exceeded
- Graceful degradation if redirect system fails

---

## Onboarding Hero Banner (Dashboard)

When a provider has incomplete onboarding (`is_complete === false`), a hero banner appears on the dashboard overview page.

### Dynamic Content Based on Missing Fields

The hero banner uses `missing_fields` from the dashboard response to determine which onboarding step is incomplete:

**Missing `business_name` (Profile incomplete):**
- Headline: "You're 2 steps away from getting clients"
- Description: "Complete your profile to start receiving requests"
- CTA: "Complete your profile"

**Profile complete but missing `service` and/or `city`:**
- Headline: "You're 1 step away from getting clients"
- Description: "Add your first service to start receiving requests"
- CTA: "Add your first service"

### Step Indicator

A compact step indicator shows progress:
- **Profile step**: Green checkmark when complete, orange "1" when incomplete
- **Service step**: Gray inactive when profile incomplete, orange "2" when profile complete but service missing, green checkmark when complete
- Visual styling matches the onboarding wizard step indicator exactly

### Implementation

**Shared utilities** (`apps/web/lib/onboarding-utils.tsx`):
- `deriveOnboardingState(missing_fields)` — derives completion state from backend data
- `getHeroContent(state)` — returns headline/description/CTA based on state
- `CompactStepIndicator` — React component for the step indicator UI

**Dashboard integration** (`apps/web/app/[lang]/provider/dashboard/page.tsx`):
- Uses `deriveOnboardingState()` to compute onboarding state
- Conditionally renders hero banner with dynamic content
- Shows `CompactStepIndicator` in hero footer

### Locked Stat Cards

All 4 stat cards (Total Leads, New Leads, Rating, Accepted) are locked during incomplete onboarding:
- Padlock overlay (🔒) with blur/dimmed treatment
- Clicking any locked card redirects to profile onboarding
- **Rating card**: Shows motivational value `5.0` while locked, real value after
- **Accepted card**: Shows motivational value `137` while locked, real value after

### Bug Fix: `services` vs `service`

The backend returns `service` (singular) in `missing_fields`, not `services`. The profile page skip-to-step-2 logic was fixed to check for `'service'` instead of `'services'`.

---

## Onboarding Step 1 Draft Persistence

### Problem

When a provider fills Step 1 fields (business name, slug, description) and clicks "Skip for now", they navigate to the dashboard. Upon clicking the hero CTA to return to onboarding, all entered values were lost because they existed only in React state.

### Solution

**Frontend-only draft persistence using sessionStorage**:

- Draft is saved to `sessionStorage` whenever Step 1 values change
- Draft is scoped per provider ID to prevent cross-account leakage
- Draft contains: `business_name`, `description`, `slug`, `slugManual`, `slugEditing`

### Hydration Rules

**On page load** (after fetching backend data):
1. If backend has complete Step 1 (real business name + slug): **use backend values**, clear any stale draft
2. If backend Step 1 is incomplete (placeholder email): **try to hydrate from draft** if exists
3. If no draft: show empty form as before

### Write Rules

1. **Auto-save**: Draft saved whenever user edits Step 1 inputs (debounced via useEffect)
2. **Explicit flush**: Before "Skip for now" navigation, latest snapshot is saved
3. **Clear on success**: Draft cleared when Step 1 is successfully submitted (backend becomes source of truth)
4. **Clear on complete**: Draft cleared when full onboarding completes

### Implementation

**Shared utilities** (`apps/web/lib/onboarding-utils.tsx`):
- `saveStep1Draft(providerId, draft)` — persists to sessionStorage
- `loadStep1Draft(providerId)` — retrieves draft if exists and matches provider
- `clearStep1Draft(providerId)` — removes draft from storage
- `Step1Draft` interface — type for draft data structure

**Profile page integration** (`apps/web/app/[lang]/provider/dashboard/profile/page.tsx`):
- `providerId` state — stores current provider ID for draft scoping
- `persistStep1Draft` callback — memoized function to save current Step 1 state
- Auto-save effect — saves draft whenever Step 1 values change
- Draft hydration in initialization effect — loads draft if backend incomplete
- Explicit save on "Skip for now" — flushes latest values before navigation
- Draft clearing on successful Step 1 submit and complete onboarding

### Security Considerations

- Draft is per-provider scoped (key: `onboarding_step1_draft_{providerId}`)

---

## Role Switch Redirect Logic (April 2026)

### Overview
When a user switches their role from Client to Provider via POST /api/v1/auth/switch-role, the frontend redirects them to the main Provider Dashboard (`/provider/dashboard`) instead of the Profile page. This change ensures a smoother transition and leverages the existing Onboarding Banner for profile completion guidance.

### Implementation Details

**Backend** (`apps/api/routes/auth.py`):
- The `switch-role` endpoint accepts optional `business_name` and `preferred_slug` parameters
- When switching to provider with these parameters: creates provider record with those values (if provider doesn't exist)
- When switching to provider without these parameters: creates draft provider with temporary slug and email as placeholder business_name
- When provider already exists: only updates user role

**Frontend** (`apps/web/lib/provider-api.ts`):
- `switchRole()` function accepts optional `businessName` and `preferredSlug` parameters
- These are passed to the backend when provided

**Redirect Behavior**:
- Client dashboard settings page (`apps/web/app/[lang]/client/dashboard/settings/page.tsx`): redirects to `/${lang}/provider/dashboard` after successful switch
- Client dashboard layout (`apps/web/app/[lang]/client/dashboard/layout.tsx`): redirects to `/${lang}/provider/dashboard` after successful switch
- Provider dashboard settings page (`apps/web/app/[lang]/provider/dashboard/settings/page.tsx`): redirects to `/${lang}/` when switching back to client

### Onboarding Banner Integration
- After switching to provider, the user lands on the main Dashboard
- If onboarding is incomplete, the Onboarding Banner automatically appears with dynamic content based on `missing_fields`
- The banner guides users through profile completion without requiring a separate redirect to the Profile page
- This provides a cohesive user experience with clear next steps

### Translation Keys
New i18n keys for the onboarding banner have been added to the Bulgarian and English translation files in the `provider_dashboard` namespace. These keys support the dynamic hero content, step indicators, and CTAs displayed during the onboarding process.

---

## URL Redirect System

### Purpose

Maintain SEO value and user experience when providers change their public URL slug. Old URLs automatically redirect to new ones with 301 status codes.

### Database Schema

**url_redirects table:**
- `provider_id` - Foreign key to providers table
- `old_slug` - The previous slug that should redirect
- `new_slug` - The current slug that should receive traffic
- `active` - Boolean flag to enable/disable redirects
- `created_at` - Timestamp for tracking

**Provider model relationships:**
- `slug_change_count` - Number of real changes made (onboarding changes don't count)
- `redirects` - One-to-many relationship to url_redirects

### Redirect Logic

**Backend Functions:**
- `resolve_provider_slug(slug, db)` - Resolves current slug or active redirect
- `resolve_provider_slug_safe(slug, db)` - Same but with loop prevention (max depth 5)
- `_record_slug_change(provider, db, old_slug, new_slug, request_ip, user_agent)` - Creates redirect record

**API Endpoints:**
- `GET /api/v1/providers/{slug}` - Returns 301 redirect if old slug found
- `GET /api/v1/providers/resolve/{slug}` - Checks if slug redirects without following

### Security Features

**Loop Prevention:**
- Tracks visited slugs to prevent infinite redirect chains
- Maximum depth of 5 redirects before aborting
- Returns 404 if loop detected

**Change Limit Enforcement:**
- `MAX_SLUG_CHANGES = 1` - Only one real change allowed after onboarding
- Backend automatically detects onboarding completion using `check_onboarding_complete()`
- Frontend parameter `is_onboarding_setup` is ignored for security

### Frontend Integration

**Provider Pages:**
- Automatic redirect detection via `resolveSlug()` API call
- Browser URL updates seamlessly using Next.js `redirect()`
- No user interruption - transparent redirect experience

**Settings Page:**
- Shows remaining changes allowed based on `slug_change_count`
- Displays "URL locked" when limit reached
- Provides support contact information

### User Experience

**Slug Change Flow:**
1. User changes slug in settings (if allowed)
2. Backend validates and creates redirect record
3. Old URLs immediately start redirecting to new URL
4. SEO value preserved with 301 redirects
5. Browser address bar updates automatically

**Error Handling:**
- 404 for non-existent slugs
- 409 for slug change limit exceeded
- Graceful degradation if redirect system fails

---

## Provider Dashboard (Phase 1 — Backend + Frontend Complete)

### Endpoints (all under /api/v1/provider/, JWT required)

| Method | Path | Purpose |
|--------|------|---------|
| GET | /dashboard | KPIs + profile completeness |
| GET | /leads | Leads inbox |
| PATCH | /leads/{id} | Update lead status (contacted/done/rejected) |
| GET | /profile | Full provider profile |
| PATCH | /profile | Update business_name, description, availability_status, slug |
| GET | /slug/check | Check slug availability + get suggestions |
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

### Image Processing Pipeline

**Supported Input Formats:**
- JPEG, PNG, WebP, HEIC, HEIF (iPhone formats)

**Processing Steps:**
1. **EXIF Orientation Correction**: `ImageOps.exif_transpose(img)` is applied immediately after `Image.open()` to correctly orient images taken with mobile phones. Mobile cameras physically capture in landscape mode and store rotation in EXIF metadata — without this step, portrait photos appear rotated 90°.
2. **Format Conversion**: All images automatically converted to WebP format for optimization
3. **Resize**: Images larger than 1200px are resized proportionally to max 1200px width/height
4. **Quality**: WebP quality set to 85% for optimal balance between quality and file size
5. **HEIC/HEIF Support**: iPhone formats are converted to WebP using pillow-heif library

**Storage:**
- Phase 1: Local filesystem at uploads/provider_images/{provider_id}.webp
- Served via FastAPI StaticFiles mount at /static/provider_images
- Storage abstraction (save_provider_image in provider_service.py) ready for S3/R2 migration
- **STATIC_FILES_BASE_URL**: Backend uses this environment variable to generate full URLs for static files. In Docker, this must point to the API server port (8000), not the frontend port (3000). The upload endpoint in `apps/api/routes/provider.py` prioritizes this variable over request headers for URL generation.

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

**Leads** — Table with lead data (phone, description, source, notes, status, date). Filter tabs by status (All, New, Contacted, Done, Rejected). Empty state when no leads. Notes column shows first 40 characters with sticky note icon (📝) for quick preview. Search uses debounced local state (500ms delay) with subtle inline loading spinner; table data persists while loading to prevent UI flicker.

**LeadDetailModal** — Modal component for viewing and editing individual lead details:
- Opens when clicking any lead row
- Displays full lead information: phone, description, source, status, created_at
- **Private Notes Section**: Textarea for provider_notes field (provider-private, not visible to clients)
- Notes saved via PATCH /api/v1/provider/leads/{lead_id}/notes with debounced 500ms delay
- Auto-saves on blur (when textarea loses focus)
- Shows loading spinner while saving
- Notes are persisted to leads.provider_notes column in database
- Translation key: label_private_notes (provider_dashboard namespace)
- Search functionality: searches across client_name, client_email, client_phone, description, and provider_notes fields with case-insensitive partial matching

**Services** — Grid of service cards showing: title, category, cities (as badges), price + currency, price_type. "Add Service" button. Each card has Edit and Delete buttons. Delete triggers confirmation dialog → DELETE endpoint. Add → empty "New Service" form. Edit → pre-filled "Edit Service" form. Empty state when no services.

**Analytics** — KPI cards (Total Leads, Contacted, Conversion %). Period toggle: 7 days / 30 days. Source breakdown horizontal bars (seo, direct, widget, qr).

**QR Code** — Dedicated page. "Generate" button → displays QR code image + public provider URL.

**Profile** — Two modes:
- New provider (is_complete === false): 2-step onboarding wizard
  - Step 1: Profile photo upload + Company or personal name + Description
    - **Label**: "Company or personal name" (universal for businesses and freelancers)
    - **Placeholder**: "e.g. Maria's Massage Ltd or Maria Kowalska"
    - **Note**: Texts come from provider_dashboard namespace in translations table
  - Step 2: Add First Service — Title, Category (select), **Cities (multi-select with SearchInput)**, Price Type (fixed/hourly/request/per_sqm), Price, Currency (auto-detected from first city)
  - **Progress indicator**: Step numbers turn green when required fields are valid (orange → green transition)
  - **Real-time inline validation**: Green border when valid, red border + error message when invalid, immediate feedback on typing
  - **Field placeholders**: "Search or select a category", "Select cities where you offer this service", "e.g. Emergency pipe repair, Deep tissue massage (60 min)"
- Existing provider (is_complete === true): Edit mode with all profile fields

**Settings** — Account info display, Availability status toggle (Active/Busy/Offline), Public URL slug display, "Switch to Client" button, Logout button.

#### Client Dashboard
Client dashboard now mirrors the provider dashboard shell under `/[lang]/client/dashboard/*`, but uses client-specific routes, guards, and actions.

- **Layout** — Client-only guard based on JWT presence plus `role='client'`, dedicated sidebar with `Overview`, `My Requests`, `Reviews`, `Settings`, orange `НАМЕРИ УСЛУГА` CTA to `/${lang}`, and top bar showing the authenticated email.
- **Route entry** — Base route `/[lang]/client/dashboard` immediately redirects to `/overview`.
- **Overview** — `GET /api/v1/client/dashboard` drives 3 KPI cards (`active_leads`, `completed_leads`, `reviews_written`) plus recent lead cards with marketplace/provider distinction and grouped status badges.
- **My Requests** — `GET /api/v1/client/leads` powers status tabs (`all`, `active`, `done`, `rejected`), card rows, and inline review submission only when `status='done'`, `has_review=false`, and a provider is assigned.
- **Reviews** — `GET /api/v1/client/reviews` powers the "Написани" tab; `GET /api/v1/client/reviews/eligible-leads` powers the "Чакащи ревю" tab, with frontend filtering on `has_review=false` for the pending-review UX. Provider replies are rendered as expandable sections.
- **Settings** — Read-only email, reset-password link, review reply email toggle (same backend preference as Reviews), `Стани доставчик` role switch, and logout.

#### Role Switching
Provider ↔ Client switching works. Updates user role via API and redirects to appropriate dashboard.

**Client → Provider Flow:**
- When switching to provider without business_name/preferred_slug: creates draft provider record with temporary slug (draft{token}) and email as placeholder business_name, then redirects to `/provider/dashboard/profile` for onboarding
- When switching to provider with business_name/preferred_slug: creates provider record with those values (if provider doesn't exist)
- When provider already exists: only updates user role
- Frontend calls `switchRole('provider')` from client dashboard sidebar and settings page
- After successful switch, user is redirected to `/provider/dashboard/profile` to complete onboarding

**Provider → Client Flow:**
- Updates user role to client
- Redirects to `/client/dashboard/overview`
- Provider record remains intact (user can switch back)

#### Service Form Architecture
- Service creation/edit includes: title, category_id, city_ids[], description, price_type, base_price, currency
- currency field supports 13 currencies: EUR, BGN, USD, GBP, CHF, CZK, DKK, HUF, PLN, RON, SEK, NOK, TRY, ALL, MKD, RSD, BAM, HRK
- price_type supports: fixed, hourly, request, per_sqm
- Creating a service auto-syncs provider_cities for lead matching
- **SearchInput Component**: Unified searchable select component supporting both single and multi-select modes
  - Location: `apps/web/components/dashboard/SearchInput.tsx`
  - Props: `mode: 'single' | 'multi'`, `options`, `value/values`, `onChange`, `placeholder`, `error`
  - Used in: Profile onboarding (Category, Cities), Services page (Cities)
  - Features: Search filtering, keyboard navigation (Enter/Escape), click-outside close, auto-focus input

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
- **Provider registration**: no slug selection on auth page; account created immediately with temporary draft slug, redirect to onboarding step 1 for slug configuration
- Forgot step: sends reset link → success toast "Провери имейла си"; catch also shows success (no enumeration)
- All buttons: orange active (bg-orange-500), gray disabled (bg-gray-300)
- Browser password save: Credential Management API (saveCredentials in apps/web/lib/password-save.ts) + hidden email input in register form + onInput handler for browser autofill compatibility. generateStrongPassword removed — browser native strong password suggestion used instead.
- Post-auth: `saveAuth(token, user)` → localStorage; redirect by role (provider → /provider/dashboard/profile for onboarding, client → /)
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
- POST /api/v1/auth/register → { token: JWT, user: {id, email, role} } (provider created with draft slug, actual slug set during onboarding)
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

## Lead Capture → Account Linking Flow

### Overview

A three-phase system that converts anonymous lead submissions into authenticated client accounts with full lead ownership history. This bridges the gap between high-conversion anonymous submission and account-based features (lead tracking, reviews, notifications).

### Phase 1: Success Screen with Email Capture (Frontend)

**Location:** `apps/web/components/category/LeadForm.tsx`

**Flow:**
1. User submits lead form (phone + description + category/city)
2. Backend creates lead, returns lead_id
3. Frontend shows two-step success screen:
   - **Step 1:** "Запитването е изпратено!" + "Want to track your request?"
     - "Continue with email →" button
     - "No thanks" skip button (resets form to initial state)
   - **Step 2:** Email input form
4. On email submit:
   - POST to `/api/v1/leads/{lead_id}/claim-email`
   - Save to localStorage: `nevumo_pending_claim` = `{ lead_id, email, phone, submitted_at }`
   - Redirect to `/{lang}/auth?email={email}&intent=client`

**Rate Limit Handling:**
- If lead submission returns 429 RATE_LIMIT_EXCEEDED, still show Step 1 success screen
- User can still claim the lead even if rate limited (lead was created)

### Phase 2: Pending Lead Claims (Backend)

**Table:** `pending_lead_claims`

**Purpose:** Store intent to claim anonymous leads until user authenticates.

**Key Fields:**
- `lead_id` — FK to leads table (CASCADE DELETE)
- `email` — Primary matching key for account linking
- `phone` — Secondary matching key for account linking
- `claimed` — Boolean, set to TRUE when linked to a user
- `claimed_at` — Timestamp of successful linking
- `magic_link_sent` — Boolean, set when delayed magic link is sent
- `expires_at` — 7 days from creation (TTL for claim validity)

**Idempotent Registration:**
```
POST /api/v1/leads/{lead_id}/claim-email
Body: { email, phone? }
```
- Creates new claim or refreshes existing claim's `created_at` and `expires_at`
- No authentication required

**Auth Hooks:**
- `link_pending_claims(user_id, email, phone, db)` in `auth_service.py`
- Called in BOTH `/register` and `/login` after successful authentication
- Finds all unclaimed claims matching email OR phone
- Updates `leads.client_id` to the new/logged-in user
- Marks matching claims as `claimed=TRUE` with `claimed_at` timestamp
- Wrapped in try/except — never blocks auth flow

### Phase 3: Magic Link Authentication (Backend + Frontend)

**Table:** `magic_link_tokens`

**Purpose:** Enable passwordless account creation and authentication for users who claimed leads but haven't set passwords.

**Background Job:** `apps/api/jobs/send_magic_links.py`

**Schedule:** Every 5 minutes via APScheduler

**Query Logic:**
```sql
SELECT * FROM pending_lead_claims 
WHERE claimed = FALSE 
  AND magic_link_sent = FALSE
  AND expires_at > NOW()
  AND created_at <= NOW() - INTERVAL '30 minutes'
```

**Job Actions:**
1. For each eligible claim:
   - Generate raw token: `secrets.token_urlsafe(32)`
   - Store SHA-256 hash in `magic_link_tokens` table
   - Set `expires_at` to 48 hours from creation
   - Console log the magic link: `{APP_URL}/en/auth/magic?token={raw_token}`
   - Mark claim as `magic_link_sent=TRUE`

**Frontend Magic Link Handler:**

**Location:** `apps/web/app/[lang]/auth/magic/page.tsx` + `MagicLinkClient.tsx`

**Flow:**
1. Page loads, reads `?token=` from URL
2. Shows loading state while validating
3. POST to `/api/v1/auth/magic-link` with token
4. On success:
   - `saveAuth(token, user)` to localStorage
   - Redirect to `/client/dashboard`
5. On error (expired/invalid/used):
   - Show Bulgarian error message
   - CTA button to `/auth` for manual login

**API Endpoint:** `POST /api/v1/auth/magic-link`

**Response (Success):**
```json
{
  "success": true,
  "data": {
    "token": "JWT",
    "user": { "id": "uuid", "email": "...", "role": "client" }
  }
}
```

**Error Codes:**
- `TOKEN_INVALID` — token hash not found in DB
- `TOKEN_EXPIRED` — token past expires_at timestamp
- `TOKEN_USED` — token already has used_at timestamp

### Security Considerations

1. **Timing Attack Prevention:** Magic links sent after 30-minute delay to prevent real-time email interception attacks
2. **Short TTL:** Magic tokens expire in 48 hours (vs 30 min for password reset)
3. **One-Time Use:** Tokens marked as used after first successful auth
4. **Hash Storage:** Raw token never stored in DB — SHA-256 hash only
5. **Claim Expiration:** Unclaimed leads expire after 7 days
6. **No Enumeration:** Magic link endpoint returns generic errors (same timing for invalid/expired/used)

### Data Flow Summary

```
Anonymous User                          Authenticated User
     │                                         │
     ▼                                         ▼
┌─────────────┐      ┌──────────────────┐     ┌──────────────┐
│ Submit Lead │─────▶│ pending_lead_    │────▶│ Client       │
│ (phone)     │      │ claims (email)   │     │ Dashboard    │
└─────────────┘      └──────────────────┘     └──────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
     ┌────────────────┐      ┌──────────────────┐
     │ Immediate:       │      │ Delayed (30min): │
     │ Register/Login   │      │ Magic Link Email │
     │ → link_pending_  │      │ → magic_link_    │
     │   claims()       │      │   tokens table   │
     └────────────────┘      └──────────────────┘
```

---

## Key Principles

- Keep backend simple
- Optimize for SEO first
- Leads = core revenue
- Avoid over-engineering
- Build for scale, but start lean

---

## Review System (Closed Trust Conversation Model)

### Overview

The review system implements a **closed trust conversation model** that enables structured feedback between clients and providers while preventing abuse and maintaining simplicity.

### Product Rules

1. **Client review is the starting message** — Always the first message in the conversation
2. **Provider has exactly one reply per review** — Single reply, editable unlimited times
3. **Conversation closes after provider reply** — No further messages allowed
4. **Email notifications on first reply only** — Edits do not trigger notifications
5. **Canonical client identity only** — Review UI uses `users.name` or `Client`, never email-derived names
6. **Self-review is forbidden** — Ownership of the target provider profile is checked in the backend service layer

### Architecture

**Database Schema:**
```
reviews table:
- provider_reply TEXT              -- Single reply, editable
- provider_reply_at TIMESTAMP      -- First reply timestamp
- provider_reply_edited_at TIMESTAMP -- Last edit timestamp  
- provider_reply_edit_count INTEGER -- Edit counter for UI indicator
```

**Key Constraints:**
- UNIQUE(lead_id) — One review per lead maximum
- CHECK(rating >= 1 AND rating <= 5) — Valid star ratings only
- Lead must have status='done' to be reviewable
- Client must own the lead being reviewed
- Provider profile owner cannot review their own provider record, even after role switching

### Trust Chain

**Review Eligibility:**
1. Lead must be completed (status='done')
2. Client must be authenticated and own the lead
3. Lead must have an assigned provider
4. No existing review for this lead
5. Provider.user_id must be different from the authenticated client user id

**Provider Reply Permissions:**
1. Provider can only reply to reviews on their own profile
2. Unlimited edits allowed after first reply
3. Edit history tracked via edit_count + edited_at

### Email Notification System

**Trigger Conditions:**
- First provider reply only (not on edits)
- Client must have review_reply_email_enabled = TRUE (opted in)
- Default is opted in for all users

**Email Content:**
- Subject: "{provider_name} responded to your review"
- Body: Client's review + provider's reply + link to view
- Footer: Link to manage email preferences

**Implementation:**
- Email service abstraction in `apps/api/services/email_service.py`
- Configurable via SMTP or email API (placeholder for Phase 2)
- Console logging in development mode

### Frontend Integration

**Client Dashboard:**
- `/client/dashboard/jobs` — Completed jobs with "Write a review" CTA
- `/client/dashboard/reviews` — Submitted reviews with provider replies
- Email preferences toggle in reviews section

**Provider Dashboard:**
- `/provider/dashboard` — Shows "Latest Review" preview card with unreplied count
- `/provider/dashboard/reviews` — Full review management with reply/edit
- Sidebar shows unreplied review badge

### Dynamic Rating Calculation

**Provider Rating:**
- Calculated as AVG(reviews.rating) in real-time
- Updated automatically when reviews are created/modified
- Stored in providers.rating for quick access

**Review Count:**
- Calculated as COUNT(reviews) per provider
- Used in public provider profiles for trust signals

### API Design

**Client Endpoints:**
- `GET /api/v1/client/reviews/eligible-leads` — List reviewable completed jobs
- `POST /api/v1/client/reviews` — Submit a review
- `GET /api/v1/client/reviews` — List submitted reviews
- `GET /api/v1/client/reviews/preferences` — Get email preferences
- `PATCH /api/v1/client/reviews/preferences` — Update email preferences

**Provider Endpoints:**
- `GET /api/v1/provider/reviews` — List all reviews
- `GET /api/v1/provider/reviews/latest-preview` — Dashboard preview
- `POST /api/v1/provider/reviews/{id}/reply` — First reply
- `PATCH /api/v1/provider/reviews/{id}/reply` — Edit reply

### i18n Support

All review-related UI text is translatable via the translation system:
- 34 supported languages
- Translation keys in `apps/api/scripts/seed_review_translations.py`
- Keys include: reviews_title, write_review, your_rating, provider_replied, etc.

### Security Considerations

- **Authorization:** All endpoints verify JWT + ownership
- **Rate limiting:** Inherited from auth rate limiting
- **Input validation:** Pydantic schemas enforce constraints
- **XSS prevention:** All text content escaped in templates
- **Mode switching safety:** Active role switching UX stays intact, but review authorization is enforced by ownership checks rather than relying only on the current role string

### Migration Path

```bash
# Run database migration
cd apps/api
alembic upgrade i8j9k0l1m2n3

# Seed translation keys
python scripts/seed_review_translations.py
```

### City Page UI Components

- Hero section with search placeholder and CTAs for becoming a specialist and sending requests.
  - 'Become a specialist' link updated to `/${lang}/auth?mode=register&role=provider`.
  - 'Send a free request' CTA now links to a placeholder route `/[lang]/[city]/request`.