# Nevumo Project Audit Report

**Date:** 2026-03-21
**Auditor:** Claude Code (claude-sonnet-4-6)
**Branch:** `claude/audit-nevumo-project-cpGdz`

---

## STEP 1: Repository Structure

```
nevumo/
├── .env.example
├── .github/
│   └── copilot-instructions.md
├── .gitignore
├── .npmrc
├── AGENTS.md
├── README.md
├── docker-compose.yml
├── fix_login.sql
├── package-lock.json
├── package.json
├── run-local.sh
├── turbo.json
├── apps/
│   ├── api/
│   │   ├── database.py
│   │   ├── i18n.py
│   │   ├── insert_login_translations.py
│   │   ├── load_login_nav_translations.py
│   │   ├── main.py
│   │   ├── migrate_add_provider_category.py
│   │   ├── models.py
│   │   ├── requirements.txt
│   │   ├── seed_translations.py
│   │   ├── test_redis.py
│   │   ├── update_login_heading_translations.py
│   │   └── upsert_login_meta_translations.py
│   ├── docs/
│   │   ├── .gitignore
│   │   ├── README.md
│   │   ├── app/
│   │   │   ├── favicon.ico
│   │   │   ├── fonts/
│   │   │   ├── globals.css
│   │   │   ├── layout.tsx
│   │   │   ├── page.module.css
│   │   │   └── page.tsx
│   │   ├── eslint.config.js
│   │   ├── next.config.js
│   │   ├── package.json
│   │   ├── public/
│   │   └── tsconfig.json
│   └── web/
│       ├── .gitignore
│       ├── README.md
│       ├── app/
│       │   ├── [lang]/
│       │   │   ├── [city]/
│       │   │   │   └── [category]/
│       │   │   │       └── [providerPage]/
│       │   │   │           └── page.tsx
│       │   │   ├── login/
│       │   │   │   └── page.tsx
│       │   │   └── page.tsx
│       │   ├── favicon.ico
│       │   ├── fonts/
│       │   ├── globals.css
│       │   ├── layout.tsx
│       │   ├── page.module.css
│       │   └── page.tsx
│       ├── components/
│       │   └── ui/
│       │       └── ActionCard.tsx
│       ├── eslint.config.js
│       ├── lib/
│       │   ├── locales.ts
│       │   └── slugify.ts
│       ├── middleware.ts
│       ├── next.config.js
│       ├── package.json
│       ├── postcss.config.cjs
│       ├── public/
│       ├── tailwind.config.js
│       └── tsconfig.json
├── components/
│   └── LeadForm.tsx          ← Outside apps/ (root-level, imported by web)
├── docs/
│   ├── api_contracts.md
│   ├── architecture.md
│   ├── db_schema.md
│   ├── models.py             ← Reference models (not production code)
│   └── nevumo_master_context.md
└── packages/
    ├── eslint-config/
    │   ├── README.md
    │   ├── base.js
    │   ├── next.js
    │   ├── package.json
    │   └── react-internal.js
    ├── typescript-config/
    │   ├── base.json
    │   ├── nextjs.json
    │   ├── package.json
    │   └── react-library.json
    └── ui/
        ├── eslint.config.mjs
        ├── package.json
        ├── src/
        │   ├── button.tsx
        │   ├── card.tsx
        │   ├── code.tsx
        │   └── index.ts
        ├── theme.config.ts
        └── tsconfig.json
```

---

## STEP 2: Monorepo Setup

### turbo.json — EXISTS

