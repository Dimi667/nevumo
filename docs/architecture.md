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
 - When a requested language has no rows for a namespace, the backend falls back to `en` before returning an empty payload

### Translation System Architecture
- **Source of truth**: PostgreSQL `translations` table
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

### Translation Fallback Chain
- Requested language is attempted first
- If the namespace has no rows for that language, backend falls back to `en`
- If English also has no rows, the endpoint returns an empty object
- Frontend can additionally supply local fallback strings through `t()` for critical UI rendering

### Market Scaling Principle
- New market launch should require **DB seeding only**, not new translation-fetching code paths
- Homepage/category/review pages consume the same namespaced translation endpoint regardless of market
- Operational rule: adding a new market means inserting translation rows for that locale and namespace set, with zero application logic changes

### Widget Translation Namespace
- All provider widget UI strings are stored in the `widget` namespace of the `translations` table
- Keys follow the pattern `widget.key_name` (e.g., `widget.button_text`, `widget.phone_label`)
- Backend serves them via `get_widget_translations(lang, db)` in `apps/api/routes/providers.py`
- Frontend `ProviderWidget` receives them as `provider.translations` prop and accesses via `const t = provider.translations`
- Fallback: if requested lang has no widget rows, falls back to English
- Total keys: 23 per language
 
 ---
 
## Frontend Architecture
- Next.js App Router
- Server Components for SEO pages
- Client components for interactions

### Homepage Architecture (Provider-First Acquisition)
- Route: `apps/web/app/[lang]/page.tsx`
- Homepage is provider-first: it is designed primarily to convert service providers into registrations, not to browse providers
- Rendering strategy is SSR so hero copy, metadata, and translated acquisition content are available on first response
- Metadata is generated server-side from the `homepage` namespace translations
- Main CTA drives to `/${lang}/auth`
- Top navigation includes a secondary service-seeker escape hatch to a real marketplace route

### Homepage Content System
- Homepage copy is fully DB-driven through the `homepage` namespace
- The hero uses split keys (`hero_prefix`, `hero_suffix`) plus a rotating category component in the middle
- Social proof, trust bullets, step copy, category-card labels, activity feed copy, footer links, and CTA copy all read from the same namespace
- This keeps homepage localization operationally simple: content edits can be made in DB without changing React code

### Rotating Categories Decision
- `RotatingCategory` is the only client component in the homepage hero path
- Rotation values come from the DB key `homepage.rotating_categories` as a comma-separated list
- Server component loads the translated string, splits it into categories, then passes the array to the client component
- Rotation interval is 3 seconds with a short fade transition
- Architectural goal: keep the page mostly SSR while isolating animation to a tiny client island

### Category Page Architecture (Client-First Conversion, SEO-Stable Routing)
- Route: `apps/web/app/[lang]/[city]/[category]/page.tsx`
- Category pages are SEO landing pages with a strong conversion layer for clients requesting a service
- Page shell, metadata, provider list, trust bar, SEO body copy, and related links are server-rendered
- Conversion interaction is centered around the lead form and in-page CTA anchors
- The page is "client-first" in product intent: the main user action is sending a request, while provider join CTAs are secondary
- Mobile sticky CTA behavior is handled by `CategoryPageClient` + `StickyLeadFormButton`, which target the mobile form wrapper through `id="lead-form-anchor"`
- The sticky CTA is rendered as a fixed client component that starts hidden with `translateY(100%)`, stays hidden while the mobile form anchor is intersecting, and slides in with `translateY(0)` only after the form wrapper leaves the viewport on mobile

### Category Slug Mapping Decision
- Public localized route slugs are intentionally decoupled from backend canonical category slugs
- Example mapping in current implementation:
  - `masaz` → `massage`
  - `sprzatanie` → `cleaning`
  - `hydraulik` → `plumbing`
- This preserves localized, SEO-friendly URLs while keeping backend API contracts stable and canonical
- The same mapping also drives translation key selection (`massage`, `cleaning`, `plumbing`) for category-specific copy

### Category Page Data Composition
- Provider list comes from `getProviders(categorySlug, citySlug, lang)`
- Each visible provider is then enriched with `getProviderBySlug(...)` for extra trust fields such as description, jobs completed, and latest lead preview timestamp
- Trust bar combines dynamic provider count and rating with translated category copy
- SEO body sections and FAQ content are rendered from translation keys keyed by mapped category type
- Lead form remains in a sticky sidebar on large screens for persistent conversion visibility

### Category Page SEO Decisions
- `generateMetadata()` uses category translations to produce localized title/description per route
- `generateHreflangAlternates()` is used for language alternates on both homepage and category routes
- FAQ structured data is rendered through JSON-LD for richer search appearance
- Related internal links are category-aware to strengthen crawl paths between major service pages
- Long-form SEO text is still rendered in the main page response, not lazy-loaded, to preserve crawlability---

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
- API Key: stored in apps/api/services/translation_service.py
- Format: POST { "q": text, "target": lang } with Authorization: Bearer header
- Timeout: 30 seconds per request

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

Replace automatic numeric suffix slug generation with user-controlled slug selection featuring smart suggestions and validation. Prevents SEO-unfriendly URLs like "devs-1", "devs-2".

### Validation Rules

**Forbidden patterns:**
- `devs-1`, `devs-123` (any numeric suffix)
- `DevS` (uppercase)
- `devs_studio` (underscores)
- `devs@studio` (special chars)

**Allowed patterns:**
- `devs-sofia`
- `devs-massage`
- `devs-pro`
- `devs-studio-bg`

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

### Profile update endpoint:
- Accepts optional `slug` field
- Validates format (no numeric suffixes, only a-z/0-9/-)
- Returns 409 SLUG_TAKEN with suggestions if slug in use
- Returns 400 INVALID_SLUG for format violations
- **SECURITY**: Backend automatically detects onboarding status using `check_onboarding_complete()`
- **SLUG CHANGE LIMIT**: 1 change allowed after onboarding completion
- **REDIRECT SYSTEM**: Automatic 301 redirects for old slugs to new slugs

**Registration endpoint:**
- Accepts optional `slug`, `city_slug`, `category_slug` fields
- For provider role: validates slug uniqueness, returns 409 SLUG_TAKEN if taken
- Auto-generates slug from email if not provided
- Rolls back user creation if provider creation fails

### User Flow

**Profile Update Flow:**
1. User enters business name → base slug auto-generated (no suffix)
2. If base slug is taken → error shown + 3-5 suggestions displayed
3. User can:
   - Click suggestion to use it
   - Edit slug manually with real-time validation
   - Check availability via "Check" button
4. On save → server validates again, returns error with suggestions if needed

**Registration Flow (Provider):**
1. User enters email + password
2. Account created immediately with temporary draft slug (not visible to user)
3. Redirect to onboarding step 1 (`/[lang]/provider/dashboard/profile`)
4. User enters business name → slug auto-generated from business name (not email)
5. Real-time availability check shows suggestions if taken
6. User can edit slug manually with validation
7. On save with `is_onboarding_setup: true` → slug set without consuming allowed change count

**Registration Flow (Client):**
- No slug selection step
- Registration proceeds directly after password entry

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
- Draft is stored in sessionStorage (cleared when tab closes, not shared across tabs)
- Safety check ensures loaded draft matches current providerId before use

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
- Browser password save: hidden iframe technique (triggerPasswordSave)
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