# Nevumo — План за имплементация: Provider Full Page + Gallery + Badge система

**Версия:** 1.0  
**Дата:** 2026-05-21  
**Статус:** Одобрен за имплементация  

---

## Контекст и цел

Страницата на доставчик (`/[lang]/[city]/[category]/[provider-slug]`) в момента използва `ProviderWidget` компонента и за пълната страница, и за embed виджета. Това е правилно за мобилен изглед и embed, но на десктоп страницата изглежда като тесен мобилен елемент и пропуска огромен потенциал за конверсия.

Целта на тази задача е:
1. Създаване на нов `ProviderFullPage` компонент за десктоп — двуколонен layout с висока конверсия
2. Имплементиране на multi-image галерия за доставчици
3. Автоматизирана система за badge-ове (Нов / Верифициран / Топ специалист)
4. Актуализиране на социалното доказателство с пълна fallback логика

**Embed виджетът (`?embed=1`) остава непроменен.**

---

## Дизайн решения (одобрени)

### Layout — десктоп

Двуколонен layout:
- **Лява колона (fluid):** Hero → Галерия → За специалиста → Услуги и цени → Ревюта
- **Дясна колона (340px, sticky):** Форма за заявка с чипсове за избор на услуга

На мобилен (`< md`) — едноколонен layout, sticky панелът пада под съдържанието.

### Sticky панел — форма за заявка

Структура отгоре надолу:
1. Заглавие: "Изпратете заявка на [Име]" + "Безплатно • Без ангажимент"
2. Чипсове за избор на услуга (от provider.services) — всеки чип показва
   името на услугата + форматирана цена според service.price_type:
   - fixed:    „Релакс масаж  80 PLN"
   - hourly:   „Спортен масаж  60 PLN/час"
   - per_sqm:  „Основно почистване  12 PLN/кв.м"
   - request:  „Дълбока тъкан  по договаряне"
   - null base_price: третира се като request
   Цената се взема от service.base_price. Валутата от service.currency.
   Единиците „/час" и „/кв.м" се взимат от translation keys — не се хардкодват.
3. Поле за телефон
4. Поле за бележки
5. Сигнал за доверие (виж Зона 3 по-долу)
6. Бутон "Заявете услуга" — **единственият оранжев елемент на страницата**
7. Trust row: Верифициран • Без такса • Директен контакт

### Корица (cover)

- **Без галерия:** Бял фон — чисто, неутрално
- **С галерия:** Първата снимка от галерията автоматично се използва като корица

### Service карти — интерактивност (одобрено и изпълнено)

**Desktop:**
- Hover → оранжев border + появяващ се бутон „Заяви услуга"
- Click (карта или бутон) → scroll to sticky panel + активира съответния чип + pre-fill textarea

**Mobile:**
- Цялата карта е tappable
- Тънък оранжев border по default (винаги видим)
- Под цената: малък текст „Избери тази услуга →" (винаги видим)
- Tap → scroll to sticky panel + активира чип + pre-fill textarea

### Чипсове — toggle логика (одобрено и изпълнено)

- Click неактивен чип → активира се (оранжев)
- Click активен чип → деактивира се визуално (сивее), textarea НЕ се изчиства
- Синхрон: кликната карта → съответният чип автоматично се активира

---

## Badge система (одобрена)

### Три нива

| Ниво | Условие | Badge | Цвят |
|------|---------|-------|------|
| **Нов** | 0 завършени заявки ИЛИ непопълнен профил | ⚡ Нов в Nevumo — отговаря бързо | Amber |
| **Верифициран** | 1+ завършена заявка + снимка + описание + поне 1 услуга | ✓ Верифициран специалист | Зелен |
| **Топ специалист** | 10+ завършени заявки + среден рейтинг ≥ 4.5 | ★ Топ специалист в [град] | Златен |

### Правила

- Badge-овете се изчисляват **автоматично** от backend-а при всяка промяна на `jobs_completed`, `rating`, или профилните данни
- Съхранява се в нова колона `verification_level` в `providers` таблицата (0, 1, 2)
- "Отговаря до 30 мин." badge се показва само при Ниво 1 (Верифициран)
- При Ниво 0 (Нов) — "Отговаря до 30 мин." се скрива, amber badge го замества
- При Ниво 2 (Топ) — "Отговаря до 30 мин." се скрива, златен badge го замества
- "Топ специалист в [град]" използва града от текущия URL контекст

