# Nevumo API Contracts

## Core Principles

- REST-based API (FastAPI)
- JSON only
- Consistent response format
- Optimized for frontend (Next.js)
- Minimal payloads for performance

---

## Base URL

/api/v1

---

## Standard Response Format

### Success

{
  "success": true,
  "data": {}
}

### Error

{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  }
}

---

## Authentication (Phase 1) — DONE

- Email-based auth: register, login, forgot/reset password
- JWT tokens: 30-day expiry, stored in localStorage (Phase 1)
- All 6 endpoints live at `/api/v1/auth/`
- Provider dashboard: JWT required (auth infrastructure ready)

---

# 🔹 AUTHENTICATION ENDPOINTS — COMPLETE

---

## POST /api/v1/auth/check-email

### Body
{ "email": "user@example.com" }

### Response
{ "success": true, "data": { "exists": true } }

---

## POST /api/v1/auth/register

### Body
```json
{ 
  "email": "user@example.com", 
  "password": "min8chars", 
  "role": "client | provider"
}
```

`role` defaults to "provider". For provider role, a provider record is created automatically with a temporary draft slug (not visible to users). The actual public slug and business name are set during onboarding step 1.

### Response (201)
```json
{ "success": true, "data": { "token": "JWT", "user": { "id": "uuid", "email": "...", "role": "client" } } }
```

### Errors
- 409 EMAIL_ALREADY_EXISTS
- 429 RATE_LIMIT_EXCEEDED
- 422 VALIDATION_ERROR

---

## GET /api/v1/auth/register/slug/check

Checks if a slug is available for registration and returns smart suggestions if taken. No authentication required.

### Query Params
- `slug` (required, 2-50 chars) — slug to check
- `city_slug` (optional) — for contextual suggestions
- `category_slug` (optional) — for contextual suggestions

### Example
```
GET /api/v1/auth/register/slug/check?slug=devs&city_slug=sofia&category_slug=massage
```

### Response (Available)
```json
{
  "success": true,
  "data": {
    "available": true,
    "valid": true
  }
}
```

### Response (Taken)
```json
{
  "success": true,
  "data": {
    "available": false,
    "valid": true,
    "suggestions": ["devs-sofia", "devs-massage", "devs-pro", "devs-studio"]
  }
}
```

### Response (Invalid Format)
```json
{
  "success": true,
  "data": {
    "available": false,
    "valid": false,
    "error": "Numeric suffixes like '-1', '-123' are not allowed for SEO reasons"
  }
}
```

---

## POST /api/v1/auth/login

### Body
{ "email": "user@example.com", "password": "..." }

### Response
{ "success": true, "data": { "token": "JWT", "user": { "id": "uuid", "email": "...", "role": "client" } } }

### Errors
- 401 INVALID_CREDENTIALS
- 403 ACCOUNT_DISABLED
- 429 RATE_LIMIT_EXCEEDED

---

## POST /api/v1/auth/forgot-password

### Body
{ "email": "user@example.com" }

### Response (always same — no email enumeration)
{ "success": true, "data": { "message": "If an account with this email exists, a reset link has been sent." } }

### Errors
- 429 RATE_LIMIT_EXCEEDED

---

## POST /api/v1/auth/validate-reset-token

### Body
{ "token": "raw_token_from_url" }

### Response
{ "success": true, "data": { "valid": true } }
{ "success": true, "data": { "valid": false, "error": "expired | used" } }

---

## POST /api/v1/auth/reset-password

### Body
{ "token": "raw_token_from_url", "password": "newpassword" }

### Response — auto-login (returns JWT)
{ "success": true, "data": { "token": "JWT", "user": { "id": "uuid", "email": "...", "role": "client" } } }

### Errors
- 400 TOKEN_INVALID
- 400 TOKEN_EXPIRED
- 400 TOKEN_USED
- 429 RATE_LIMIT_EXCEEDED

---

## Auth Error Codes

| Code | Status | Meaning |
|------|--------|---------|
| INVALID_CREDENTIALS | 401 | Wrong email or password |
| EMAIL_ALREADY_EXISTS | 409 | Email already registered |
| SLUG_TAKEN | 409 | Slug already in use (returns `extra_data.suggestions`) |
| INVALID_SLUG | 400 | Slug format invalid (numeric suffix, invalid chars, wrong length) |
| RATE_LIMIT_EXCEEDED | 429 | Too many attempts (5/15 min per IP) |
| ACCOUNT_DISABLED | 403 | Account is deactivated |
| TOKEN_INVALID | 400 | Reset token not found |
| TOKEN_EXPIRED | 400 | Reset token expired (30 min TTL) |
| TOKEN_USED | 400 | Reset token already used |
| VALIDATION_ERROR | 422 | Request body validation failed |

