# Nevumo Master Context

## Project Overview
Nevumo е уеб платформа за marketplace на услуги.
- Доставчици публикуват услуги
- Клиенти търсят и се свързват с доставчици
- Платформата е мултиезична (34 езика)
- Основен фокус: scalability, SEO, conversion

---

## Tech Stack

### Architecture
- Monorepo: Turborepo
  - apps/web (frontend)
  - apps/api (backend)
  - apps/docs

### Frontend
- Next.js 16
- React 19
- TypeScript 5 (strict mode)
- Tailwind CSS 4
- PostCSS

### Backend
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

### Database & Caching
- PostgreSQL (nevumo_leads)
- Redis (caching layer)

### Tracking
- Google Analytics 4 (GA4) — G-HKW6GBJJCK
- Custom DB events — page_events таблица + /api/v1/page-events endpoint
- Shared utility: lib/tracking.ts — trackPageEvent()

### Auth (Phase 1 — COMPLETE)
- Email-based: register, login, forgot password, reset password
- Backend: 6 endpoints на /api/v1/auth/, bcrypt hashing, JWT tokens
- Frontend: lib/auth-api.ts (typed API calls), lib/auth-store.ts (localStorage)
- Security: rate limiting, no email enumeration, token hashing, password policy
- Phase 2 (future): OAuth Google + Facebook, email sending via Resend/SendGrid

### Shared
- packages/ui (shared UI components)
- packages/typescript-config (shared TS config)

---

## AI Development Tools

- Windsurf IDE + Cascade (SWE-1.5)
- Codex CLI (gpt-5.1-codex-mini)
- Continue extension (Groq, Gemini, DeepSeek)
- GitHub Copilot

---

## Config Files

- .windsurfrules
- ~/.codeium/windsurf/memories/global_rules.md
- .github/copilot-instructions.md
- ~/.continue/config.yaml
- AGENTS.md

---

## Translations Workflow

- Claude генерира преводите
- Codex CLI ги записва в PostgreSQL
- Redis кешира преводите
- UI copy за homepage и category страниците вече се подава от PostgreSQL през namespaced endpoint (`homepage.*`, `category.*`)

### Supported languages (34):
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, is, it, lb, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, ru, sk, sl, sq, sr, sv, tr, uk

- Default language: en
- UI translation seed status (April 4, 2026):
  - `43` homepage keys per language
  - `24` category-page keys per language
  - `67` total UI keys per language
  - `2,278` rows in `translations` for homepage/category namespaces across 34 languages

---

## Engineering Rules (CRITICAL)

- Никога не рефакторирай код извън текущата задача
- Никога не добавяй функционалност, която не е поискана
- Никога не модифицирай .env файлове
- Винаги спазвай текущата архитектура

### TypeScript
- Strict mode задължително
- Забранен any тип

### Python
- Type hints задължителни
- Използвай Pydantic за validation

### Financial Logic
- Използвай Decimal (Python)
- Никога float за пари

---

## AI Behavior Rules (IMPORTANT)

- Отговорите трябва да са practically oriented (без теория)
- Да се съобразяват със съществуващия stack
- Да не предлагат технологии извън stack-а, освен ако не е изрично поискано
- Да мислят в контекста на marketplace (clients + providers)
- Да приоритизират performance и scalability
- Да предлагат production-ready решения

---

## Priority Focus

1. SEO (critical for growth)
2. Conversion (landing → signup → action)
3. Scalable architecture
4. Clean DX (developer experience)

### Current Go-To-Market Focus (April 2026)
- Single-city launch playbook first: Warsaw before multi-city rollout
- Single-country proof with limited categories before expansion
- Provider-first homepage to acquire supply
- Client-first category pages to capture SEO demand and convert leads

---

## Roadmap Status