### Логика за изчисляване (backend)

```python
def calculate_verification_level(provider) -> int:
    profile_complete = (
        provider.image_url is not None and
        provider.description is not None and
        len(provider.description) > 0 and
        len(provider.services) >= 1
    )
    if provider.jobs_completed >= 10 and provider.rating >= 4.5:
        return 2  # Топ специалист
    if provider.jobs_completed >= 1 and profile_complete:
        return 1  # Верифициран
    return 0  # Нов
```

Функцията се извиква при:
- `PATCH /api/v1/provider/profile` (промяна на профил)
- `POST /api/v1/provider/services` (добавяне на услуга)
- `PATCH /api/v1/provider/leads/{id}` когато status → `done`

---

## Система за социално доказателство (5 зони)

### Зона 1 — Hero метрики

Показват се само ако стойността е > 0:

```
jobs_completed > 0  → "[N] Завършени услуги"
services.length > 0 → "[N] Услуги"           (винаги видимо)
cities.length > 0   → "[N] Града"            (винаги видимо)
rating > 0          → "[X.X] ★ ([N] ревюта)"  (само ако има ревюта)
```

Никога не показваме "0" за метрика.

### Зона 2 — Badge

Виж Badge система по-горе. Взаимно изключващо се с "Отговаря до 30 мин."

### Зона 3 — Sticky панел сигнал за доверие

Каскадна логика — показва се само първото изпълнено условие:

```
1. review_count > 0 AND latest_review != null
   → Последно ревю: "★★★★★ „[preview текст]" — [Клиент И.]"

2. review_count = 0 AND jobs_completed > 0
   → "✓ [N] завършени услуги"

3. review_count = 0 AND jobs_completed = 0 AND city_leads > 0
   → "[N] заявки за [категория] в [град] тази година"

4. review_count = 0 AND jobs_completed = 0 AND city_leads = 0
   AND leads_received > 0 AND latest_lead_preview != null
   → "[Клиент] от [Град] поръча наскоро"

5. Fallback (нов доставчик, нищо няма)
   → Checklist: "Безплатна заявка • Без ангажимент • Директен контакт"
```

### Зона 4 — Reviews секция (вляво)

```
review_count > 0  → Пълна секция: рейтинг overview + rating bars + карти с ревюта
review_count = 0  → Секцията се скрива изцяло
```

### Зона 5 — Галерия секция (вляво)

```
images.length > 0  → Галерия секция се показва (grid 4 колони, главна снимка 2x2)
images.length = 0  → Секцията се скрива изцяло
```

---

## Декомпозиция на задачите

### Задача A — Backend: Badge логика + DB migration
**Модел:** SWE-1.6  
**Зависимости:** няма  

**Scope:**
- Alembic migration: добавя `verification_level INT DEFAULT 0` в `providers` таблицата
- Функция `calculate_verification_level(provider)` в `provider_service.py`
- Извикване на функцията при: `PATCH /profile`, `POST /services`, `PATCH /leads/{id}` (status=done)
- `GET /api/v1/providers/{slug}` — добавя `verification_level` в публичния response
- Backfill скрипт: изчислява `verification_level` за всички съществуващи доставчици

**Нови translation keys (namespace: `widget`):**
```
badge_new_provider        → "Нов в Nevumo — отговаря бързо"
badge_verified            → "Верифициран специалист"
badge_top_specialist      → "Топ специалист в {city}"
```

---

### Задача B — Backend: Multi-image галерия
**Модел:** SWE-1.6  
**Зависимости:** Задача A (паралелно е възможно)  

**Нова таблица `provider_images`:**
```sql
CREATE TABLE provider_images (
    id          SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    url         TEXT NOT NULL,
    position    INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_provider_images_provider_id ON provider_images(provider_id);
```

**Нови endpoints (всички под `/api/v1/provider/`, JWT required):**

| Method | Path | Purpose |
|--------|------|---------|
| GET | /images | Списък на снимките на доставчика |
| POST | /images | Качване на нова снимка (multipart, max 5MB, max 8 снимки) |
| DELETE | /images/{id} | Изтриване на снимка |
| PATCH | /images/reorder | Пренареждане (масив от {id, position}) |

**Правила:**
- Максимум 8 снимки на доставчик
- Същият pipeline като съществуващия: HEIC→WebP, max 1200px, 85% качество
- Storage: `uploads/provider_gallery/{provider_id}/{image_id}.webp`
- Позиция 0 = корица (използва се в hero на FullPage)
- `GET /api/v1/providers/{slug}` — добавя `gallery: [{id, url, position}]` в публичния response