---

# 🔹 PROVIDER DASHBOARD ENDPOINTS (JWT Required)

All endpoints require `Authorization: Bearer <JWT>` header.
Provider must have a provider record (role=provider + completed registration).

---

## GET /api/v1/provider/dashboard

### Response
```json
{
  "success": true,
  "data": {
    "stats": {
      "total_leads": 24,
      "new_leads": 5,
      "contacted_leads": 15,
      "rating": 4.8,
      "verified": true,
      "availability_status": "active"
    },
    "profile": {
      "id": "uuid",
      "business_name": "Maria Massage",
      "slug": "maria-massage",
      "is_complete": true,
      "missing_fields": []
    }
  }
}
```

### Onboarding Completeness (missing_fields)

When `is_complete` is `false`, `missing_fields` contains the specific items needed to complete onboarding:

| Field | Meaning |
|-------|---------|
| `business_name` | Profile incomplete (no business name set) |
| `service` | No service created |
| `city` | Service exists but has no cities assigned |

**Example incomplete states:**

```json
// Fresh provider with no profile or service
"missing_fields": ["business_name", "service", "city"]

// Profile complete, service missing
"missing_fields": ["service", "city"]

// Has service but no cities assigned
"missing_fields": ["city"]
```

---

## GET /api/v1/provider/leads

### Query Params

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | string | `all` | Filter by status: `all`, `new` (maps to DB `created`), `contacted`, `done`, `rejected` |
| `period` | string | `all` | Preset period: `all`, `7`, `30`, `90` (days) |
| `date_from` | string | - | Custom start date (YYYY-MM-DD), overrides `period` |
| `date_to` | string | - | Custom end date (YYYY-MM-DD), overrides `period` |

### Response
```json
{
  "success": true,
  "data": {
    "leads": [
      {
        "id": "uuid",
        "phone": "+359...",
        "description": "...",
        "status": "created",
        "source": "seo",
        "created_at": "2025-01-15T10:30:00"
      }
    ],
    "total": 24
  }
}
```

### Notes
- Results are ordered by `created_at DESC`
- `total` is the real count after filters (not limited by pagination)
- `status=new` filters by DB status `created`

---

## PATCH /api/v1/provider/leads/{lead_id}

### Body
```json
{ "status": "contacted" }
```
Allowed values: `contacted` | `done` | `rejected`

### Response
```json
{ "success": true, "data": { "lead_id": "uuid", "status": "contacted" } }
```

### Errors
- 400 INVALID_STATUS_TRANSITION — invalid state change
- 404 LEAD_NOT_FOUND — lead doesn't exist or provider doesn't own it

---

## GET /api/v1/provider/profile