### ✅ Complete
- **Retro-matching** — при добавяне на първа услуга, новият доставчик автоматично получава всички съществуващи необработени заявки (status: created / pending_match) за същата категория + град. Имплементирано в `apps/api/services/provider_service.py` (функция `retro_match_provider`) и извиквано от `POST /api/v1/provider/services` в `apps/api/routes/provider.py`. Отговорът на endpoint-а съдържа `retro_matched_leads: int`.
- SEO infrastructure (robots, sitemap, JSON-LD, hreflang, OG tags)
- Provider listing + detail pages
- Lead form (LeadForm component)
- Event tracking (GA4 + custom DB)
- Auth backend — Phase A (6 endpoints, bcrypt, JWT, rate limiting)
- Auth frontend — connected to real API (login, register, forgot, reset)
- Provider Dashboard backend — 10 endpoints, JWT auth, lead status management, image upload, QR generation, onboarding support
- Provider Dashboard frontend — all pages (Overview, Leads, Services, Analytics, QR Code, Profile, Settings, Reviews)
- Provider onboarding — 2-step wizard (profile info → first service), completeness check with auto-redirect
- Service CRUD — add/edit/delete with category, multi-city, price type, currency
- Client Dashboard — frontend + backend complete with guarded sidebar/topbar layout, Overview, My Requests, Reviews, Settings, inline review submission, review reply toggle preferences, role switch, and logout
- DB: service_cities table (many-to-many service↔city), currency on services, per_sqm price type
- SearchInput Component: Unified searchable select component (single/multi-select modes)
- **URL Redirect System** — Complete slug change management with 301 redirects, SEO protection, loop prevention
- **Slug Change Security** — Backend-controlled change limits (1 change after onboarding), frontend manipulation protection
- **Automatic Redirect Resolution** — Seamless frontend URL updates, browser address bar synchronization
- **Review System (Closed Trust Conversation Model)** — Complete review/rating system with:
  - Client reviews for completed jobs
  - Provider single reply (editable)
  - Email notifications on first reply (with opt-out)
  - Provider dashboard reviews section with reply/edit functionality
  - Client dashboard completed jobs with review CTA
  - Client email preferences toggle
  - Translation keys for all 34 languages
- **Rating card** on provider dashboard clearly labeled as "Overall Rating" from all client reviews
- **Warsaw Launch Data Seeded** — Complete Warsaw marketplace setup:
  - City: Warszawa (PL) with coordinates 52.2297, 21.0122
  - Categories: cleaning, plumbing, massage
  - Category translation rows: 102 (`3` categories × `34` languages)
  - Seed script: apps/api/scripts/seed_warsaw_launch.py (idempotent)
- **Warsaw Homepage** — Provider-first landing page implemented at `apps/web/app/[lang]/page.tsx`:
  - SSR metadata and hreflang generation
  - Database-backed homepage copy via `fetchTranslations(lang, 'homepage')`
  - Hero with rotating categories, trust bullets, social proof and primary CTA to auth
  - Category cards for cleaning, plumbing, massage
  - Live activity feed, Why Nevumo section, footer service links, mobile sticky CTA
- **Warsaw Category Pages** — Client-first SEO pages implemented at `apps/web/app/[lang]/[city]/[category]/page.tsx`:
  - SSR metadata from DB translations
  - Provider listing cards enriched with provider details, rating, jobs completed and recent lead preview
  - Sticky sidebar lead form
  - SEO body blocks, FAQ schema, internal related links and provider acquisition CTA
- **Namespaced UI Translations** — Public DB-backed translation delivery is live:
  - Endpoint: `GET /api/v1/translations?lang={lang}&namespace={namespace}`
  - Backend file: `apps/api/routes/translations.py`
  - Router mounted in `apps/api/main.py`
  - Redis cache key pattern: `translations:{lang}:{namespace}` with 1 hour TTL
  - English fallback when requested language has no rows for a namespace
- **Verified UI Translation Coverage** — Homepage and category UI copy seeded for 34 languages:
  - Source script: `apps/api/scripts/seed_ui_translations.py`
  - Exact DB-backed UI key counts: `43` homepage + `24` category = `67` per language
  - Total namespace rows seeded/upserted: `2,278`
- **Client Dashboard Shell Upgrade** — `apps/web/app/[lang]/client/dashboard/layout.tsx` now includes:
  - Logout in topbar and sidebar
  - `Стани доставчик` role-switch CTA
  - `НАМЕРИ УСЛУГА` CTA after settings
- **Provider Widget UX Improvement** — `apps/web/components/ProviderWidget.tsx` now supports:
  - Filtering visible service tags by current category
  - Selecting a service tag to auto-fill the description
  - Expand-to-show-all services flow
- **Frontend API Shape Alignment** — `apps/web/lib/api.ts` `ServiceOut` now exposes `category_slug` for category-aware UI filtering
- **Global Phone Field System** — Complete phone persistence and UX:
  - users.phone column added (migration p1q2r3s4t5u6)
  - GET/PATCH /api/v1/user/profile endpoints
  - usePhone hook: sync between localStorage and DB
  - PhoneInput component: auto-prefix by country, soft validation
  - Auto-fill for anonymous (localStorage) and logged-in (DB) users
  - countryCode wired in: category pages, provider pages, 
    ProviderWidget, provider/client dashboard settings
  - GDPR: Legitimate Interest basis, Privacy Policy update pending

### 🔜 Next
- Register first real providers in Warsaw for the 3 seeded launch categories
- Validate live SEO indexing/performance for `/[lang]/warszawa/{category}` pages across priority languages
- Replace placeholder social-proof/activity numbers with real marketplace data once supply is live
- Decide whether homepage/category translation source of truth remains DB-only or also gets script-level auditing/tests
- Monetization sequencing remains:
  - Phase now: free acquisition + lead volume validation
  - Primary business model: pay-per-lead
  - Later experiment: featured placement after initial liquidity
