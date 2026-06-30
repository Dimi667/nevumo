# Nevumo — Claimed Profiles: Master Campaign Plan v2

**Статус:** 🔴 Active — Pre-launch preparation
**Версия:** 2.0
**Дата:** 21 юни 2026
**Замества:** `claimed_profiles_plan_1.md` (архивиран в Git)
**Следваща незабавна стъпка:** Раздел 2 — Pre-Launch Блокери

---

## РАЗДЕЛ 0 — Постигнато в Plan 1 (архив)

> Пълният Plan 1 е в Git историята. Тук е само резюмето за справка.

### ✅ Фаза 1 — Данни (ЗАВЪРШЕНА)

| Source | Имейли | Телефони |
|---|---|---|
| CEIDG (scraping + email extractor) | 864 | 230 |
| Panoramafirm.pl (scraping + email extractor) | 772 | — |
| **Общо уникални** | **~1,636** | **230** |

Скриптове: `collect_ceidg_providers.py`, `clean_ceidg_csv.py`, `scrape_panoramafirm.py`,
`panoramafirm_requests_only.py`, `extract_emails_from_websites.py`, `bing_website_finder.py`
Финален CSV: `warszawa_providers_ceidg.csv` + `panoramafirm_emails_final.csv`

### ✅ Фаза 2 — Backend (ЗАВЪРШЕНА)

- `GET /api/v1/providers/claim/{token}` — публичен preview (без auth)
- `POST /api/v1/providers/claim/{token}` — claim с JWT auth
- `GET /api/v1/providers/{slug}` — връща `claim_token` + `search_volume`
- DB: `is_claimed`, `claim_token`, `data_source` полета в providers
- DB: `city_category_search_volume` таблица (Warsaw: cleaning=7000, plumbing=5400, massage=6900)

### ✅ Фаза 3 — Имейл шаблони (ЗАВЪРШЕНА)

- **Outreach имейл:** `apps/api/scripts/templates/outreach_email_pl.html`
  - Jinja2 variables: `{{ business_name }}`, `{{ service_label }}`, `{{ claim_link }}`
  - Subject lines по категория (под 50 символа, реални CEIDG данни)
  - Тестван в Gmail (desktop + iPhone) ✅
- **Art. 14 GDPR имейл:** `apps/api/services/templates/article14_confirmation_pl.html`
  - Тестван: ✅ изпратен до dimitar.j.dimitroff@gmail.com
- **Bulk скрипт:** `apps/api/scripts/send_outreach_bulk.py`
  - Jinja2 rendering, 37s delay (100/час), idempotent via log

### ✅ Фаза 4 — Frontend (ЗАВЪРШЕНА с pending)

- Claim страница `/[lang]/claim/[token]` — висококонверсионен дизайн
- Unclaimed banner на Provider Full Page (Task 4Б) — **ПОДОБРЕНО (29 юни 2026)**: Капитализирана първа буква на всички преводи; Добавена локативна форма за градове в полския език (напр. "w Warszawie" вместо "w Warszawa")
- CTA бутон adaptive layout за дълги имена (Task 4В)
- 5 error states с преводи (имплементирани, НЕ browser-тествани → в QA Gate)
- Auth redirect bugs: 9 бъга намерени и оправени по E2E тест (21 юни 2026)

### ✅ E2E Тест (21 юни 2026)

- Тест провайдър "Hydraulik Testowy E2E" claimed успешно ✅
- Google OAuth → Dashboard ✅
- Email/password login → НЕ ТЕСТВАН ⚠️ (в QA Gate)
- Art. 14 email → НЕ СЕ ИЗПРАЩА от providers.py ⚠️ (блокер в Раздел 2)

---

## РАЗДЕЛ 1 — Архитектура на кампанията

### 1.1 Два фунела — не един

```
ФУНЕЛ 1: ACQUISITION (привличане)
Email/SMS изпратен → Отворен → Кликнат → Регистриран → Claimed
     1,636           ~655        ~118        ~83          ~75

ФУНЕЛ 2: ACTIVATION (активиране) — КРИТИЧЕН, ПРОПУСКАН!
Claimed → Попълнен профил → Получава 1ви lead → Активен провайдър
  ~75          ~45               ~38                  ~32
```

**Ключов принцип:** Claimed провайдър с непопълнен профил е невидим за клиенти.
Двата фунела са еднакво важни. Activation sequence е Фунел 2.

### 1.2 Канали

| Канал | Получатели | Open rate | Цена |
|---|---|---|---|
| Email sequence (4 имейла) | ~1,636 | 35-50% | $0 (Resend Pro $20/мес) |
| SMS (паралелно) | 230 | 95-98% | ~4 EUR (SMSapi.pl) |

### 1.3 Email Sequence — Timing (Warsaw Time / CET/CEST)

| Имейл | Ден | Час | Цел |
|---|---|---|---|
| #1 Introduction | Вторник | 10:00 | First impression, profile awareness |
| #2 Insight | Петък | 18:00 | Second touch, competitor insight |
| #3 Social Proof | Сряда (следваща) | 10:00 | Trust, address objections |
| #4 Break-up | Понеделник (следваща) | 10:00 | Last chance, binary choice |

SMS: изпраща се паралелно с Email #1 и #4.

### 1.4 Content Matrix — 12 шаблона (4 × 3 категории)

| | Cleaning | Plumbing | Massage |
|---|---|---|---|
| Email #1 | ✍️ | ✍️ | ✍️ |
| Email #2 | ✍️ | ✍️ | ✍️ |
| Email #3 | ✍️ | ✍️ | ✍️ |
| Email #4 | ✍️ | ✍️ | ✍️ |
| SMS | ✍️ | ✍️ | ✍️ |

> ✍️ = За писане в Раздел 4

### 1.5 Очаквана конверсия (при пълна кампания)

| Сценарий | Claimed | Active |
|---|---|---|
| 1 имейл (baseline) | 16–49 | ~25 |
| 4-email sequence | 65–120 | ~55 |
| + SMS + segmentation | 120–180 | ~100 |
| Всички тактики + Activation | **150–245** | **130–215** |

---

## РАЗДЕЛ 2 — PRE-LAUNCH БЛОКЕРИ

> ⛔ **НИЩО не се изпраща докато тези задачи не са 100% завършени.**
> Наредени по приоритет и зависимост.

### Блокер 1 — Auto-claim след login (Задача 4Д) ✅ ЗАВЪРШЕН (22 юни 2026)

**Проблем:** Потребителят трябва да кликне бутона ДВА ПЪТИ (claim страница → auth → обратно → claim). Огромна загуба на конверсия.

**Решение:** AutoClaimTrigger компонент в claim страницата. При detect на authenticated user + redirect от auth → автоматично изпраща POST claim → Dashboard.

**Файлове:** `apps/web/app/[lang]/claim/[token]/page.tsx`, нов `AutoClaimTrigger.tsx`
**Модел:** Kimi-2.6

**Имплементация (22 юни 2026):**
- Нов: `AutoClaimTrigger.tsx` — Client Component с useRef idempotency guard
- Нов: `ClaimCTAWrapper.tsx` — скрива CTA по време на auto-claim
- Нов: `actions.ts` — Server Action за manual claim
- Променен: `page.tsx` — интегрира AutoClaimTrigger и ClaimCTAWrapper
- Променен: `LoginClient.tsx` — addFromAuthParam() + urlRole fix
- Променен: `oauth-callback/page.tsx` — addFromAuthParam()
- Променен: `OAuthTermsClient.tsx` — addFromAuthParam()
- Seeded: 10 нови translation ключа в claim namespace (34 езика)
- Bug fix: ?role=provider не се четеше за intent при регистрация

**QA резултати:**
- Сценарий 1 (Main flow): ✅
- Сценарий 2 (Direct link): ✅
- Сценарий 3 (Already claimed): ✅
- Сценарий 4 (Reload idempotency): ✅
- Сценарий 5 (Auth expired): ✅
- Сценарий 6 (Network retry): ⚠️ Код OK, не тестван
  (Playwright не поддържа network blocking)

**Known issue (не е от Блокер 1):**
Google OAuth + claim flow → може да попадне на onboarding
вместо директно на claimed dashboard. Tracker-ва се отделно.

---

### Блокер 2 — Art. 14 GDPR имейл в providers.py (Задача 4Е) ✅ ЗАВЪРШЕН (22 юни 2026)

**Проблем:** `send_article14_notification()` липсва в `POST /api/v1/providers/claim/{token}` в `providers.py`. Изпраща се само от `provider.py` (dashboard flow). Правно задължение.

**Решение:** Добавяне след `db.commit()` в `claim_provider` функцията — следва pattern от `provider.py ~line 675`.

**Файл:** `apps/api/routes/providers.py`
**Модел:** Kimi-2.6

**Имплементация (22 юни 2026):**
- Добавено извикване на send_article14_notification() след db.commit() в claim_provider
- Fix: _send_email() параметри to→to_email, html→html_body (ca8957c)
- Commits: f967053, ca8957c
- E2E тест: ✅ Art. 14 изпратен успешно (без [EMAIL_WARNING] в Railway логове)

---

### Блокер 3 — Unsubscribe механизъм (НОВ — GDPR/RODO задължение) ✅

**Проблем:** Нямаме unsubscribe линк в outreach имейлите. 4 последователни имейла без opt-out = нарушение на RODO (Полша) и GDPR Чл. 21.

**Решение (3 части):**

**3a — DB таблица** `outreach_unsubscribes`:
```sql
CREATE TABLE outreach_unsubscribes (
    email TEXT PRIMARY KEY,
    unsubscribed_at TIMESTAMPTZ DEFAULT NOW(),
    reason TEXT  -- 'user_request', 'bounce', 'complaint'
);
```

**3b — Backend endpoint:**
`GET /api/v1/outreach/unsubscribe?token={token}` — публичен, без auth
- Верифицира HMAC токен (email + secret)
- Записва в `outreach_unsubscribes`
- Показва потвърждение на Polish

**3c — Интеграция в bulk скрипт:**
- `send_outreach_bulk.py` проверява `outreach_unsubscribes` преди всяко изпращане
- Ако email е там → skip (логва като UNSUBSCRIBED)

**Unsubscribe линк в имейла:** `https://nevumo.com/pl/outreach/unsubscribe?token={hmac_token}`

**Файлове:** нова `outreach_unsubscribes` таблица, `apps/api/routes/outreach.py`, `send_outreach_bulk.py`
**Модел:** SWE-1.6 (backend) + Kimi-2.6 (bulk script update)

**Имплементация (22 юни 2026):**
- Step 2: `OutreachUnsubscribe` model в `models.py` + `OUTREACH_HMAC_SECRET` в `Settings` + Alembic migration `u1v2w3x4y5z6_add_outreach_unsubscribes.py`
- Step 3: `GET /api/v1/outreach/unsubscribe` — HMAC-SHA256 верификация, DB write, 302 redirect; регистриран в `main.py`
- Step 4: `apps/web/app/[lang]/outreach/unsubscribe/page.tsx` — async Server Component с `await searchParams` (Next.js 16 compatible)
- Step 5: `{{ unsubscribe_url }}` добавен в `outreach_email_pl.html` + `_generate_unsubscribe_url()` + DB check в `send_outreach_bulk.py`
- E2E тест: ✅ invalid token → 400, valid token → 302, DB record created (reason=user_request), bulk skip logic верифицирана, cleanup OK

