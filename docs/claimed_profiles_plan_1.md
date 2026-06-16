# Nevumo — Claimed Profiles: Пълен план

**Статус:** 🟡 В процес — Задача 2Б ✅, 3А ✅ и 4А ✅ завършени
**Последна актуализация:** 16 юни 2026
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

**Цел: 3,000+ имейла и 750+ телефона за outreach кампанията**

**Задача 1А — CEIDG скрипт** ✅ Завършена
- Събрани: 2,375 уникални доставчика
- С имейл: 701 | С телефон: 257
- Файл: apps/scripts/warszawa_providers_ceidg.csv

**Задача 1Б — Преглед и почистване на CSV** ✅ Завършена (15 юни 2026)
- Скрипт: apps/scripts/clean_ceidg_csv.py
- Input: warszawa_providers_ceidg.csv (2,375 реда)
- Output: warszawa_providers_clean.csv (2,122 реда)
- Резултат: 633 валидни имейли, 230 валидни телефони (+48 формат)
- Открит проблем: колона "address" съдържа имейли вместо физически адреси
  (скраперът е записал email и в address полето) — при seed скрипта (2А)
  address колоната се зарежда като ПРАЗНА
- Открит проблем: 176 реда с партньорски бизнес имена ("1. FIRM A, 2. FIRM B
  wspólnik s.c.") — seed скриптът (2А) взема само първото име преди запетаята

**Задача 1В — CEIDG re-scrape за уебсайтове** ✅ Завършена (16 юни 2026)
- Скрипт: apps/scripts/rescrape_websites.py (Python 3.13, sync Playwright)
- Изпълнен: 16 юни 2026
- Input: apps/scripts/warszawa_providers_clean.csv (2,122 реда)
- Output: apps/scripts/warszawa_providers_with_websites.csv
- Резултат: 51 уебсайта намерени от 2,122 реда (2.4%)
- Бележка: Повечето малки полски фирми не попълват уебсайт в CEIDG.
  Останалите 2,071 без уебсайт ще се обработят в Задача 1Ж (Bing API)
- Технически бележки (критично за бъдещи CEIDG скриптове):
  * CEIDG API (dane.biznes.gov.pl) — мъртво, връща 404
  * Директен URL по NIP не работи
  * Търсенето изисква NIP (#MainContentForm_txtNip) + PKD (#MainContentForm_txtPkd)
  * Бутон: #MainContentForm_btnInputSearch
  * headless=False задължително — Akamai CDN блокира headless Chromium
  * Label за уебсайт: "Adres strony internetowej" (НЕ "Strona" — CEIDG го е сменил)
  * Selector за резултати: a[href*='SearchDetails.aspx']
  * Selector за полета: section.block → dt/dd двойки
  * sync_playwright, viewport 1920x1080, реален Chrome UA

**Задача 1Г — Email extractor от уебсайтове**
- Playwright скрипт посещава всеки уебсайт от 1В
- Търси `mailto:` линкове и `contact@` адреси
- Очаквано: +200-400 нови имейла
- Модел: Kimi-2.6

**Задача 1Д — SMS скрипт за телефоните**
- 257 телефона от CEIDG → SMS чрез SMSapi.pl
- Цена: ~18 PLN (~4 EUR) за всички
- Съдържание: кратко съобщение с claim линк
- Модел: Kimi-2.6

**Задача 1Е — Panoramafirm.pl scraper за бизнес имена** 🟡 В процес (15 юни 2026)
- **Fixly.pl проучен и отхвърлен (15 юни 2026):**
  * Не е browsable directory — activity feed модел, без pagination
  * GraphQL API (api.fixly.pl/graphql) достъпен без auth, но searchProvidersByLonLatCategoryId връща само total: Int, не списък с провайдъри
  * Имената на listing са предимно лични (Piotr Serocki, Mateusz G) — неподходящи за Bing API
- **Pivot: Panoramafirm.pl** (проверен browsable business directory):
  * Скрипт: apps/scripts/scrape_panoramafirm.py (Python 3.13, sync Playwright, headless=False)
  * Output: apps/scripts/warszawa_providers_panoramafirm.csv
  * Статус: Работи overnight (15 юни) — page 32/250 за cleaning, 780 records
  * Колони: business_name, phone, website, category, source=panoramafirm, profile_url
  * ВАЖНО: Телефоните от Panoramafirm са call-tracking номера (224573095) — не се ползват
  * Уебсайтовете са реални → директно към Email extractor (Task 1З) без нужда от Bing API
- Реалистично очаквани records: ~3,000-5,000 Warsaw фирми (3 категории)
- Модел: SWE-1.6

**Задача 1Ж — Bing API → намиране на уебсайтове**
- Bing Search API (безплатно до 3,000 заявки/месец)
- Търси по бизнес имена → намира уебсайтовете им
- Модел: Kimi-2.6
- ВАЖНО: Panoramafirm.pl вече дава уебсайтове директно → Task 1Ж нужен САМО за records от Panoramafirm без уебсайт

**Задача 1З — Email extractor от Fixly уебсайтове**
- Същия email extractor от Задача 1Г
- Очаквано: +2,000-3,000 нови имейла
- Модел: Kimi-2.6

**Задача 1И — Google Places API скрипт** *(опционален, при нужда от повече данни)*
- Търси: "sprzątanie Warszawa", "masażysta Warszawa", "hydraulik Warszawa"
- Цена: ~$10-15 за 300-500 резултата
- Използва се само ако 1А-1З не дадат достатъчно данни
- Модел: Kimi-2.6

**Очакван краен резултат от Фаза 1:**

| Слой | Имейли | Телефони |
|---|---|---|
| CEIDG директно (1А) | 701 | 257 |
| CEIDG уебсайтове (1Г) | +300 | — |
| SMS кампания (1Д) | — | 257 |
| Fixly → Bing → сайт (1З) | +2,000-3,000 | +500 |
| Google Places (1И, опц.) | +200 | +200 |
| **Общо** | **~3,000+** | **~750+** |

При 8-15% конверсия = **240-450 claimed профила за Warsaw launch.**

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

## Следваща незабавна стъпка

1. Задача 1Ж — Bing API за уебсайтове (Kimi-2.6) — за останалите 2,071 фирми без уебсайт
2. Задача 1Г — Email extractor от CEIDG уебсайтове (Kimi-2.6) — изчаква повече уебсайтове
3. Задача 1З — Email extractor от Panoramafirm уебсайтове (Kimi-2.6) — изчаква повече уебсайтове
4. Задача 2А — seed_unclaimed_providers.py (Kimi-2.6) — изчаква 1В ✅
4. Задача 5А — Bulk имейл кампания (Kimi-2.6) — изчаква 2А

**Паралелно (може веднага, не чака overnight):**
- Задача 4Б — Unclaimed банер на Provider Full Page (Kimi-2.6)
- Задача 3Б — Art. 14 Confirmation имейл шаблон (Claude)
