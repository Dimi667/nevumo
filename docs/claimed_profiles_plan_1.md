# Nevumo — Claimed Profiles: Пълен план

**Статус:** 🟡 В процес — Задача 1Ж ✅, 1Ж-ext ✅, 2Б ✅, 3А ✅, 4А ✅ и 4А редизайн ✅ завършени
**Последна актуализация:** 17 юни 2026
**Приоритет:** 🔴 Висок — преди Warsaw outreach кампания

---

## Какво са Claimed Profiles

Невумо създава предварителни профили на доставчици от публично достъпни данни (CEIDG, Google Maps и др.) преди доставчикът да се е регистрирал сам. Доставчикът може да "поеме" (claim) профила си чрез верификационен процес.

**Правна основа:** Вече е документирана и внедрена:
- T&C за доставчици, Чл. 4.5 — Claimed Profiles клауза
- Privacy Policy, Чл. 3.7 — GDPR Art. 14 уведомление при claiming
- DB схема: `providers.is_claimed`, `providers.claim_token`, `providers.data_source`

---

## Конкурентен контекст

| Платформа | Тип | Модел | Релевантност |
|---|---|---|---|
| **Fixly.pl** | Marketplace (leads) | Pay-per-lead | 🔴 Директен конкурент — собственост на OLX Group |
| **Oferteo.pl** | Marketplace (leads) | Pay-per-lead | 🔴 Директен конкурент |
| **Oferia.com.pl** | Marketplace (leads) | Без комисиона | 🟡 Конкурент с различно позициониране |
| **Panoramafirm.pl** | Directory | Безплатен listing | 🟢 Не е конкурент — само source на данни |

**Ключов инсайт:** Fixly провайдърите вече плащат за leads и познават модела. Те са идеална целева група — разочаровани от pay-per-lead дори когато клиентът не е сериозен.

**Positioning на Nevumo:** *"Твоят профил е вече на Nevumo. Клиентите те намират директно — без да плащаш за всяко запитване."*

---

## Sources за данни

| Source | Тип | Данни | Статус |
|---|---|---|---|
| **CEIDG API (dane.biznes.gov.pl)** | Правителствен регистър | Пълни (тел, имейл, адрес) | 🟡 Скрипт върви |
| **Google Places API** | GMaps бизнеси | Добри (тел, сайт, рейтинг) | ⏳ Следваща стъпка |
| **Panoramafirm.pl** | Бизнес директория | Частични | ⏳ При нужда |

**PKD кодове по категория (CEIDG):**

| Категория Nevumo | PKD кодове |
|---|---|
| 🧹 Cleaning | `81.21.Z`, `81.22.Z`, `81.29.Z` |
| 💆 Massage | `96.04.Z`, `96.02.Z`, `86.90.A` |
| 🔧 Plumbing | `43.22.Z`, `43.21.Z` |

**Важно откритие:** CEIDG изисква `Województwo = "Mazowieckie"` + `Miejscowość = "Warszawa"` за да намери резултати. Само с Miejscowość връща 0 за някои PKD кодове.

---

## Скрипт за събиране на данни

**Файл:** `apps/scripts/collect_ceidg_providers.py`
**Runtime:** Python 3.13 + Playwright (Chromium)
**Output:** `apps/scripts/warszawa_providers_ceidg.csv`

**Колони в CSV:**
```
business_name, owner_name, address, phone, email, website, nip, pkd_code, category, source
```

**Стартиране:**
```bash
python3.13 apps/scripts/collect_ceidg_providers.py
```

**Статус на първо изпълнение (14 юни 2026):** 🟡 В процес
- 81.22.Z cleaning: 90 ✅
- 81.29.Z cleaning: 30 ✅
- 96.04.Z massage: 72 ✅
- 43.21.Z plumbing: 76 ✅
- Останалите PKD кодове: в процес с Province = Mazowieckie fix

---

## ПЪЛЕН ROADMAP — Задачи по ред

