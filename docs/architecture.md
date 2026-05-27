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
- **Volume Mapping (May 5, 2026)**: Local development for the web service now uses selective volume mounting to prevent host node_modules from overriding container-specific native dependencies:
  - `./apps/web:/workspace/apps/web` — Source code hot-reload
  - `./packages:/workspace/packages` — Shared packages
  - `./apps/web/.env.local:/workspace/apps/web/.env.local` — Environment variables
  - `web_node_modules:/workspace/node_modules` — Named volume to preserve container node_modules (prevents host override)
- **Base Image Selection (May 5, 2026)**: The web service uses `node:22-slim` (Debian with glibc) instead of Alpine to ensure compatibility with native npm modules like lightningcss that require glibc. Alpine's musl libc is incompatible with certain native dependencies.
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
- **Inter-container Communication**: Containers in Docker Compose communicate using service names (e.g., `nevumo-api`, `nevumo-postgres`) rather than `localhost`.
- **CORS Configuration (April 2026)**: Added `CORSMiddleware` to `apps/api/main.py` using a configurable `CORS_ORIGINS` setting from `.env` (via `load_dotenv()`) to allow secure communication from the frontend domain.

### 5. Next.js & UI (Metadata + i18n)
- **Universal Slug Generation (April 30, 2026)**: Unified URL slug generation logic between Frontend and Backend to support all 34 languages.
  - **Frontend**: Removed the hardcoded 'bg' locale from `apps/web/lib/slug-utils.ts` and replaced the primitive implementation in `apps/web/lib/slugify.ts` with the robust `slugify` library.
  - **Backend**: Standardized `apps/api/services/provider_service.py` to use a consistent `slugify` wrapper with pre-defined Cyrillic replacements, ensuring identical output for special characters (Turkish İ/ı, German ü/ö, Icelandic ð/þ, etc.) across the entire stack.
- **Universal Currency Logic (April 30, 2026)**: Implemented a centralized currency determination system based on provider location.
  - **Source of Truth**: Currency is derived from `provider.services[0].currency` with fallback to `provider.city.country_code` via `apps/web/lib/currency.ts`.
  - **Fallback Chain**: Service currency → City country code → Country default → 'EUR'
  - **Special Rule (Bulgaria)**: For country "BG", from 01.01.2026 the currency is strictly "EUR" (Euro), regardless of previous BGN defaults.
  - **Scope**: Applied to both JSON-LD (`priceCurrency`) and UI visualization (ProviderWidget).
  - **Country Defaults**: RSD for RS (Serbia), PLN for PL (Poland), EUR for BG (Bulgaria), with dynamic defaults for other countries.
- **Provider Page Error Fixes & SEO Enhancement (April 30, 2026)**:
  - **ReferenceError Fix**: Resolved "currency is not defined" in `ProviderWidget.tsx` by ensuring the variable is scoped correctly and has a multi-layer fallback (service data -> city data -> country default -> 'EUR').
  - **Parsing Error Fix**: Corrected misaligned and missing closing `div` tags in `apps/web/app/[lang]/[city]/[category]/[providerPage]/page.tsx` that interfered with Next.js metadata generation.
  - **Service Schema**: Added explicit `Service` JSON-LD schema to `ProviderWidget.tsx` to complement the `LocalBusiness` schema, providing search engines with detailed price and location data for specific offerings.
- **Dynamic Category FAQ System & "Golden Standard" (May 2026)**:
  - **Implementation**: Refactored `apps/web/app/[lang]/[city]/[category]/page.tsx` to use dynamic translations for the FAQ section.
  - **Key Pattern**: `category.faq_${catKey}_q1` through `q3` and `a1` through `a3`.
  - **Interpolation**: Added support for `{city}`, `{category_name}`, `{min_price}`, `{max_price}`, and `{currency}` variables within translation strings.
  - **Placeholder Safety (May 2, 2026)**: Implemented aggressive regex-based removal of price placeholders when no valid price data is available. If `hasValidPrice` is false, any phrase containing `{min_price}`, `{max_price}`, or `{currency}` is automatically replaced with the "Price on request" translation.
  - **Fallback Chain**: Database translation → Hardcoded `CATEGORY_CONTENT` fallback → `getPriceText` (for empty price-related answers).
  - **SEO Synchronization**: The same translated and interpolated FAQ items are used for both the visual UI section and the `FAQPage` JSON-LD schema, ensuring consistency for both users and search engines.
  - **FAQ Section Removal (May 6, 2026)**: Removed the FAQ section rendering block from category pages due to content duplication with the SEO section. The SEO section now provides all necessary content without redundancy.
  - **SEO Section {city} Variable Replacement (May 6, 2026)**: Added `replaceCity` helper function to replace `{city}` placeholder with actual city name in SEO section translations. This ensures dynamic city names appear correctly in all SEO content across all languages.
- **Dynamic Preposition & Declension Logic (May 2026)**:
  - **Implementation**: Enhanced `getLocalizedCityText` in `apps/web/lib/cityHelpers.ts` to handle both language-specific prepositions (e.g., PL: "w" vs "we") and grammatical declension for specific languages (e.g., Polish locative and genitive forms).
  - **Rules**:
    - **Prepositions**: Change based on the first letter of the city name (BG: в/във, PL: w/we, CS/SK/RU: v/ve, etc.).
    - **Declension (All Slavic Languages)**: 
      - **Locative**: Used for "in {city}" context (e.g., PL: Warszawa → Warszawie, BG: Варшава → Варшава, RU: Варшава → Варшаве).
      - **Genitive**: Used for "from {city}" context (e.g., PL: Warszawa → Warszawy, BG: Варшава → Варшава, RU: Варшава → Варшавы).
  - **Keys**: Uses `locative_form` and `genitive_form` from the `city` translation namespace.
  - **Helper Function**: `getLocalizedCityText(text, lang, cityName, cityT, grammaticalCase)` handles the replacement of `{city}` and the adjustment of surrounding prepositions.
  - **Seed Scripts**: 
    - `apps/api/scripts/seed_city_preposition_translations.py` - Seeds preposition and declension keys for all 34 languages.
  - **Current Implementation Status (May 6, 2026)**:
    - **✅ Completed**: All Slavic languages (bg, cs, sk, ru, uk, sr, hr, mk, sl, pl) - Declension and dynamic prepositions working correctly
    - **✅ Completed**: All 34 languages - Locative and genitive forms seeded for Warsaw
    - **✅ Completed**: Homepage (/bg/warsaw, /pl/warsaw, /ru/warsaw, /cs/warsaw, etc.) - All declension and dynamic prepositions working correctly
    - **✅ Completed**: City pages - All declension and dynamic prepositions working correctly
    - **✅ Completed**: Category pages - All declension and dynamic prepositions working correctly
    - **✅ Completed**: Seed script executed and database populated with all language forms
    - **✅ Completed**: cityHelpers.ts extended with grammaticalCase parameter for all Slavic languages
    - **✅ Completed**: Homepage, city page, and category page components updated with Slavic language support
    - **✅ Completed (May 6, 2026)**: Category page preposition logic fix - Changed from hardcoded "in" to dynamic `prepBase` from `categoryT` namespace; Updated title, heading, related links, and provider CTA to use `categoryT` instead of `cityT` for preposition logic; Added regex-based replacement in cityHelpers.ts to handle prepositions without leading space
    - **✅ Completed (May 10, 2026)**: city.locative_form / city.genitive_form премахнати от translations таблицата; данните преместени в location_translations; getLocalizedCityText обновен с cityForms параметър; category h1/subtitle/provider_cta_suffix ключове обновени с {city} placeholder за всички 34 езика
  - **Metadata & UI Integration**:
    - **Homepage** (`apps/web/app/[lang]/page.tsx`): Fully integrated for meta tags, heroes, categories grid, SEO content blocks, and footer links with Slavic language support
    - **City Page** (`apps/web/app/[lang]/[city]/page.tsx`): Fully integrated for all UI elements with Slavic language support
    - **Category Pages** (`apps/web/app/[lang]/[city]/[category]/page.tsx`): Fully integrated for all UI elements with Slavic language support
  - **Scope**: Warsaw has declension forms seeded for all 34 languages. Adding declension forms for other cities requires running the seed script with city-specific data.
