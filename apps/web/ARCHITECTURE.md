# Nevumo Web Architecture

**PWA Library Migration (June 11, 2026)** — COMPLETE:
- **Problem**: next-pwa v5 incompatible with Turbopack — `customWorkerDir` triggers webpack pipeline which does not run under Turbopack → `sw.js` not generated → push handlers not appended → push notifications silently broken in production.
- **Solution**: Migrated from `next-pwa` ^5.6.0 to `@ducanh2912/next-pwa` ^10.2.9 (Turbopack-compatible fork).
- **Files changed**:
  - `apps/web/package.json` — removed `next-pwa` from devDependencies, added `@ducanh2912/next-pwa` to dependencies
  - `apps/web/next.config.mjs` — updated import and config: removed `customWorkerDir`, `skipWaiting`, `register: true`; added `register: false`, `reloadOnOnline: true`, `cacheOnFrontEndNav: true`
  - root `.gitignore` — removed `apps/web/public/sw.js` (line 70)
- **Unchanged (intentionally preserved)**:
  - `apps/web/worker/index.js` — push/notificationclick handlers
  - `apps/web/scripts/append-sw-handlers.js` — postbuild script with `[NEVUMO-CUSTOM-SW]` marker
  - `apps/web/package.json` postbuild hook — `"postbuild": "node scripts/append-sw-handlers.js"`
  - `apps/web/components/sw/ServiceWorkerRegistration.tsx` — manual SW registration
- **Build flow**: `next build` → @ducanh2912/next-pwa generates `sw.js` in `public/` (Turbopack-compatible) → `postbuild` appends push handlers → Vercel serves `sw.js` with `[NEVUMO-CUSTOM-SW]` section.
- **Key rule**: `register: false` in withPWA config because `ServiceWorkerRegistration.tsx` handles registration manually.

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