### 🟦 ФАЗА 1 — ДАННИ

**Цел: максимален брой имейли и телефони за outreach кампанията**

**Задача 1А — CEIDG скрипт** ✅ Завършена (14 юни 2026)
- Събрани: 2,375 уникални доставчика
- С имейл: 701 | С телефон: 257
- Файл: apps/scripts/warszawa_providers_ceidg.csv

**Задача 1Б — Преглед и почистване на CSV** ✅ Завършена (15 юни 2026)
- Скрипт: apps/scripts/clean_ceidg_csv.py
- Output: warszawa_providers_clean.csv (2,122 реда)
- Резултат: 633 валидни имейли, 230 валидни телефони (+48 формат)

**Задача 1В — CEIDG re-scrape за уебсайтове** ✅ Завършена (16 юни 2026)
- Output: apps/scripts/warszawa_providers_with_websites.csv (2,122 реда)
- Резултат: само 51 уебсайта от 2,122 фирми (2.4%) — CEIDG не публикува сайтове
- Технически бележки:
  * headless=False задължително (Akamai)
  * Label: "Adres strony internetowej"

**Задача 1Г — Email extractor от CEIDG уебсайтове** ❌ ПРОПУСНАТА
- Причина: само 51 уебсайта от CEIDG — не си струва усилието
- Решение: Panoramafirm дава директно имейлите (Task 1Е)

**Задача 1Д — SMS скрипт за телефоните** ⏳ Следваща
- 230 телефона от CEIDG → SMS чрез SMSapi.pl
- Цена: ~18 PLN (~4 EUR) за всички
- Съдържание: кратко съобщение на полски с claim линк
- Модел: Kimi-2.6

**Задача 1Е — Panoramafirm.pl scraper** ✅ Завършена (15-17 юни 2026)
- Оригиналният план за Fixly отхвърлен: no browsable directory, GraphQL само count
- Pivot: Panoramafirm.pl — реален business directory
- Скриптове:
  * apps/scripts/scrape_panoramafirm.py — scrape на листинг страници (Playwright)
  * apps/scripts/panoramafirm_requests_only.py — email enrichment (само requests)
- Output: apps/scripts/panoramafirm_emails_final.csv
- Резултат: 19,147 записа | 612 уникални имейла | 967 уебсайта
- Ключово откритие: имейлът е в data-popup-param-email атрибут в статичен HTML
  → не е нужен Playwright за профилните страници
- Разбивка по категория: plumbing 10,106 с имейл | cleaning 1,150 с имейл
- Технически бележки:
  * Playwright за листинг страници (h2 selector)
  * requests за профилни страници (10x по-бързо, без memory leak)
  * headless=True за листинг (не изисква Akamai обход)
  * Телефоните от Panoramafirm са call-tracking (224573095) — не се ползват
  * 233 уебсайта БЕЗ имейл → Task 1З

**Задача 1Ж — DuckDuckGo Website Finder** ✅ ЗАВЪРШЕНА (17 юни 2026)
- Script: apps/scripts/bing_website_finder.py
- Input: warszawa_providers_with_websites.csv (1,473 реда без email + без website)
- Намерени уебсайтове: 562 (38% success rate)
- Encoding fix: utf-8-sig (BOM)
- Blocklist: social media + directories + international TLDs
- Output: warszawa_providers_with_websites.csv (website колона обновена)
- Runtime: ~37 минути
- DuckDuckGo API (ddgs пакет) вместо Bing Search API (безплатно, не изисква key)

**Задача 1Ж-ext — Email Extractor CEIDG** ✅ ЗАВЪРШЕНА (17 юни 2026)
- Script: apps/scripts/extract_emails_ceidg.py
- Input: warszawa_providers_with_websites.csv (568 реда с website != "" AND email == "")
- Намерени имейли: 231 (40.7% success rate)
- Стратегия: homepage + /kontakt + /contact, https с http fallback
- Output: warszawa_providers_with_websites.csv (email колона обновена)
- CEIDG CSV финален резултат: 864 имейла | 613 уебсайта | 2,122 реда

