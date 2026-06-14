# Nevumo — Claimed Profiles: Пълен план

**Статус:** 🟡 В процес — Задача 2Б ✅ и 3А ✅ завършени
**Последна актуализация:** 14 юни 2026
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

**Задача 1А — CEIDG скрипт** ✅ В процес
- Скриптът тече локално
- Очакван резултат: 500-1,500 уникални доставчика в CSV
- След приключване: преглед на CSV качеството

**Задача 1Б — Преглед и почистване на CSV**
- Отвори `warszawa_providers_ceidg.csv` в Excel/Google Sheets
- Провери качеството на данните (колко имат телефон, колко имейл)
- Изтрий редове с business_name = само цифри или явно грешни
- **Правиш го ти** — 30 минути

**Задача 1В — Google Places API скрипт** *(опционален, при нужда от повече данни)*
- Kimi-2.6 пише Python скрипт за Google Places API
- Търси: "sprzątanie Warszawa", "masażysta Warszawa", "hydraulik Warszawa"
- Цена: ~$10-15 за 300-500 резултата
- Обединява с CEIDG данните в общ CSV

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

**Задача 4А — `/[lang]/claim/[token]` страница**
- Показва профила (само за четене): name, category, city
- CTA: "Твой ли е този профил? Вземи го безплатно →"
- При клик → регистрация/вход → профилът е твой
- Redirect към Provider Dashboard след успех
- **Модел: Kimi-2.6**

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

1. Задача 3Б — Art. 14 Confirmation имейл (Claude пише шаблона)
2. Задача 4А — `/[lang]/claim/[token]` страница (Kimi-2.6)
3. Задача 4Б — "Unclaimed" банер на Provider Full Page (Kimi-2.6)
4. Задача 1Б — Преглед и почистване на CSV (ръчно)
5. Задача 2А — seed_unclaimed_providers.py (Kimi-2.6)
6. Задача 5А — Bulk имейл кампания (Kimi-2.6)