- **City Placeholder System (May 2, 2026)**:
  - **Purpose**: Replaced hardcoded city names in homepage translations with a dynamic `{city}` placeholder that resolves based on user context.
  - **Files Created**:
    - `apps/web/lib/city-preference.ts`: localStorage utility for managing user city preference
    - `apps/web/lib/default-city.ts`: City resolver with priority-based logic
  - **Files Modified**:
    - `apps/web/app/[lang]/page.tsx`: Added dynamic city resolution and `{city}` placeholder replacement
    - `apps/api/scripts/seed_ui_translations.py`: Updated homepage translations to use `{city}` placeholder
    - `apps/api/scripts/seed_select_city_translations.py`: Added new `homepage.select_city_link` translation key
  - **City Resolution Priority Order**:
    1. **User Preference** (localStorage): If user has previously selected a city via `saveCityPreference()`
    2. **Language Mapping**: Maps language codes to default cities (e.g., `pl` → `warszawa`)
    3. **Fallback**: Defaults to `warsaw` if no preference or mapping exists
  - **User City Preference System**:
    - Stored in localStorage under key `nevumo_city_preference`
    - Functions: `saveCityPreference(citySlug)`, `getCityPreference()`, `clearCityPreference()`
    - Persists across sessions for returning users
    - Can be cleared by user via browser settings or UI (future implementation)
  - **Default City Mapping**:
    - Defined in `LANGUAGE_TO_CITY` constant in `default-city.ts`
    - Current mapping: `pl` → `warsaw`
    - Fallback: `DEFAULT_CITY = 'warsaw'` for all languages without explicit mapping
    - Extensible for future markets (e.g., `bg` → `sofia`, `sr` → `belgrade`)
  - **Translation Pattern**:
    - Homepage translations now use `{city}` placeholder instead of hardcoded city names
    - Affected keys: `homepage.hero_suffix`, `homepage.footer_title`, `homepage.footer_link_*`, `homepage.activity_*`, `homepage.social_proof`
    - Placeholder is replaced server-side (SSR) with the resolved city name from the database
    - City names are fetched from `location_translations` table with fallback chain: `location_translations.city_name` → `locations.city_en` → `locations.city`
  - **API Integration**:
    - Uses existing endpoint `GET /api/v1/cities/{slug}?lang={lang}` for city data
    - Endpoint returns city object directly (unwrapped), handled correctly in `apps/web/lib/api.ts`
    - No new database schema changes required
  - **Homepage Links**:
    - All homepage category links (cleaning, plumbing, massage) are now dynamic based on resolved city
    - "Select City" link added to homepage using new `homepage.select_city_link` translation key
    - Links redirect to `/[lang]/izberi-grad` (City Selection page)
  - **Metadata Generation**:
    - City resolution is integrated into metadata generation for SEO
    - Dynamic city names appear in page titles and descriptions
  - **Scalability**:
    - System is global and designed to support unlimited cities
    - Adding a new city requires: database entry + language mapping update
    - No code changes needed for homepage or category pages
  - **GDPR Considerations**:
    - City preference is stored in localStorage (client-side, non-sensitive data)
    - Does not require explicit consent under GDPR for basic functionality
    - Must be documented in Privacy Policy and Cookie Policy when those documents are created (future task)
    - User can clear preference via browser localStorage management

### 6. Handling Empty Categories & Price Fallbacks ("Golden Standard")
- **Core Logic**: When a category contains no active providers, the system must preserve the marketing value of the FAQ section while ensuring no broken price strings are shown.
- **Price Template Replacement**: Instead of showing broken ranges (e.g., "Prices from 0 to 0"), the frontend (`page.tsx`) is responsible for a "clean" replacement. The entire price template (including any surrounding text like "Prices from... to...") must be replaced with a single localized phrase: **"Price on request"**.
- **Frontend Responsibility**: The logic for this replacement resides in the frontend components to avoid server-side complexity and ensure that raw placeholders or grammatically incorrect strings never reach the DOM.
- **i18n Best Practices**:
  - **No Concatenation**: Never build price strings by joining "Price from" + value + "to". Always use full template strings with placeholders or full phrase replacement.
  - **Full Replacement on Null**: If `priceData` is null or invalid, the entire phrase must be swapped for the "Price on request" equivalent.
  - **Currency Removal**: When price data is missing, the `{currency}` placeholder must be removed entirely from the text, not just left empty or replaced with a symbol.

### 7. Currency & Localization Logic
- **Universal Currency Logic (April 30, 2026)**: Implemented a centralized currency determination system based on provider location.
  - **Source of Truth**: Currency is derived from `provider.services[0].currency` with fallback to `provider.city.country_code` via `apps/web/lib/currency.ts`.
  - **Fallback Chain**: Service currency → City country code → Country default → 'EUR'
  - **Special Rule (Bulgaria)**: From **01.01.2026**, the currency for Bulgaria (BG) is strictly **EUR (Euro)**. This is a hardcoded system logic to reflect the national currency transition.
  - **Country Defaults**: RSD for RS (Serbia), PLN for PL (Poland), EUR for BG (Bulgaria).
- **PRODUCTION_READY_AUTH**: Implemented session checks and BFCache (Back-Forward Cache) handling in the authentication flow. Replaced legacy hidden iframe hacks with the modern **Credential Management API** (`navigator.credentials.store`) for robust password saving across all modern browsers including iOS Safari.
- **Client Dashboard Optimization (April 2026)**: Resolved issues where client data was not loading correctly after a role switch, implemented robust status tracking for leads and reviews, synchronized missing translation keys for the dashboard overview, and integrated `ClientLeadDetailModal` into the requests page.
- **Provider Dashboard Language Context Propagation (May 27, 2026)**: Fixed language context propagation in the provider dashboard to ensure that:
  - Widget preview iframe displays content in the current dashboard language (e.g., `/bg/provider/dashboard/widget` shows Bulgarian widget preview)
  - Public profile link ("View my profile") opens the public page in the current dashboard language
  - Implementation: Added `lang` query parameter to `/api/v1/provider/dashboard` endpoint and passed it through `build_public_url()` and `build_qr_public_url()` functions
  - Frontend: Updated `getProviderDashboard()` to accept and forward the `lang` parameter from the dashboard layout
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

- **Hreflang Coverage (May 8, 2026)**: All public pages now have complete hreflang tags for all 34 supported languages via `generateHreflangAlternates`:
  - Homepage (`/[lang]/page.tsx`)
  - City pages (`/[lang]/[city]/page.tsx`)
  - Category pages (`/[lang]/[city]/[category]/page.tsx`)
  - Provider pages (`/[lang]/[city]/[category]/[providerPage]/page.tsx`)
  - City selection (`/[lang]/izberi-grad/page.tsx`)
  - Login page (`/[lang]/login/page.tsx`)
  - Polish landing page (`/[lang]/dolacz/page.tsx`)
  - Claim page (`/[lang]/claim/[token]/page.tsx`)
  - Request form (`/[lang]/[city]/request/page.tsx`)

- **Provider Page SEO Optimization (April 30, 2026)**:
  - **Dynamic Robots Meta**: Implemented conditional `robots` tag logic based on the `embed=1` query parameter. Embedded views are set to `noindex, nofollow` to prevent duplicate content, while full pages are set to `index, follow`.
  - **Canonical URLs**: Added dynamic canonical tags that always point to the full page version (stripping the `embed` parameter) to consolidate SEO authority.
  - **Localized Schema**: Updated `LocalBusiness` JSON-LD to use the translated city name from the database (`addressLocality`) instead of the URL slug.
  - **Universal City Data**: Removed hardcoded `CITY_COUNTRY_MAP` and replaced it with a dynamic API-driven approach using `getCityBySlug`. This allows the platform to support any city added to the database without code changes.
  - **Hreflang Alternates**: Programmatically generated `alternates.languages` for all 34+ supported languages.

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

### SEO & Indexing (ProviderWidget JSON-LD)
The ProviderWidget component implements comprehensive Schema.org structured data to enhance search engine visibility and rich snippet display:

#### ProviderWidget JSON-LD Implementation
- **Location**: `apps/web/components/provider/ProviderWidget.tsx`
- **Schema Types**:
  1. **LocalBusiness Schema**: Represents the provider as a local business entity
     - Includes: name, description, address, telephone, url, areaServed
     - Uses localized city name from database (`addressLocality`)
     - Dynamic price range based on provider services
  2. **Service Schema**: Represents individual services offered by the provider
     - Includes: name, description, provider, areaServed, priceCurrency, price
     - Links to LocalBusiness via `provider` field
     - Currency determined by fallback chain (Service → City → Country default → EUR)
- **Currency Handling**:
  - Uses `apps/web/lib/currency.ts` for currency determination
  - Fallback chain: `service.currency` → `city.country_code` → country default → 'EUR'
  - Special rule: Bulgaria (BG) always uses EUR (effective 01.01.2026)
- **SEO Benefits**:
  - Rich snippets in Google search results
  - Price and service information directly visible in SERP
  - Local business schema enables Google Maps integration
  - Structured data validation passes Google's Rich Results Test
- **Integrity Requirement**: Any modifications to ProviderWidget must preserve JSON-LD structure and required fields to maintain SEO compliance

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

### Docker Environment Variable Pattern (May 7, 2026 - Updated May 23, 2026)
Next.js in Docker requires two separate environment variables to handle server-side and client-side API communication correctly:

- **API_URL=http://nevumo-api:8000** — Used server-side (SSR, Next.js rewrites) for container-to-container communication within the Docker network
- **NEXT_PUBLIC_API_URL** — Used client-side (browser) for API calls; set to browser-accessible URL to avoid hydration mismatches
  - **Local Development**: Set to `http://192.168.0.15:8000` (host IP) in `.env.local` for local network access from other devices
  - **Production**: Set to `https://api.nevumo.com` (production API domain) in `.env`
  - **Pattern**: `.env` contains production-ready value, `.env.local` (gitignored) contains local dev override

This pattern is applied in:
- **docker-compose.yml**: `API_URL` is defined for server-side (Docker internal network), `NEXT_PUBLIC_API_URL` is set to `http://localhost:8000` as default with `${NEXT_PUBLIC_API_URL:-http://localhost:8000}` override
- **apps/web/.env.local**: `NEXT_PUBLIC_API_URL=http://192.168.0.15:8000` for local network access (Mac + mobile devices)
- **apps/web/lib/api.ts**: `API_BASE` checks `process.env.API_URL` first, then falls back to `NEXT_PUBLIC_API_URL` for server-side; uses `NEXT_PUBLIC_API_URL` for client-side
- **apps/web/lib/ui-translations.ts**: Same fallback pattern for translation fetching
- **apps/web/lib/locales.ts**: Updated to use `API_URL || NEXT_PUBLIC_API_URL` fallback for server-side fetch
- **apps/web/app/[lang]/claim/[token]/page.tsx**: Server component uses `API_URL || NEXT_PUBLIC_API_URL` for API calls
- **apps/web/app/[lang]/terms/page.tsx**: Server component uses `API_URL || NEXT_PUBLIC_API_URL || 'http://localhost:8000'` for translation API calls (May 15, 2026)
- **apps/web/components/ProviderWidget.tsx**: Client component uses `process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'` for image URLs to avoid hydration mismatches