---

### Задача C — Frontend: Provider Dashboard — Gallery UI
**Модел:** Kimi-2.6  
**Зависимости:** Задача B  

**Scope:**
- Нова секция в `apps/web/app/[lang]/provider/dashboard/profile/page.tsx`
- Grid от снимки с drag-and-drop пренареждане
- Upload зона (drag-drop или click-to-select, multiple files)
- Preview преди качване
- Бутон за изтриване с confirmation
- Индикатор "Снимка 1 = корица на вашата публична страница"
- Лимит индикатор: "3/8 снимки качени"

**Нови translation keys (namespace: `provider_dashboard`):**
```
gallery_section_title     → "Галерия"
gallery_upload_hint       → "Първата снимка се показва като корица на вашата страница"
gallery_limit             → "{count}/8 снимки"
gallery_add_photos        → "Добавете снимки"
gallery_delete_confirm    → "Изтриване на снимката?"
gallery_cover_label       → "Корица"
gallery_drag_hint         → "Плъзнете за пренареждане"
```

---

### Задача D — Frontend: ProviderFullPage компонент
**Модел:** Kimi-2.6  
**Зависимости:** Задача A, Задача B  

**Нов файл:** `apps/web/components/provider/ProviderFullPage.tsx`

**Структура:**
```
ProviderFullPage
├── Breadcrumb (Варшава › Масаж › [Име])
├── Two-column grid (desktop) / single column (mobile)
│   ├── LEFT COLUMN
│   │   ├── HeroSection
│   │   │   ├── CoverImage (gallery[0] или бял фон)
│   │   │   ├── Avatar
│   │   │   ├── Name + Category + City
│   │   │   ├── BadgeRow (verification_level based)
│   │   │   ├── RatingRow (само ако rating > 0)
│   │   │   ├── MetaRow (jobs, services, cities, rating)
│   │   │   └── ActionRow (Сподели, QR код)
│   │   ├── GallerySection (само ако gallery.length > 0)
│   │   ├── AboutSection
│   │   ├── ServicesSection (информационни карти)
│   │   └── ReviewsSection (само ако review_count > 0)
│   └── RIGHT COLUMN (sticky)
│       └── LeadPanel
│           ├── Header (Изпратете заявка на [Име])
│           ├── ServiceChips (от provider.services)
│           ├── PhoneField
│           ├── NotesField
│           ├── SocialProofSignal (Зона 3 каскада)
│           ├── CTAButton (ЕДИНСТВЕНОТО оранжево)
│           └── TrustRow
```

**Условен render в `page.tsx`:**
```typescript
// apps/web/app/[lang]/[city]/[category]/[providerPage]/page.tsx
const isEmbed = searchParams.embed === '1';

return isEmbed
  ? <ProviderWidget provider={provider} translations={t} lang={lang} />
  : <ProviderFullPage provider={provider} translations={t} lang={lang} />;
```

**Нови translation keys (namespace: `provider_page`):**
```
section_gallery           → "Галерия"
section_about             → "За специалиста"
section_services          → "Услуги и цени"
section_reviews           → "Ревюта"
read_more                 → "Прочети повече"
select_service            → "Изберете услуга"
or_general_request        → "Или изпратете обща заявка ↓"
service_selected          → "Избрано: {service}"
share_button              → "Сподели"
completed_jobs            → "{count} Завършени услуги"
meta_services             → "Услуги"
meta_cities               → "Града"
meta_response_rate        → "Отговор"
reviews_count             → "Ревюта ({count})"
link_copied               → "Линкът е копиран!"
```

---

### ✅ Задача E — ShareButton интеграция → COMPLETE (May 22, 2026)
**Модел:** Kimi-2.6  
**Зависимости:** няма  

**Нов файл:** `apps/web/components/shared/ShareButton.tsx`

**Логика:**
- Mobile: Web Share API (`navigator.share`) → нативен share sheet
- Desktop: копира URL в клипборда → toast "Линкът е копиран!"
- GDPR-friendly: никакви social media tracker-и, никакви external scripts
- Използва се на: Provider page (ProviderFullPage), Category page (опционално)

**Implementation details:**
- ShareButton добавен в HeroSection ActionRow в ProviderFullPage.tsx
- Fallback fix: navigator.clipboard → document.execCommand за HTTP контексти
- Translation keys: share_button, link_copied (вече заредени)