### Response
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "business_name": "Maria Massage",
    "description": "...",
    "slug": "maria-massage",
    "profile_image_url": "/static/provider_images/uuid.jpg",
    "rating": 4.8,
    "verified": true,
    "availability_status": "active",
    "created_at": "..."
  }
}
```

---

## PATCH /api/v1/provider/profile

### Body
```json
{ 
  "business_name": "New Name", 
  "description": "New desc", 
  "availability_status": "busy",
  "slug": "new-business-name"
}
```
All fields optional. `availability_status` must be `active` | `busy` | `offline`.
`slug` must be 2-50 chars, lowercase letters/numbers/hyphens only, no numeric suffixes (e.g., `devs-1`).

### Response
```json
{ "success": true, "data": { ...updated provider... } }
```

### Errors
- 400 INVALID_SLUG — slug format invalid (numeric suffix, invalid chars, wrong length)
- 409 SLUG_TAKEN — slug already in use (returns suggestions in `data.suggestions`)

---

## GET /api/v1/provider/slug/check

Checks if a slug is available and returns smart suggestions if taken.

### Query Params
- `slug` (required, 2-50 chars) — slug to check
- `city_slug` (optional) — for contextual suggestions
- `category_slug` (optional) — for contextual suggestions

### Example
```
GET /api/v1/provider/slug/check?slug=devs&city_slug=sofia&category_slug=massage
```

### Response (Available)
```json
{
  "success": true,
  "data": {
    "available": true,
    "suggestions": null
  }
}
```

### Response (Taken)
```json
{
  "success": true,
  "data": {
    "available": false,
    "suggestions": ["devs-sofia", "devs-massage", "devs-pro", "devs-studio"]
  }
}
```

### Response (Invalid Format)
```json
{
  "success": false,
  "error": { "code": "INVALID_SLUG", "message": "Numeric suffixes not allowed (e.g., devs-1)" },
  "data": { "available": false, "suggestions": [] }
}
```

### Suggestion Logic
Suggestions are generated in priority order:
1. `{slug}-{city_slug}` (if city provided)
2. `{slug}-{category_slug}` (if category provided)
3. `{slug}-{city_slug}-{category_slug}` (if both provided)
4. Generic: `{slug}-pro`, `{slug}-studio`, `{slug}-bg`

Taken slugs are filtered out. Maximum 5 suggestions returned.

---

## POST /api/v1/provider/profile/image

### Body
`multipart/form-data`, field: `file` (jpeg/png/webp, max 5MB)

### Response
```json
{ "success": true, "data": { "image_url": "http://localhost:8000/static/provider_images/uuid.jpg" } }
```

**Note**: Returns full URL to support cross-origin loading and future cloud storage migration.

---

## GET /api/v1/provider/services

### Response
```json
{
  "success": true,
  "data": {
    "services": [
      {
        "id": "uuid",
        "title": "Relax Massage",
        "category_id": 1,
        "category_slug": "massage",
        "cities": [
          { "id": 1, "slug": "sofia", "city": "Sofia" }
        ],
        "description": "...",
        "price_type": "fixed",
        "base_price": 50.0,
        "currency": "EUR"
      }
    ]
  }
}
```

---

## POST /api/v1/provider/services

### Body
```json
{
  "title": "Relax Massage",
  "category_id": 1,
  "city_ids": [1, 2],
  "description": "...",
  "price_type": "fixed",
  "base_price": 50,
  "currency": "EUR"
}
```
`price_type` must be `fixed` | `hourly` | `request` | `per_sqm`
`currency` is optional. If not provided, auto-detected from first city's country_code using country-to-currency mapping. Must be one of: EUR, USD, GBP, CHF, CZK, DKK, HUF, PLN, RON, SEK, NOK, TRY, ALL, MKD, RSD, BAM, HRK
`city_ids` must contain at least 1 item.
Creating a service also upserts those cities into `provider_cities` (for lead matching).

### Response (201)
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "title": "Relax Massage",
    "category_id": 1,
    "category_slug": "massage",
    "cities": [{ "id": 1, "slug": "sofia", "city": "Sofia" }],
    "description": "...",
    "price_type": "fixed",
    "base_price": 50.0,
    "currency": "EUR"
  }
}
```

### Errors
- 404 CATEGORY_NOT_FOUND — invalid category_id
- 404 CITY_NOT_FOUND — one or more city_ids not found
- 422 INVALID_CURRENCY — currency code not in allowed list

---

## PUT /api/v1/provider/services/{service_id}

All fields optional — only provided fields are updated.
If `city_ids` is provided, replaces all service cities and syncs `provider_cities`.

### Body
```json
{
  "title": "Updated Name",
  "city_ids": [3],
  "price_type": "hourly",
  "base_price": 60,
  "currency": "BGN"
}
```

### Response
```json
{ "success": true, "data": { ...full ServiceResponse... } }
```

### Errors
- 404 SERVICE_NOT_FOUND — service doesn't exist or provider doesn't own it
- 404 CATEGORY_NOT_FOUND — invalid category_id
- 404 CITY_NOT_FOUND — invalid city_ids
- 422 INVALID_CURRENCY

---

## DELETE /api/v1/provider/services/{service_id}

Deletes the service and cascades to `service_cities`.

### Response
```json
{ "success": true, "data": { "message": "Service deleted" } }
```

### Errors
- 404 SERVICE_NOT_FOUND — service doesn't exist or provider doesn't own it

---

## POST /api/v1/provider/cities

### Body
```json
{ "city_id": 1 }
```

### Response (201)
```json
{ "success": true, "data": { "message": "City added" } }
```

### Errors
- 404 CITY_NOT_FOUND — invalid city_id
- 409 CITY_ALREADY_ADDED — duplicate provider+city

---

## GET /api/v1/provider/qr-code