```json
{
  "$schema": "https://turborepo.dev/schema.json",
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "lint": { "dependsOn": ["^lint"] },
    "check-types": { "dependsOn": ["^check-types"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

### root package.json — EXISTS

- `name`: `my-monorepo` (not updated to "nevumo")
- `workspaces`: `["apps/*", "packages/*"]`
- `packageManager`: `npm@11.11.0`
- `turbo`: `^2.8.14`

### Directory Existence

| Directory | Exists | package.json / config |
|---|---|---|
| `apps/web` | ✅ | `next@16.1.5`, `react@^19.2.0` |
| `apps/api` | ✅ | `requirements.txt` (Python) |
| `apps/docs` | ✅ | Turborepo default starter |
| `packages/ui` | ✅ | `@repo/ui`, Button, Card, Code |
| `packages/typescript-config` | ✅ | base.json, nextjs.json |

> **Note:** `apps/docs` is a stock Turborepo starter; not customized for Nevumo.

---

## STEP 3: Backend Audit (`apps/api`)

### FastAPI Initialization

`apps/api/main.py` initializes FastAPI correctly:

```python
app = FastAPI(title="Nevumo API")
```

CORS middleware is added with `allow_origins=["*"]` — overly permissive for production.

### models.py — PARTIAL (3 of 12 required tables)

**Found in `apps/api/models.py`:**

| Model | Table | Status |
|---|---|---|
| `Lead` | `leads` | ✅ (simplified: id, client_name, phone, service_type, notes) |
| `Translation` | `translations` | ✅ (id, lang, key, value) |
| `Provider` | `providers` | ✅ (id, name, job_title, category, rating, jobs_completed, is_verified, city, profile_image_url, slug) |

**Missing from `models.py` (per expected model list):**

| Expected Model | Status |
|---|---|
| `Users` | ❌ MISSING |
| `ProviderCity` | ❌ MISSING |
| `Location` | ❌ MISSING |
| `Category` | ❌ MISSING |
| `CategoryTranslation` | ❌ MISSING |
| `Service` | ❌ MISSING |
| `LeadMatch` | ❌ MISSING |
| `Message` | ❌ MISSING |
| `LeadEvent` | ❌ MISSING |
| `LeadRateLimit` | ❌ MISSING |

> **Note:** `docs/db_schema.md` documents all 12 tables in full SQL, but none are implemented in `models.py`. The existing `Lead` model in `models.py` diverges from the spec (uses `INT` primary key, missing `status`, `utm_*`, `source`, etc.). Additionally, `Lead` is duplicated between `database.py` and `models.py`.

### Pydantic Schemas — PARTIAL

- **No dedicated `schemas.py` file.**
- Schemas are defined inline in `main.py`:
  - `ProviderSchema` (id, name, slug, job_title, job_title_key, category, category_key, rating, jobs_completed, is_verified, city, profile_image_url)
  - `ProviderCategoryUpdateSchema` (category_key, translations)
- Lead creation uses raw `dict` instead of a typed Pydantic model: `async def create_lead(lead: dict, ...)`.

### API Routes — PARTIAL (4 routes, none match required spec)

**Implemented routes:**

| Method | Path | Description |
|---|---|---|
| GET | `/translations/{lang}` | Fetch i18n translations (Redis-cached) |
| GET | `/provider-info/{provider_id}` | Get provider by integer ID |
| PUT | `/providers/{provider_id}/category` | Update provider category |
| POST | `/leads/` | Create a lead (minimal fields) |

**Required endpoints vs. found:**

| Required Endpoint | Status | Notes |
|---|---|---|
| `GET /api/v1/providers` (category_slug, city_slug, lang) | ❌ MISSING | Replaced by `/provider-info/{id}` |
| `GET /api/v1/providers/{provider_slug}` | ❌ MISSING | Route uses integer ID not slug |
| `POST /api/v1/leads` | ⚠️ PARTIAL | Exists as `POST /leads/`, missing UTM fields, validation, rate limiting |
| `GET /api/v1/categories` | ❌ MISSING | |
| `GET /api/v1/cities` | ❌ MISSING | |
| `POST /api/v1/events` | ❌ MISSING | |
| `GET /api/v1/provider/leads` | ❌ MISSING | |
| `PATCH /api/v1/provider/leads/{id}` | ❌ MISSING | |

> **Critical:** No routes use the `/api/v1` prefix. The API base URL in `copilot-instructions.md` specifies `/api/v1` but is not implemented.

### Alembic — MISSING

- No `alembic.ini`
- No `alembic/` directory
- No migration files
- Database schema is created via `init_db()` calling `Base.metadata.create_all()` — no version-controlled migrations.

### Requirements (`requirements.txt`) — EXISTS

Key dependencies:
- `fastapi==0.135.1`
- `SQLAlchemy==2.0.48`
- `pydantic==2.12.5`
- `redis==7.3.0`
- `psycopg2-binary==2.9.11`
- `uvicorn==0.42.0`

### Redis Configuration — PARTIAL

Redis client initialized in `main.py`:
```python
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
```

- ✅ Try/except fallback if Redis unavailable
- ✅ Used for caching translations (`setex` with 3600s TTL) and cache invalidation on category updates
- ❌ Hardcoded `localhost:6379` — does not read from environment variables
- ❌ Redis service missing from `docker-compose.yml` (only PostgreSQL defined)

---

## STEP 4: Frontend Audit (`apps/web`)

### Next.js — EXISTS

`next.config.js`:
```js
const nextConfig = {
  reactStrictMode: true,
  transpilePackages: ["@repo/ui"],
  images: {
    remotePatterns: [
      { protocol: 'http', hostname: '127.0.0.1', port: '8000', pathname: '/**' },
      { protocol: 'https', hostname: 'i.pravatar.cc', pathname: '/**' }
    ]
  }
};
```

**Next.js version:** `16.1.5` (React 19 compatible)

### Tailwind CSS 4 — PARTIAL

- `tailwindcss@^4.2.2` installed (`package.json`)
- `@tailwindcss/postcss@^4.2.2` installed
- `postcss.config.cjs` correctly uses `@tailwindcss/postcss` plugin (v4 style)

**However, `tailwind.config.js` uses v3 syntax:**
```js
module.exports = {
  content: [...],
  theme: { extend: { colors: {...}, borderRadius: {...} } },
  plugins: []
}
```

Tailwind CSS v4 uses CSS-first configuration (`@theme` in CSS) rather than `tailwind.config.js`. This is a version mismatch — v4 packages with v3 config syntax.

### `app/` Directory Structure

```
app/
├── [lang]/
│   ├── [city]/
│   │   └── [category]/
│   │       └── [providerPage]/   ← page.tsx (provider profile)
│   ├── login/
│   │   └── page.tsx
│   └── page.tsx                  ← lang landing page
├── favicon.ico
├── fonts/
├── globals.css
├── layout.tsx
├── page.module.css
└── page.tsx                      ← root page
```

### SEO Route Structure — PARTIAL

| Route | Status | Notes |
|---|---|---|
| `/[lang]/[city]/[category]/[providerPage]/page.tsx` | ✅ EXISTS | Provider profile page with `generateMetadata` |
| `/[lang]/[city]/[category]/page.tsx` | ❌ MISSING | Category/city listing page (critical for SEO) |
| `/[lang]/page.tsx` | ✅ EXISTS | Language landing page (placeholder content) |

> **Note:** The `[providerPage]` segment parses `{slug}-{id}` format (e.g., `maria-petrova-1`) using regex. It calls the backend via hardcoded `http://127.0.0.1:8000` — no `NEXT_PUBLIC_API_URL` env variable usage.

