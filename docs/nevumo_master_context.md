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

### Supported languages (32):
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, it, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, sk, sl, sq, sr, sv, tr

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
- Client Dashboard — with reviews, completed jobs, and email preferences
- DB: service_cities table (many-to-many service↔city), currency on services, per_sqm price type
- SearchInput Component: Unified searchable select component (single/multi-select modes)
- **URL Redirect System** — Complete slug change management with 301 redirects, SEO protection, loop prevention
- **Slug Change Security** — Backend-controlled change limits (1 change after onboarding), frontend manipulation protection
- **Automatic Redirect Resolution** — Seamless frontend URL updates, browser address bar synchronization
- **Review System (Closed Trust Conversation Model)** — Complete review/rating system with:
  - Client reviews for completed jobs
  - Provider single reply (editable)
  - Email notifications on first reply (with opt-out)
  - Dashboard integration (provider reviews section, client reviews page)
  - 34-language translation support

### 🔜 Next
- Dashboard design polish (UI refinements across all pages)
- UX simplification: auto-currency from city, conditional price field
- Email sending for reset password (Resend / SendGrid)
- OAuth — Google + Facebook

### Recent Changes (April 2026)
- **Implemented Review/Rating System** — Closed trust conversation model:
  - Database migration for provider reply fields and user email preferences
  - Backend API endpoints for client and provider review flows
  - Email notification service with opt-out mechanism
  - Provider dashboard reviews section with reply/edit functionality
  - Client dashboard completed jobs with review CTA
  - Client email preferences toggle
  - Translation keys for all 34 languages
  - Updated documentation (api_contracts, db_schema, architecture)
- **Rating card** on provider dashboard clearly labeled as "Overall Rating" from all client reviews

### 🔮 Future
- AI lead matching
- Subscription / pay-per-lead billing
- Multi-region DB partitioning
- Advanced provider analytics