### Response
```json
{
  "success": true,
  "data": {
    "public_url": "https://nevumo.com/en/sofia/massage/maria-massage",
    "qr_code": "data:image/png;base64,iVBOR..."
  }
}
```

---

## Provider Dashboard Error Codes

| Code | Status | When |
|------|--------|------|
| LEAD_NOT_FOUND | 404 | Lead doesn't exist or provider doesn't own it |
| INVALID_STATUS_TRANSITION | 400 | Invalid status change (e.g. done → contacted) |
| CATEGORY_NOT_FOUND | 404 | Invalid category_id |
| CITY_NOT_FOUND | 404 | Invalid city_id in city_ids |
| CITY_ALREADY_ADDED | 409 | Duplicate provider+city |
| SERVICE_NOT_FOUND | 404 | Service doesn't exist or provider doesn't own it |
| INVALID_CURRENCY | 422 | currency code not in the allowed list |

---

# 🔹 PUBLIC ENDPOINTS (CRITICAL FOR SEO + WIDGET)

---

## 1. Get Providers by Category + City

### GET
/api/v1/providers

### Query Params

- category_slug (required)
- city_slug (required)
- lang (optional)

### Example

/api/v1/providers?category_slug=massage&city_slug=sofia&lang=en

### Response

{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "business_name": "Maria Massage",
      "rating": 4.8,
      "verified": true,
      "slug": "maria-petrova"
    }
  ]
}

---

## 2. Get Provider Details

### GET
/api/v1/providers/{provider_slug}?lang={lang}

### Query Params
- lang: optional, default 'en' (supports all 32 languages)
- city_slug: optional, enables city-specific widget stats like `city_leads`

### Response

{
  "success": true,
  "data": {
    "id": "uuid",
    "business_name": "Maria Massage",
    "description": "...",
    "slug": "maria-petrova",
    "slug_change_count": 0,
    "profile_image_url": "/static/provider_images/uuid.jpg",
    "rating": 4.9,
    "verified": true,
    "availability_status": "active",
    "created_at": "...",
    "services": [
      {
        "id": "uuid",
        "title": "Relax Massage",
        "price_type": "fixed",
        "base_price": 50
      }
    ],
    "jobs_completed": 120,
    "review_count": 45,
    "leads_received": 128,
    "city_leads": 1240,
    "latest_lead_preview": {
      "client_name": "Anna",
      "city_name": "Sofia",
      "created_at": "2025-04-02T14:30:00",
      "client_image_url": null
    },
    "latest_review": {
      "client_name": "Ivan Petrov",
      "rating": 5,
      "comment_preview": "Excellent service, very professional!",
      "created_at": "2025-04-01T10:30:00"
    },
    "translations": {
      "verified_label": "✓ Verified professional",
      "rating_label": "rating",
      "jobs_label": "jobs completed",
      "phone_label": "Phone",
      "phone_placeholder": "e.g. +359 888 123 456",
      "notes_label": "Notes",
      "notes_placeholder": "Describe your request (time, address, details)",
      "response_time": "⏱ Provider usually responds within 30 minutes",
      "button_text": "Request Service",
      "disclaimer": "Free request • No obligation",
      "success_title": "✓ Successfully sent!",
      "success_message": "We will contact you soon.",
      "new_request_button": "New Request",
      "new_badge": "New",
      "no_reviews_yet": "No reviews yet",
      "recent_request_label": "{name} from {city} requested recently",
      "city_leads_label": "{count} requests for {category} in {city} this year",
      "free_request_no_obligation": "Free request, no obligation",
      "no_registration": "No registration",
      "direct_contact_with_provider": "Direct contact with the provider"
    }
  }
}

### Notes
- **rating** is calculated dynamically as AVG(reviews.rating) from reviews table
- **jobs_completed** is calculated from leads.status='done' + lead_matches.status='done'
- **review_count** is the total number of reviews for this provider
- **leads_received** is the total number of direct leads received by this provider
- **city_leads** is the total number of leads created in the requested `city_slug`; omitted context returns `0`
- **latest_lead_preview** contains the most recent lead preview-safe data for widget fallback states
- **latest_lead_preview.client_name** uses `users.name` when available and falls back to `Client`; no email local-part leakage
- **latest_lead_preview.client_image_url** is currently nullable and returns `null` because the public user model has no client avatar field
- **latest_review** contains the most recent review for this provider; `comment_preview` may be `null`
- **latest_review.client_name** uses `users.name` when available and falls back to `Client`; email local-parts are never exposed
- **translations** contains widget-specific translations for the requested language
- **slug_change_count** indicates remaining URL changes (0 = 1 change allowed, 1 = locked)
- The embed widget treats the top and bottom trust sections independently:
  - top: `rating` → `jobs_completed` → `latest_lead_preview` → `new_badge/no_reviews_yet`
  - bottom: `latest_review` → `city_leads` → checklist translations