---

### Блокер 3Б — Welcome имейл след claim (await bug) 🟡

**Проблем:** `send_claim_welcome_email` хвърля `object bool can't be used in 'await' expression`.
Функцията не е async, но се извиква с await. Pre-existing bug, открит при E2E теста на Блокер 2.

**Последствие:** Провайдърът не получава welcome имейл след успешен claim.
Не е правно задължение, но влияе пряко на Фунел 2 (Activation).

**Файл:** `apps/api/routes/providers.py` — функцията claim_provider, блокът Send welcome email

**Решение:** Премахни await пред извикването на send_claim_welcome_email() или
направи функцията async — провери сигнатурата в email_service.py преди fix.

**Модел:** Kimi-2.6
**Приоритет:** Преди QA Gate, след Блокер 3.

**Имплементация (22 юни 2026):**
- Премахнат `await` пред `email_service.send_claim_welcome_email()` в `apps/api/routes/providers.py` ред 499
- Функцията е синхронна (`def`, не `async def`) — `await` върху sync функция хвърляше `TypeError`
- Fix: Kimi-2.6
- E2E тест: ✅ Claim flow завършен без грешки, redirect към dashboard успешен

---

### Блокер 4 — Resend Webhooks (НОВ — tracking + bounce protection) 🔴

**Проблем:** Без webhooks нямаме данни за opens/clicks и не обработваме bounces/complaints. Акумулирани bounces = domain reputation damage = бъдещите имейли отиват в spam.

**Решение:**

**4a — FastAPI webhook endpoint:**
`POST /api/v1/webhooks/resend` — верифицира Resend signature header

Обработва events:
- `email.delivered` → log
- `email.opened` → log
- `email.clicked` → log
- `email.bounced` → добавя в `outreach_unsubscribes` с reason='bounce'
- `email.complained` → добавя в `outreach_unsubscribes` с reason='complaint' (НЕЗАБАВНО)

**4b — DB таблица** `outreach_events`:
```sql
CREATE TABLE outreach_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resend_message_id TEXT NOT NULL,
    email TEXT NOT NULL,
    event_type TEXT NOT NULL,  -- delivered/opened/clicked/bounced/complained
    occurred_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_outreach_events_email ON outreach_events(email);
```

**4c — Resend dashboard:** Активиране на webhook в Resend UI → URL: `https://api.nevumo.com/api/v1/webhooks/resend`
Events: delivered, opened, clicked, bounced, complained

**Файлове:** `apps/api/routes/webhooks.py`, Alembic migration, `apps/api/models.py`
**Модел:** SWE-1.6

**Имплементация (22 юни 2026):**
- Step 1: `OutreachEvent` модел в `models.py` + `RESEND_WEBHOOK_SECRET` в `Settings` + Alembic migration `v1w2x3y4z5a6_add_outreach_events.py`
- Step 2: `apps/api/routes/webhooks.py` — svix signature verification, event logging, bounce/complaint suppression; регистриран в `main.py`
- Ръчна конфигурация: Webhook създаден в Resend Dashboard (Enabled), `RESEND_WEBHOOK_SECRET` добавен в Railway
- E2E тест: ✅ изпратен реален имейл → `email.sent` + `email.delivered` записани в `outreach_events` (resend_message_id: 9764744d-5be9-4425-8a87-147535920076)

---

### Блокер 5 — outreach_sequence_log DB таблица ✅ ЗАВЪРШЕН (22 юни 2026)

**Проблем:** `outreach_sent_log.csv` е локален файл — не работи с Railway scheduler и е ненадежден.

**Решение — DB таблица:**
```sql
CREATE TABLE outreach_sequence_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    business_name TEXT,
    category TEXT,  -- cleaning/plumbing/massage
    sequence_step INTEGER NOT NULL,  -- 1/2/3/4
    resend_message_id TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'sent',  -- sent/failed
    UNIQUE(email, sequence_step)
);
CREATE INDEX idx_outreach_seq_email ON outreach_sequence_log(email);
```

**Интеграция:** `send_outreach_bulk.py` пише в таблицата вместо CSV.
Scheduler проверява: "Кой email на коя стъпка е следващ?"

**Файлове:** Alembic migration `w1x2y3z4a5b6_add_outreach_sequence_log.py`, `apps/api/models.py`, `send_outreach_bulk.py`
**Модел:** SWE-1.6

**Имплементация (22 юни 2026):**
- `OutreachSequenceLog` модел добавен в `models.py` с UNIQUE(email, sequence_step)
- Alembic migration `w1x2y3z4a5b6_add_outreach_sequence_log.py` — приложена успешно
- `send_outreach_bulk.py` — пълна замяна: CSV → DB (SessionLocal, ON CONFLICT DO NOTHING)
- `--sequence-step` CLI аргумент добавен (default: 1, range: 1-4)
- Alembic merge migrations: 4 merge файла за почистване на натрупани heads
- `alembic_version.version_num` разширена от VARCHAR(32) → VARCHAR(128) (pre-existing issue)
- Commits: `4cbdb17` (implementation), `d70616d` (merge migrations)
- Dry-run тест: ✅ 3/3 реда, 0 грешки, template рендерира коректно

---

### Блокер 6 — Верификация при claim ✅ ЗАВЪРШЕН (23 юни 2026, commit 7ee1361)

**Имплементация:**
- DB: `scraped_email` колона на `providers` + `pending_claim_verifications`
  таблица (migration b1c2d3e4f5g6)
- DB: `category_slug` колона на `providers` (migration c1d2e3f4g5h6)
- Backend: `send_claim_verification_email()` + обновена логика в
  `claim_provider()` + нов endpoint `POST /api/v1/providers/claim/{token}/verify`
- Backend: `data_source` добавен в `get_provider_profile()` response
- Backend: `category_slug` добавен в `get_provider_profile()` response
- Bug fix: `scraped_email=None` → `scraped_email=provider.scraped_email` в
  `send_article14_notification()` call
- Bug fix: Email verification премахната от token-based claim flow
  (токенът е достатъчно доказателство за собственост)
- Email template: `apps/api/scripts/templates/claim_verification_pl.html`
- Translations: 12 ключа × 34 езика = 408 реда
  (seed_claim_verify_translations.py)
- Frontend: `/[lang]/claim/[token]/verify/page.tsx` + `VerifyCodeForm.tsx`
  (запазени за future "claim from public listing" feature)
- Frontend: AutoClaimTrigger redirect → `/provider/dashboard/profile`
  (wizard вместо dashboard)
- Frontend: `ownership_blocked` error UI fix в claim page.tsx

**Wizard pre-fill за scraped провайдъри:**
- Scraped провайдъри започват от Step 1 (не прескачат към Step 2)
- Step 1: business_name + description pre-filled от scraped данни
- Step 1: heading "Znaleźliśmy Twoją firmę na Nevumo!" за scraped провайдъри
- Step 2: category_slug pre-selected автоматично
- Step 2: Warsaw pre-selected автоматично
- Fix: `data_source` липсваше в API response → всички scraped checks failing
- Fix: `pointerEvents: none` на file input → photo upload не работеше

**Три сценария за верификация:**
| Случай | scraped_email | Резултат |
|--------|--------------|---------|
| Email съвпада | match | Директен claim (200) |
| Email не съвпада | mismatch | 6-цифрен код (запазено за future) |
| Няма scraped_email | NULL | ownership_blocked UI |

**QA резултати:**
- Backend API tests: ✅ PASS (всичките 3 сценария)
- Browser tests: ✅ PASS (Step 1 wizard, Step 2 pre-fill)
- Photo upload: 🔴 FIX PENDING (pointerEvents: none)

---

### Блокер 6 — Magic Link Flow + Cookie Source of Truth ✅ ЗАВЪРШЕН (23 юни 2026)

**Архитектура:**
- Claim token от email = proof of identity (без login)
- POST /providers/claim/{token} — no JWT required
- get_or_create_claim_user() в auth_service.py
- Cookie = единствен source of truth

**Файлове:**
- apps/api/services/auth_service.py — нова get_or_create_claim_user()
- apps/api/routes/providers.py — claim endpoint redesign
- apps/web/lib/auth-store.ts — isAuthenticated() чете Cookie
- apps/web/app/[lang]/claim/[token]/ClaimProcessor.tsx — нов компонент
- apps/web/app/[lang]/claim/[token]/page.tsx — интегриран ClaimProcessor
- apps/web/app/[lang]/provider/dashboard/profile/page.tsx — wizard heading логика

**Translations добавени:**
- claim.processing — 34 езика
- provider_dashboard.wizard_welcome_heading — 34 езика
- provider_dashboard.wizard_welcome_subtitle — 34 езика

---

### Блокер 7А — Banner Flow Redesign: No auth before code ✅ ЗАВЪРШЕН (23 юни 2026, като част от Блокер 6)

**Имплементация:**
- Claim token от email = proof of identity (без login)
- POST /providers/claim/{token} — no JWT required
- get_or_create_claim_user() в auth_service.py
- Cookie = единствен source of truth

**Файлове:**
- apps/api/services/auth_service.py — get_or_create_claim_user()
- apps/api/routes/providers.py — claim endpoint redesign
- apps/web/lib/auth-store.ts — isAuthenticated() чете Cookie
- apps/web/app/[lang]/claim/[token]/ClaimProcessor.tsx
- apps/web/app/[lang]/claim/[token]/page.tsx

**QA резултати:** ✅ Блокер 7Д потвърди "Email claim flow работи коректно след Блокер 7А промените"

---

### Блокер 7Б — Magic Link Login за passwordless потребители ✅ ЗАВЪРШЕН (24 юни 2026, Auth Phase 3)

**Имплементация:**
- POST /api/v1/auth/request-magic-link — изпраща magic link по email
- GET /api/v1/auth/magic-link/verify?token={token} — верифицира, връща JWT
- Magic link: https://nevumo.com/{lang}/auth/magic-link?token={token} (24h TTL)
- DB: magic_link_tokens таблица (token, user_id, expires_at, used)
- Email template: magic_link_pl.html
- Работи паралелно с парола и Google OAuth

**Файлове:**
- apps/api/routes/auth.py — 2 нови endpoints
- apps/api/models.py — MagicLinkToken модел
- apps/api/services/email_service.py — send_magic_link_email()
- apps/web/app/[lang]/auth/magic-link/page.tsx

**QA резултати:** ✅ Auth Phase 3 COMPLETE (June 24, 2026)

---