---

### Задача F — Seed scripts: нови translation keys
**Модел:** Kimi-2.6  
**Зависимости:** Задача D, Задача C  

**Три отделни seed скрипта** (по namespace):
- `apps/api/scripts/seed_provider_page_translations.py` — namespace `provider_page`
- `apps/api/scripts/seed_provider_gallery_translations.py` — namespace `provider_dashboard` (gallery keys)
- `apps/api/scripts/seed_badge_translations.py` — namespace `widget` (badge keys)

Всеки скрипт: 34 езика × N ключа, `ON CONFLICT DO UPDATE`.

---

### Задача G — Документация update
**Модел:** Phoenix (read) → Claude (пише)  
**Зависимости:** след Задача A-F  

Обновяват се:
- `nevumo_master_context.md` — нова секция за Badge система и ProviderFullPage
- `ARCHITECTURE.md` — нови компоненти, нови endpoints, нова таблица
- `db_schema.md` — `provider_images` таблица, `verification_level` колона

---

## Ред на изпълнение

```
Задача A (Backend: Badge)
    ↓
Задача B (Backend: Gallery)     ← паралелно с A е OK
    ↓
Задача C (Dashboard Gallery UI)
    ↓
Задача D (ProviderFullPage)
    ↓
Задача E (ShareButton)          ← паралелно с D е OK
    ↓
Задача F (Seed scripts)
    ↓
Задача G (Документация)
```

---

## Правни документи — необходими обновления

### 1. Условия за доставчици (`terms_conditions_providers_nevumo.md`)

Добавя се нова секция **"Badge система и верификационни нива"** в трите езика (EN, PL, BG):

**Съдържание:**

> **Provider Status Badges**
>
> Nevumo automatically assigns status badges to Provider profiles based on objective, measurable criteria. Badges are calculated automatically by the Platform and updated in real time.
>
> **New Provider** (⚡): Displayed when the Provider has not yet completed their first service request via the Platform. This badge is replaced automatically once the verification criteria below are met.
>
> **Verified Specialist** (✓): Awarded automatically when all of the following conditions are met:
> - At least 1 service request completed via the Platform (status: done);
> - A profile photo uploaded;
> - A profile description filled in;
> - At least 1 active service listing.
>
> **Top Specialist** (★): Awarded automatically when all of the following conditions are met:
> - At least 10 service requests completed via the Platform;
> - Average client rating of 4.5 or above (minimum 1 review required).
>
> The "Top Specialist" badge includes the name of the city in which the Provider is active.
>
> Nevumo reserves the right to modify badge criteria upon 15 days' prior notice. Badge downgrades may occur automatically if the underlying criteria cease to be met (e.g. average rating falls below 4.5). Providers may not purchase, transfer, or otherwise artificially obtain a badge. Any attempt to manipulate badge criteria constitutes a material breach of these Terms and may result in account suspension.

### 2. Privacy Policy (`privacy_policy_nevumo_FINAL.md`)

Добавя се кратка бележка в секцията за обработка на данни:

> **Provider performance data:** Nevumo automatically calculates and stores aggregated performance indicators (completed jobs count, average rating, verification level) based on platform activity. These indicators are used to determine the Provider's public status badge and are visible to Clients on the Provider's public profile.

### 3. Кой обновява документите

- Правният текст на EN, PL, BG за badge секцията — **Claude генерира**, Димитров преглежда
- Seed скриптове за новите текстове в Terms — **отделна задача след одобрение на правния текст**

---

## Технически бележки

- `ProviderFullPage` е Server Component с `generateStaticParams` за всички 34 езика
- Embed виджетът (`?embed=1`) ползва `ProviderWidget` — **без промени**
- Mobile responsive: под `md` breakpoint — едноколонен layout, sticky панелът пада под
- `verification_level` се добавя към съществуващия публичен provider response — **не е breaking change**
- Gallery images се сервират от FastAPI StaticFiles: `uploads/provider_gallery/{provider_id}/{id}.webp`
- ShareButton използва само Web APIs — без external dependencies

---

## Отворени въпроси (за решаване преди имплементация)