This separation ensures that:
- Server-side rendering can reach the backend container via Docker network (API_URL)
- Client-side browser requests use browser-accessible URLs (NEXT_PUBLIC_API_URL)
- No hydration mismatches between server and client rendering
- Works in local network (laptop + phones) without hardcoded IP addresses
- Independent of OrbStack network configuration changes
- Production-ready with environment variable changes only (set NEXT_PUBLIC_API_URL to production API domain)
- .env.example documents environment-specific configuration (Docker, local dev, production)
- **API_BASE Fix (May 8, 2026)**: Fixed client dashboard API returning HTML instead of JSON by ensuring `API_BASE` always uses the full API URL (http://localhost:8000 in local dev) instead of empty string in browser context. This prevents requests from being sent to the Next.js frontend instead of the actual API server.
- **Provider Photo Loading Fix (May 8, 2026)**: Fixed provider photo not loading on provider pages by using absolute URLs constructed from `API_BASE` for `profile_image_url` in `ProviderWidget.tsx`. The component now converts relative paths (`/api/v1/static/...`) to absolute URLs (`http://localhost:8000/api/v1/static/...`) to avoid issues with Next.js rewrites.
- **Provider Image Hydration Mismatch Fix (May 10, 2026)**: Fixed React hydration mismatch for provider images by implementing `resolveStaticUrl()` utility in `apps/web/lib/urlUtils.ts`. The utility uses relative URLs for local development (works on localhost:3000 and 192.168.0.15:3000) and absolute URLs for production CDN. This eliminates hydration mismatch by ensuring server and client render identical HTML. Backend `STATIC_FILES_BASE_URL` config supports CDN/S3 in production. Added `NEXT_PUBLIC_STATIC_URL` to `.env.example` documentation.
- **Next.js Config Fix (May 8, 2026)**: Fixed 404 errors on provider and client dashboard pages by removing invalid `loaderScript` configuration from `next.config.mjs`. The invalid configuration was causing the Next.js dev server to crash with "Unrecognized key(s) in object: 'loaderScript'" error.
- **OG Image Runtime & Font (May 8, 2026)**:
  - Changed OG image runtime from `edge` to `nodejs` in all opengraph-image.tsx files to enable custom font loading with `fs.readFileSync`.
  - Downloaded valid Noto Sans Bold font file (NotoSans-Bold.ttf, 575740 bytes) from GitHub to `apps/web/public/fonts/`.
  - Updated `BaseOGImage` component to load Noto Sans Bold font and apply it to the CTA button with `fontWeight: 700` for proper bold rendering.

### 6. PDF Generation with Cyrillic Support (May 15, 2026)
- **PDF Service**: `apps/api/services/pdf_service.py` generates withdrawal form PDFs from markdown content
- **Font Registration**: NotoSans-Regular.ttf and NotoSans-Bold.ttf registered in ReportLab for proper Cyrillic character rendering
- **Font Location**: `apps/api/fonts/` directory
- **Supported Languages**: en, bg, pl (extracts language-specific sections from `docs/withdrawal_form_nevumo.md`)
- **API Endpoint**: `GET /api/v1/legal/withdrawal-form/{lang}` returns binary PDF
- **Markdown Parsing**: Converts markdown bold syntax (`**text**`) to HTML tags (`<b>text</b>`) using regex
- **Styles**: Custom ParagraphStyle instances with NotoSans font for headings and body text
  - Previous Inter-Bold.ttf file was corrupted causing "Unsupported OpenType signature" errors.
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
- **Client Dashboard Review Eligibility Fix (May 25, 2026)** — COMPLETE:
  - **Problem:** After introducing the shared status change system (migration 0535f00974f4), completed requests were not showing the Review button and not appearing in the "Pending Review" tab. Root cause was that the client status change endpoint was not synchronizing status updates to the `LeadMatch` table, which is required for review eligibility.
  - **Solution:** Added `LeadMatch` synchronization in `apps/api/routes/client.py` (lines 132-143) to sync `match.status` with the new status when `lead.provider_id` exists. When a client changes a request status to "done", the corresponding `LeadMatch` record is also updated to "done", making the request eligible for review.
  - **Status Transitions:** 
    - Provider transitions: new → contacted/cancelled, contacted → cancelled
    - Client transitions: new → contacted → done, new/c → cancelled
  - **Review Eligibility:** Only leads with `LeadMatch.status IN ('contacted', 'done')` are eligible for review.
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
- **Provider Card Services Display (May 26, 2026)** — COMPLETE:
  - **Change:** Provider cards on category pages now display up to 4 services instead of 2
  - **File:** `apps/web/components/category/CategoryPageClient.tsx`
  - **Implementation:** Changed `.slice(0, 2)` to `.slice(0, 4)` and updated "more services" condition from `> 2` to `> 4`
- **Provider Dashboard Widget Page (May 27, 2026)** — COMPLETE:
  - **TikTok Share Button (May 27, 2026)**: Added TikTok share button next to Instagram button in the share section
    - Icon: Inline SVG TikTok logo
    - Translation key: `provider_dashboard.widget_share_tiktok` (34 languages)
    - Action: Copies public URL to clipboard with "Copied!" feedback
    - Style: Black background with white text
    - Seed script: `apps/api/scripts/seed_provider_dashboard_widget_part11.py`
  - **File:** `apps/web/app/[lang]/provider/dashboard/widget/page.tsx`
  - **Features:** 
    - Live iframe preview of provider's public profile
    - Size selector (Standard 360px / Wide 480px)
    - Embed code generator with copy functionality
    - "How it works" section with 3 steps
    - Platform integration cards (WordPress, Wix, Squarespace)
    - Link in bio information section
    - Social sharing buttons (Facebook sharer, Instagram clipboard copy)
  - **Sidebar Integration:** Added Widget nav item in `DashboardSidebar.tsx` before QR Code with `LayoutTemplate` icon
  - **Translation Keys:** 15 keys in `provider_dashboard` namespace (widget_title, widget_subtitle, widget_size_standard, widget_size_wide, widget_preview_title, widget_code_title, widget_code_copy, widget_code_copied, widget_how_title, widget_how_step1, widget_how_step2, widget_how_step3, msg_failed_load_widget, msg_no_widget_data, nav_widget)
  - **Additional Keys:** 10 keys for new sections (widget_site_title, widget_site_wordpress, widget_site_wix, widget_site_squarespace, widget_bio_title, widget_bio_description, widget_share_title, widget_share_facebook, widget_share_instagram)
  - **Seed Scripts:** 10 parts with 780 translation rows across 34 languages (seed_provider_dashboard_widget_part1-10.py)
  - **Build Error Fix:** lucide-react doesn't have Facebook/Instagram icons → replaced with inline SVGs
  - **Iframe Network Fix:** Uses `window.location.origin` for embed code to work on local network (mobile devices accessing via IP)
  - **API Endpoint:** Uses existing `GET /api/v1/provider/qr-code` endpoint
- **Legal Document Modal System (May 27, 2026)** — COMPLETE:
  - **Purpose:** Unified legal document display across the application using a modal instead of page navigation
  - **Component:** `apps/web/components/auth/LegalModal.tsx`
  - **Supported Document Types:** terms, provider_terms, privacy, cookies, withdrawal, contact_dsa
  - **Implementation:**
    - Modal displays legal documents in an iframe with `?modal=true` query parameter
    - Uses translation keys for modal titles (e.g., `modal_title_terms`, `modal_title_privacy`)
    - Props: `isOpen`, `onClose`, `lang`, `type`, `authDict`
    - **Namespace Standardization (May 27, 2026):** Fixed namespace mismatches:
      - `terms-provider` → `provider_terms` (matches document page namespace)
      - `contact-dsa` → `contact_dsa` (matches document page namespace)
    - **Dismiss Button Translation (May 27, 2026):** Added `dismiss_button` key to `auth` namespace for all 34 languages (seeded from `pwa.dismiss_button`)
  - **Integration Points:**
    - **ProviderWidget** (`apps/web/components/ProviderWidget.tsx`): Terms & Privacy links in widget footer now open modal
    - **GlobalFooter** (`apps/web/components/GlobalFooter.tsx`): All 6 legal links now open modal instead of navigating to separate pages
    - **LoginClient** (`apps/web/components/auth/LoginClient.tsx`): Terms link uses `provider_terms` namespace
    - **OAuthTermsClient** (`apps/web/components/auth/OAuthTermsClient.tsx`): Terms link uses `provider_terms` namespace
  - **Benefits:**
    - Improved UX: Users stay on current page while viewing legal documents
    - Consistent behavior across all legal document links
    - No page reload or navigation context loss
  - **CookieSettingsLink Exception:** Cookie Settings link uses custom event system (`open-cookie-settings`) instead of modal, as it opens the cookie banner UI
  - **Embed Mode Support (May 27, 2026):** GlobalFooter hidden in embed mode via `[data-global-footer] { display: none !important; }` CSS rule in provider page
  - **UX Improvement:** Provides better visibility of provider offerings while maintaining progressive disclosure for providers with many services
  - **Note:** Services are filtered by category - on cleaning pages only cleaning services are shown per provider
- **Namespaced Translations Validator**: Implemented a mandatory `namespace.key` pattern at the ORM layer to ensure all UI copy is properly organized and to avoid cache conflicts.
- **Redis Sync**: After updating translations in the database, Redis MUST be flushed (`FLUSHALL`) to clear the cache and reflect changes in the UI.
- **ProviderWidget Translation Fixes (May 27, 2026)** — COMPLETE:
  - **Translation Key Mismatch Fix:** Fixed `mergedT` object in provider page - translations are merged without `footer.` prefix (keys are `terms_link`, `privacy_policy_link`), but ProviderWidget was looking for `footer.terms_link` and `footer.privacy_policy_link`. Removed the `footer.` prefix from t() function calls.
  - **Hydration Mismatch Fix:** Fixed React hydration mismatch for provider images by implementing `resolveStaticUrl()` utility in `apps/web/lib/urlUtils.ts`. Uses relative URLs for local development and absolute URLs for production CDN.
  - **Translation Syntax Fix:** Fixed incorrect syntax `t['or_general_request']` which returned undefined, triggering hardcoded Bulgarian fallback. Changed to `t('or_general_request', ...)` function call in:
    - ProviderWidget.tsx (line 734)
    - LeadPanel.tsx (line 388) - changed fallback to English
    - BottomSheetForm.tsx (line 443) - changed fallback to English
  - **Undefined Locale Fix:** Fixed undefined locale variable that was causing runtime errors in ProviderWidget
  - **Footer Link Spacing Fix:** HTML spaces between links get compressed by browsers - fixed by using CSS margin instead of HTML spaces for proper spacing between "Общи условия" and "Политика за поверителност" links
  - **Files Modified:**
    - `apps/web/components/ProviderWidget.tsx` - translation keys, link formatting, translation syntax
    - `apps/web/components/LeadPanel.tsx` - translation syntax fix
    - `apps/web/components/provider/BottomSheetForm.tsx` - translation syntax fix
    - `apps/web/components/GlobalFooter.tsx` - added data attribute for embed mode hiding
    - `apps/web/app/[lang]/[city]/[category]/[providerPage]/page.tsx` - CSS rule for footer hiding in embed mode
- **Provider Page Review Card Display Fix (May 25, 2026)** — COMPLETE:
  - **Problem:** The review card in LeadPanel (right column) and BottomSheetForm (mobile) was not displaying comments correctly due to field name mismatch (`comment` vs `comment_preview` from API) and had broken UI (empty quotes, plain text initials).
  - **Solution:**
    - Fixed field name from `latestReview.comment` to `latestReview.comment_preview` in both LeadPanel.tsx and BottomSheetForm.tsx
    - Added circular avatar for client initials (w-6 h-6 rounded-full bg-orange-100) instead of plain text
    - Placed avatar on same line as comment text for better mobile layout
    - Made quotes conditional - only show when comment exists and is not empty
  - **Files Modified:** `apps/web/components/provider/LeadPanel.tsx`, `apps/web/components/provider/BottomSheetForm.tsx`
- **Sticky CTA Mobile Visibility Fix (May 25, 2026)** — COMPLETE:
  - **Problem:** The sticky "Свържи ме с [Provider]" button was not visible on mobile because the scroll check logic required the lead form to exist in DOM, but the form is hidden on mobile (`hidden md:block`).
  - **Solution:** Moved the form element check inside the `checkScroll` function in StickyProviderCTA.tsx. When the form doesn't exist (mobile), the button is always shown with `transform: translateY(0)`.
  - **File Modified:** `apps/web/components/provider/StickyProviderCTA.tsx`
- **Next.js ISR Cache Strategy (May 25, 2026)**: Reduced revalidate time from 3600s to 60s for provider list endpoint (`getProviders` in apps/web/lib/api.ts) to ensure rating and review count data stays fresh. Dynamic ratings are calculated from Review table in real-time, so shorter cache times are appropriate for these frequently-changing metrics.
- **Translation Seed Script Separation (May 13, 2026)**: To prevent language mixing issues, translation keys must not be duplicated across seed scripts. Each seed script should have exclusive ownership of its keys:
  - `seed_provider_dashboard_translations.py`: Contains general provider dashboard UI translations
  - `seed_onboarding_hero_v2.py`: Contains onboarding hero banner translations (setup_title, setup_subtitle, btn_complete_setup, step_profile, step_service, etc.)
  - When keys are duplicated with `row_bg()` (incomplete translations) in one script and full translations in another, executing the incomplete script will overwrite the good translations with English fallback text for non-EN/BG languages
  - Solution: Remove duplicate keys from the script that uses `row_bg()` and let the specialized script handle those keys with full 34-language translations
- **Mobile Language Dropdown Fix (May 15, 2026)**: Fixed language dropdown in GlobalFooter component that was going off-screen on mobile devices (375px width). Changed positioning from `right-0` to responsive `left-0 md:right-0 md:left-auto` to ensure dropdown stays within viewport bounds on small screens while maintaining right alignment on desktop.
- **Mobile Bottom Sheet Form (May 23, 2026)** — COMPLETE:
  - **New Component**: `apps/web/components/provider/BottomSheetForm.tsx` with slide-up animation (translateY 100% → 0), overlay with click-to-close, X close button (top-right), body scroll lock
  - **Form Features**: PhoneInput with usePhone hook (auto-fill for logged-in users, auto-prefix for anonymous), service chips, textarea for notes, trust signal, submit button
  - **Validation Logic**: Phone required AND (selectedService !== null OR note.trim().length > 0) — error message shows as `error_service_or_note` under chips row
  - **LeadPanel Update**: Added `serviceNoteError` state and validation check in handleSubmit
  - **StickyProviderCTA Update**: Accepts `onOpenSheet` prop and calls it instead of scrolling to form
  - **ProviderFullPage Integration**: Added `isSheetOpen` state, passes `isOpen/onClose` to BottomSheetForm, `onOpenSheet` to StickyProviderCTA, shares `selectedService` state between LeadPanel and BottomSheetForm
  - **Pre-fill Behavior**: Selecting a service replaces notes content with service text (not append); deselecting clears notes
  - **useCallback Fix**: handleServicePreFill wrapped in useCallback to prevent useEffect re-running on every render
  - **Translation Key**: `error_service_or_note` from `provider_page` namespace (seed script: `apps/api/scripts/seed_provider_page_error_keys.py`)
  - **X Button Fix**: Replaced drag handle with X close button positioned absolute top-4 right-4; fixed CSS positioning conflicts (removed `relative` class, switched to inline style for transform animation)
- **Provider Page Service Selection Toggle (May 23, 2026)**: Implemented shared state and toggle functionality for service selection cards and chips in ProviderFullPage.tsx and LeadPanel.tsx.
  - **Shared State Pattern**: Both cards and chips use the same `selectedService` state with toggle logic (click selected → deselect to null, click unselected → select)
  - **Desktop Behavior**: Selected card + hover shows gray deselect button instead of orange select button
  - **Mobile Behavior**: Unselected shows `select_this_service`, selected shows `service_selected_confirm`
  - **Textarea Behavior**: Does NOT clear on deselect as per requirements
  - **Translation Keys**: Added 3 new keys in `provider_page` namespace (`select_this_service`, `service_selected_confirm`, `service_deselect`) for all 34 languages
  - **Seed Script**: `apps/api/scripts/seed_provider_page_service_select.py` (102 rows)
  - **API Note**: `get_namespaced_translations` in `apps/web/lib/ui-translations.ts` strips namespace prefix from keys, so frontend uses keys WITHOUT prefix (e.g., `select_this_service` NOT `provider_page.select_this_service`)
- **Provider Page Pricing Display (May 23, 2026)**: Implemented dynamic pricing logic in provider components based on service price_type (fixed, hourly, per_sqm, request) with proper currency and unit labels using translation keys.
  - **ProviderFullPage.tsx**: Added `currency: string` to ProviderService interface, replaced hardcoded currency with dynamic pricing logic based on price_type
  - **LeadPanel.tsx**: Updated services type to include base_price, price_type, currency; added formatServicePrice helper function; updated chip rendering
  - **Translation keys**: Added `provider_page.price_per_hour` and `provider_page.price_on_request` for all 34 languages (seed script: seed_provider_page_price_units.py)
  - **Translation namespace fix**: Changed translation keys from `provider_page.price_on_request`/`provider_page.price_per_hour` to `price_on_request`/`price_per_hour` (without namespace prefix) to match API response format
  - **Merge order fix**: Changed page.tsx merge order to `{ ...categoryT, ...widgetT, ...providerPageT }` to ensure provider_page translations have priority over category translations
- **Sticky Positioning Fix (May 23, 2026)** — COMPLETE:
  - **PROBLEM**: Right column (lead form with button) on provider page was not sticking to viewport when scrolling.
  - **ROOT CAUSE**: `overflow-x: hidden` on `html` and `body` elements in `apps/web/app/globals.css` completely breaks `position: sticky` for all descendants.
  - **SOLUTION**:
    - Changed `overflow-x: hidden` to `overflow-x: clip` in both `html` and `body` selectors in `apps/web/app/globals.css`
    - `overflow-x: clip` provides the same horizontal overflow prevention as `hidden` but does NOT break sticky positioning
    - Also corrected invalid Tailwind class `align-self-start` to `self-start` in `apps/web/components/provider/ProviderFullPage.tsx`
  - **Verification**: Tested with Playwright - element now sticks at exactly 24px (top-6) when scrolling instead of scrolling with page
- **Header/Footer Visibility Logic (May 21, 2026)** — COMPLETE:
  - **PROBLEM**: Header and footer visibility was inconsistent in dashboard pages. Server-side layout controlled initial render, but client-side navigation caused race conditions where header/footer wouldn't appear or disappear correctly.
  - **SOLUTION**:
    - Created shared `isDashboardPath()` utility in `apps/web/lib/dashboard-path.ts` for centralized dashboard path detection (`/client/dashboard/*` and `/provider/dashboard/*`)
    - Modified `apps/web/app/[lang]/layout.tsx`: Removed server-side `!isDashboard` check, now relies on client-side control only (kept modal/embed checks)
    - Modified `apps/web/components/SmartGlobalFooter.tsx`: Removed dashboard-specific hiding logic - footer now visible on all pages
    - Modified `apps/web/components/GlobalHeader.tsx`: Added state-based re-rendering with useEffect and `forceUpdate` state to handle navigation changes
    - **Key Decision**: Server-side layout doesn't control dashboard header visibility anymore - only client-side logic in GlobalHeader (modal/embed checks still apply in layout)
  - **Logout Redirect Fix (May 21, 2026)** — COMPLETE:
    - **PROBLEM**: Logout redirected to auth page instead of home page, and localStorage race condition prevented proper session clearing
    - **SOLUTION**:
      - Changed logout redirect from `/${lang}/auth` to `/${lang}` in `apps/web/components/dashboard/DashboardTopBar.tsx` and `apps/web/app/[lang]/client/dashboard/layout.tsx`
      - Added `requestAnimationFrame()` after `clearAuth()` to ensure localStorage changes are processed before navigation
  - **Result**: Header is hidden in dashboard pages, visible on home pages and non-dashboard pages, footer visible on all pages, logout redirects to home page with proper header visibility, works with all login methods (Google OAuth, email/password)
- **City Page CTA Link Enhancement (May 20, 2026)** — COMPLETE:
  - **PROBLEM:** City pages had a simple "Become a specialist" link that didn't pass city information for pre-population during registration, unlike category pages which passed both city and category.
  - **SOLUTION:**
    - Updated `apps/web/app/[lang]/[city]/page.tsx` to use responsive design (two-line on mobile, one-line on desktop)
    - Added new translation keys `city.nav_cta_line1` and `city.nav_cta_line2` for all 34 languages
    - Link now passes `city=${city}` parameter to auth page for automatic city pre-population
    - Arrow `→` is hardcoded in frontend (not part of translations)
    - Text structure: "{nav_cta_line1} {cityName}? {nav_cta_line2} →"
    - Seed script: `apps/api/scripts/seed_city_nav_cta_translations.py`
  - **Result:** City page CTA link now matches category page functionality with city pre-population and responsive design.
- **Dashboard Header Duplication Fix (May 20, 2026)** — COMPLETE:
  - **PROBLEM:** GlobalHeader from base layout was showing on dashboard pages (`/client/dashboard/*` and `/provider/dashboard/*`), causing logo duplication since dashboard layouts have their own sidebars with logos.
  - **SOLUTION:**
    - Added `x-pathname` header to all responses in `apps/web/proxy.ts` (Next.js 16 uses proxy.ts instead of deprecated middleware.ts)
    - Modified `apps/web/app/[lang]/layout.tsx` to read pathname from headers and skip rendering GlobalHeader/SmartGlobalFooter on dashboard routes
    - Used `headers().get('x-pathname')` in server component to detect dashboard paths
  - **Implementation Details:**
    - Added `response.headers.set('x-pathname', pathname)` to all response cases in proxy.ts (static routes, language propagation, redirects)
    - Added `isDashboard` check in layout.tsx: `pathname.includes('/client/dashboard/') || pathname.includes('/provider/dashboard/')`
    - Existing modal/embed logic preserved: `{!isDashboard && modal !== 'true' && embed !== '1' && <GlobalHeader lang={lang} />}`
  - **Result:** Dashboard pages no longer show duplicate header/logo; normal pages continue to show GlobalHeader as expected.
- **Terms & Conditions Page (May 15, 2026)** — COMPLETE:
  - **Frontend**: Server component at `apps/web/app/[lang]/terms/page.tsx`
  - **Features**:
    - Renders 15 articles + Annex 1 with full legal content
    - Dynamic content rendering with Polish-specific [PL] markers for conditional display
- **Terms & Conditions for Service Providers Page (May 17, 2026)** — COMPLETE:
  - **Frontend**: Server component at `apps/web/app/[lang]/provider-terms/page.tsx`
  - **Features**:
    - Renders 18 articles + Annex 1 + Annex 2 with full legal content for service providers
    - Supports all 34 languages with translations from `provider_terms` namespace
    - Dynamic content rendering with Polish-specific [PL] markers for conditional display
    - Legal compliance: P2B Regulation (EU) 2019/1150 compliance
  - **Backend**: 23 seed scripts in `apps/api/scripts/` for provider_terms translations
    - seed_provider_terms_p1_meta.py through seed_provider_terms_p23_footer.py
    - Total: 50+ keys × 34 languages = 1,700+ rows
  - **Documentation**: Full legal content in `docs/terms_conditions_providers_nevumo.md` (EN + BG + PL versions)
  - **Namespace**: `provider_terms`
  - **Keys**: page_title, meta_description, effective_date, version, pl_notice, art1_title through art18_title, art1_body through art18_body, annex1_title, annex1_body, annex2_title, annex2_body, footer
    - PDF download button for withdrawal form (links to `/api/v1/legal/withdrawal-form/{lang}`)
    - Online withdrawal form link (links to `/[lang]/withdrawal`)
    - Translations fetched from `/api/v1/translations/terms?lang={lang}`
    - SEO metadata with dynamic title and description
  - **Backend**: Multiple seed scripts for terms translations:
    - `seed_terms_p1.py` - Article 1 titles and buttons
    - `seed_terms_p1_bodies.py` through `seed_terms_p15_bodies.py` - Article bodies (15 articles)
    - `seed_terms_annex_bodies.py` - Annex 1 content
    - `seed_terms_buttons.py` - Button translations
  - **Namespace**: `terms` with keys: page_title, meta_description, effective_date, version, pl_notice, art1_title through art15_title, art1_body through art15_body, annex1_title, annex1_body, download_pdf, online_form, back_to_home
- **Withdrawal Form Page (May 15, 2026)** — COMPLETE:
  - **Frontend**: Client component at `apps/web/app/[lang]/withdrawal/page.tsx`
  - **Features**:
    - Interactive form with validation for all required fields
    - Real-time error messages for each field
    - Success state with confirmation message
    - Translations fetched from `/api/v1/translations/withdrawal?lang={lang}`
    - Form submission to `POST /api/v1/legal/withdrawal`
    - Cancel button linking back to terms page
  - **Backend**:
    - New endpoint: `POST /api/v1/legal/withdrawal` in `apps/api/routes/legal.py`
    - Email service integration: sends withdrawal form data to legal@nevumo.com
    - Validation: service_description, contract_date, consumer_name, consumer_address, email (required), account_id (optional)
    - Seed script: `seed_withdrawal_translations_4.py` (19 keys × 34 languages = 646 rows)
  - **Namespace**: `withdrawal` with keys: page_title, page_description, label_service_description, label_contract_date, label_consumer_name, label_consumer_address, label_account_id, label_email, label_submission_date, optional, cancel, submit, submitting, error_* (7 error keys), success_title, success_message, back_to_home
- **Provider Full Page — Задачи A, B, C (May 21, 2026)** — COMPLETE:
  - **Задача A — Badge логика + DB migration:**
    - Нова колона `verification_level INT DEFAULT 0` в таблица `providers`
    - Alembic migration: `add_verification_level`
    - Функция `calculate_verification_level(provider, db)` в `provider_service.py`
      - Level 0: Нов (default)
      - Level 1: Верифициран (1+ завършени заявки + пълен профил)
      - Level 2: Топ специалист (10+ завършени заявки + рейтинг ≥ 4.5)
    - Извиква се при: `update_provider_profile()`, `add_service()`, `change_lead_status()` (status=done)
    - `verification_level` добавен в `ProviderDetail` и `ProviderListItem` schemas
    - Backfill скрипт: `apps/api/scripts/backfill_verification_levels.py`
    - Result: 152 providers Level 0, 1 provider Level 2
  - **Задача B — Multi-image галерия:**
    - Нова таблица `provider_images` (id, provider_id, url, position, created_at)
    - Index: `idx_provider_images_provider_id`
    - Alembic migration: `add_provider_gallery`
    - Нов SQLAlchemy модел `ProviderImage` в `models.py`
    - Relationship `gallery_images` в `Provider` модела
    - Нов StaticFiles mount: `/api/v1/static/provider_gallery`
    - Storage path: `uploads/provider_gallery/{provider_id}/{image_id}.webp`
    - HEIC→WebP pipeline: max 1200px, 85% quality (идентичен с profile image pipeline)
    - Максимум 8 снимки на доставчик
    - Нови endpoints (JWT required):
      - GET /api/v1/provider/images
      - POST /api/v1/provider/images (multipart, max 5MB)
      - DELETE /api/v1/provider/images/{id}
      - PATCH /api/v1/provider/images/reorder
    - `gallery: [{id, url, position}]` добавен в публичния ProviderDetail response
  - **Задача C — Dashboard Gallery UI:**
    - Нов компонент: `apps/web/components/dashboard/GallerySection.tsx`
      - Grid: 4 колони десктоп / 2 колони мобилен
      - HTML5 Drag-and-drop пренареждане (без external libraries)
      - Upload: multiple files, HEIC/WebP/JPG/PNG, max 5MB
      - Position 0 badge: "🖼 корица"
      - Inline грешки
    - Интегриран в EDIT MODE на `apps/web/app/[lang]/provider/dashboard/profile/page.tsx`
    - Нови API функции в `apps/web/lib/provider-api.ts`:
      - getGalleryImages(), uploadGalleryImage(), deleteGalleryImage(), reorderGalleryImages()
    - Нов тип `GalleryImage` в `apps/web/types/provider.ts`
    - Translation keys (namespace: provider_dashboard): gallery_title, gallery_subtitle, gallery_cover_hint, gallery_upload_btn, gallery_uploading, gallery_delete_confirm, gallery_max_reached, gallery_empty, gallery_drag_hint
    - Seed скрипт: `apps/api/scripts/seed_provider_gallery_translations.py`
  - **Важна бележка — seed скрипт правило:**
    - Seed скриптовете НЕ трябва да съдържат `DELETE FROM translations WHERE key LIKE 'namespace.%'`
    - Използват само `ON CONFLICT (lang, key) DO UPDATE SET value = EXCLUDED.value` или INSERT без предварително изтриване.

---

## Cookie Consent Banner (GDPR Compliance) — May 8, 2026

### Component Structure
- **Location**: `apps/web/components/ui/CookieConsentBanner.tsx`
- **Hook**: `apps/web/hooks/useCookieConsent.ts`
- **Integration**: Added to `apps/web/app/layout.tsx` for global banner display

### Features Implemented
- **Banner Display**: Accept All / Reject All / Customize buttons on first visit
- **Cookie Storage**: First-party cookie `nevumo_consent` with structure:
  ```json
  {
    "v": 2,
    "ts": timestamp,
    "categories": {
      "necessary": true,
      "functional": boolean,
      "analytics": boolean,
      "marketing": boolean
    },
    "policy_version": "2026-05-01"
  }
  ```
- **Footer Link**: "Cookie Settings" button in footer to reopen banner without reload
- **Localization**: Supported in EN, PL, BG (cookie_banner namespace)
- **Backend Logging**: POST /api/v1/consent endpoint logs consent decisions to consent_logs table
- **Audit Trail**: Anonymized session_hash and ip_hash for GDPR compliance (24-month retention)

### Pending Items (Future Tasks)
- GA4 Consent Mode v2 integration (Task 2)
- Stripe.js conditional loading
- Mobile touch targets verification (44×44px)
- 12-month re-prompt logic

- **Cookie Settings Link — Global Footer Fix (May 20, 2026)** — COMPLETE:
  - **Проблем:** "Настройки на бисквитките" линкът се показваше само на homepage, вместо на всяка страница
  - **Причина:** CookieSettingsLink компонентът беше в apps/web/components/homepage/Footer.tsx (само homepage), не в GlobalFooter
  - **Решение:**
    - Добавен import и <CookieSettingsLink lang={lang} /> в apps/web/components/GlobalFooter.tsx след withdrawal линка (!minimal блок)
    - Премахнат CookieSettingsLink от apps/web/components/homepage/Footer.tsx
  - **Бонус fix:** Language dropdown излизаше извън екрана на мобилен — оправен чрез right-0 на dropdown контейнера и ml-auto на wrapper div-а
  - **Засегнати файлове:**
    - apps/web/components/GlobalFooter.tsx
    - apps/web/components/homepage/Footer.tsx
  - **Резултат:** Cookie Settings е достъпен от footer-а на всяка страница в системата

---

## Data Export Endpoint (GDPR Article 20 - Right to Portability) — May 8, 2026

### Backend Implementation
- **Endpoint**: `GET /api/v1/user/export` (JWT protected)
- **Service**: `apps/api/services/export_service.py`
- **Rate Limiting**: 1 request per 24 hours per user (Redis key: `export_rl:{user_id}`, TTL 86400)
- **Response Headers**: `Cache-Control: no-store` (Safari fix for download behavior)
- **Error Handling**: 429 status returns `RATE_LIMIT_EXCEEDED` error code

### Data Exported
- User profile (id, email, name, phone, country_code, role, created_at)
- Leads submitted (category, city, description, status, created_at)
- Services listed (if provider: title, category, price_type, base_price, currency)
- Reviews (rating, comment, created_at)
- Consent log (policy_version, categories, created_at)

### Frontend Integration
- **Client Dashboard**: "Download my data" button in settings page
- **Provider Dashboard**: "Download my data" button in settings page
- **Error Display**: Shows `settings.export_rate_limited` translation key on 429 response
- **Translation Keys**: 7 keys in `settings` namespace × 34 languages = 238 rows
  - export_title, export_description, export_button, export_success
  - export_error, export_rate_limited, export_format

### Compliance Notes
- Implements GDPR Article 20 (Right to Data Portability)
- Machine-readable JSON format
- Immediate response for datasets under 2MB
- Audit trail via rate limiting logs in Redis

---

## Legal Pages & Compliance

### Legal Pages Architecture
Nevumo implements three main legal pages with a modal-based preview system:

1. **Terms & Conditions (Clients)** — `/[lang]/terms`
   - Server component rendering 15 articles + Annex 1
   - Supports PDF download of withdrawal form
   - Online withdrawal form link
   - Translations from `terms` namespace

2. **Terms & Conditions (Providers)** — `/[lang]/terms-provider`
   - Server component rendering 18 articles + Annex 1 + Annex 2
   - P2B Regulation (EU) 2019/1150 compliance
   - Translations from `provider_terms` namespace

3. **Cookie Policy** — `/[lang]/cookies`
   - Server component with full cookie/storage registry
   - Translations from `cookies` namespace
   - Includes GA4 Advanced Consent Mode v2 disclosure

4. **DSA Contact Point** — `/[lang]/contact-dsa`
   - Server component for DSA Article 11 compliance
   - Translations from `contact_dsa` namespace
   - EN/BG/PL full translations, others fallback to EN for body texts

### Footer Legal Links
- privacy_policy_link → /[lang]/privacy ✅
- cookies_link → /[lang]/cookies ✅
- terms_link → /[lang]/terms ✅
- provider_terms_link → /[lang]/provider-terms ✅
- withdrawal_link → /[lang]/withdrawal ✅
- contact_dsa_link → /[lang]/contact-dsa ✅
- Footer contains 6 legal links: privacy, cookies, terms, provider-terms, withdrawal, contact-dsa ✅

### ?modal=true Mechanism
All legal pages support a `?modal=true` query parameter for iframe embedding:
- When loaded with `?modal=true`, the page detects it's in an iframe context
- SmartGlobalFooter is automatically hidden via `isInIframe` detection
- This allows LegalModal to display legal content without user leaving the /auth flow
- The iframe approach ensures clean separation of concerns and proper URL-based navigation

### LegalModal Component
- **Location**: `apps/web/components/auth/LegalModal.tsx`
- **Purpose**: Allows users to review legal documents without leaving the /auth page
- **Implementation**: Uses iframe approach with `?modal=true` parameter
- **Features**:
  - Displays Terms, Privacy Policy, or Provider Terms in a modal
  - SmartGlobalFooter hidden in iframe context via detection
  - Maintains auth flow context while providing legal document access
  - Used in email registration (LoginClient.tsx) with different documents for client/provider

### OAuth Terms Flow
- **oauth-terms Page**: `apps/web/app/[lang]/auth/oauth-terms/page.tsx`
  - Dedicated page for Google OAuth terms acceptance
  - Forces users to accept T&C before account creation
  - Client component: `OAuthTermsClient.tsx`
  - select_role step shown only when nevumo_intent is missing

- **OAuth Flow Updates**:
  - State parameter now carries: `lang|intent|category|city`
  - Backend checks if user exists before creating account
  - New providers automatically receive providers record
  - `OAUTH_REDIRECT_BASE` added to root .env and apps/api/config.py as configurable variable

### GlobalHeader Component
- **Location**: `apps/web/components/GlobalHeader.tsx`
- **Purpose**: Site-wide header with logo and auth button
- **Features**:
  - Logo link to homepage with language context
  - Auth button (AuthHeaderButtonWrapper) for login/signup
  - Hides in iframe context via `window.self !== window.top` detection
  - Client component with 'use client' directive
  - Early return null when in iframe to prevent rendering
- **Usage**: Imported directly in `apps/web/app/[lang]/layout.tsx` (no dynamic wrapper)

### AuthHeaderButton Component
- **Location**: `apps/web/components/AuthHeaderButtonWrapper.tsx`
- **Purpose**: Auth button in GlobalHeader
- **Features**:
  - Hidden on auth routes (/auth/*) and dashboard routes (/client/dashboard, /provider/dashboard)
  - Fixed positioning removed (no longer sticky/fixed)
  - Conditionally rendered based on route path
- **Usage**: Wrapped in GlobalHeader, rendered when `!hideAuthButton`

### select_role Step Logic
- **LoginClient**: `apps/web/app/[lang]/auth/LoginClient.tsx`
  - select_role step shown only when nevumo_intent is missing from localStorage
  - When intent exists (client or provider), skips role selection
  - Intent cleared after successful auth (clearStoredIntent)
- **OAuth Terms**: `apps/web/app/[lang]/auth/oauth-terms/page.tsx`
  - select_role shown only when intent is missing in OAuth flow
  - State parameter carries intent, used to determine if role selection needed

### embed=1 Parameter
- **Purpose**: Hides GlobalHeader via CSS for embedded views
- **Implementation**: `data-global-header` attribute on header element
- **CSS Rule**: `[data-global-header] { display: none; }` when embed=1
- **Usage**: Provider pages support embed=1 query parameter for widget embedding
- **Layout Integration**: `apps/web/app/[lang]/layout.tsx` checks embed parameter alongside modal

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

#### Leads Modal Translation Restore (May 2026)

**Incident:** Following a database deletion incident, 13 translation keys from `LeadsClient.tsx` and `LeadDetailModal.tsx` were missing from the `provider_dashboard` namespace.

**Diagnosis:** Comparison of three database archives established the timeline:
- Archive 23.05.2026 — 12 of 13 keys missing (post-incident)
- Archive 16.05.2026 — 12 of 13 keys missing (post-incident)
- Archive 07.05.2026 — 11 keys available with 34 languages (pre-incident)
- 2 keys never existed in the database

**Restore Process:**
- 11 keys extracted from archive `nevumo_leads_20260507_155146.sql.gz` via `grep` + Python INSERT SQL generator
- 2 new keys created via seed script: `apps/api/scripts/seed_leads_missing_keys.py`

**Affected Keys (13):**
`aria_close`, `btn_close`, `btn_save_notes`, `label_cancelled_leads`, `label_client_message`, `label_notes_privacy_disclaimer`, `label_private_notes`, `lead_detail_title`, `msg_no_description`, `msg_notes_save_failed`, `msg_notes_saved`, `msg_saving`, `placeholder_private_notes`

**Result:** All 13 keys verified with `lang_count = 34`. Redis cache cleared for `provider_dashboard` namespace.

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
- ShareButton: apps/web/components/shared/ShareButton.tsx
  - GDPR-friendly share компонент, Web Share API на mobile, Clipboard API на desktop, inline toast, без external dependencies

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

Layout: Sidebar (logo + nav links + "View public profile" button on mobile + "НАМЕРИ УСЛУГА" CTA) + TopBar with user info + "View public profile" button on desktop.

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

## Authentication Phase 2 — Google OAuth (May 9, 2026)

### Overview
Backend OAuth flow — Google OAuth се управлява от FastAPI, не от Next.js.

### New Files & Changes
- **apps/api/routes/auth.py** — 2 нови endpoint-а:
  - `GET /api/v1/auth/google` — redirect към Google consent page, приема `lang` query param, подава го като `state`
  - `GET /api/v1/auth/google/callback` — обработва callback, създава/намира user, издава JWT, redirect към frontend
- **apps/api/services/auth_service.py** — нова функция `get_or_create_oauth_user(email, name, oauth_provider, oauth_id, db)`:
  - Търси по oauth_provider + oauth_id → по email → създава нов user
  - Нови users получават role="client" по подразбиране
  - Извиква link_pending_claims() след create/login
- **apps/api/config.py** — нови settings: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, OAUTH_REDIRECT_BASE
- **apps/web/app/[lang]/auth/oauth-callback/page.tsx** — нова страница, чете token + redirect params, извиква saveAuth(), redirect по role
- **apps/web/app/[lang]/auth/LoginClient.tsx** — Google бутон активиран с `?lang={lang}` param

### DB Migration
- Migration: `1433ea08e073_add_oauth_fields_to_users.py`
- Нови колони в users: `oauth_provider VARCHAR(20)`, `oauth_id VARCHAR(255)`
- Constraint: `uq_users_oauth UNIQUE (oauth_provider, oauth_id)`

### OAuth Flow
1. User натиска "Sign in with Google" → `GET /api/v1/auth/google?lang=bg`
2. Backend redirect към Google с `state=bg`
3. Google callback → `GET /api/v1/auth/google/callback?code=...&state=bg`
4. Backend: token exchange → user info → get_or_create_oauth_user()
5. Redirect към `/{lang}/auth/oauth-callback?token={jwt}&redirect=/{lang}/client/dashboard`
6. Frontend: saveAuth() → redirect по role

### Redirect Logic (Post-Login)
| Role | Redirect |
|------|----------|
| client | /{lang}/client/dashboard |
| provider | /{lang}/provider/dashboard |

### Translation Keys Added
- `auth.oauth_error` — 34 езика, seed: `apps/api/scripts/seed_auth_translations.py`

### Env Variables Required
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
OAUTH_REDIRECT_BASE=http://localhost:3000
В apps/web/.env.local:
NEXTAUTH_SECRET=...
NEXTAUTH_URL=http://localhost:3000

### Facebook OAuth
Деактивиран за сега — добавяне след Warsaw launch с Meta Business верификация.

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

---

## Future Tasks

### Geolocation Implementation (Standing Task)

**When to implement:** When adding a new city beyond Warsaw (e.g., Sofia, Belgrade)

**Requirements:**
- Implement GDPR-compliant geolocation with opt-in consent
- Add to priority order: User preference → Geolocation (opt-in) → Language mapping → Fallback
- No storage of geolocation data (temporary use only)
- Clear opt-out option for users
- Update Privacy Policy and Cookie Policy

**Implementation location:** `apps/web/lib/geo-location.ts`

**GDPR compliance:**
- Explicit user consent required (opt-in)
- No data persistence
- Transparent purpose explanation

---

### Provider Full Page & Badge система (May 21, 2026)

#### Badge система (verification_level)
- Нова колона `verification_level INTEGER DEFAULT 0` в `providers` таблицата
- Функция `calculate_verification_level(provider)` в `apps/api/services/provider_service.py`
- Три нива: 0 = Нов (amber), 1 = Верифициран (green), 2 = Топ специалист (yellow)
- Автоматично се преизчислява при: `PATCH /profile`, `POST /services`, `PATCH /leads/{id}` (status=done)
- Badge downgrade работи в реално време — не само нагоре

#### Нови компоненти
- `apps/web/components/provider/ProviderFullPage.tsx` — Server Component, двуколонен десктоп layout (1fr + 340px sticky), едноколонен мобилен
- `apps/web/components/provider/AboutSection.tsx` — Client Component, read_more toggle
- `apps/web/components/provider/LeadPanel.tsx` — Client Component, full lead submission logic identical to ProviderWidget.tsx post-lead flow: success screen, email capture nudge, pending_lead_claim registration, PWA prompt trigger
- Условен render в `page.tsx`: `?embed=1` → ProviderWidget (непроменен), иначе → ProviderFullPage

#### Gallery backend
- Нова таблица `provider_images` (id, provider_id, url, position, created_at)
- Endpoints: GET/POST/DELETE /api/v1/provider/images, PATCH /api/v1/provider/images/reorder
- Storage: `uploads/provider_gallery/{provider_id}/{image_id}.webp`
- Position 0 = корица (cover) в hero на ProviderFullPage
- Cover image: фиксирана височина h-48, object-cover, object-top
- Gallery секция: показва gallery.slice(1) — без корицата; видима само ако gallery.length > 1

#### Category page badge актуализация
- `apps/web/app/[lang]/[city]/[category]/page.tsx` актуализиран да ползва `verification_level` (0/1/2) вместо `is_verified`
- Консистентни цветове: amber-100/text-amber-700 (Нов), green-100/text-green-700 (Верифициран), yellow-100/text-yellow-700 (Топ)

#### Mobile Sticky CTA за Provider страница (May 22, 2026) — COMPLETE
- Нов компонент: `apps/web/components/provider/StickyProviderCTA.tsx`
- Логика идентична с `StickyLeadFormButton` (md:hidden, isFormInView, paddingBottom)
- Target: id="provider-lead-form" в ProviderFullPage.tsx
- Translation key: cta_button (namespace: provider_page)
- Seed скрипт: apps/api/scripts/seed_provider_cta_button.py (34 езика)
- Изтрити грешно въведени zh преводи (24 реда)
- Bugs fixed по време на имплементацията:
  - ProviderFullPage не зареждаше provider_page namespace (translations={} → translations={providerPageT})
  - t['provider_page.KEY'] → t['KEY'] в ProviderFullPage.tsx и LeadPanel.tsx (18 замени)

#### Translation keys добавени
- namespace `widget`: badge_new_provider, badge_verified, badge_top_specialist
- namespace `provider_page`: section_gallery, section_about, section_services, section_reviews, read_more, read_less, completed_jobs, meta_services, meta_cities, reviews_count, request_panel_title, request_panel_free, request_panel_no_commitment, or_general_request, phone_placeholder, notes_placeholder, cta_button, trust_verified, trust_free, trust_direct
- Seed скрипт: apps/api/scripts/seed_provider_page_translations.py
- Easy opt-out mechanism