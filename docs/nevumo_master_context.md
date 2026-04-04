# Nevumo Master Context

## Project Overview
Nevumo е уеб платформа за marketplace на услуги.
- Доставчици публикуват услуги
- Клиенти търсят и се свързват с доставчици
- Платформата е мултиезична (32 езика)
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

### Supported languages (34):
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, it, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, sk, sl, sq, sr, sv, tr, uk

- Default language: en

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

---

## Roadmap Status

### ✅ Complete
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
  - Translations: 34 languages for all categories
  - Seed script: apps/api/scripts/seed_warsaw_launch.py (idempotent)

### 🔜 Next
- ✅ Homepage (Warsaw, provider-first)
- ✅ Category page (client-first, SEO)
- ✅ Warsaw launch data seeding
- 🔜 Register first real providers in Warsaw
- 🔜 Monetization: Featured placement (month 6)
- Dashboard design polish (UI refinements across all pages)
- UX simplification: auto-currency from city, conditional price field
- Email sending for reset password (Resend / SendGrid)
- OAuth — Google + Facebook

### Recent Changes (April 2026)
- **Homepage Implementation (Warsaw)** — Provider-first landing page:
  - Polish content with SSR optimization
  - Rotating hero section with provider testimonials
  - Category cards with icons and counts
  - Live activity feed showing recent requests
  - Mobile-responsive design with Tailwind CSS
- **Category Page Implementation** — Client-first service discovery:
  - Server-side rendering for SEO optimization
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