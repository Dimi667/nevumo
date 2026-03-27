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
      "accepted_matches": 15,
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

---

## GET /api/v1/provider/leads

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
        "status": "new",
        "source": "seo",
        "created_at": "2025-01-15T10:30:00"
      }
    ],
    "total": 24
  }
}
```

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

### Response

{
  "success": true,
  "data": {
    "id": "uuid",
    "business_name": "Maria Massage",
    "description": "...",
    "slug": "maria-petrova",
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
      "new_request_button": "New Request"
    }
  }
}

### Notes
- **rating** is calculated dynamically as AVG(reviews.rating) from reviews table
- **jobs_completed** is calculated from leads.status='done' + lead_matches.status='done'
- **review_count** is the total number of reviews for this provider
- **translations** contains widget-specific translations for the requested language
- If rating = 0 and jobs_completed = 0, these fields are still returned but UI should hide them
- All 32 supported languages are available (see i18n.py for full list)

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

- If provider_slug:
  → direct lead (provider_id set)

- If no provider:
  → marketplace lead (matching triggered)

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

# 🔹 INTERNAL / MATCHING (BACKGROUND)

---

## 6. Match Providers to Lead

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

## 7. Get Provider Leads — MOVED

See `GET /api/v1/provider/leads` in the Provider Dashboard section above.

---

## 8. Update Lead Status — MOVED

### PATCH
/api/v1/provider/leads/{id}

### Body

{
  "status": "contacted | done | rejected"
}

---

# 🔹 TRACKING (IMPORTANT)

---

## 9. Track Event

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