### Блокер 7В — "Add/Change password" в Provider Settings ✅ ЗАВЪРШЕН (24 юни 2026)
(Изисква: Блокер 7А. Може паралелно с 7Б)
Проблем: Passwordless потребители (от banner claim) нямат парола в акаунта.

Трябва опция да добавят парола след като са влезли.
Решение:
- Provider Settings → секция "Сигурност" → бутон "Задай парола" (ако няма) / "Смени парола" (ако има)
- Backend: POST /api/v1/auth/password (global endpoint, не provider-specific)
  - Ако passwordless: просто задава нова парола (без old_password)
  - Ако има парола: изисква old_password за потвърждение
- Backend: GET /api/v1/auth/me (single source of truth за has_password)
- Frontend: PasswordSection.tsx (shared компонент за provider и client)
  - Използва getMe() за зареждане на password status от /api/v1/auth/me
  - Автоматично показва 2-field (set password) или 3-field (change password) форма
- Translations: account_settings namespace (14 ключа × 34 езика = 476 rows)
  - seed_account_settings_translations.py
  - Keys: section_security, security_description_no_password, security_description_has_password, label_current_password, label_new_password, label_confirm_password, btn_set_password, btn_change_password, btn_save_password, msg_password_set, msg_password_changed, error_current_password_invalid, error_passwords_dont_match, error_password_too_short
- Architecture refactor: Премахнат has_password от provider profile и client dashboard responses
  - Централизиран password status в /api/v1/auth/me endpoint
  - Елиминира stale context data проблеми
  - Опростява компонент interface (не са нужни props)

Модел: Kimi-2.6 (frontend) + SWE-1.6 (backend endpoint)

**Имплементация (24 юни 2026):**
- Initial implementation: POST /api/v1/auth/password endpoint + PasswordSection.tsx (commit 3c8cda9)
- Bug fix: authFetch response handling (commit a7f8344)
- Self-healing: local state + CURRENT_PASSWORD_REQUIRED handling (commit 6c382ea)
- Backend refactor: GET /api/v1/auth/me endpoint + removed has_password from dashboard responses (commit 7602bb4)
- Frontend refactor: PasswordSection uses /api/v1/auth/me as single source of truth (commit 5228cc3)

**QA резултати:**
- ✅ Работи за provider settings
- ✅ Работи за client settings
- ✅ Работи паралелно с magic link login
- ✅ Работи паралелно с Google OAuth login
- ✅ Правилно показва 2-field (set password) vs 3-field (change password) форма

---

### Блокер 7Г — "Изпрати ми нов login link" на Auth страницата ✅ ЗАВЪРШЕН (24 юни 2026, като част от Блокер 7Б)

**Имплементация:**
- Frontend: LoginClient.tsx — "Brak hasła? Zaloguj się linkiem na email →"
- Появява се на step 2 (след въвеждане на email)
- Кликване → изпраща линк до вече въведения email → success message
- Използва POST /api/v1/auth/request-magic-link от Блокер 7Б
- requestMagicLink() function в auth-api.ts

**Translations:** 8 ключа × 34 езика (seed_magic_link_translations.py)

**QA резултати:** ✅ Tested: passwordless provider → magic link → provider dashboard

---

### Блокер 7Д — Потвърждение на Outreach Flow ✅ ЗАВЪРШЕН (26 юни 2026)
(E2E верификация — само тестове, без код)

**QA резултати (26 юни 2026):**
- ✅ T1 (Happy Path): `/pl/claim/{token}` (без ?source=banner) → 200 → cookie `nevumo_auth_token` → redirect `/pl/provider/dashboard/profile?claimed=success` → wizard зареден, 0 console errors
- ✅ T2 (Already Claimed): Същият token → error UI "Ten link jest nieprawidłowy lub wygasł" → без unauthorized достъп, 0 console errors
- ✅ T3 (Invalid Token): Фалшив token → error UI "Profil, do którego prowadzi ten link, nie został znaleziony..." → чист error page, 0 console errors

Заключение: Email claim flow работи коректно след Блокер 7А промените в providers.py.

---

### Блокер 7Е — Onboarding Redirect Logic ✅ ЗАВЪРШЕН (25 юни 2026, като част от Блокер 7Г+7Е)

**Имплементация:**
- Backend: determine_post_auth_redirect() функция в auth_service.py — single source of truth за всички post-auth redirects
- Priority order: claim_token → effective_role → onboarding completeness check
- For providers: check_onboarding_complete() → redirect based on missing_fields
  - Няма description/photo → Step 1 (profile)
  - Няма услуги → Step 2 (services)
  - Всичко попълнено → Dashboard Overview
- Dual-role потребители: redirect по role (provider → /provider/dashboard, client → /client/dashboard)
- New endpoint: POST /api/v1/auth/check-email → returns {exists, has_password, role, oauth_connected}
- Frontend: LoginClient.tsx smart detection flow (check-email → passwordless auto magic link → magic_link_sent UI)
- Frontend: ClaimProcessor.tsx updated redirect logic with is_onboarding_complete field

**Файлове:**
- apps/api/services/auth_service.py — determine_post_auth_redirect()
- apps/api/routes/auth.py — check-email endpoint, redirect integration
- apps/web/app/[lang]/auth/LoginClient.tsx — smart detection flow
- apps/web/app/[lang]/claim/[token]/ClaimProcessor.tsx — onboarding redirect logic
- apps/api/scripts/seed_magic_link_sent_translations.py — 34 languages, 3 keys

**QA резултати:** ✅ check-email response, ✅ passwordless auto magic link, ✅ login redirect (correct lang), ✅ magic link redirect, ✅ register redirect, ✅ Google OAuth redirect

---

### Блокер 7Ж — Onboarding Pre-fill за Scraped Providers ✅ ЗАВЪРШЕН (26 юни 2026)

**Имплементация (June 23, 2026):**
- DB: category_slug column added to providers (migration c1d2e3f4g5h6)
- Expose category_slug в dashboard API profile response
- Fix: scraped providers start from Step 1 (not skipped to Step 2)
- Pre-fill category_slug и Warsaw в Step 2 за scraped providers
- Add claimed-specific heading в Step 1 за scraped providers ("Znaleźliśmy Twoją firmę na Nevumo!")

**Имплементация (June 26, 2026):**
- DB: scraped_phone TEXT column added to providers (migration d2e3f4g5h6i7)
- models.py: scraped_phone field added to Provider model
- provider_service.py: scraped_phone included in get_provider_profile() response
- auth_service.py: get_or_create_claim_user() pre-fills user.phone from scraped_phone if user.phone is None
- providers.py: both call sites pass scraped_phone=provider.scraped_phone

**Файлове:**
- apps/api/alembic/versions/c1d2e3f4g5h6_add_provider_category_slug.py
- apps/api/alembic/versions/d2e3f4g5h6i7_add_scraped_phone_to_providers.py
- apps/api/models.py — category_slug, scraped_phone fields
- apps/api/services/provider_service.py — get_provider_profile() response
- apps/api/services/auth_service.py — get_or_create_claim_user()
- apps/api/routes/providers.py — claim endpoints
- apps/web/app/[lang]/provider/dashboard/profile/page.tsx — pre-fill logic
- apps/web/app/[lang]/claim/[token]/page.tsx — heading logic

**QA резултати:** ✅ E2E verified: claim flow → user.phone populated from scraped_phone

---

### Блокер 7З — Claim Flow UX Hardening ✅ ЗАВЪРШЕН (29 юни 2026)
(Изисква: Блокер 7Д. Блокира: Блокер 8, QA Gate)
Проблем: Тест на Banner flow с реален акаунт разкри 3 класа дефекти при нестандартно потребителско поведение (грешка, изтекъл код, Back/Refresh). Happy path работи. Edge cases — не.

**Имплементирани компоненти:**
- Backend: verify_claim() разграничава CODE_EXPIRED vs CODE_INVALID (отделни detail.code)
- Frontend VerifyCodeForm.tsx: отделни error messages за CODE_INVALID, CODE_EXPIRED, network error; resend бутон с 60s delay + 30s cooldown след error
- Frontend ClaimProcessor.tsx: sessionStorage='sent' при 202 + claim_sent_to_{token} за sentTo; router.replace() при Back (елиминира loop); ALREADY_CLAIMED UI state с redirect към dashboard; getAuthToken() check при mount
- Seed: seed_claim_verify_errors.py — 238 translations (7 ключа × 34 езика): verify_error_invalid, verify_error_expired, verify_error_network, verify_error_format, resend_code, resend_cooldown, already_claimed_redirect
- QA: T1 PASS, T2 by design (router.replace елиминира loop), T3 PASS, T4 PASS, T5 PASS, T6 PASS

Компонент 1 — Различни error messages

Backend verify_claim() → CODE_EXPIRED vs CODE_INVALID (различни body кодове)
Frontend VerifyCodeForm.tsx → различни translation ключа за двата случая
Seed: 2 нови ключа × 34 езика в claim namespace

Компонент 2 — "Изпрати нов код" бутон

Backend: вече работи (повторен POST /claim/{token}?source=banner генерира нов код)
Frontend VerifyCodeForm.tsx:

Бутон се показва: след error ИЛИ след 60s без действие
30-секунден cooldown след натискане
Translation ключове: claim.resend_code, claim.resend_cooldown (34 езика)



Компонент 3 — State management на целия Banner Claim flow
ТочкаСценарийЖелано поведениеClaim pageRefresh след POST 202SessionStorage banner_sent_{token} → redirect към /verify, не нов POSTClaim pageBack от /verifyСъщото — "Email изпратен" state + линк към /verify/verifyRefreshФорма се зарежда отново → OK (код валиден 24h)/verifySubmit след вече claimedBackend → ALREADY_CLAIMED → redirect към dashboard/verifyNetwork error"Опитайте отново" бутон, не мъртъв екранWizard Step 1/2RefreshЗарежда от API — диагнозата ще потвърдиWizardBack към claim pageClaim page проверява is_claimed → "already claimed" state
Засегнати файлове:

apps/api/routes/providers.py — verify_claim()
apps/web/app/[lang]/claim/[token]/ClaimProcessor.tsx
apps/web/app/[lang]/claim/[token]/page.tsx
apps/web/app/[lang]/claim/[token]/verify/VerifyCodeForm.tsx
apps/api/scripts/seed_*.py — нови translation ключове

Ред на изпълнение:

Диагноза (SWE-1.6, read-only) → картографира реалното поведение при Back/Refresh на всяка стъпка
Backend fix (SWE-1.6)
Frontend fix + seed (Kimi-2.6)
Мануален регресионен тест

Модели: SWE-1.6 (диагноза + backend) → Kimi-2.6 (frontend + seed)


---

### Блокер 7Ж/Task 6A — Profile Strength Email ✅ ЗАВЪРШЕН (30 юни 2026)

**Архитектура (преработена от оригиналния план):**
Универсален имейл за ВСИЧКИ провайдъри (не само claimed/campaign), изпращан през Railway Scheduler ежедневен job — не event-driven trigger при POST /services.

