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
{ "email": "user@example.com", "password": "min8chars", "role": "client | provider" }

### Response (201)
{ "success": true, "data": { "token": "JWT", "user": { "id": "uuid", "email": "...", "role": "client" } } }

### Errors
- 409 EMAIL_ALREADY_EXISTS
- 429 RATE_LIMIT_EXCEEDED
- 422 VALIDATION_ERROR

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
{ "business_name": "New Name", "description": "New desc", "availability_status": "busy" }
```
All fields optional. `availability_status` must be `active` | `busy` | `offline`.

### Response
```json
{ "success": true, "data": { ...updated provider... } }
```

---

## POST /api/v1/provider/profile/image

### Body
`multipart/form-data`, field: `file` (jpeg/png/webp, max 5MB)

### Response
```json
{ "success": true, "data": { "image_url": "/static/provider_images/uuid.jpg" } }
```

---

## GET /api/v1/provider/services

### Response
```json
{ "success": true, "data": { "services": [ { "id": "uuid", "title": "...", "price_type": "fixed", "base_price": 50.0 } ] } }
```

---

## POST /api/v1/provider/services

### Body
```json
{ "category_id": 1, "title": "Relax Massage", "description": "...", "price_type": "fixed", "base_price": 50 }
```

### Response (201)
```json
{ "success": true, "data": { "id": "uuid", "title": "Relax Massage", "category_id": 1, "price_type": "fixed", "base_price": 50.0 } }
```

### Errors
- 404 CATEGORY_NOT_FOUND — invalid category_id
- 400 INVALID_PRICE_TYPE — must be fixed | hourly | request

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
| INVALID_PRICE_TYPE | 400 | price_type not in fixed/hourly/request |
| CITY_NOT_FOUND | 404 | Invalid city_id |
| CITY_ALREADY_ADDED | 409 | Duplicate provider+city |

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
/api/v1/providers/{provider_slug}

### Response

{
  "success": true,
  "data": {
    "id": "uuid",
    "business_name": "Maria Massage",
    "description": "...",
    "rating": 4.8,
    "verified": true,
    "services": [
      {
        "id": "uuid",
        "title": "Relax Massage",
        "price_type": "fixed",
        "base_price": 50
      }
    ]
  }
}

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
/ api/v1/categories?lang=en

### Response

{
  "success": true,
  "data": [
    {
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
      "slug": "sofia",
      "name": "Sofia"
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