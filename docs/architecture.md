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

---

## Scaling Strategy

### Phase 1 (0–10k users)
- Single PostgreSQL instance
- Redis caching
- Basic indexing

---

### Phase 2 (10k–100k users)
- Read replicas
- Query optimization
- Background jobs (Celery / RQ)

---

### Phase 3 (100k+ users, multi-country)

#### 🔥 KEY DECISION: Region-aware architecture

Partition by:
- country
- or region

Options:
1. Single DB + partitioning  
2. Multi-DB per region (EU, US, etc.)

---

## API Design

- REST (FastAPI)

Future:
- GraphQL (optional)

---

## Frontend Architecture

- Next.js App Router
- Server Components for SEO pages
- Client components for interactions

---

## SEO Architecture (CRITICAL)

### URL Structure (ACTUAL)

- /{lang}/{city}/{category}
- /{lang}/{city}/{category}/{providerSlug}

Examples:
- /en/sofia/massage
- /en/sofia/massage/maria-petrova

---

### Strategy:
- programmatic SEO
- localized content (32 languages)
- SSR for indexing

---

## Monetization Strategy

Primary:
- pay-per-lead

Future:
- subscriptions (providers)
- featured listings
- ads

---

## What NOT to build early

❌ Booking system  
❌ Payments  
❌ Complex chat  
❌ Advanced reviews system  

---

## Future Extensions

- AI lead matching
- Auto-translation
- Smart pricing suggestions
- Provider ranking algorithm

---

## Embedded Lead Widget (CRITICAL GROWTH COMPONENT)

Nevumo предоставя **embeddable lead widget**, който providers могат да използват извън платформата.

---

### Purpose

- Capture leads извън Nevumo (external traffic)
- Increase provider adoption
- Enable viral growth via providers

---

### Entry Points

#### 1. Direct URL (Primary)

/{lang}/{city}/{category}/{providerSlug}

---

#### 2. Embeddable Widget (iframe / script)

Example:

<iframe src="https://nevumo.com/en/sofia/massage/maria-petrova" />

---

#### 3. QR Code (Offline → Online)

QR → opens provider lead page

Used for:
- business cards
- flyers
- physical locations

---

### Provider Ownership

Each provider има:

- unique public URL
- embeddable widget URL

This URL acts as:

- lead entry point
- tracking identifier
- provider funnel

This is a core part of provider acquisition strategy.

---

### UX Flow

1. User opens widget / page  
2. Sees provider info + trust signals  
3. Submits request  

→ lead is created  
→ assigned to provider  

---

### Lead Handling Logic

If lead is created via provider page:

- lead.provider_id = конкретния provider  
- НЕ се изпраща към други providers (default)

Optional (future):
- fallback matching ако provider не отговори  

---

### Data Tracking (IMPORTANT)

Track:

- source: seo | direct | widget | qr
- provider_id
- conversion rate per provider
- external vs internal traffic

---

### Technical Notes

- SSR (ultra-fast)
- mobile-first (QR usage)
- minimal friction (2 fields max)

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

## Key Principles

- Keep backend simple
- Optimize for SEO first
- Leads = core revenue
- Avoid over-engineering
- Build for scale, but start lean