**Тригер:** Railway Scheduler daily cron, `apps/api/scripts/job_profile_strength_email.py`
Условие: `business_name IS NOT NULL AND category_slug IS NOT NULL AND (profile_strength_email_sent_at IS NULL OR sent_at < NOW() - 14 days) AND (photo missing OR gallery empty OR description < 100 chars OR phone missing)`
Self-correcting: автоматичен повторен имейл на всеки 14 дни ако профилът остава непълен; спира автоматично щом полетата се попълнят.

**Съдържание:** 4 секции (профилна снимка, галерия снимки, описание с категорийно-специфичен пример, телефон) + FOMO subject line с динамичен брой липсващи неща.

**Автентикация в имейл линковете:** Magic Link (Blocker 7Б), не claim token.
- Нова колона `magic_link_tokens.multi_use` (BOOLEAN) — explicit разделение: стандартен login = single-use, profile strength email линкове = multi_use=True
- 5 отделни tokens на провайдър (по един за всяка секция + главен CTA), 14-дневен expiry, кликваеми многократно
- `generate_magic_link_token(email, db, hours, invalidate_existing, multi_use)` — reusable функция в auth_service.py

**Deep-linking:** всеки CTA отвежда директно до секцията (`#photo-section`, `#gallery-section`, `#details-section`) с auto-scroll на frontend, не само общ dashboard URL.

**Файлове:**
- apps/api/models.py — `Provider.profile_strength_email_sent_at`, `MagicLinkToken.multi_use`
- apps/api/services/email_service.py — `send_profile_strength_email()`
- apps/api/services/templates/profile_strength.html — единен Jinja2 template (34 езика чрез DB lookup, не отделни файлове по език)
- apps/api/scripts/seed_profile_strength_email_{1,2,3}.py — 34 езика, 23 ключа всеки (816 преводи общо)
- apps/api/scripts/job_profile_strength_email.py — scheduler job
- apps/api/routes/auth.py — magic_link_auth() conditional single-use/multi-use check
- apps/api/alembic/versions/ff8bc78d912a_*, 2d8e3cfff429_*, 5469b385e382_* — миграции

**Модел:** Claude (34 езика текст + архитектура) → Kimi-2.6 (seed скриптове, template, job script) → SWE-1.6 (backend логика, migrations, diagnostics, git)

**E2E тествано в production:** ✅ 2 тест провайдъра, всички 5 CTA линка, multi-use потвърдено в DB (used_at без блокиране на следващ клик), 14-дневен expiry потвърден.

---

### Блокер 8 — Task 2A: seed_unclaimed_providers.py 🔴

**Проблем:** Реалните Warsaw провайдъри все още не са в Neon DB.

**Решение:**
- Input: `warszawa_providers_ceidg.csv` + `panoramafirm_emails_final.csv`
- Merge по email (dedup)
- Insert в `providers` таблица с `is_claimed=False`, `data_source='scraped'`, `claim_token=secrets.token_hex(32)`
- Попълва `scraped_email` поле (задължително за верификация при claim — Блокер 6)
- Output: `outreach_ready.csv` (email, business_name, claim_token, category)
- Idempotent: `ON CONFLICT (email) DO NOTHING`

**Важни бележки от Plan 1:**
- `address` колона в CEIDG CSV е счупена (съдържа имейли) → зарежда се като NULL
- 176 partnership имена "1. X, 2. Y" → взема се само първото

**Команда:** `railway run python3.13 -m apps.api.scripts.seed_unclaimed_providers`
**Модел:** Kimi-2.6

---

### Блокер 8 — Railway Scheduler за автоматична sequence 🔴

**Решение:**

Един Railway Cron Job: `run_outreach_sequence.py`
- Проверява кой имейл е следващ за всеки провайдър (`outreach_sequence_log`)
- Проверява `outreach_unsubscribes` (skip)
- Проверява `providers.is_claimed` (skip ако вече claimed)
- Изпраща правилния шаблон (по `category` + `sequence_step`)
- Timing в Railway Cron (Warsaw/CET/CEST):

```
# Email #1: Вторник 10:00 Warsaw = 09:00 UTC (зима) / 08:00 UTC (лято)
0 8 * * 2   python3.13 -m apps.api.scripts.run_outreach_sequence --step 1

# Email #2: Петък 18:00 Warsaw = 17:00 UTC (зима) / 16:00 UTC (лято)
0 16 * * 5  python3.13 -m apps.api.scripts.run_outreach_sequence --step 2

# Email #3: Сряда 10:00 Warsaw (следваща)
0 8 * * 3   python3.13 -m apps.api.scripts.run_outreach_sequence --step 3

# Email #4: Понеделник 10:00 Warsaw (следваща)
0 8 * * 1   python3.13 -m apps.api.scripts.run_outreach_sequence --step 4
```

⚠️ **ВАЖНО:** Railway Cron използва UTC. При лятно часово (CEST = UTC+2) имейлите трябва да излизат в UTC-2h спрямо Warsaw time.

**Файл:** `apps/api/scripts/run_outreach_sequence.py`
**Модел:** Kimi-2.6

---

### Блокер 9 — Cleanup на E2E тестови провайдъри 🟡

**Команда:**
```bash
railway run python3.13 -m apps.api.scripts.e2e_outreach_cleanup
```
Изтрива всички провайдъри с `data_source='e2e_test'`.

---

### Блокер 10 — Resend Pro Upgrade 🔴 (преди bulk, не преди пилот)

**Действие:** Upgrade от Free (3,000/мес) към Pro ($20/мес = 50,000 имейла/мес)
в Resend Dashboard → Billing.

**Timeline:** Задължително ПРЕДИ bulk send (1,636 × 4 = 6,544 имейла).
**НЕ е нужен:** за технически тестове и пилотна вълна (20-30 адреса × 4 = max 120 имейла).

---

## РАЗДЕЛ 2.1 — Нови блокери преди Banner-only launch (30 юни 2026)

> Контекст: кампанията стартира САМО с Banner канал (Email/SMS outreach
> отложени за следваща фаза). По-долу логиката GATE = твърдо изискване
> преди production run на Б14 (seed-а), останалите следват успоредно/след.

### Блокер 11 — Banner Tracking Statistics ✅ ЗАВЪРШЕН (30 юни 2026)
Проблем: Нямаме жива статистика за Banner funnel-а (view → claim) преди
сийдването да направи профилите публични.
Решение: Event tracking за claim funnel стъпки, лек автоматизиран отчет
(Railway Scheduler → SQL → имейл summary), без нужда от dashboard UI.
Модел: SWE-1.6 (backend events) + Kimi-2.6 (frontend instrumentation при нужда)

**Стъпка 1 — claimed_at Timestamp (June 30, 2026):** ✅ COMPLETE
- claimed_at TIMESTAMPTZ поле добавено в providers таблицата (nullable)
- Попълва се при двата claim пътя: fast-path (claim_provider()) и verification (verify_claim_code())
- Production тестван: двата пътя валидирани с уникални test users, timestamp format потвърден (UTC)
- Засегнати файлове: alembic migration 20260630_add_claimed_at, models.py, routes/providers.py
- Тестови данни изчистени: всички test providers/users премахнати от production

**Стъпка 2 — Frontend Event Tracking (June 30, 2026):** ✅ COMPLETE
- trackPageEvent() извиквания в: ClaimProfileBanner.tsx, ClaimProcessor.tsx, VerifyCodeForm.tsx, ProviderFullPage.tsx
- Event names: banner_view, banner_claim_click, claim_page_view, claim_request_sent, verify_page_view, verify_code_submitted, verify_success, verify_error
- useRef guard за single execution на view events
- Production тестван: 7/7 events tracked успешно (verify_success потвърден след timezone fix)
- Засегнати файлове: 4 frontend файла (ClaimProfileBanner, ClaimProcessor, VerifyCodeForm, ProviderFullPage)
- Commit: fe31cbd

**Timezone Bug Fix (June 30, 2026):** ✅ FIXED
- Открит по време на функционален тест на Стъпка 2: 500 Internal Server Error при verify_claim_code()
- Root cause: Migration ff8bc78d912a (commit 925f091) сменила pending_claim_verifications от timezone-aware на naive, но кодът още използваше datetime.now(timezone.utc)
- Fix: datetime.now(timezone.utc) → datetime.utcnow() на 2 места в providers.py (commit 6b08f51)
- Импакт: 0 реални потребители засегнати — открито само от E2E тест преди bulk кампанията
- Виж docs/incident_logs.md за пълни детайли

**Финален E2E тест (June 30, 2026):** ✅ PASS
- Всички 7 event-а tracked в правилния ред (banner_view → verify_success)
- HTTP response: 200 OK (без 500 грешка)
- providers.claimed_at: попълнен с коректен UTC timestamp
- providers.is_claimed: True
- Test provider, user, и page events изчистени след тест

### Блокер 12 — Автоматизиран GDPR Objection/Delete Flow 🔴 GATE
(Изисква: чл.14 текст от Б14)
Проблем: Без ръчен капацитет за обработка на чл.21 възражения при >1,000
потенциални получателя.
Решение: HMAC token линк в чл.14 имейла → GET confirmation страница
(без авто-действие, защита срещу email scanner-и) → POST бутон → еднократно
занулява лични полета (business_name, scraped_email, scraped_phone, nip,
address, website) + маха от listing/sitemap + пази минимален audit trail
(id, category_slug, city_id, data_source, created_at, objected_at, honored_at).
Модел: SWE-1.6 (backend endpoint + migration) + Kimi-2.6 (confirmation
страница + 34 езика)

### Блокер 13 — Потвърждение Email/Password Login Flow за Banner 🔴 GATE
Проблем: Стар checklist елемент, никога browser-тестван за Banner flow
конкретно (само OAuth тестван при E2E).
Решение: mcp-playwright тест на email/password регистрация/login през
Banner claim flow.
Модел: SWE-1.6 + @mcp-playwright

### Блокер 14 — Seed Script: CSV обработка + листинг + sitemap + Art.14 тригер 🔴 GATE — финална стъпка
(Изисква: Б11, Б12, Б13 завършени)
Проблем: seed_unclaimed_providers.py не съществува; provider страници не
влизат в категориен листинг/sitemap без Service+ProviderCity записи
(INNER JOIN изисква и двете); чл.14 имейлът тригерира само при claim,
не при публикуване.
Решение:
- Филтър: само редове с реален email (third "-"/празно/NULL = липсва);
  изключва business_name=empty
- Insert: providers + placeholder Service (price_type='request', title
  от category_translations) + ProviderCity (Warszawa)
- чл.14 имейл тригер преместен от claim_provider() в самия seed insert
  момент, нов текст (не "профилът е поет", а "създадохме профил")
- phone-only редове (без реален email, 25 от CEIDG) → отделен
  phone_only_providers.csv, архивирани за бъдеща SMS фаза
Модел: Kimi-2.6

