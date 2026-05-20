# Nevumo Web Architecture

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