### API Client Utilities — PARTIAL

- No dedicated API client module
- All fetch calls are inline in page components with hardcoded `http://127.0.0.1:8000`
- `lib/locales.ts` contains `getDictionary()` with hardcoded base URL
- `NEXT_PUBLIC_API_URL` is defined in `.env.example` but not used anywhere in code

### TypeScript — PARTIAL (strict mode inherited)

`apps/web/tsconfig.json` extends `@repo/typescript-config/nextjs.json`, which extends `base.json`:

```json
// base.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true
  }
}
```

`apps/web/tsconfig.json` adds `"strictNullChecks": true` (already implied by `strict: true`).

> **Issue:** `apps/web/tsconfig.json` does **not** have `"strict": true` explicitly, relying on inheritance. However, `locales.ts` uses `any` types in `TranslationDictionary` and `getDictionary()` return type, violating the strict no-`any` rule.

---

## STEP 5: Shared Packages

### `packages/ui` — PARTIAL

Components exported:

| Component | File | Description |
|---|---|---|
| `Button` | `src/button.tsx` | Client component, triggers `alert()` on click |
| `Card` | `src/card.tsx` | Anchor link card |
| `Code` | `src/code.tsx` | Code display element |

- `src/index.ts` exports from `../theme.config.ts` (not the components)
- `package.json` has **duplicate `exports` field** (both `"."` pointing to `./src/index.ts` and `"./*"` pointing to `./src/*.tsx`) — the second overrides the first
- No Nevumo-specific components (e.g., ProviderCard, LeadForm, SearchBar)
- `LeadForm.tsx` is at root `components/` (not in `packages/ui`)
- `ActionCard.tsx` is in `apps/web/components/ui/` (not in `packages/ui`)