### Блокер 15 — Resend Webhook Одит + Dead-Email Feedback Loop 🟡
Проблем: Неясно дали bounce/complaint webhook резултатите влияят на claim
verification сценария (различно от outreach marketing skip логиката).
Решение: read-only диагностика на текущата webhook логика спрямо
scraped_email verification path.
Модел: SWE-1.6

### Блокер 16 — UX Конфликт /auth CTA на Claim Страницата 🟡
Проблем: Потенциален конфликт между auth бутоните и claim flow-а на
основната конверсионна страница — неанализиран.
Модел: SWE-1.6 (диагностика) → решение по резултат

### Блокер 17 — Badge Логика преди Claim 🟡
Проблем: Unclaimed провайдъри не би трябвало да показват verification
badge статус въобще.
Решение: потвърждение, че Level 0/1/2 логиката изключва unclaimed профили
(вероятно вече вярно структурно, нужно явно потвърждение, не предположение).
Модел: SWE-1.6 (read-only диагностика)

### Блокер 18 — Abandoned Banner Claim Reminder Sequence 🟢 (не gate, висок leverage)
Проблем: Потребител отваря /claim?source=banner, получава 202 (код изпратен),
не въвежда код — няма follow-up в момента.
Решение: transactional reminder (1ч + 24ч), SMS reminder ако има
scraped_phone — преизползва съществуваща magic-link инфраструктура, не
чака маркетинг QA Gate (не е marketing имейл).
Модел: SWE-1.6 (backend job) + Kimi-2.6 (templates, 34 езика)

### Блокер 19 — Бързо Индексиране (Google Indexing API / IndexNow) 🟢 (веднага след go-live)
Решение: автоматично подаване на нови provider URL-и след всеки seed run.
Модел: SWE-1.6

### Блокер 20 — Технически Дълг: AutoClaimTrigger/ClaimCTAWrapper 🟢
Проблем: Заменени от ClaimProcessor.tsx, не изтрити — риск при бъдещ
рефакторинг от агент, незапознат с актуалното състояние.
Решение: потвърждение, че никой активен code path ги ползва → изтриване.
Модел: SWE-1.6

### Блокер 21 — Конкурентен Натиск Social Proof ⏸️ (отложен)
Условие за активиране: поне 1 claimed конкурент в категория+град.
Засега N=0 навсякъде — неприложимо до първите реални claim-ове.

### [Разгледан и отхвърлен] — Retargeting/Lookalike Audiences
Meta pixel / Google Ads remarketing / custom audience от scraped_email —
отпада. Различна цел на обработване от установената правна основа
(легитимен интерес за marketplace функционалност), риск за balancing test.
Изисква отделен правен преглед преди евентуално бъдещо преразглеждане.

---

## РАЗДЕЛ 3 — Съдържание (имейл шаблони)

> BG версиите са финализирани (28 юни 2026).
> PL версиите се създават в следващата фаза.

### 3.1 Категорийна персонализация

| | 🧹 Почистване | 🔧 ВиК | 💆 Масаж |
|---|---|---|---|
| Search vol. | 7 363/мес | 10 707/мес | 3 635/мес |
| Email #2 protagonist | Хигиенисти | ВиК майстор | Масажисти |
| Email #3 protagonist | Хигиенисти (мн.ч.) | ВиК майстор (ед.ч.) | Масажист (ед.ч.) |

---

### 3.2 Email #1 — Представяне (Вт 10:00) — HTML с лого

**Subject:**
- Почистване: `7 363 клиента за почистване — намират ли те?`
- ВиК: `10 707 клиента с ВиК проблеми — намират ли те?`
- Масаж: `3 635 клиента търсят масаж — намират ли те?`

**Preview text:**
- Почистване: `Профилът ви чака — безплатно, без комисиона.`
- ВиК: `Клиентите търсят ВиК майстор в 21:00 — бъдете там пръв.`
- Масаж: `Постоянните клиенти започват онлайн — профилът ви е готов.`

**BG шаблон — Почистване:**
[HTML с лого]
7 363 клиента търсят почистване във Варшава всеки месец. Намират ли именно Вас?
БУТОН[Вземете профила си безплатно →]
Подготвихме профил за [business_name] в Nevumo — платформата, където клиентите намират услуги за почистване във Варшава. Профилът ви чака. Нужни са само 2 минути.
С Nevumo ✓

Профилът ви е видим при търсене в Google
Клиентите се свързват директно с вас
Без комисиони

Комисионни платформи ✗

Клиентите търсят онлайн но не намират вас...
Комисионите на платформите растат всяка година
Комисиони от всяка поръчка

БУТОН[Вземете профила си безплатно →]
Димитър

Nevumo

Информация за обработване на лични данни (чл. 14 GDPR):

Nevumo обработва публично достъпни данни за вашата фирма от регистъра CEIDG (Полша).

Фирма: [business_name] | Адрес: [address] | Тел: [phone] | Имейл: [email]

Цел: показване на фирмен профил в Nevumo. Основание: чл. 6(1)(f) GDPR — законен интерес.

Администратор: ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ ООД | privacy@nevumo.com

Права: достъп, коригиране, изтриване — пишете на privacy@nevumo.com
[Отписване от имейли]

**BG шаблон — ВиК:** (същата структура, различни данни)
[HTML с лого]
10 707 клиента търсят ВиК услуги във Варшава всеки месец. Намират ли именно Вас?
БУТОН[Вземете профила си безплатно →]
Подготвихме профил за [business_name] в Nevumo — платформата, където клиентите намират ВиК майстори в Варшава. Профилът ви чака. Нужни са само 2 минути.
С Nevumo ✓

Профилът ви е видим при търсене в Google
Клиентите се свързват директно с вас
Без комисиони

Комисионни платформи ✗

Клиентите търсят онлайн — вас не ви намират
Комисионите на платформите растат всяка година
Комисиони от всяка поръчка

БУТОН[Вземете профила си безплатно →]
Димитър

Nevumo
[Същият GDPR footer]

[Отписване от имейли]

**BG шаблон — Масаж:**
[HTML с лого]
3 635 клиента търсят масаж в Варшава всеки месец. Намират ли именно Вас?
БУТОН[Вземете профила си безплатно →]
Подготвихме профил за [business_name] в Nevumo — платформата, където клиентите резервират масаж в Варшава. Профилът ви чака. Нужни са само 2 минути.
С Nevumo ✓

Профилът ви е видим при търсене в Google
Резервации онлайн — дни напред
Без комисиони

Комисионни платформи ✗

Клиентите търсят онлайн но не намират вас
Комисионите на платформите растат всяка година
Нямате директен контакт с клиента

БУТОН[Вземете профила си безплатно →]
Димитър

Nevumo
[Същият GDPR footer]

[Отписване от имейли]

---

### 3.3 Email #2 — Инсайт (Пт 18:00) — Plain text

**Subject:**
- Почистване: `Хигиенисти получават по 8 поръчки на седмица`
- ВиК: `ВиК майстор получава заявки 24/7`
- Масаж: `Масажисти получават резервации за 2 седмици напред`

**BG шаблон — Почистване:**
Здравейте, [business_name],
Забелязах нещо за Варшава. Хигиенисти като вас получават по 8 нови поръчки на седмица в Nevumo — директно, без посредник.

Въпрос: когато клиент търси почистване в Google, ще намери ли именно вас?
[Вземете профила си безплатно →]

Без ангажименти.
Поздрави

Димитър

Nevumo
[Отписване от имейли]

**BG шаблон — ВиК:**
Здравейте, [business_name],
Забелязах нещо за пазара във Варшава.

ВиК майстор като вас е в Nevumo от седмица. Получава заявки 24/7.

Въпрос: когато клиент има авария в 21:00 и търси в Google, ще ви намери ли?
[Вземете профила си безплатно →]

Без ангажименти.
Поздрави

Димитър

Nevumo
[Отписване от имейли]

**BG шаблон — Масаж:**
Здравейте, [business_name],
Забелязах нещо за Варшава. Масажисти в Nevumo получават заявки за 2 седмици напред — предвидим график, постоянни клиенти…

Въпрос: запълнен ли е графикът ви напред?
[Вземете профила си безплатно →]

Без ангажименти.
Поздрави

Димитър

Nevumo
[Отписване от имейли]

---

### 3.4 Email #3 — Социално доказателство (Ср 10:00) — Plain text

**Subject:**
- Почистване: `Ето какво стана с онези хигиенисти`
- ВиК: `Ето какво стана с онзи ВиК майстор`
- Масаж: `Ето какво стана с онзи масажист`

**BG шаблон — Почистване:**
Здравейте, [business_name],
Нещо преди да затворя профила ви:

Хигиенистите за които писах, след 10 дни в Nevumo избират кои поръчки да приемат. Без комисиони…

А как е при вас?
[Вземете профила си безплатно →]
[Отписване от имейли]
Поздрави

Димитър

**BG шаблон — ВиК:**
Здравейте, [business_name],
Нещо преди да затворя профила ви:

ВиК майсторът за когото писах, след 10 дни в Nevumo избира кои поръчки да приема. Без комисиони…

А как е при вас?
[Вземете профила си безплатно →]
[Отписване от имейли]
Поздрави

Димитър

**BG шаблон — Масаж:**
Здравейте, [business_name],
Нещо преди да затворя профила ви:

Масажистът за когото писах, след 10 дни в Nevumo избира кои поръчки да приема. Без комисиони…

А как е при вас?
[Вземете профила си безплатно →]
[Отписване от имейли]
Поздрави

Димитър

---

### 3.5 Email #4 — Break-up (Пн 10:00) — Plain text — Общ за всички категории

**Subject:** `Тази седмица изтриваме непотърсените профили`

**BG шаблон:**
Здравейте, [business_name],
Разбирам ако моментът не е подходящ. Тази седмица изтриваме непотърсените профили за Варшава. Исках да проверя все пак преди да продължа.
Ако сте заинтересовани — вземете профила си тук: → [Да, искам профила си]
Ако не сега — кликнете тук и ще се върна след време: → [Не сега]
В двата случая — без ангажимент.
Димитър

Nevumo
[Отписване от имейли]

---

### 3.6 Feedback Page — nevumo.com/pl/outreach/feedback

**Заглавие:** `Разбирам, ако моментът не е подходящ`

**Текст:** `За да можем да подобрим комуникацията, кажете ни защо не сега:`

**Опции (radio buttons):**
1. `Вече работя с друга платформа`
2. `Не ми трябва нови клиенти в момента`
3. `Искам повече информация`
4. `Друго` (с опционално текстово поле)

**Бутон:** `Изпрати`

**Success messages:**
- Опции 1 и 2: `Благодаря! Ще се свържем отново след 3 месеца.`
- Опция 3: `Благодаря! Ще се свържем до 48 часа с вас.`
- Опция 4: `Получено. Димитър ще го прочете лично.`

**Footer:** `Димитър | Nevumo | privacy@nevumo.com`

**Технически детайли:**
- URL параметри: `email={email}&token={hmac}` за валидация
- Backend endpoint: `POST /api/v1/outreach/feedback`
- DB таблица: `outreach_feedback` (email, reason, custom_text, created_at)
- Security: HMAC валидация на токена