**Задача 1З — Email extractor от Panoramafirm уебсайтове** ✅ Завършена (17 юни 2026)
- Script: apps/scripts/extract_emails_from_websites.py
- Input: panoramafirm_emails_final.csv (233 реда с website != "" AND email == "")
- Уникални домейни посетени: 308
- Нови имейла намерени: 160
- Success rate: 51.9%
- Стратегия: requests + BeautifulSoup, без Playwright
- Страници на домейн: homepage → /kontakt → /contact (спира при първи намерен имейл)
- Delay: 1.0s между домейни
- Cleanup: 10 мръсни имейла → 0 след двустъпков regex fix
- Output: panoramafirm_emails_final.csv (обновен in-place) + panoramafirm_1z_report.csv

**Задача 1И — Google Places API скрипт** ⏳ Опционална (платена)
- Търси: "sprzątanie Warszawa", "masażysta Warszawa", "hydraulik Warszawa"
- Цена: ~$10-15 за 300-500 резултата
- Потенциал: +200-500 нови фирми с телефони и уебсайтове
- Ползва се само ако 1Д+1Ж+1З не дадат достатъчно данни
- Модел: Kimi-2.6

**Задача 1К — Oferteo.pl scraper** ⏳ Нисък приоритет
- Втори marketplace след Fixly с публични профили
- Потенциал: нови фирми извън Panoramafirm
- Усилие: 2-3 дни за нов scraper
- Пуска се само ако всички останали задачи не дадат достатъчно данни
- Модел: SWE-1.6

**Текущ резултат от Фаза 1 (17 юни 2026):**

| Source | Имейли | Телефони | Уебсайтове |
|---|---|---|---|
| CEIDG (1А + 1В + 1Ж-ext) | 864 | 230 | 613 |
| Panoramafirm (1Е + 1З) | 772 уникални | — | 967 |
| **Общо досега** | **~1,636** | **230** | **~1,580** |
| След 1Д (SMS) | — | 230 SMS | — |
| След 1И (Google, опц.) | +200-300 | +200 | — |
| **Прогнозен краен** | **~1,800-2,000** | **~430+** | — |

При 8-15% конверсия = **144-300 claimed профила за Warsaw launch.**

---

### 🟩 ФАЗА 2 — BACKEND

**Задача 2А — `seed_unclaimed_providers.py`**
- Чете `warszawa_providers_ceidg.csv`
- Зарежда в `providers` таблицата с:
  - `is_claimed = FALSE`
  - `data_source = 'scraped'`
  - `user_id = NULL`
  - `claim_token = secrets.token_hex(32)` (автогенериран)
  - `slug` автогенериран от `business_name`
- Свързва с `provider_cities` (Warszawa) и `services` (категория)
- Идемпотентен: `ON CONFLICT (nip) DO NOTHING` или по slug
- **Модел: Kimi-2.6 (без reasoning)**

**Задача 2Б — Claim Backend Endpoint** ✅ ЗАВЪРШЕНА (14 юни 2026)
- GET /api/v1/providers/claim/{token} — публичен preview (без auth)
- POST /api/v1/providers/claim/{token} — клейм с JWT auth
- Проверява токена → is_claimed=FALSE → свързва user_id
- Изтрива draft provider row ако съществува (slug startswith "draft" AND business_name == user.email)
- is_claimed = TRUE, claim_token = NULL, verification_level рекалкулиран
- Art. 14 GDPR имейл изпратен автоматично (non-blocking)
- Имплементирано в: apps/api/routes/providers.py

---

### 🟨 ФАЗА 3 — ИМЕЙЛИ

