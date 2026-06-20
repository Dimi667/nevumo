# Nevumo Web Architecture

**%26 URL Fix (June 2026)** — COMPLETE:
- Problem: URLs like /bg/%26/masaz returned HTTP 200, causing Google to index "%26" in page titles
- Root cause: Next.js [city] route accepted any URL-encoded value without decoding or validation
- Fix: Added decodeURIComponent(params.city) + notFound() guard in apps/web/app/[lang]/[city]/page.tsx and apps/web/app/[lang]/[city]/[category]/page.tsx
- Result: Invalid city slugs now return HTTP 404; valid pages unaffected

---

**PWA Library Migration (June 11, 2026)** — COMPLETE:
- **Problem**: Both next-pwa v5 and @ducanh2912/next-pwa v10 incompatible with Turbopack — both rely on Webpack plugin to generate sw.js. turbopack:{} in next.config.mjs prevents Webpack from running → sw.js never generated in production.
- **Solution**: Removed all PWA libraries. Static sw.js created directly in apps/web/public/sw.js.
- **Architecture**: Zero external PWA dependencies.
  - apps/web/public/sw.js — static base Service Worker (install/activate/fetch handlers)
  - apps/web/worker/index.js — push/notificationclick handlers (unchanged)
  - apps/web/scripts/append-sw-handlers.js — postbuild appends worker/index.js into sw.js (unchanged)
  - apps/web/components/sw/ServiceWorkerRegistration.tsx — registers /sw.js (unchanged)
- **Build flow**: next build → postbuild appends push handlers → [NEVUMO-CUSTOM-SW] marker in sw.js → Vercel serves static sw.js
- **Files changed**:
  - apps/web/package.json — removed next-pwa and @ducanh2912/next-pwa
  - apps/web/next.config.mjs — removed withPWA wrapper, plain nextConfig
  - apps/web/public/sw.js — new static base Service Worker
- **Key rule**: sw.js is a static committed file in git. The postbuild script appends push handlers idempotently on every build using the [NEVUMO-CUSTOM-SW] marker.

---

## Slug Validation Mechanism (May 2026)

**Проблем:** Хардкоднати грешни slug-ове във frontend файлове (`warsaw` вместо `warszawa`, `hydraulik` вместо `plumbing`).

**Решение:** Централен валидатор `apps/web/lib/slugs.ts`:
- `getValidCitySlugs()` — зарежда валидни city slug-ове от `GET /api/v1/cities/active` 
- `getValidCategorySlugs()` — зарежда валидни category slug-ове от `GET /api/v1/categories` 
- `validateCitySlug(slug)` — валидира city slug; хвърля Error в dev, логва warning в prod
- `validateCategorySlug(slug)` — валидира category slug; хвърля Error в dev, логва warning в prod

**Single source of truth:** DB е единственият авторитет за валидни slug-ове. Frontend никога не хардкодва slug-ове.

**Засегнати файлове:**
- `apps/web/lib/slugs.ts` — нов файл
- `apps/web/lib/default-city.ts` — всички return-и минават през `validateCitySlug()` 
- `apps/web/components/homepage/Footer.tsx` — category slug-ове коригирани към DB стойности
- `apps/web/app/[lang]/dolacz/page.tsx` — city/category slug коригиран

**Правило:** При добавяне на нов град или категория — само DB seed, нула code changes.