> ⚠️ PL версиите на всички шаблони се създават в следващата фаза.

---

## РАЗДЕЛ 4 — Post-Claim Activation Sequence (Фунел 2)

> Тригерира се автоматично след успешен claim. Изпраща се чрез Resend.
> Цел: claimed → активен провайдър с попълнен профил.

### Activation Email #1 — час след claim

**Subject:** `Profil aktywny ✓ — zrób jeszcze jeden krok`
**Trigger:** POST /api/v1/providers/claim/{token} success → queue job

```
Witaj [business_name],

Twój profil na Nevumo jest już aktywny.

Jeden krok, który zwiększa szanse na pierwsze zapytanie 3x:
→ Dodaj zdjęcie profilowe i krótki opis swojej firmy

[Uzupełnij profil →]   (link do /provider/dashboard/profile)

Klienci 4x częściej kontaktują się z dostawcami ze zdjęciem.

Dimitar
Nevumo
```

### Activation Email #2 — ден 3 (само ако профилът е под 80% completeness)

**Subject:** `Twój profil jest w 60% gotowy — klienci widzą to`

```
Cześć [business_name],

Sprawdziłem Twój profil — brakuje jeszcze kilku rzeczy, które
klienci sprawdzają przed kontaktem.

Co zostało:
□ Zdjęcie profilowe
□ Opis usług (2-3 zdania)
□ Obszar działania (dzielnice Warszawy)

[Dokończ profil w 3 minuty →]

Po uzupełnieniu Twój profil pojawi się wyżej w wynikach.

Dimitar
```

### Activation Email #3 — ден 7

**Subject:** `Klient szuka [usługi] w Twojej okolicy`

```
Cześć [business_name],

W tym tygodniu [N] klientów szukało [usługi] w Warszawie przez Nevumo.

Twój profil jest aktywny — upewnij się, że jesteś gotowy na pierwsze zapytanie.

[Zobacz swój profil →]

Dimitar
```

### Activation Email #4 — ден 14 (само за тези с попълнен профил)

**Subject:** `Twój profil widoczny dla [search_volume] klientów miesięcznie`

```
Cześć [business_name],

Szybka aktualizacja: Twój profil na Nevumo jest teraz widoczny
dla potencjalnych klientów szukających [usługi] w Warszawie.

W tym miesiącu: [search_volume] wyszukiwań w Twojej kategorii.

Zero prowizji. Zero subskrypcji. Tylko bezpośredni kontakt.

Dimitar
```

---

## РАЗДЕЛ 5 — QA GATE ⛔

> **АБСОЛЮТНА ЗАБРАНА:** Нито един реален имейл не излиза докато
> всеки checkbox по-долу не е ✅.
> 
> Тестовите инструменти са изброени при всяка точка.
> Статус: ⏳ = не тестван | ✅ = преминал | ❌ = провален

### 5.1 Technical QA Checklist

#### A. Email Deliverability

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| A1 | mail-tester.com score ≥ 9/10 за outreach имейл (cleaning версия) | mail-tester.com (ръчно) | ⏳ |
| A2 | mail-tester.com score ≥ 9/10 за outreach имейл (plumbing версия) | mail-tester.com (ръчно) | ⏳ |
| A3 | mail-tester.com score ≥ 9/10 за outreach имейл (massage версия) | mail-tester.com (ръчно) | ⏳ |
| A4 | SPF record верифициран за nevumo.com | Resend Dashboard / MXToolbox | ⏳ |
| A5 | DKIM верифициран за nevumo.com | Resend Dashboard / MXToolbox | ⏳ |
| A6 | DMARC policy активна | MXToolbox.com | ⏳ |
| A7 | Имейлът не попада в Gmail spam (тест до лична Gmail сметка) | Ръчно | ⏳ |
| A8 | Имейлът не попада в Outlook spam | Ръчно | ⏳ |

#### B. Email Rendering

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| B1 | Gmail web (desktop) — коректен layout, изображения зареждат | Claude in Chrome | ⏳ |
| B2 | Gmail mobile iOS — CTA бутон видим ПРЕДИ скрол | Claude in Chrome / ръчно на iPhone | ⏳ |
| B3 | Gmail mobile Android — CTA бутон видим ПРЕДИ скрол | Ръчно | ⏳ |
| B4 | Outlook 365 — layout не е счупен | Ръчно | ⏳ |
| B5 | Apple Mail desktop — коректен rendering | Ръчно | ⏳ |
| B6 | Jinja2 variables попълнени (без {{ }} в output) | mcp-playwright / ръчно | ⏳ |
| B7 | Unsubscribe линк видим в footer на всеки имейл | Claude in Chrome | ⏳ |
| B8 | Preview text видим в Gmail inbox list | Ръчно | ⏳ |
| B9 | Subject lines под 60 символа (preview не е отрязан) | Ръчно count | ⏳ |
| B10 | Cleaning/Plumbing/Massage — различни subject lines | mcp-playwright | ⏳ |

#### C. Claim Flow — Error States

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| C1 | Claim страница зарежда за unclaimed провайдър (valid state) | mcp-playwright | ⏳ |
| C2 | Claim страница показва correct error за not_found token | mcp-playwright | ⏳ |
| C3 | Claim страница показва correct error за already_claimed | mcp-playwright | ⏳ |
| C4 | Claim страница показва correct error за expired token | mcp-playwright | ⏳ |
| C5 | Claim страница показва correct error за invalid format token | mcp-playwright | ⏳ |

#### C2. Claim Flow — Fast Path (email match ✅)

> Тества директен claim когато `current_user.email == provider.scraped_email`

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| C6 | Outreach имейл → кликва линк → Google OAuth (scraped_email) → Auto-claim → Dashboard | Claude in Chrome | ⏳ |
| C7 | Outreach имейл → кликва линк → email/парола (scraped_email) → Auto-claim → Dashboard | Claude in Chrome | ⏳ |
| C8 | Банер на страницата → регистрира се СЪС scraped_email → директен claim (без код) | mcp-playwright | ⏳ |
| C9 | Art. 14 GDPR имейл пристига след fast path claim | Ръчно (провери inbox) | ⏳ |
| C10 | Welcome имейл пристига след claim (не дублира Art. 14) | Ръчно (провери inbox) | ⏳ |
| C11 | Draft provider record е изтрит след claim | mcp-playwright / DB check | ⏳ |
| C12 | Provider Dashboard показва claimed профил | Claude in Chrome | ⏳ |

#### C3. Claim Flow — Verification Path (email mismatch ❌)

> Тества верификационен код когато `current_user.email ≠ provider.scraped_email`
> Симулира: собственик с личен Gmail или потенциален измамник от банера

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| C13 | Банер → регистрира се с РАЗЛИЧЕН имейл → backend НЕ клеймва веднага | mcp-playwright | ⏳ |
| C14 | Backend изпраща 6-цифрен код до `scraped_email` | Ръчно (провери inbox на scraped_email) | ⏳ |
| C15 | Frontend показва "Въведете кода от имейла на бизнеса" | mcp-playwright | ⏳ |
| C16 | Правилен код → claim успешен → Dashboard | mcp-playwright | ⏳ |
| C17 | Грешен код → error "Невалиден код" (без claim) | mcp-playwright | ⏳ |
| C18 | Изтекъл код (TTL 24h) → error "Кодът е изтекъл" | mcp-playwright (манипулира expires_at в DB) | ⏳ |
| C19 | Вторичен опит с изтекъл код НЕ клеймва профила | mcp-playwright / DB check | ⏳ |
| C20 | Art. 14 GDPR имейл пристига след verification path claim | Ръчно (провери inbox) | ⏳ |

#### C4. Claim Flow — NULL scraped_email (блокиран)

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| C21 | Провайдър без scraped_email + различен имейл → error "cannot_verify_ownership" | mcp-playwright | ⏳ |
| C22 | Frontend показва "Свържете се с support@nevumo.com" | mcp-playwright | ⏳ |

#### D. Unsubscribe механизъм

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| D1 | Unsubscribe линк в имейла е кликваем и отваря страница | Claude in Chrome | ⏳ |
| D2 | Clicking unsubscribe → записва в outreach_unsubscribes | mcp-playwright / DB check | ⏳ |
| D3 | Confirmation страница се показва на полски | mcp-playwright | ⏳ |
| D4 | Email #2 НЕ се изпраща до unsubscribed адрес | mcp-playwright + bulk script dry run | ⏳ |
| D5 | Email #3 НЕ се изпраща до unsubscribed адрес | mcp-playwright + bulk script dry run | ⏳ |
| D6 | Email #4 НЕ се изпраща до unsubscribed адрес | mcp-playwright + bulk script dry run | ⏳ |
| D7 | HMAC токен верификация в unsubscribe endpoint работи | mcp-playwright | ⏳ |
| D8 | Невалиден token връща 400, не 500 | mcp-playwright | ⏳ |

#### E. Resend Webhooks

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| E1 | email.delivered event записва се в outreach_events | Resend Dashboard / DB check | ⏳ |
| E2 | email.opened event записва се в outreach_events | Resend Dashboard / DB check | ⏳ |
| E3 | email.clicked event записва се в outreach_events | Resend Dashboard / DB check | ⏳ |
| E4 | email.bounced → email в outreach_unsubscribes (reason=bounce) | Resend test event | ⏳ |
| E5 | email.complained → email в outreach_unsubscribes (reason=complaint) | Resend test event | ⏳ |
| E6 | Webhook signature верификация (невалиден подпис → 401) | curl / mcp-playwright | ⏳ |

#### F. Sequence Logic

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| F1 | Email #2 НЕ се изпраща до вече claimed провайдър | bulk script dry run | ⏳ |
| F2 | Email #2 НЕ се изпраща до bounced адрес | bulk script dry run | ⏳ |
| F3 | outreach_sequence_log записва всяка стъпка | DB check | ⏳ |
| F4 | Idempotency: повторно пускане на скрипта НЕ изпраща дубликати | bulk script dry run ×2 | ⏳ |
| F5 | Category routing: cleaning → cleaning template (не plumbing) | bulk script dry run | ⏳ |
| F6 | Category routing: plumbing → plumbing template | bulk script dry run | ⏳ |
| F7 | Category routing: massage → massage template | bulk script dry run | ⏳ |

#### G. SMS

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| G1 | Тест SMS до +48XXXXXXXXX (собствен номер) | SMSapi.pl скрипт | ⏳ |
| G2 | Claim линк в SMS е коректен и кратък | Ръчно | ⏳ |
| G3 | SMS дължина ≤ 160 символа | Ръчно count | ⏳ |
| G4 | STOP механизъм в SMS работи | SMSapi.pl | ⏳ |
| G5 | Delivery report получен от SMSapi.pl | SMSapi.pl Dashboard | ⏳ |

#### H. Railway Scheduler