1. **Mobile sticky CTA** — на мобилен трябва ли да имаме плаващ оранжев бутон "Заявете услуга" (като на Category страницата) или sticky панелът пада просто в края?
2. **Максимален брой снимки** — одобрен лимит от 8. Ок ли е?
3. **Badge downgrade** — ако доставчик падне под критериите за Топ (рейтингът спадне под 4.5) — автоматично се сваля ли badge-ът? Предлагаме да — да се запише в правилата.

---

## Обновления на плана (v1.1 — 2026-05-21)

### Решени отворени въпроси

**1. Mobile sticky CTA — решено**

Имплементираме плаващ фиксиран бутон в долната част на екрана на мобилен — същият модел като Category страницата (`StickyLeadFormButton`).

- Видимост: само на мобилен (`md:hidden`)
- Показва се когато формата НЕ е в viewport (above OR below)
- При натискане: smooth scroll до формата
- Скрива се когато потребителят вижда формата (за да не се дублира)
- Нов компонент: `apps/web/components/provider/StickyProviderCTA.tsx`

**2. Badge downgrade — решено и записано в правилата**

Badge-ът се сваля автоматично ако условията престанат да бъдат изпълнени:

- Топ → Верифициран: ако `jobs_completed` падне под 10 ИЛИ `rating` падне под 4.5
- Верифициран → Нов: ако профилът стане непълен (изтрита снимка, изтрити всички услуги)

`calculate_verification_level()` се извиква при ВСЯКА промяна — не само при нагоре, но и при надолу. `verification_level` се обновява в реално време.

Записано в правния текст: *"Badge downgrades occur automatically and in real time if the underlying criteria cease to be met."*

---

### Нови задачи добавени към плана

**Задача H — Правен текст: Badge система**
**Модел:** Claude генерира → Димитров одобрява → Kimi-2.6 seed скрипт

Отделен документ с пълния правен текст на трите езика (EN, PL, BG):
- Нова секция в `terms_conditions_providers_nevumo.md`: "Provider Status Badges"
- Кратка добавка в `privacy_policy_nevumo_FINAL.md`: обработка на performance data
- След одобрение: seed скрипт за translations таблицата ако текстът се показва в UI

**Задача I — Category page: Badge актуализация**
**Модел:** Kimi-2.6  
**Зависимости:** Задача A (Badge логика в backend)

При имплементацията на badge системата трябва да се прегледат и обновят всички места където badge-ът се показва извън ProviderFullPage:

- `apps/web/app/[lang]/[city]/[category]/page.tsx` — Provider cards в листинга
- `apps/web/components/category/ProviderCard.tsx` (или еквивалент) — badge rendering
- Проверка: показва ли се сега `is_verified` или hardcoded текст?
- Обновяване спрямо новата `verification_level` логика (0/1/2)
- Amber badge за Нов, зелен за Верифициран, златен за Топ — навсякъде консистентно

**Задача J — Mobile Sticky CTA за Provider страница — COMPLETE (May 22, 2026)**
**Модел:** Kimi-2.6  
**Зависимости:** Задача D (ProviderFullPage)

- Нов компонент `apps/web/components/provider/StickyProviderCTA.tsx`
- Логика идентична с `StickyLeadFormButton` от Category страницата (md:hidden, isFormInView, paddingBottom)
- Target: `id="provider-lead-form"` на формата в sticky панела
- Translation key: `provider_page.cta_button` (namespace: provider_page)
- Seed скрипт: apps/api/scripts/seed_provider_cta_button.py (34 езика)
- Изтрити грешно въведени zh преводи (24 реда)
- Bugs fixed по време на имплементацията:
  - ProviderFullPage не зареждаше provider_page namespace (translations={} → translations={providerPageT})
  - t['provider_page.KEY'] → t['KEY'] в ProviderFullPage.tsx и LeadPanel.tsx (18 замени)

---

### Актуализиран ред на изпълнение

```
Задача A  Backend: Badge логика + DB migration
    │
    ├──► Задача B  Backend: Multi-image галерия (паралелно)
    │        │
    │        └──► Задача C  Dashboard Gallery UI
    │
    └──► Задача I  Category page badge актуализация (след A)
    │
    ↓
Задача D  ProviderFullPage компонент
    │
    ├──► Задача E  ShareButton (паралелно)
    ├──► Задача J  Mobile Sticky CTA (паралелно)
    │
    ↓
Задача F  Seed scripts (всички нови translation keys)
    │
    ├──► Задача H  Правен текст: Badge система (паралелно)
    │
    ↓
Задача G  Документация update (nevumo_master_context, ARCHITECTURE, db_schema)
```