- Dashboard design polish (UI refinements across all pages)
- UX simplification: auto-currency from city, conditional price field
- Email sending for reset password (Resend / SendGrid)
- OAuth — Google + Facebook
- Privacy Policy + Cookie/Storage Banner 
  (must mention phone localStorage storage)

### Recent Changes (April 2026)
- **April 4 Strategic Decisions — Warsaw launch operating model**
  - **Categories**: launch scope is intentionally constrained to `cleaning`, `plumbing`, and `massage` to validate supply-demand fit before adding more verticals
  - **Homepage strategy**: homepage is provider-first and optimized for specialist acquisition, not for client browsing
  - **Category-page strategy**: `/[lang]/[city]/[category]` pages are client-first and optimized for SEO capture + lead conversion
  - **SEO strategy**: build programmatic, multilingual city/category landing pages with SSR metadata, hreflang, internal linking, FAQ schema and text blocks
  - **Monetization strategy**: do not monetize early Warsaw launch traffic aggressively; validate liquidity first, keep primary long-term model as pay-per-lead, and treat featured placement as a later-stage monetization layer

- **April 4 Database Changes — launch market data + translation infrastructure**
  - **Locations**:
    - Added Warsaw launch city in `locations`: `Warszawa`, country `PL`, slug `warszawa`, coordinates `52.2297, 21.0122`
  - **Categories**:
    - Seeded/ensured root categories `cleaning`, `plumbing`, `massage`
  - **Category translations**:
    - Script: `apps/api/scripts/seed_warsaw_launch.py`
    - Exact rows: `102` category translation rows (`3` categories × `34` languages)
    - Stored in `category_translations`
  - **UI translations**:
    - Script: `apps/api/scripts/seed_ui_translations.py`
    - Namespace model stored in `translations` table as `namespace.key`
    - Exact final key counts per language: `43` homepage keys + `24` category keys = `67`
    - Exact seeded/upserted UI translation rows across all supported languages: `2,278`
  - **Language set expanded and normalized to 34 supported languages**:
    - `bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, is, it, lb, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, ru, sk, sl, sq, sr, sv, tr, uk`

- **April 4 Backend Changes**
  - **New public endpoint**: `GET /api/v1/translations?lang={lang}&namespace={namespace}`
    - File: `apps/api/routes/translations.py`
    - Returns flat translation payload without namespace prefix
    - Falls back to English if requested language namespace is missing
    - Caches successful payloads in Redis for 1 hour
  - **Router wiring**:
    - File: `apps/api/main.py`
    - `translations_router` mounted under `/api/v1`
  - **New seed scripts**:
    - `apps/api/scripts/seed_warsaw_launch.py` — idempotent Warsaw location/category/category-translation bootstrap
    - `apps/api/scripts/seed_ui_translations.py` — DB seed/upsert for homepage/category UI copy in 34 languages

- **April 4 Frontend Changes**
  - **`apps/web/app/[lang]/page.tsx`**
    - Homepage converted to DB-backed multilingual SSR page
    - Metadata now resolved via homepage namespace translations
    - Navigation/service links normalized around Warsaw launch URLs
    - Provider-first content structure finalized: hero, trust row, how-it-works, category cards, activity feed, why section, second CTA, footer, mobile sticky CTA
  - **`apps/web/components/homepage/RotatingCategory.tsx`**
    - Client component rotates translated category labels from DB-fed homepage data
  - **`apps/web/app/[lang]/[city]/[category]/page.tsx`**
    - Category page converted to DB-backed multilingual SSR page
    - Heading/subtitle/SEO copy/provider CTA now read from category/homepage translation namespaces
    - Provider cards enriched using provider detail fetches for better trust signals
    - FAQ JSON-LD retained for search visibility
    - Internal related-link structure created between the 3 Warsaw launch categories
  - **`apps/web/components/category/LeadForm.tsx`**
    - Lead form made reusable/translation-ready through prop-based title, subtitle, placeholders, button label and trust-item inputs
    - Continues to submit minimal conversion payload (`phone`, optional `description`, `source: 'seo'`)
  - **`apps/web/lib/ui-translations.ts`**
    - Added frontend helper for fetching namespace translations from the API with hourly revalidation
    - Supported-language guard now matches the 34-language rollout
  - **`apps/web/lib/api.ts`**
    - `ServiceOut` extended with `category_slug`, enabling category-aware UI behavior
  - **`apps/web/app/[lang]/client/dashboard/layout.tsx`**
    - Added logout, role switch and homepage CTA improvements in the client shell
  - **`apps/web/components/ProviderWidget.tsx`**
    - Added selectable service chips, auto-filled request description and expanded service-list behavior
  - **Asset cleanup**:
    - `apps/web/public/Nevumo_logo-2.svg` removed as unused duplicate asset