- All 32 supported languages are available (see i18n.py for full list)

---

## 2.1. Resolve Slug (Redirect Check)

### GET
/api/v1/providers/resolve/{slug}

### Purpose
Check if a slug redirects to another slug without following the redirect. Used by frontend for seamless URL updates.

### Response

**Found (no redirect):**
```json
{
  "found": true,
  "slug": "current-slug",
  "redirected": false
}
```

**Found (with redirect):**
```json
{
  "found": true,
  "slug": "new-slug",
  "redirected": true,
  "from_slug": "old-slug"
}
```

**Not found:**
```json
{
  "found": false,
  "slug": null,
  "redirected": false
}
```

### Notes
- Used by frontend to detect redirects and update browser URL seamlessly
- Prevents infinite redirect loops with max depth protection
- Returns 404 for non-existent slugs
- Security-hardened against frontend manipulation

---

## 3. Create Lead (🔥 MOST IMPORTANT)

### POST
/api/v1/leads

### Body

{
  "category_slug": "massage",
  "city_slug": "sofia",
  "provider_slug": "maria-petrova",   // optional
  "phone": "+359888123456",
  "description": "optional",
  "utm_source": "google",
  "utm_campaign": "ads",
  "source": "seo | widget | qr | direct"
}

### Logic

- If request includes a valid `Authorization: Bearer <jwt>` header:
  → `lead.client_id` is linked to the authenticated user

- If provider_slug:
  → direct lead (provider_id set)

- If no provider:
  → marketplace lead (matching triggered)

- If request is anonymous:
  → `lead.client_id` remains null and the lead cannot be used for authenticated review ownership

---

### Response

{
  "success": true,
  "data": {
    "lead_id": "uuid"
  }
}

---

## 4. Get Categories

### GET
/api/v1/categories?lang=en

### Response

{
  "success": true,
  "data": [
    {
      "id": 1,
      "slug": "massage",
      "name": "Massage"
    }
  ]
}

---

## 5. Get Cities

### GET
/api/v1/cities?country=BG

### Response

{
  "success": true,
  "data": [
    {
      "id": 1,
      "slug": "sofia",
      "name": "Sofia",
      "country_code": "BG",
      "currency": "EUR"
    },
    {
      "id": 2,
      "slug": "belgrade",
      "name": "Belgrade",
      "country_code": "RS",
      "currency": "RSD"
    }
  ]
}

---

## 6. Get Namespaced Translations

### GET
/api/v1/translations?lang=en&namespace=homepage

### Query Params

- `lang` (required, 2-5 chars)
- `namespace` (required, 1-50 chars)

### Behavior

- Returns all translation keys for the requested namespace
- Translation records are stored in DB as `namespace.key`
- Response strips the namespace prefix and returns a flat object
- Redis cache key: `translations:{lang}:{namespace}` with 1 hour TTL
- If no keys are found for the requested language and `lang != en`, the endpoint falls back to English

### Response

```json
{
  "success": true,
  "data": {
    "hero_title": "Find trusted providers",
    "hero_subtitle": "Compare local services"
  }
}
```

### Empty Response Example

```json
{
  "success": true,
  "data": {}
}
```

---

## 7. Match Providers to Lead

### Triggered automatically after lead creation

Pseudo-flow:

1. Find providers:
   - same category
   - same city
   - active

2. Insert into lead_matches

3. Notify providers (future)

---

# 🔹 PROVIDER DASHBOARD — see "PROVIDER DASHBOARD ENDPOINTS" section above (COMPLETE)

---

## 8. Get Provider Leads — MOVED

See `GET /api/v1/provider/leads` in the Provider Dashboard section above.

---

## 9. Update Lead Status — MOVED

### PATCH
/api/v1/provider/leads/{id}

### Body

{
  "status": "contacted | done | rejected"
}

---

# 🔹 TRACKING (IMPORTANT)

---

## 10. Track Event

### POST
/api/v1/events

### Body

{
  "lead_id": "uuid",
  "event_type": "view | submit | contact",
  "metadata": {}
}

---

# 🔥 CRITICAL DESIGN DECISIONS