| # | Тест | Инструмент | Статус |
|---|---|---|---|
| H1 | Cron job се вижда в Railway Dashboard | Railway UI | ⏳ |
| H2 | Timezone Europe/Warsaw е конфигуриран | Railway env / скрипт log | ⏳ |
| H3 | Rate limiting (37s между имейли) работи | log output | ⏳ |
| H4 | Dry run (--dry-run flag) показва правилни адреси без изпращане | CLI | ⏳ |

### 5.2 Пилотна Вълна — 20-30 реални бизнеса

> **Пилотът е задължителен и предхожда bulk изпращането с минимум 14 дни.**

#### Избор на пилотни адреси

**Критерии:**
- Реални бизнеси от `outreach_ready.csv` (след Task 2A)
- По ~7-10 от всяка категория (cleaning, plumbing, massage)
- Микс: малки (1 човек) + средни (2-5 човека) бизнеси
- Само с валиден бизнес имейл (не @gmail.com, не @wp.pl)
- Ръчно прегледани — бизнесът да изглежда активен

**Файл:** `pilot_wave.csv` (20-30 реда, отделен от основния CSV)

#### Какво наблюдаваме (14 дни след Email #1)

| Метрика | Мин. приемлив резултат | Действие при провал |
|---|---|---|
| Email delivery rate | > 90% | Провери SPF/DKIM, смени sender |
| Open rate Email #1 | > 25% | Промени subject line преди bulk |
| Click rate Email #1 | > 8% | Промени copy/CTA |
| Bounce rate | < 5% | Почисти списъка |
| Spam complaint rate | < 0.1% | СПРИ — анализирай причината |
| Claimed от пилота | > 1 (поне 1 реален claim) | Провери claim flow |

#### Пилотен schedule

| Действие | Дата/Ден | Отговорник |
|---|---|---|
| Избор на 20-30 адреса | Ден 0 | Dimitar (ръчно) |
| Изпращане Email #1 | Вторник 10:00 Warsaw | Railway scheduler |
| Проверка на opens/bounces | 48 часа след #1 | Claude in Chrome / Resend Dashboard |
| SMS до пилота (тел. номера) | Ден 0 паралелно | SMSapi.pl скрипт |
| Email #2 | Петък 18:00 Warsaw | Railway scheduler |
| Email #3 | Следваща сряда 10:00 | Railway scheduler |
| Email #4 | Следващ понеделник 10:00 | Railway scheduler |
| **Анализ на пилота** | **Ден 14** | **Dimitar + Claude** |
| **Go/No-Go за bulk** | **Ден 14** | **Dimitar** |

> ⚠️ **Go/No-Go е задължително решение.** Без него bulk не стартира.

---

## РАЗДЕЛ 6 — Bulk Campaign Execution

> Стартира само след: ✅ всички QA checkboxes зелени + ✅ пилот Go + ✅ Resend Pro активен

### 6.1 Pre-Bulk Checklist

- [ ] Всички Раздел 5.1 checkboxes = ✅
- [ ] Пилот = ✅ Go decision
- [ ] Resend Pro upgrade = ✅
- [ ] E2E cleanup (тестови провайдъри изтрити) = ✅
- [ ] outreach_ready.csv генериран от Task 2A = ✅
- [ ] pilot_wave.csv адресите ИЗКЛЮЧЕНИ от bulk CSV = ✅

### 6.2 Bulk Send Timeline

| Имейл | Ден | Час (Warsaw) | Действие |
|---|---|---|---|
| Email #1 | Вторник | 10:00 | Railway cron → step 1 (skip пилот адреси) |
| SMS | Вторник | 10:30 | SMSapi.pl скрипт (230 телефона) |
| Email #2 | Петък | 18:00 | Railway cron → step 2 (skip claimed + unsubscribed) |
| Email #3 | Следваща Сряда | 10:00 | Railway cron → step 3 |
| Email #4 | Следващ Понеделник | 10:00 | Railway cron → step 4 |

### 6.3 Monitoring During Bulk

**Проверки след Email #1 (до 24 часа):**
- Resend Dashboard → Delivery rate, Bounce rate, Complaint rate
- `SELECT * FROM outreach_events WHERE event_type='complained'` → ако > 0, пауза и анализ
- `SELECT COUNT(*) FROM outreach_sequence_log WHERE sequence_step=1` → очакван брой

**Стоп условия (незабавна пауза на кампанията):**
- Bounce rate > 5%
- Complaint rate > 0.1%
- Технически грешки в Railway logs

---

## РАЗДЕЛ 7 — Анализ & Re-engagement

### 7.1 30-дневен анализ (след Email #4)

**Query:**
```sql
SELECT
  category,
  COUNT(DISTINCT email) as sent,
  COUNT(DISTINCT CASE WHEN event_type='opened' THEN email END) as opened,
  COUNT(DISTINCT CASE WHEN event_type='clicked' THEN email END) as clicked,
  COUNT(DISTINCT CASE WHEN p.is_claimed=TRUE THEN sl.email END) as claimed
FROM outreach_sequence_log sl
LEFT JOIN outreach_events oe ON sl.email = oe.email
LEFT JOIN providers p ON p.scraped_email = sl.email
WHERE sl.sequence_step = 1
GROUP BY category;
```

**Решения след анализа:**
- Open rate < 20% → A/B тест на subject lines за re-engagement
- Click rate < 5% → Промяна на copy
- Claimed < 5% → Анализ на claim page drop-off

### 7.2 "NOT NOW" Feedback Loop

При отговор "NIE TERAZ" на Email #4 → redirect към `/pl/outreach/feedback?reason=`:
4 бутона на полски:
1. "Wже работя с друга платформа" → `reason=competitor`
2. "Нямам нужда от нови клиенти" → `reason=no_need`
3. "Исках повече информация" → `reason=more_info`
4. "Звучи скъпо" → `reason=price`

Записва се в `outreach_feedback` таблица. Дава market intelligence за бъдещи кампании.

### 7.3 90-дневен Re-engagement (автоматичен)

**Trigger:** 90 дни след Email #4 + `is_claimed=FALSE` + не в `outreach_unsubscribes`

**Subject:**
- Cleaning: `W tym miesiącu 7 000 klientów szukało sprzątania w Warszawie`
- Plumbing: `Aktualizacja: hydraulicy na Nevumo w Twojej dzielnicy`
- Massage: `Nowe rezerwacje masażu w Warszawie — wolne miejsca`

**Различен angle:** По това време ще имаме реални claimed провайдъри = реален social proof.

---

## РАЗДЕЛ 8 — Метрики за Успех

### Conversion Targets

| Метрика | Минимален | Целеви | Отличен |
|---|---|---|---|
| Email delivery rate | 90% | 95%+ | 97%+ |
| Open rate (средно 4 имейла) | 25% | 40% | 50%+ |
| Claim conversion | 5% | 10% | 15%+ |
| Claimed провайдъри | 50 | 100 | 150+ |
| Active провайдъри (попълнен профил) | 30 | 70 | 120+ |

### Monitoring Schedule

| Период | Действие | Инструмент |
|---|---|---|
| След всеки имейл (24h) | Bounce/complaint check | Resend Dashboard + DB |
| Седмично | Opens/clicks по категория | `outreach_events` query |
| Ден 14 (след пилот) | Go/No-Go за bulk | Анализ с Claude |
| Ден 30 | Пълен анализ, оптимизации | SQL + Resend Dashboard |
| Ден 90 | Re-engagement decision | SQL + анализ |

---

## РАЗДЕЛ 9 — Технически референции

### Нови DB таблици (Alembic migrations)

```sql
-- 1. outreach_unsubscribes
CREATE TABLE outreach_unsubscribes (
    email TEXT PRIMARY KEY,
    unsubscribed_at TIMESTAMPTZ DEFAULT NOW(),
    reason TEXT CHECK (reason IN ('user_request', 'bounce', 'complaint'))
);

-- 2. outreach_events
CREATE TABLE outreach_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    resend_message_id TEXT NOT NULL,
    email TEXT NOT NULL,
    event_type TEXT NOT NULL,
    occurred_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_outreach_events_email ON outreach_events(email);
CREATE INDEX idx_outreach_events_type ON outreach_events(event_type);

-- 3. outreach_sequence_log (замества outreach_sent_log.csv)
CREATE TABLE outreach_sequence_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL,
    business_name TEXT,
    category TEXT,
    sequence_step INTEGER NOT NULL,
    resend_message_id TEXT,
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    status TEXT DEFAULT 'sent',
    UNIQUE(email, sequence_step)
);
CREATE INDEX idx_outreach_seq_email ON outreach_sequence_log(email);

-- 4. outreach_feedback
CREATE TABLE outreach_feedback (
    email TEXT PRIMARY KEY,
    reason TEXT,
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Нови файлове

```
apps/api/
├── routes/
│   ├── outreach.py          # Unsubscribe endpoint + feedback
│   ├── webhooks.py          # Resend webhook receiver
│   └── providers.py         # Claim endpoints (email matching + verification)
├── scripts/
│   ├── seed_unclaimed_providers.py    # Task 2A
│   ├── run_outreach_sequence.py       # Railway scheduler script
│   ├── templates/
│   │   ├── outreach_email_pl.html     # Email #1 (update: preview text + unsubscribe)
│   │   ├── outreach_email_2_pl.html   # Email #2 (plain text × 3 категории)
│   │   ├── outreach_email_3_pl.html   # Email #3 (plain text × 3 категории)
│   │   ├── outreach_email_4_pl.html   # Email #4 (plain text × 3 категории)
│   │   ├── activation_email_1_pl.html # Post-claim #1
│   │   ├── activation_email_2_pl.html # Post-claim #2
│   │   ├── activation_email_3_pl.html # Post-claim #3
│   │   ├── activation_email_4_pl.html # Post-claim #4
│   │   └── claim_verification_pl.html # 6-цифрен код за верификация при банер claim
│   └── pilot_wave.csv                 # 20-30 ръчно избрани адреса

apps/web/app/[lang]/
├── outreach/
│   ├── unsubscribe/page.tsx   # Unsubscribe confirmation page
│   └── feedback/page.tsx      # NOT NOW feedback page
└── claim/[token]/
    └── verify/page.tsx        # Verification code input (за non-matching email)
```

### Railway команди

```bash
# Seed unclaimed providers
railway run python3.13 -m apps.api.scripts.seed_unclaimed_providers

# E2E cleanup
railway run python3.13 -m apps.api.scripts.e2e_outreach_cleanup

# Dry run (без изпращане)
railway run python3.13 -m apps.api.scripts.run_outreach_sequence --step 1 --dry-run

# Manual trigger (при нужда)
railway run python3.13 -m apps.api.scripts.run_outreach_sequence --step 1
```

### Критични константи

```python
# apps/api/scripts/run_outreach_sequence.py
RATE_LIMIT_DELAY = 37  # секунди между имейли (100/час)
RESEND_FROM = "Dimitar z Nevumo <support@nevumo.com>"
TIMEZONE = "Europe/Warsaw"

