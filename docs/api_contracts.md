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

## Authentication (Phase 1)

- Public endpoints (no auth)
- Provider dashboard (future → JWT)

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

# 🔹 PROVIDER (FUTURE DASHBOARD)

---

## 7. Get Provider Leads

### GET
/api/v1/provider/leads

(Auth required)

### Response

{
  "success": true,
  "data": [
    {
      "id": "uuid",
      "phone": "+359...",
      "status": "created",
      "created_at": "..."
    }
  ]
}

---

## 8. Update Lead Status

### PATCH
/api/v1/provider/leads/{id}

### Body

{
  "status": "accepted | rejected"
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

- INVALID_PHONE
- CATEGORY_NOT_FOUND
- CITY_NOT_FOUND
- PROVIDER_NOT_FOUND
- RATE_LIMIT_EXCEEDED

---

## Future Extensions

- JWT authentication
- Webhooks (provider notifications)
- GraphQL layer
- AI matching endpoint