---

## Slugs вместо IDs

Frontend работи със:
- category_slug
- city_slug
- provider_slug

Backend:
→ resolve към IDs

---

## Minimal Lead Form

Phase 1:

- phone (required)
- description (optional)

---

## Widget Compatibility

Same endpoint:
- SEO page
- provider page
- iframe widget
- QR traffic

---

## 🔹 API SCHEMAS

### SlugCheckRequest
```python
class SlugCheckRequest(BaseModel):
    slug: str  # 2-50 chars, lowercase letters/numbers/hyphens only
```

### SlugCheckResponse
```python
class SlugCheckResponse(BaseModel):
    success: bool = True
    data: dict  # Contains: available, valid, suggestions[], error
```

---

## Performance

- Providers endpoint must be cached (Redis)
- Categories & cities → cached
- Leads → never cached

---

## Validation Rules

- phone required
- category must exist
- city must exist
- provider must belong to category

---

## Error Codes (Examples)

Lead/provider errors:
- INVALID_PHONE
- CATEGORY_NOT_FOUND
- CITY_NOT_FOUND
- PROVIDER_NOT_FOUND
- RATE_LIMIT_EXCEEDED

Auth errors (see Auth section for full list):
- INVALID_CREDENTIALS
- EMAIL_ALREADY_EXISTS
- TOKEN_EXPIRED / TOKEN_USED / TOKEN_INVALID
- ACCOUNT_DISABLED
- VALIDATION_ERROR

---

## Future Extensions

- OAuth (Google + Facebook) — UI placeholders exist
- Webhooks (provider notifications)
- GraphQL layer
- AI matching endpoint

---

# 🔹 REVIEW SYSTEM API (Closed Trust Conversation Model)

## Overview

The review system implements a closed trust conversation model:
- **Client review is the starting message**
- **Provider has exactly one reply per review** (editable unlimited times)
- **Conversation closes after provider reply** - no further messages
- **Email notifications** - Sent to client on first provider reply only (if opted in)
- **Client display name privacy** - Review surfaces use `users.name` or `Client`, never email-derived names

---

## Client Endpoints (JWT Required)

### GET /api/v1/client/dashboard

**Purpose:** Return overview KPI stats and the latest 3 client-owned leads for the authenticated client dashboard.

**Rules:**
- Requires `Authorization: Bearer <JWT>`
- User must have `role='client'`
- `active_leads` maps to DB statuses: `created`, `pending_match`, `matched`, `contacted`
- `completed_leads` maps to DB status: `done`
- `reviews_written` counts rows in `reviews` where `reviews.client_id = current_user.id`
- `category_name` uses `category_translations.lang='en'` with fallback to `categories.slug`
- `provider_business_name` is `null` when the lead has no assigned provider

**Response:**
```json
{
  "success": true,
  "data": {
    "stats": {
      "active_leads": 4,
      "completed_leads": 2,
      "reviews_written": 1
    },
    "recent_leads": [
      {
        "id": "uuid",
        "category_slug": "massage",
        "category_name": "Massage",
        "city": "Sofia",
        "provider_business_name": "Maria Massage",
        "status": "contacted",
        "created_at": "2025-01-15T10:30:00"
      }
    ]
  }
}
```

**Errors:**
- 403 NOT_A_CLIENT

---

### GET /api/v1/client/leads

**Purpose:** List the authenticated client's leads with dashboard-friendly filters and review state.

**Query Params:**
- `status` (`all` | `active` | `done` | `rejected`, default `all`)
- `limit` (int, default `50`, max `100`)
- `offset` (int, default `0`)