# категория → search volume (за personalization)
SEARCH_VOLUME = {
    "cleaning": 7000,
    "plumbing": 5400,
    "massage": 6900
}

# категория → полски label
CATEGORY_LABEL_PL = {
    "cleaning": "sprzątania",
    "plumbing": "usług hydraulicznych",
    "massage": "masażu"
}
```

---

## Appendix: Пълен Task Order — Правилен ред за изпълнение

> Никаква фаза не стартира докато предишната не е 100% завършена и тествана.

---

### ФАЗА 0 — Оправяме всичко преди кампанията

[x] Stale localStorage crash (all code paths) — RESOLVED (June 26, 2026):
    - getAuthToken() wrapped in try-catch
    - isAuthenticated() document.cookie wrapped in try-catch
    - ClaimProcessor.tsx sessionStorage wrapped in try-catch
    - AuthHeaderButton.tsx: replaced direct localStorage read with getAuthUser()/getAuthToken() from auth-store.ts
    - Root cause: AuthHeaderButton read raw { v:"2", user: UserInfo } wrapper as AuthUser → user.email undefined → charAt crash
    - E2E verified: claim flow works for returning visitors (no incognito)
[ ] Pre-launch UX fixes:
    [x] Double "Nevumo" на claim page ✅ ЗАВЪРШЕН (26 юни 2026)
       - Анализ показа, че няма проблем с double "Nevumo"
       - Всички срещания са логични и контекстуално правилни
       - Header лого е стандартно за всички страници
       - Няма нужда от корекции
    [x] CTA above fold на мобилно и десктоп ✅ ЗАВЪРШЕН (26 юни 2026)
       - Добавени 2 инлайн CTA бутона за desktop и iOS 26+ mobile
       - Първи бутон: след provider card (above fold на мобилно)
       - Втори бутон: преди time signal (най-долу)
       - Sticky bar остава за non-iOS 26 mobile
       - Файлове: apps/web/app/[lang]/claim/[token]/page.tsx
       - E2E verified: бутоните работят коректно на desktop и mobile
    [x] Email logo качен на R2 (images.nevumo.com) ✅ ЗАВЪРШЕН (26 юни 2026)
       - Логото е качено на https://images.nevumo.com/nevumo-logo.png
       - Всички email templates използват R2 URL
       - Скрипт: apps/api/scripts/upload_logo_to_r2.py
       - Templates: outreach_email_pl.html, claim_verification_pl.html, article14_confirmation_pl.html
    [x] Email subject line под 50 символа → проверка + корекция ✅ ЗАВЪРШЕН (28 юни 2026)
[x] Технически дълг (cleanup) ✅ ЗАВЪРШЕН (28 юни 2026):
    [x] AutoClaimTrigger.tsx — изтрит (заменен от ClaimProcessor) ✅
    [x] ClaimCTAWrapper.tsx — изтрит (заменен от ClaimProcessor) ✅
    [x] LoginClient.tsx, OAuthTermsClient.tsx, oauth-callback/page.tsx — addFromAuthParam() премахнат, actions.ts изтрит ✅

---

### ФАЗА 1 — БАНЕР

⚠️ Ред е критичен: първо тест, после реални данни.

[ ] Ръчен тест на целия Banner flow (симулирани провайдъри)
[ ] Блокер 8: seed_unclaimed_providers.py — реалните Warsaw провайдъри в Neon

---

### ФАЗА 2 — ИМЕЙЛ

[ ] HTML шаблони:
    [ ] outreach_email_pl.html — добавяне на preview text (текстът е в Раздел 3.2)
    [ ] outreach_email_2_pl.html — Email #2 × 3 категории (текстът е в Раздел 3.3)
    [ ] outreach_email_3_pl.html — Email #3 × 3 категории (текстът е в Раздел 3.4)
    [ ] outreach_email_4_pl.html — Email #4 × 3 категории (текстът е в Раздел 3.5)
    [ ] activation_email_1_pl.html — post-claim #1 (текстът е в Раздел 4)
    [ ] activation_email_2_pl.html — post-claim #2
    [ ] activation_email_3_pl.html — post-claim #3
    [ ] activation_email_4_pl.html — post-claim #4
    Модел: Kimi-2.6
[ ] Задача 6А: Profile Strength Email — Claude (текст) → Kimi-2.6 (template) → SWE-1.6 (backend trigger)
[ ] Блокер 9: run_outreach_sequence.py — Railway Cron scheduler за 4-email sequence → Kimi-2.6
[ ] Преглед на всички имейл текстове (с Dimitar)
[ ] Реален тест — изпращане до собствени имейли:
    [ ] mail-tester.com score ≥ 9/10 (и трите категории)
    [ ] SPF / DKIM / DMARC верифицирани (MXToolbox)
    [ ] Gmail web desktop — layout ОК
    [ ] Gmail mobile iOS — CTA видим ПРЕДИ скрол
    [ ] Outlook 365 — layout не е счупен
    [ ] Preview text видим в Gmail inbox list
    [ ] Unsubscribe линк видим в footer
    [ ] Jinja2 variables попълнени (без {{ }} в output)
    [ ] Subject lines под 50 символа
    Инструмент: Claude in Chrome + ръчно

---

### ФАЗА 3 — СМС

[ ] SMS скрипт за SMSapi.pl (230 телефона) → Kimi-2.6
[ ] Тест до собствен номер:
    [ ] Claim линк е коректен
    [ ] Дължина ≤ 160 символа
    [ ] STOP механизъм работи
    [ ] Delivery report получен от SMSapi.pl Dashboard

---

### ФАЗА 4 — QA GATE ⛔

[ ] Пълен Checklist 5.1 A-H (всички ✅) → SWE-1.6 + mcp-playwright + ръчно
    (Вж. Раздел 5 за пълния списък)

---

### ФАЗА 5 — ПИЛОТ

[ ] Блокер 10: E2E cleanup — railway run python3.13 -m apps.api.scripts.e2e_outreach_cleanup
[ ] Resend Pro upgrade ($20/мес) → Dimitar (ръчно в Resend Dashboard)
[ ] Pilot wave CSV — 20-30 ръчно избрани адреса → Dimitar
    (пилотните адреси да бъдат ИЗКЛЮЧЕНИ от bulk CSV)
[ ] Pilot wave изпращане → Email #1 → #2 → #3 → #4
[ ] Анализ след 14 дни → Claude + Resend Dashboard
[ ] Go/No-Go решение → Dimitar

---

### ФАЗА 6 — BULK CAMPAIGN

Стартира само след: ✅ QA Gate + ✅ Пилот Go + ✅ Resend Pro

[ ] Email #1 bulk send (вторник 10:00 Warsaw) → Railway scheduler
[ ] SMS bulk send (230 телефона) → SMSapi.pl скрипт
[ ] Monitoring 24h след #1 → Resend Dashboard + DB
[ ] Email #2, #3, #4 → Railway scheduler (автоматично)
[ ] 30-дневен анализ → SQL + Claude

---

### POST-CAMPAIGN

[ ] "NOT NOW" feedback processing → DB analysis
[ ] 90-дневен re-engagement setup → Railway scheduler
[ ] Task 4Г пълна имплементация (6-цифрен код за email mismatch) → SWE-1.6 + Kimi-2.6

---

## KNOWN ISSUES — Pre-Launch (June 23, 2026)

### ✅ РЕШЕНИ (23 юни 2026)

**Issue 1 + Issue 2 — Magic Link Claim Flow** ✅ ЗАВЪРШЕН
- Решение: claim токенът от имейла = доказателство за самоличност
- POST /providers/claim/{token} вече работи БЕЗ JWT
- auto-login/register от scraped_email чрез get_or_create_claim_user()
- Нов ClaimProcessor.tsx замества AutoClaimTrigger + ClaimCTAWrapper
- Cookie = единствен source of truth (auth-store.ts)
- Redirect логика:
  * Нов провайдър → wizard Step 1 (category + city pre-filled)
  * Returning незавършен → wizard Step 1
  * Returning завършен (description + photo + услуги) → dashboard overview
  * Вече регистриран с реален профил → реален dashboard (scraped stub изтрит)
- Wizard heading: "Witamy!" при първо влизане (sessionStorage)
- Wizard subtitle: wizard_welcome_subtitle (34 езика) докато не завърши
- Commits: c705215
- Тествани сценарии: ✅ нов провайдър, ✅ returning незавършен,
  ✅ returning завършен, ✅ вече регистриран

**Issue 3 — Photo upload** ✅ ЗАВЪРШЕН
- Photo upload работи на desktop (тестван 23 юни 2026)
- Fix беше деплойнат в по-ранен commit

**Issue 4 — JWT expiry причинява безкраен loop** ✅ РЕШЕН (23 юни 2026)
- Root cause: authFetch() и clientFetch() не обработваха 401 → redirect loop между provider и client dashboard
- Fix 1: 401 interceptor в authFetch() → apps/web/lib/provider-api.ts
- Fix 2: 401 interceptor + null safety в clientFetch() → apps/web/lib/client-api.ts
- Pattern: 401 → clearAuth() → window.location.replace(/{lang}/auth) → full page reload
- Null safety: json.error?.code ?? 'UNKNOWN_ERROR' предотвратява crash при нестандартен error body
- Тестван мануално в production: provider dashboard ✅ + client dashboard ✅

### 🟡 ВАЖНИ — Влияят на UX

**Issue 5 — Banner Claim Flow 🟡 ЧАСТИЧНО ИМПЛЕМЕНТИРАН (24 юни 2026)**
Имплементирано:
- ClaimProfileBanner.tsx: показва scraped_email под името на бизнеса
- ClaimProfileBanner.tsx: ?source=banner добавен към href
- ClaimProcessor.tsx: обработва 202 → redirect към /verify?sent_to=...
- ClaimProcessor.tsx: обработва 401 → redirect към /auth
- verify/page.tsx: подава sentTo prop към VerifyCodeForm
- VerifyCodeForm.tsx: показва "Kod wysłano na: {sentTo}"
- VerifyCodeForm.tsx: праща lang параметър към API за запазване на езиковата преценност (28 юни 2026)
- providers.py: source=banner логика (401/422/202/200 сценарии)
- providers.py: masked email в sent_to полето на 202 response

Проблем (открит при E2E тест): Архитектурата изисква login ПРЕДИ кода.

Правилният flow: Banner → /verify директно (без login) → код →
get_or_create_claim_user → JWT → onboarding.
Пълният план за финализиране: вж. Блокери 7A–7G по-долу.

### 🧹 ТЕХНИЧЕСКИ ДЪЛГ

**Cleanup — остарели файлове (не блокират кампанията):**
- AutoClaimTrigger.tsx — заменен от ClaimProcessor, не е изтрит
- ClaimCTAWrapper.tsx — заменен от ClaimProcessor, не е изтрит
- LoginClient.tsx — ?from=auth логиката не е почистена

---

*Документът се обновява след всяка завършена задача.*
*Git: `git push nevumo-git main` след всяка актуализация.*