### `packages/typescript-config` — EXISTS

| File | Purpose |
|---|---|
| `base.json` | Strict TypeScript base (strict: true, noUncheckedIndexedAccess) |
| `nextjs.json` | Next.js-specific (extends base, adds jsx: preserve, noEmit) |
| `react-library.json` | React library config |

---

## STEP 6: Infrastructure & Config

### Environment Variables (`.env.example`) — EXISTS

Variable names only (no values shown):

```
DATABASE_URL
POSTGRES_DB
POSTGRES_USER
POSTGRES_PASSWORD
REDIS_HOST
REDIS_PORT
REDIS_DB
API_HOST
API_PORT
API_RELOAD
SECRET_KEY
CORS_ORIGINS
NEXT_PUBLIC_API_URL
NEXT_PUBLIC_SITE_URL
NEXT_PUBLIC_DEFAULT_LANG
NODE_ENV
PYTHON_ENV
```

> **Note:** Environment variables are defined in `.env.example` but the backend (`main.py`, `database.py`) uses **hardcoded values** (`localhost`, `secure_password`, etc.) rather than reading from environment.

### Docker / docker-compose — PARTIAL

`docker-compose.yml` defines only:
- `db` (PostgreSQL 15)

**Missing:**
- Redis service
- API (FastAPI) service
- Web (Next.js) service

### CI/CD — MISSING

- `.github/workflows/` directory does **not** exist
- No automated build, test, or deploy pipelines

### Agent/AI Instructions — EXISTS

| File | Status |
|---|---|
| `.github/copilot-instructions.md` | ✅ EXISTS (comprehensive rules) |
| `AGENTS.md` | ✅ EXISTS (concise rules) |
| `.windsurfrules` | ❌ MISSING |

---

## STEP 7: Gap Analysis