- **Design System Decisions Established**
  - **Primary brand action color**: orange remains the dominant CTA and emphasis color across homepage, category pages and dashboard actions
  - **Surface system**: white primary surfaces, light gray secondary sections, rounded-xl cards, soft borders and soft shadows
  - **Conversion-first UI**: one primary action per section, short trust bullets, friction-minimized forms, immediate CTA visibility on mobile via sticky controls
  - **Trust modules**: ratings, specialist counts, request velocity, FAQ content and proof snippets are reusable building blocks across SEO pages and widgets
  - **Responsive layout pattern**:
    - Homepage: stacked storytelling sections with repeated CTA opportunities
    - Category page: content/listing column + sticky conversion sidebar

- **Scale Principles Reaffirmed**
  - **Programmatic rollout over bespoke pages**: one reusable homepage pattern and one reusable category-page pattern should scale city-by-city and language-by-language
  - **DB as content source of truth**: UI copy moved out of hardcoded components and into PostgreSQL so new languages/markets can be rolled out without reworking page structure
  - **Cache multilingual payloads aggressively**: Redis namespaced caching keeps translation reads cheap while preserving server-rendered SEO output
  - **Launch narrow, then expand**: prove liquidity in one city and three categories before broadening the matrix of locations/categories
  - **Keep conversion payload minimal**: public lead capture remains intentionally simple to maximize completion rate and support future scaling

- **Homepage Implementation (Warsaw)** — Provider-first landing page:
  - DB-backed multilingual SSR content fetched by namespace
  - Rotating hero section with translated launch categories
  - Category cards with icons and counts
  - Live activity feed showing recent requests
  - Mobile-responsive design with Tailwind CSS
- **Category Page Implementation** — Client-first service discovery:
  - Server-side rendering with DB-backed translations
  - Two-column layout with lead form and provider listings
  - SEO text blocks for content marketing
  - FAQ schema markup for search visibility
  - Internal linking structure for navigation
- **Warsaw Launch** — Complete marketplace initialization:
  - 1 city: Warszawa (PL)
  - 3 categories: cleaning, plumbing, massage
  - 34 language translations for all categories
  - Idempotent seed script for safe re-running
- **Implemented Review/Rating System** — Closed trust conversation model:
  - Database migration for provider reply fields and user email preferences
  - Backend API endpoints for client and provider review flows
  - Email notification service with opt-out mechanism
  - Provider dashboard reviews section with reply/edit functionality
  - Client dashboard completed jobs with review CTA
  - Client email preferences toggle
  - Translation keys for all 34 languages
  - Updated documentation (api_contracts, db_schema, architecture)
- **Social Proof + Multi-Role Review Restore** — Root-cause fix and review hardening:
  - Applied `users.name` migration (`i8j9k0l1m2n3`) to restore embed/social-proof and authenticated dashboard queries
  - Provider dashboard route now loads provider profile through the correct `get_provider_profile(provider, db)` contract
  - Review surfaces now use canonical `users.name` display names with `Client` fallback, never email-derived names
  - Backend review eligibility, can-review checks, and create-review flow now block self-reviews via `Provider.user_id == client_id`
  - Public `POST /api/v1/leads` now links authenticated submissions to `lead.client_id`, enabling real review eligibility for logged-in users
- **Rating card** on provider dashboard clearly labeled as "Overall Rating" from all client reviews
- **Client Dashboard Backend Expansion** — Added authenticated `/api/v1/client/dashboard` and `/api/v1/client/leads` endpoints:
  - Dashboard overview now returns `active_leads`, `completed_leads`, `reviews_written`, and latest 3 leads for the current client
  - Leads inbox now supports `all|active|done|rejected` filters, provider metadata, English category fallback, and `has_review`
  - `main.py` already included the shared `client_router`, so no new router wiring was needed beyond extending `routes/client.py`
- **Client Dashboard Frontend** — Implemented provider-style client shell and pages:
  - New guarded layout at `/[lang]/client/dashboard/*` with dedicated sidebar/topbar, active nav state, email in topbar, and orange `НАМЕРИ УСЛУГА` CTA
  - `apps/web/lib/client-api.ts` adds strict typed wrappers for dashboard, leads, reviews, eligible leads, review submission, and review preferences
  - Overview page renders KPI cards + recent leads hero/empty state
  - My Requests page renders status tabs, lead cards, and inline review submission for completed provider-linked jobs without reviews
  - Reviews page now splits into `Написани` and `Чакащи ревю`, with collapsible provider replies and the shared review-reply email toggle
  - Settings page now contains readonly email, reset-password link, `Стани доставчик`, and logout

### 🔮 Future
- AI lead matching
- Subscription / pay-per-lead billing
- Multi-region DB partitioning
- Advanced provider analytics