**Status mapping:**
- `active` → `created`, `pending_match`, `matched`, `contacted`
- `done` → `done`
- `rejected` → `rejected`, `expired`, `cancelled`

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "category_slug": "massage",
        "category_name": "Massage",
        "city": "Sofia",
        "city_slug": "sofia",
        "provider_id": "uuid",
        "provider_business_name": "Maria Massage",
        "provider_slug": "maria-massage",
        "status": "contacted",
        "description": "Need massage therapy",
        "source": "seo",
        "created_at": "2025-01-15T10:30:00",
        "has_review": false
      }
    ],
    "total": 24
  }
}
```

**Notes:**
- Results are ordered by `created_at DESC`
- `total` is the real count after filters, before pagination
- `has_review` is `true` when a review exists for the exact `lead_id`
- Provider fields are nullable for unmatched leads
- Client dashboard review CTAs should only be shown when `status='done'`, `has_review=false`, and `provider_id` is not null

**Errors:**
- 403 NOT_A_CLIENT

---

### GET /api/v1/client/reviews/eligible-leads

**Purpose:** List completed leads owned by the authenticated client that can appear in the review flow.

**Rules:**
- Requires a lead with `lead.client_id = current_user.id`
- Excludes completed leads pointing to a provider profile owned by the same user
- Frontend pending-review views should use `has_review=false` when rendering "Чакащи ревю"

**Response:**
```json
{
  "success": true,
  "data": {
    "leads": [
      {
        "id": "uuid",
        "description": "Need massage therapy for back pain",
        "created_at": "2025-01-15T10:30:00",
        "provider_id": "uuid",
        "provider_business_name": "Maria Massage",
        "has_review": false
      }
    ],
    "count": 3
  }
}
```

---

### POST /api/v1/client/reviews

**Purpose:** Create a review for a completed lead.

**Body:**
```json
{
  "lead_id": "uuid",
  "rating": 5,
  "comment": "Excellent service, very professional!"
}
```

**Rules:**
- Client must own the lead
- Lead must have status='done'
- Client cannot review their own provider profile
- One review per lead only
- Rating: 1-5 stars
- Comment: optional, max 1000 chars

**Response (201):**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "provider_id": "uuid",
    "lead_id": "uuid",
    "rating": 5,
    "comment": "Excellent service, very professional!",
    "created_at": "2025-04-02T14:30:00"
  }
}
```

**Errors:**
- 404 LEAD_NOT_FOUND
- 400 LEAD_NOT_COMPLETED - lead status is not 'done'
- 403 NOT_YOUR_LEAD - client doesn't own this lead
- 403 SELF_REVIEW_NOT_ALLOWED - client owns the target provider profile
- 409 REVIEW_EXISTS - review already exists for this lead

---

### GET /api/v1/client/reviews

**Purpose:** List all reviews submitted by the client.

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "provider_id": "uuid",
        "provider_business_name": "Maria Massage",
        "lead_id": "uuid",
        "lead_description": "Need massage therapy",
        "rating": 5,
        "comment": "Excellent service!",
        "created_at": "2025-04-02T14:30:00",
        "provider_reply": "Thank you for your kind words!",
        "provider_reply_at": "2025-04-02T16:00:00",
        "provider_reply_edited_at": null,
        "provider_reply_edit_count": 0,
        "is_reply_edited": false
      }
    ],
    "total": 10,
    "limit": 50,
    "offset": 0
  }
}
```

---

### GET /api/v1/client/reviews/preferences

**Purpose:** Get email notification preferences.

**Response:**
```json
{
  "success": true,
  "data": {
    "review_reply_email_enabled": true,
    "description": "Receive email notifications when providers reply to your reviews"
  }
}
```

---

### PATCH /api/v1/client/reviews/preferences

**Purpose:** Update email notification preferences.

**Query Params:**
- `review_reply_email_enabled` (boolean, required)

**Response:**
```json
{
  "success": true,
  "data": {
    "review_reply_email_enabled": false,
    "description": "Receive email notifications when providers reply to your reviews"
  }
}
```

---

### GET /api/v1/client/reviews/can-review-provider/{provider_id}

**Purpose:** Check if client can review a specific provider.

**Response (can review):**
```json
{
  "success": true,
  "data": {
    "can_review": true,
    "eligible_leads": [
      {
        "id": "uuid",
        "description": "Need massage therapy",
        "created_at": "2025-01-15T10:30:00"
      }
    ]
  }
}
```

**Response (cannot review):**
```json
{
  "success": true,
  "data": {
    "can_review": false,
    "reason": "self_review_not_allowed",
    "message": "You cannot review your own provider profile"
  }
}
```

`reason` can currently be `no_completed_jobs`, `already_reviewed`, or `self_review_not_allowed`.

---

## Provider Endpoints (JWT Required)

### GET /api/v1/provider/reviews

**Purpose:** List all review conversations for the provider.

**Query Params:**
- `limit` (int, default 50, max 100)
- `offset` (int, default 0)
- `unreplied_only` (boolean, default false)

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [
      {
        "id": "uuid",
        "provider_id": "uuid",
        "client_id": "uuid",
        "client_name": "Maria",
        "lead_id": "uuid",
        "rating": 5,
        "comment": "Great service!",
        "created_at": "2025-04-02T14:30:00",
        "provider_reply": "Thank you!",
        "provider_reply_at": "2025-04-02T16:00:00",
        "provider_reply_edited_at": null,
        "provider_reply_edit_count": 0,
        "is_reply_edited": false
      }
    ],
    "total": 25,
    "limit": 50,
    "offset": 0
  }
}
```