**Задача 3А — Outreach имейл шаблон** ✅ ЗАВЪРШЕНА (14 юни 2026)
- Тема: "Twój profil jest już na Nevumo — odbierz go bezpłatnie"
- Файл: `apps/api/scripts/templates/outreach_email_pl.html`
- Jinja2 променливи: `{{ business_name }}`, `{{ claim_link }}`, `{{ provider_phone }}`, `{{ provider_email }}`, `{{ provider_address }}`, `{{ provider_website }}`
- Съдържа:
  - GDPR Art. 14 уведомление (CEIDG source, данни, права, mailto за изтриване)
  - FOMO блок: "Im wcześniej przejmiesz swój profil, tym wyżej pojawisz się w wynikach..."
  - Сравнение Nevumo vs Fixly (9 ползи vs 6 недостатъка)
  - 2 CTA бутона: "Odbierz swój profil →" и "Przejmij profil bezpłatnie →"
- Дизайн: бял хедър с лого PNG, оранжеви CTA (#F97316), светлосив футър — идентичен на сайта
- Лого: конвертирано от SVG → PNG (cairosvg), вградено като base64 за преглед; за продъкшън се качва на `images.nevumo.com/nevumo-logo.png`
- Sender: `Nevumo <support@nevumo.com>` via Resend
- Gravatar: настроен за `support@nevumo.com` с apple-touch-icon (120×120px) ✅
- **Subject lines (първа порция — за A/B тест и конвършън мониторинг):**
  - plumbing: `10 707 firm instalacyjnych w Warszawie — czy Twoi klienci Cię znajdą?` 
  - cleaning: `7 363 firm sprzątających w Warszawie — czy Twoi klienci Cię znajdą?` 
  - massage: `3 635 gabinetów masażu w Warszawie — czy Twoi klienci Cię znajdą?` 
  - Числата са от официален CEIDG регистър (PKD: 43.22.Z, 81.21.Z, 96.04.Z), верифицирани юни 2026
  - Маппингът category → subject се имплементира в скрипта в Задача 5А
  - ⚠️ При конвършън под 5% след първата порция — смени subject lines и тествай нов вариант

**Задача 3Б — Art. 14 Confirmation имейл**
- Изпраща се АВТОМАТИЧНО след успешен claim
- Съдържа: "Данните, които обработвахме преди: [name, phone, website]. Вече контролираш профила си напълно."
- **Аз (Claude) пиша шаблона**

---

### 🟧 ФАЗА 4 — FRONTEND

**Задача 4А — `/[lang]/claim/[token]` страница** ✅ ЗАВЪРШЕНА (16 юни 2026)
- Показва профила (само за четене): name, category, city
- CTA: "Твой ли е този профил? Вземи го безплатно →"
- При клик → регистрация/вход → профилът е твой
- Redirect към Provider Dashboard след успех
- Welcome email при успешен claim (send_claim_welcome_email, non-blocking)
- Translations: namespace 'claim', 12 ключа, 34 езика, 408 превода
- E2E тестове: ✅ всички 3 теста преминаха успешно
- Fix: claim page обновен да работи с директен API response format (commit 67ccc5a)
- Файлове: apps/web/app/[lang]/claim/[token]/page.tsx, apps/api/routes/providers.py, apps/api/services/email_service.py

**Редизайн (16 юни 2026) ✅**
- Висококонверсионен дизайн: urgency bar, leads teaser, benefits grid, Fixly comparison, social proof
- Social proof: 3-фазна логика (zero/few/many) с {city} и {count} параметри
- city_name локализиран от location_translations (не city_slug)
- claimed_count от API за динамичен social proof
- 1,190 нови превода: seed_claim_v2_p1.py + seed_claim_v2_p2.py (34 езика × 35 ключа)
- E2E тестове: ✅ 4/4 минаха включително PL локализация
E2E тест June 17, 2026 (production):
- valid state: ✅ PASS
- not_found state: ✅ PASS
- already_claimed state: ❌ FAIL — backend бъг (виж bugs backlog в architecture.md)

Bugs backlog преди Task 5A:
🔴 already_claimed endpoint fix (apps/api/routes/providers.py)
🔴 Outreach email Jinja2 rendering (bulk script Task 5A)
🟡 Двойно "Nevumo" на claim страницата
🟡 CTA above the fold на мобилен
✅ Email лого на R2 — COMPLETE (June 18, 2026)
✅ Email subject lines — COMPLETE (June 18, 2026): category-based, под 50 символа, реални keyword данни

**Задача 4Б — "Unclaimed" банер на Provider Full Page**
- Видим само за некредентовани профили (`is_claimed = FALSE`)
- Текст: "Собственик ли сте на тази фирма? [Вземете профила безплатно →]"
- Линк към `/[lang]/claim/[token]`
- **Модел: Kimi-2.6**

---

### 🟥 ФАЗА 5 — OUTREACH

**Задача 5А — Bulk имейл кампания**
- Изпраща outreach имейла до всички доставчици с имейл в CSV
- Чрез Resend (вече интегриран в Nevumo)
- Python скрипт: чете CSV → изпраща → логва статус
- Rate limit: max 100 имейла/час (Resend free tier)
- **Модел: Kimi-2.6 за скрипта**

**Задача 5Б — SMS кампания** *(опционална)*
- За доставчици без имейл, само с телефон
- SMSapi.pl — ~0.07 PLN/SMS (~3 EUR за 200 SMS)
- Кратко съобщение на полски с линк към claim страницата

---

### 🔵 ФАЗА 6 — МОНИТОРИНГ

**Задача 6А — Tracking в Provider Dashboard (Admin)**
- Страница показваща: общо unclaimed профили, claimed тази седмица, % conversion
- **Приоритет: нисък — след launch**

---

## Технически детайли (вече в DB)

```sql
-- providers таблица (вече съществува)
is_claimed BOOLEAN NOT NULL DEFAULT TRUE  -- FALSE за unclaimed
claim_token TEXT UNIQUE                    -- магически токен
data_source TEXT NOT NULL DEFAULT 'manual' -- 'scraped' за CEIDG данни
user_id UUID REFERENCES users(id)          -- NULL за unclaimed

-- Индекси (вече съществуват)
CREATE INDEX idx_providers_is_claimed ON providers(is_claimed);
CREATE UNIQUE INDEX idx_providers_claim_token ON providers(claim_token);
```

---

## Целеви числа

| Метрика | Цел |
|---|---|
| Провайдъри в CSV | 500+ |
| Провайдъри с имейл | 200+ |
| Провайдъри с телефон | 400+ |
| Claimed след 1 месец outreach | 20-50 (10-25%) |

---

## Зависимости и рискове

**Рискове:**
- CEIDG може да промени HTML структурата → скриптът спира (нисък риск)
- Доставчици без имейл → само SMS или без outreach
- Claim conversion rate може да е нисък → A/B тест на съобщенията

**Зависимости:**
- Фаза 2 изисква финален CSV от Фаза 1
- Фаза 3 имейли се пишат паралелно с Фаза 2
- Фаза 4 frontend изисква Фаза 2Б backend endpoint
- Фаза 5 outreach изисква всичко от Фази 1-4

---

## Следваща незабавна стъпка (17 юни 2026)

**Приоритетен ред:**
1. Задача 1Д — SMS кампания 230 телефона (Kimi-2.6 + SMSapi.pl, ~4 EUR) ← СЛЕДВАЩА
2. Задача 1Ж — Bing Search API за фирми без уебсайт (Kimi-2.6, безплатно)
3. Задача 1И — Google Places API (Kimi-2.6, ~$10-15, при нужда)
4. Задача 1К — Oferteo.pl scraper (SWE-1.6, нисък приоритет)

**Паралелно (не чака данните):**
- Задача 2А — seed_unclaimed_providers.py (Kimi-2.6) — зарежда вече събраните данни
- Задача 4А — /[lang]/claim/[token] страница (Kimi-2.6) — translations seed готов
- Задача 4Б — Unclaimed банер (Kimi-2.6)
- Задача 3Б — Art. 14 Confirmation имейл (Claude)