| # | Component | Status | Details |
|---|---|---|---|
| 1 | Turborepo monorepo setup | ✅ EXISTS | `turbo.json` + root `package.json` with workspaces; all apps and packages present |
| 2 | Backend FastAPI app initialization | ✅ EXISTS | `apps/api/main.py` with `FastAPI(title="Nevumo API")`, CORS middleware, Redis init |
| 3 | SQLAlchemy models (all 12 tables) | ❌ MISSING | Only 3 of 12 tables implemented (`Lead`, `Translation`, `Provider`); missing `Users`, `ProviderCity`, `Location`, `Category`, `CategoryTranslation`, `Service`, `LeadMatch`, `Message`, `LeadEvent`, `LeadRateLimit` |
| 4 | Alembic migrations | ❌ MISSING | No `alembic.ini`, no `alembic/` directory; schema managed via `create_all()` only |
| 5 | Pydantic schemas | ⚠️ PARTIAL | 2 schemas exist inline in `main.py`; no `schemas.py`; lead creation uses raw `dict` |
| 6 | API routes (all 8 endpoints) | ❌ MISSING | 4 routes exist but none use `/api/v1` prefix; 7 of 8 required endpoints are missing or mis-implemented |
| 7 | Redis caching layer | ⚠️ PARTIAL | Client initialized with fallback; translations cached; but hardcoded config, Redis absent from docker-compose |
| 8 | Frontend Next.js setup | ✅ EXISTS | Next.js 16.1.5 + React 19, `reactStrictMode: true`, i18n middleware, SEO metadata |
| 9 | SEO route structure (`/{lang}/{city}/{category}`) | ⚠️ PARTIAL | `/[lang]/[city]/[category]/[providerPage]` exists; **listing page** `/[lang]/[city]/[category]` is **missing** |
| 10 | Tailwind CSS 4 config | ⚠️ PARTIAL | v4 packages installed + PostCSS plugin correct; `tailwind.config.js` uses v3 syntax (incompatible with v4 CSS-first approach) |
| 11 | TypeScript strict mode | ⚠️ PARTIAL | `strict: true` in shared `base.json` (inherited); some files use `any` types violating strict rule |
| 12 | Shared UI package | ⚠️ PARTIAL | 3 generic components (Button, Card, Code); no Nevumo-specific components; duplicate `exports` in `package.json`; `index.ts` only exports theme config |
| 13 | Shared TypeScript config | ✅ EXISTS | `packages/typescript-config` with `base.json`, `nextjs.json`, `react-library.json` |
| 14 | Environment config (`.env.example`) | ✅ EXISTS | 17 variables documented; backend code does **not** read from env vars |
| 15 | Translation system (32 languages) | ⚠️ PARTIAL | 30 languages implemented (vs. 32 documented); DB-backed with Redis cache; i18n middleware functional; `getDictionary()` uses `any` types and hardcoded URL |

---

## Summary of Critical Issues

### 🔴 Blockers (must fix before launch)

1. **Models incomplete** — 9 of 12 required SQLAlchemy models are missing. The entire data model (users, categories, locations, services, lead matching, messaging, events, rate limiting) is not implemented.

2. **API routes do not match spec** — None of the 8 required `/api/v1/...` endpoints exist. The implemented routes use different paths and different conventions (integer IDs vs. slugs).

3. **No Alembic migrations** — Database versioning is entirely absent. `create_all()` cannot handle schema evolution in production.

4. **Hardcoded credentials** — `database.py` has a hardcoded connection string with credentials. `main.py` has hardcoded Redis config. `.env.example` is defined but ignored by the code.

5. **Missing category/city listing page** — `/[lang]/[city]/[category]` (the core SEO page) does not exist. Only the individual provider profile page is implemented.

### 🟡 Important Issues (fix before production)

6. **Tailwind CSS v4/v3 config mismatch** — `tailwind.config.js` uses v3 `module.exports` syntax while v4 packages are installed. Styles may break on build.

7. **Redis missing from docker-compose** — Starting the project with `docker-compose up` will not start Redis, causing the caching layer to silently fail.

8. **No API client utility** — All fetch calls are hardcoded to `http://127.0.0.1:8000` inline in components. `NEXT_PUBLIC_API_URL` env var is defined but unused.

9. **`any` types in TypeScript** — `lib/locales.ts` uses `any` in multiple places, violating the strict no-`any` code convention.

10. **CORS wildcard** — `allow_origins=["*"]` in FastAPI CORS config is unsafe for production.

11. **Language count discrepancy** — Documentation claims 32 languages; only 30 are implemented.

12. **Root-level `components/` directory** — `LeadForm.tsx` lives at the root `components/` rather than in `apps/web/components/` or `packages/ui/`, violating the monorepo folder conventions.

### 🟢 What's working well

- Turborepo monorepo structure is correctly configured
- Next.js 16 + React 19 setup is functional
- i18n middleware correctly handles language detection, cookie management, and redirects
- 30-language translation system is implemented with DB persistence and Redis caching
- TypeScript config inheritance (strict mode) is properly set up
- `.env.example` is comprehensive and well-documented
- `AGENTS.md` and `copilot-instructions.md` provide clear development guidelines
- Provider profile page (`[providerPage]`) has `generateMetadata` for SEO

---

*Report generated by automated audit on 2026-03-21.*