`client_name` is always the canonical review display name: `users.name` when present, otherwise `Client`.

---

### GET /api/v1/provider/reviews/latest-preview

**Purpose:** Get latest review preview for dashboard.

**Response (has reviews):**
```json
{
  "success": true,
  "data": {
    "has_reviews": true,
    "latest_review": {
      "id": "uuid",
      "client_name": "client_name",
      "rating": 5,
      "comment_preview": "Excellent service...",
      "has_reply": false,
      "created_at": "2025-04-02T14:30:00",
      "unreplied_count": 3
    },
    "unreplied_count": 3
  }
}
```

**Response (no reviews):**
```json
{
  "success": true,
  "data": {
    "has_reviews": false,
    "unreplied_count": 0
  }
}
```

---

### POST /api/v1/provider/reviews/{review_id}/reply

**Purpose:** Add first reply to a client review.

**Body:**
```json
{
  "reply": "Thank you for your review!"
}
```

**Rules:**
- Provider can only reply to their own reviews
- Only one reply per review (use PATCH for edits)
- Triggers email notification to client on first reply (if opted in)
- Max 2000 characters

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "provider_reply": "Thank you for your review!",
    "provider_reply_at": "2025-04-02T16:00:00",
    "provider_reply_edited_at": null,
    "provider_reply_edit_count": 0,
    "is_reply_edited": false
  }
}
```

**Errors:**
- 404 REVIEW_NOT_FOUND - review doesn't exist or not owned by provider

---

### PATCH /api/v1/provider/reviews/{review_id}/reply

**Purpose:** Edit existing reply (unlimited edits allowed).

**Body:**
```json
{
  "reply": "Updated: Thank you very much for your kind review!"
}
```

**Rules:**
- Can edit unlimited times
- Does NOT trigger email notification (only first reply sends email)
- Max 2000 characters

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "provider_reply": "Updated: Thank you very much!",
    "provider_reply_at": "2025-04-02T16:00:00",
    "provider_reply_edited_at": "2025-04-02T17:00:00",
    "provider_reply_edit_count": 1,
    "is_reply_edited": true
  }
}
```

---

## Review System Error Codes

| Code | Status | Description |
|------|--------|-------------|
| LEAD_NOT_FOUND | 404 | Lead doesn't exist |
| LEAD_NOT_COMPLETED | 400 | Lead status is not 'done' |
| NOT_YOUR_LEAD | 403 | Client doesn't own this lead |
| SELF_REVIEW_NOT_ALLOWED | 403 | Client attempted to review their own provider profile |
| REVIEW_EXISTS | 409 | Review already exists for this lead |
| REVIEW_NOT_FOUND | 404 | Review doesn't exist or provider doesn't own it |
| INVALID_RATING | 422 | Rating must be 1-5 |
| INVALID_REPLY | 422 | Reply cannot be empty or exceeds 2000 chars |

---

## Email Notification Behavior

### Provider Reply Notifications

**Trigger:** First provider reply only

**Recipient:** Client who submitted the review

**Condition:** Only sent if `user.review_reply_email_enabled = true` (opted in)

**Content:**
- Subject: "{provider_name} responded to your review"
- Body includes: client review, provider reply, link to view reviews
- Footer: Link to manage email preferences

**Opt-out:** Client can disable in dashboard settings (`/api/v1/client/reviews/preferences`)

### Edit Notifications

**No emails sent** when provider edits an existing reply. Only the first reply triggers notification.

---

## Frontend Integration

### Client Dashboard
- `/client/dashboard/jobs` - List completed jobs with "Write a review" CTA
- `/client/dashboard/reviews` - List submitted reviews with provider replies
- Email preferences toggle in reviews section

### Provider Dashboard
- `/provider/dashboard` - Shows "Latest Review" preview card
- `/provider/dashboard/reviews` - Full review management with reply/edit functionality
- Unreplied review count badge in sidebar

---

## Migration Required

Run the following to enable the review system:

```bash
# Run database migration
cd apps/api
alembic upgrade g6h7i8j9k0l1

# Seed translation keys
python scripts/seed_review_translations.py
```