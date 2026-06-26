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
- Unclaimed banner на Provider Full Page (Task 4Б)
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

### Блокер 7А — Banner Flow Redesign: No auth before code 🔴
(Изисква: Блокер 6. Блокира: Блокери 7Б–7Ж, Блокер 8)
Проблем: Сегашният banner flow изисква login ПРЕДИ потребителят да въведе кода.

Това е грешна архитектура — кодът сам по себе си е доказателство за собственост.
Правилен flow:
Banner click → POST /claim/{token}?source=banner (без JWT) →
  backend: генерира код → изпраща до scraped_email → връща 202
  frontend: redirect → /claim/{token}/verify?sent_to=b***@firma.pl
User въвежда код → POST /claim/{token}/verify →
  backend: verify code → get_or_create_claim_user(scraped_email) →
  claims provider → връща JWT + user данни
Frontend: saveAuth(JWT) → redirect → /provider/dashboard/profile (wizard)

Промени в backend (apps/api/routes/providers.py):
- claim_provider() при source=banner: НЕ изисква auth
- Ако provider.scraped_email = NULL → 422 NO_EMAIL
- Ако provider.is_claimed = True → 409 ALREADY_CLAIMED
- В противен случай: генерира код, записва PendingClaimVerification,
  изпраща email, връща 202 с masked sent_to — без JWT проверка
- verify_claim(): след валиден код → извиква get_or_create_claim_user(scraped_email) →
  claims provider → връща JWT + user + redirect info

Промени в frontend:
- ClaimProcessor.tsx: премахни 401 handler — banner flow не изисква auth
- ClaimProcessor.tsx: при 202 — redirect директно към /verify (вече е)
- VerifyCodeForm.tsx: след успешен verify → saveAuth(JWT) → redirect към wizard

Модел: SWE-1.6 (backend) + Kimi-2.6 (frontend)

---

### Блокер 7Б — Magic Link Login за passwordless потребители 🔴
(Изисква: Блокер 7А. Блокира: Блокер 8)
Проблем: Потребители, създадени чрез get_or_create_claim_user(), нямат парола.

Ако затворят браузъра — нямат начин да се върнат. Заключени са завинаги.
Решение — Magic Link система:

Нов endpoint: POST /api/v1/auth/magic-link — приема email, изпраща magic link
Нов endpoint: GET /api/v1/auth/magic-link/verify?token={token} — верифицира, връща JWT
Magic link: https://nevumo.com/{lang}/auth/magic-link?token={token} (24h TTL)
DB: нова таблица magic_link_tokens (token, user_id, expires_at, used)
Email template: magic_link_pl.html
Работи паралелно с парола и Google OAuth

Файлове:
- apps/api/routes/auth.py — 2 нови endpoints
- apps/api/models.py — MagicLinkToken модел
- Alembic migration
- apps/api/services/email_service.py — send_magic_link_email()
- apps/web/app/[lang]/auth/magic-link/page.tsx — landing за magic link

Модел: SWE-1.6 (backend) + Kimi-2.6 (frontend)

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

### Блокер 7Г — "Изпрати ми нов login link" на Auth страницата 🟡
(Изисква: Блокер 7Б. Може паралелно с 7В)
Проблем: Passwordless потребители, загубили magic link-а, нямат начин за вход.
Решение:
- Auth страница → под email/password формата → link "Нямате парола? Влезте с имейл линк →"
- Кликване → показва поле за email → изпраща нов magic link
- Използва POST /api/v1/auth/magic-link от Блокер 7Б

Модел: Kimi-2.6

---

### Блокер 7Д — Потвърждение на Outreach Flow ✅ ЗАВЪРШЕН (26 юни 2026)
(E2E верификация — само тестове, без код)

**QA резултати (26 юни 2026):**
- ✅ T1 (Happy Path): `/pl/claim/{token}` (без ?source=banner) → 200 → cookie `nevumo_auth_token` → redirect `/pl/provider/dashboard/profile?claimed=success` → wizard зареден, 0 console errors
- ✅ T2 (Already Claimed): Същият token → error UI "Ten link jest nieprawidłowy lub wygasł" → без unauthorized достъп, 0 console errors
- ✅ T3 (Invalid Token): Фалшив token → error UI "Profil, do którego prowadzi ten link, nie został znaleziony..." → чист error page, 0 console errors

Заключение: Email claim flow работи коректно след Блокер 7А промените в providers.py.

---

### Блокер 7Е — Onboarding Redirect Logic 🟡
(Изисква: Блокер 7А)
Проблем: При повторен login на вече claimнал потребител — системата не знае
на коя стъпка от onboarding-а е спрял.

Решение:
- При login → GET /api/v1/provider/profile → проверка на missing_fields
- Logic:
  - Няма description/photo → Step 1 (profile)
  - Няма услуги → Step 2 (services)
  - Всичко попълнено → Dashboard Overview

Файлове: ClaimProcessor.tsx, apps/api/routes/provider.py (добави missing_fields в response)
Модел: SWE-1.6 (backend) + Kimi-2.6 (frontend)

**⚠️ Dual-role потребители (добавено към 7Е):**
Nevumo ще има потребители с едновременна роля провайдър + клиент.
Redirect логиката при login (magic link, OAuth, email/password) трябва да покрива:
- role='provider' → /provider/dashboard
- role='client' → /client/dashboard
- Dual-role потребител → redirect по последно активната роля (use last_active_role
  field или role от JWT); switch-role endpoint съществува
Верифицирай MagicLinkClient.tsx redirect преди bulk кампанията.
Ако last_active_role не съществува в User модела → добави го като part of 7Е.

---

### Блокер 7Ж — Onboarding Pre-fill за Scraped Providers 🟡
(Изисква: Блокер 7А. Може паралелно с 7Е)
Проблем: Scraped провайдъри виждат празен wizard въпреки че имаме техните данни.

Налични данни за pre-fill:
- business_name ✅ (вече се pre-fill-ва)
- category_slug ✅ (вече се pre-fill-ва)
- city (Warszawa) ✅ (вече се pre-fill-ва)
- description — от scraped данни (ако има) → зарежда се в textarea
- phone — от scraped данни (ако има) → зарежда се в phone поле

Onboarding старт за scraped providers: Step 1 (Profile) — НЕ Step 2.
Насърчава попълване на снимка и description (препоръчителни, влияят на конверсия).

Проверка на текущото състояние преди имплементация: Провери какво вече е
pre-fill-нато и какво липсва. Не презаписвай работещ код.
Модел: SWE-1.6 (диагноза) → Kimi-2.6 (имплементация)

---

### Задача 6А — Profile Strength Email 🟡
(Не е блокер. Изпълнява се след Блокер 7А. Критична за макс ефект от кампанията.)

**Кога се изпраща:**
При първото завършване на onboarding (is_complete: False → True).
Тригер: POST /api/v1/provider/services (добавяне на първа услуга) →
backend проверява completeness → ако is_complete стане True → изпраща имейла.

**Какво проверява и съдържа имейлът:**
- Липсва снимка → "Добави профилна снимка — профилите със снимка получават значително повече запитвания. Качи снимка тук → [линк]"
- Галерия празна → "Имаш място за 8 снимки — покажи работата си. Клиентите искат да видят резултати. Добави снимки → [линк]"
- Описание < 100 символа → "Подобри описанието си — добри описания обясняват специализацията, опита и района. Пример: 'Хидравличен специалист с 10г. опит в Варшава. Авария 24/7. Безплатна оценка.'"
- Телефон липсва → "Добави телефон — клиентите предпочитат да се свържат директно. Добави → [линк]"

**Език:** lang от provider.locale
**Template:** apps/api/scripts/templates/profile_strength_pl.html (+ 34 езика)
**Тригер в код:** apps/api/routes/provider.py → POST /services → след db.commit()
**Модел:** Claude (текст на имейла на 34 езика) → Kimi-2.6 (template) → SWE-1.6 (backend тригер)

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

## РАЗДЕЛ 3 — Съдържание (12 имейл шаблона + SMS)

> Тук се описва КАКВО се пише. Текстовете се създават паралелно с блокерите.

### 3.1 Категорийна персонализация

Всеки имейл има **3 версии** — по категория. Различни са:
- Subject line (вече имаме за Email #1)
- Opening sentence
- Pain point
- Social proof числа
- Call to action

| | 🧹 Cleaning | 🔧 Plumbing | 💆 Massage |
|---|---|---|---|
| Search vol. | 7,000/мес | 5,400/мес | 6,900/мес |
| Key pain | Конкуренция → невидимост | Спешни повиквания → нощни часове | Постоянни клиенти → лоялност |
| Social proof angle | "Фирмите за почистване намират нови обекти" | "Хидравлиците взимат спешни заявки нощно" | "Масажистите изграждат лоялна клиентела" |

### 3.2 Email #1 — Introduction (Вторник 10:00)

**Subject (вече финализирани):**
- Cleaning: `7 363 firm sprzątających w Warszawie — czy Twoi klienci Cię znajdą?`
- Plumbing: `10 707 firm instalacyjnych w Warszawie — czy Twoi klienci Cię znajdą?`
- Massage: `3 635 gabinetów masażu w Warszawie — czy Twoi klienci Cię znajdą?`

**Preview text (НОВ — добавя се в outreach_email_pl.html):**
- Cleaning: `Bezpłatnie, bez prowizji — Twój profil czeka na Ciebie.`
- Plumbing: `Klienci szukają hydraulika o 21:00 — bądź tam pierwszy.`
- Massage: `Stali klienci zaczynają od online — Twój profil jest gotowy.`

**Body:** Съществуващият `outreach_email_pl.html` — само се добавя preview text и unsubscribe линк.

### 3.3 Email #2 — Insight (Петък 18:00)

**Format:** Plain text (изглежда като личен имейл, не marketing)
**Tone:** "Quick follow-up" — не formal, не повторение

**Subject:**
- Cleaning: `Jak firma sprzątająca zdobyła 8 zleceń w pierwszym tygodniu`
- Plumbing: `Hydraulicy na Nevumo: zgłoszenia też w nocy i weekendy`
- Massage: `Masażyści na Nevumo: rezerwacje z 2 tygodniowym wyprzedzeniem`

**Body (template — персонализира се по категория):**
```
Cześć [business_name],

Krótka wiadomość — sprawdziłem, ile zapytań trafia do [kategoria] w Warszawie.

W zeszłym tygodniu: [liczba] klientów szukało [usługi]. Większość dostawców
nie jest widoczna w tym miejscu.

Jedno pytanie: czy teraz pojawiasz się, gdy ktoś szuka [usługi] w Google wieczorem?

Jeśli nie — mogę pokazać dokładnie jak działa profil na Nevumo. Bez zobowiązań.

Dimitar
Nevumo
[unsubscribe link]
```

### 3.4 Email #3 — Social Proof (Сряда 10:00)

**Format:** Plain text
**Важно:** Хипотетична рамка — не измислени testimonials

**Subject:**
- Cleaning: `Firma sprzątająca: +30% przychodów w 60 dni (jak to zrobili)`
- Plumbing: `Hydraulik z Krakowa: 23 zgłoszenia w pierwszym miesiącu`
- Massage: `Gabinet masażu: lista oczekujących w 45 dni`

**Body (template):**
```
Cześć [business_name],

Jedna rzecz, zanim zamknę Twój profil.

Wyobraź sobie: dostawca [usług] w Warszawie, podobny do Twojego biznesu,
dołączył do Nevumo 60 dni temu.

Rezultaty, które widzimy przy kompletnych profilach:
- 15-25 nowych zapytań w pierwszym miesiącu
- Klienci rezerwują bezpośrednio — bez pośredników
- Zero prowizji od każdego zlecenia

Chcesz, żebym przesłał więcej szczegółów? Albo — czy to po prostu nie jest
odpowiedni moment?

Dimitar
[unsubscribe link]
```

### 3.5 Email #4 — Break-up (Понеделник 10:00)

**Format:** Plain text — НАЙ-КРАТЪК от всички
**Subject:** `Zamykam Twoje miejsce na Nevumo — ostatnia wiadomość`

**Body:**
```
Cześć [business_name],

Rozumiem, jeśli teraz nie jest odpowiedni moment.

Zamykam listę wczesnych dostawców dla Warszawy w tym tygodniu —
chciałem sprawdzić ostatni raz przed przejściem dalej.

Jeśli jesteś zainteresowany, odpowiedz TAK — zachowam Twoje miejsce.
Jeśli nie — odpowiedz NIE TERAZ — sprawdzę za 3 miesiące.

W obu przypadkach — bez pretensji.

Dimitar
Nevumo
[unsubscribe link]
```

### 3.6 SMS Template (паралелно с Email #1 и #4)

**При Email #1 (ден 0):**
```
Nevumo: Twój profil [business_name] czeka. Przejmij go bezpłatnie →
nevumo.com/pl/claim/[token]
Odpowiedz STOP aby zrezygnować
```

**При Email #4 (ден 17):**
```
Nevumo: Ostatnia szansa — zamykamy Twoje miejsce w Warszawie jutro.
nevumo.com/pl/claim/[token]
```

⚠️ **SMS дължина:** Максимум 160 символа (1 SMS). Проверявай преди изпращане.
**STOP механизъм** е задължителен — SMSapi.pl го поддържа нативно.

### 3.7 Claim Page — Social Proof Update

**Добавяне на `claimed_count` в реално изброяване на claim страницата:**
- `claimed_count` вече се връща от API
- Текст: `"[N] dostawców usług dołączyło do Nevumo w Warszawie w tym miesiącu"`
- Показва се само ако `claimed_count > 0`

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

## Appendix: Пълен Task Order (хронологичен)

> Задачите без зависимости могат да вървят паралелно.

```
БЛОКЕРИ (наредени по зависимост):
[✅] Блокер 1: Auto-claim (4Д) — ЗАВЪРШЕН (22 юни 2026)
[✅] Блокер 2: Art.14 в providers.py (4Е) — ЗАВЪРШЕН (22 юни 2026)
[✅] Блокер 3: Unsubscribe механизъм — ЗАВЪРШЕН (22 юни 2026)
[✅] Блокер 3Б: Welcome имейл след claim (await bug fix) — ЗАВЪРШЕН (22 юни 2026)
[✅] Блокер 4: Resend Webhooks — ЗАВЪРШЕН (22 юни 2026, commit 5b186c0)
[✅] Блокер 5: outreach_sequence_log таблица      → ЗАВЪРШЕН (22 юни 2026, commits 4cbdb17 + d70616d)
[✅] Блокер 6: Верификация при claim (4Г)         → ЗАВЪРШЕН (23 юни 2026, commit 7ee1361)
              email verification премахната от token flow (токенът е доказателство)
              wizard pre-fill за scraped провайдъри (category_slug + data_source в API)
              photo upload fix pending (pointerEvents: none)
[✅] Блокер 6: Magic Link Flow + Cookie Source of Truth → ЗАВЪРШЕН (23 юни 2026, commit c705215)
              claim token = proof of identity, no JWT required
              get_or_create_claim_user() auto-login/register
              Cookie = единствен source of truth
              ClaimProcessor.tsx replaces AutoClaimTrigger
              sessionStorage-based wizard welcome heading
              3 new translation keys (34 languages each)
[✅] Блокер 7А: Banner Flow Redesign (без auth)  → ЗАВЪРШЕН (24 юни 2026)

### Блокер 7А — Banner Flow Redesign ✅ ЗАВЪРШЕН (24 юни 2026)

**Промени в backend (apps/api/routes/providers.py):**
- claim_provider(): при source=banner не изисква JWT — get_optional_current_user се игнорира
- claim_provider(): при source=banner проверява само scraped_email + is_claimed
- verify_claim_code(): сменен от get_current_user на get_optional_current_user
- verify_claim_code(): вика get_or_create_claim_user(scraped_email) → връща JWT + user + redirect
- verify_claim_code(): PendingClaimVerification query филтрира само по claim_token + code + user_id==None
- verify_claim_code(): catch IntegrityError при db.commit() → 409 USER_ALREADY_HAS_PROVIDER
- verify_claim_code(): Art.14 email dashboard_link използва lang параметъра
- verify_claim_code(): welcome email ПРЕМАХНАТ — ще се изпраща от Task 6A след попълнен профил

**Промени в frontend:**
- verify/page.tsx: премахнат auth guard (проверката за nevumo_auth_token cookie)
- VerifyCodeForm.tsx: премахнат Authorization header; след успех → saveAuth(token) + window.location.replace(redirect)
- ClaimProcessor.tsx: sessionStorage guard (claim_{token}): 'processing' блокира дублиране, removeItem при success/error
- ClaimProcessor.tsx: 401 handler → setErrorCode('NETWORK') вместо redirect към /auth

**Промени в apps/web/public/sw.js:**
- Добавен ред: if (event.request.url.includes('/_next/')) return;
- Причина: SW прихващаше Next.js chunk-ове при router.push() → Application error

**E2E тест резултати (24 юни 2026):**
- Banner click → POST без JWT → 202 ✅
- Имейл с код пристига ✅ (само 1 имейл — sessionStorage guard работи)
- Код → verify → get_or_create_claim_user → JWT ✅
- Redirect → /provider/dashboard/profile (wizard, Step 1) ✅
- Pre-fill: business_name + description + category_slug ✅
- Art.14 RODO имейл пристига с правилен lang и dashboard_link ✅
- Welcome имейл НЕ се изпраща (премахнат) ✅

---

### Блокер 7Б — Magic Link Login ✅ ЗАВЪРШЕН (24 юни 2026)

**Проблем:** Потребители създадени чрез get_or_create_claim_user() нямат парола.
При затворен браузър нямат начин да влязат обратно.

**Имплементация:**
- Backend: POST /api/v1/auth/request-magic-link (нов endpoint в auth.py)
  - Rate limiting: 1 заявка/минута на email
  - Cleanup на неизползвани токени преди генериране на нов
  - Генерира secrets.token_urlsafe(32) → SHA256 hash → MagicLinkToken record
  - 24h TTL, еднократен
  - Винаги връща 200 (не разкрива дали email съществува)
- Backend: send_login_magic_link_email() — нова функция в email_service.py
  - Отделна от send_magic_link_email() (клиентски leads flow)
  - PL/EN поддръжка (технически дълг: останалите 32 езика → EN)
- Frontend: requestMagicLink() в auth-api.ts
- Frontend: LoginClient.tsx — "Brak hasła? Zaloguj się linkiem na email →"
  - Появява се на стъпка 2 (след въвеждане на email)
  - Клик → изпраща линк на вече въведения email → success съобщение
  - Без второ email поле
- Translations: 8 ключа × 34 езика (seed_magic_link_translations.py)
- Съществуваща инфраструктура: MagicLinkToken модел + POST /auth/magic-link
  (консумира токен, издава JWT) — не са пипани

**Тествани сценарии:**
- Passwordless провайдър → magic link → provider dashboard ✅
- Email пристига коректно (PL) ✅
- Rate limiting работи ✅

**Известни ограничения (технически дълг — не блокират кампанията):**
- Имейлът е само PL/EN; останалите 32 езика получават EN
- Redirect след magic link login е role-aware само частично (вж. Known Issues)

**⚠️ ВАЖНО — Глобална система, multi-role потребители:**
Nevumo ще има потребители с двойна роля (провайдър + клиент едновременно).
Magic link системата трябва да работи коректно за всички случаи:
- role='provider' → redirect към /provider/dashboard
- role='client' → redirect към /client/dashboard
- Потребител и с двете роли → redirect по последно активната роля;
  switch-role endpoint съществува и работи
Текущото MagicLinkClient.tsx redirect поведение трябва да се верифицира
преди bulk кампанията (вж. QA Gate 5.1).

---

### Блокер 7В — Add/Change Password в Provider Settings ✅ ЗАВЪРШЕН (24 юни 2026)

**Проблем:** Passwordless потребители (от banner claim) нямат парола в акаунта.
При затворен браузър не могат да сменят паролата.

**Имплементация:**
- Backend: POST /api/v1/auth/password (global endpoint)
  - Passwordless: задава нова парола (без old_password)
  - С парола: изисква old_password за потвърждение
- Backend: GET /api/v1/auth/me — single source of truth за has_password
- Frontend: PasswordSection.tsx (shared компонент за provider и client)
  - Чете has_password от /api/v1/auth/me
  - Автоматично показва 2-field (set) или 3-field (change) форма
- Translations: account_settings namespace (14 ключа × 34 езика)
  - seed_account_settings_translations.py
- Architecture: Премахнат has_password от provider profile и client dashboard responses
  - Централизиран в /api/v1/auth/me

**QA резултати:**
- ✅ Работи за provider settings
- ✅ Работи за client settings
- ✅ Работи паралелно с magic link login
- ✅ Работи паралелно с Google OAuth login
- ✅ Правилно показва 2-field vs 3-field форма

**Commits:** 3c8cda9, a7f8344, 6c382ea, 7602bb4, 5228cc3

---

### Блокер 7Г+7Е — Глобална Auth Архитектура ✅ ЗАВЪРШЕН (25 юни 2026)

**Произход:** Блокер 7Г ("Нов login link") еволюира до пълна архитектурна задача,
която покрива едновременно 7Г (smart detection) и 7Е (onboarding redirect logic).
Решава се с един имплементационен цикъл.

**Проблеми, които решава:**
1. MagicLinkClient.tsx има hardcoded redirect към /client/dashboard
2. check-email не връща has_password → passwordless потребители не се разпознават рано
3. Redirect логиката е разпръсната в login, register, magic-link, google oauth — всеки прави нещо различно
4. Google OAuth не проверява onboarding completeness
5. Passwordless потребители (от banner claim) нямат очевиден начин за вход

**Архитектурни принципи:**
- Single Source of Truth: backend взима всички redirect решения
- Separation of Concerns: check-email = само smart detection; determine_post_auth_redirect() = само redirect
- Read-Only Functions: determine_post_auth_redirect() не мутира DB
- Нула DB миграции за Фаза 1

---

#### Фаза 1 — За кампанията (нула DB миграции)

**Backend промени:**

1. POST /api/v1/auth/check-email — опростен response (само 4 полета):
exists: bool
has_password: bool          ← НОВО
role: Optional[str]         ← НОВО
oauth_connected: bool       ← НОВО
   Премахнати: has_provider_profile, provider_is_claimed, provider_is_complete
   Причина: никое от тях не се използва в smart detection логиката.
   check-email СПИРА да вика check_onboarding_complete() → нула двоен DB call.

2. apps/api/services/auth_service.py — нова функция determine_post_auth_redirect():
Приоритет:
claim_token → /auth/claim?token={claim_token}
intent ('client'|'provider') → провайдър онбординг проверка → dashboard
user.role (default) → провайдър онбординг проверка → dashboard
   - READ-ONLY: не мутира DB
   - Единственото място в системата което вика check_onboarding_complete()

3. Всички auth endpoints връщат redirect в response:
   - POST /api/v1/auth/login → добавя intent в LoginRequest + redirect в response
   - POST /api/v1/auth/register → redirect в response
   - POST /api/v1/auth/magic-link → добавя intent + claim_token в MagicLinkRequest + redirect в response
   - GET /api/v1/auth/google/callback → минава през determine_post_auth_redirect()
   - POST /api/v1/auth/google/complete → добавя intent в GoogleOAuthCompleteRequest + redirect в response

4. apps/api/schemas.py — нови Optional полета:
   - LoginRequest.intent: Optional[str]
   - MagicLinkRequest.intent: Optional[str]
   - MagicLinkRequest.claim_token: Optional[str]
   - GoogleOAuthCompleteRequest.intent: Optional[str]

**Frontend промени:**

5. apps/web/app/[lang]/auth/LoginClient.tsx — smart detection в handleCheckEmail():
!exists          → select_role или register (ако има intent)
!has_password    → auto изпраща magic link (без да показва password field)
has_password     → показва password field
   При грешна парола → показва ЕДНОВРЕМЕННО:
   - "Забравена парола?"
   - "Влез с имейл линк"

6. apps/web/app/[lang]/auth/magic/MagicLinkClient.tsx:
   - Премахва hardcoded redirect към /client/dashboard
   - Използва result.redirect от backend
   - Fallback: /{lang}/{role}/dashboard

7. apps/web/lib/auth-api.ts:
   - checkEmail() return type → { exists, has_password, role, oauth_connected }
   - magicLinkAuth() return type → включва redirect поле

**Модел:** SWE-1.6 (backend) + Kimi-2.6 (frontend)
**Зависимости:** Изисква Блокер 7Б ✅

---

#### Фаза 2 — След кампанията (2 DB миграции, когато има dual-role потребители)

**2.1 Dual-Role Support:**
- DB migration: users.last_active_role (Optional[str], nullable)
- Нова функция: update_last_active_role(user, role, db) — мутира отделно от redirect логиката
- determine_post_auth_redirect() разширена с last_active_role като стъпка 3
- switch-role endpoint: записва last_active_role при всеки превключване
- GET /api/v1/auth/me: включва last_active_role в response

**2.2 Magic Link Intent Persistence:**
- DB migration: magic_link_tokens.intent (Optional[str], nullable)
- POST /auth/request-magic-link: записва intent в MagicLinkToken записа
- POST /auth/magic-link: чете intent от DB токена (не от URL)
- URL на линка остава чист: /auth/magic?token=xxx (без ?intent=)
- Причина за Фаза 2: dual-role потребители нямаме сега; за single-role user.role е достатъчен

**Защо Фаза 2 е отделна:**
- Нямаме нито един dual-role потребител в production
- DB миграции върху Neon production = риск за кампанията
- Архитектурата е проектирана така че добавянето на last_active_role е additive (не рефакторинг)

---

**⚠️ ВАЖНО — Dual-Role честност:**
Фаза 1 НЕ решава dual-role. При fresh login на dual-role потребител системата
ще redirect-ва по user.role (base role), не по последно активната роля.
Това е съзнателен компромис за кампанията. Фаза 2 го решава правилно с DB.

**Имплементация (25 юни 2026):**

Backend:
- determine_post_auth_redirect() добавена в apps/api/services/auth_service.py
  Приоритети: claim_token → intent/role → provider onboarding check → dashboard
  READ-ONLY функция, не мутира DB
- POST /auth/check-email: разширен response с has_password, role, oauth_connected
- POST /auth/login: приема intent + lang, връща redirect в response
- POST /auth/register: връща redirect в response
- POST /auth/magic-link: приема intent, claim_token, lang; връща redirect
- GET /auth/google/callback: заменена hardcoded if/else с determine_post_auth_redirect()
- POST /auth/google/complete: връща redirect в response
- Bug fix: lang=body.lang за login, register, magic-link (коректен redirect locale)

Frontend:
- apps/web/lib/auth-types.ts: CheckEmailResult разширен (has_password, role, oauth_connected); AuthResult включва redirect
- apps/web/lib/auth-api.ts: checkEmail(), magicLinkAuth(), loginWithEmail(), registerWithEmail() — добавен lang параметър
- apps/web/app/[lang]/auth/LoginClient.tsx:
  - AuthStep добавен 'magic_link_sent'
  - handleCheckEmail() smart detection: passwordless → auto magic link → magic_link_sent UI
  - handleLogin() използва redirect от backend response
- apps/web/app/[lang]/auth/magic/MagicLinkClient.tsx:
  - Премахнат hardcoded redirect към /client/dashboard
  - Използва result.redirect от backend; fallback: /{lang}/{role}/dashboard
  - lang подаден към magicLinkAuth() за коректен locale в redirect

Translations:
- 3 нови ключа в auth namespace: magic_link_sent_title, magic_link_sent_subtitle, magic_link_use_different_email
- 102 rows × 34 езика seeded в Neon
- Seed script: apps/api/scripts/seed_magic_link_sent_translations.py

**QA резултати (25 юни 2026):**
- ✅ check-email response: exists, has_password, role, oauth_connected
- ✅ Passwordless user → auto magic link → magic_link_sent UI
- ✅ Login redirect от backend (коректен lang)
- ✅ Magic link redirect: /bg/ → /bg/client/dashboard (не /pl/)
- ✅ Register redirect от backend (коректен lang)
- ✅ Google OAuth redirect (ръчен тест)

**Commits:** feat: implement frontend for Blocker 7Г+7Е, fix: lang fixes за login/register/magic-link

---
[✅] Блокер 7В: Add/Change Password Settings     → ЗАВЪРШЕН (24 юни 2026)
[✅] Блокер 7Г+7Е: Глобална Auth Архитектура     → ЗАВЪРШЕН (25 юни 2026)
    Фаза 1 (кампания): check-email, determine_post_auth_redirect(), Google OAuth fix, smart detection
    Фаза 2 (пост-кампания): last_active_role + magic_link_tokens.intent
[✅] Блокер 7Д: Outreach Flow потвърждение        → ЗАВЪРШЕН (26 юни 2026)
[ ] Блокер 7Ж: Onboarding Pre-fill Scraped       → SWE-1.6 → Kimi-2.6
[ ] Блокер 8:  Task 2A seed_unclaimed_providers  → Kimi-2.6 (изисква 7А–7Ж)
[ ] Блокер 9:  Railway Scheduler script          → Kimi-2.6 (изисква Блокер 8)
[ ] Блокер 10: E2E cleanup                       → CLI команда

СЪДЪРЖАНИЕ (паралелно с блокерите):
[ ] Email #2, #3, #4 templates (× 3 категории)  → Claude пише текст
[ ] Preview text за Email #1                     → Claude пише текст
[ ] Activation emails #1-4                       → Claude пише текст
[ ] SMS templates                                → Claude пише текст
[ ] Pilot wave CSV (20-30 адреса)               → Dimitar избира ръчно
[ ] Задача 6А: Profile Strength Email              → Claude (текст) + SWE-1.6 + Kimi-2.6

QA GATE (след всички блокери):
[ ] QA Checklist 5.1 A-H (всички ✅)           → SWE-1.6 + mcp-playwright + ръчно
[ ] Pilot Wave изпратен                          → Railway scheduler
[ ] Pilot Wave анализ (ден 14)                   → Claude + Resend Dashboard
[ ] Go/No-Go решение                             → Dimitar

ПРЕДИ BULK:
[ ] Resend Pro upgrade ($20/мес)                 → Dimitar (ръчно в Resend Dashboard)

BULK CAMPAIGN:
[ ] Email #1 + SMS bulk send                     → Railway scheduler
[ ] Monitoring (24h след #1)                     → Resend Dashboard + DB
[ ] Email #2, #3, #4 автоматично                → Railway scheduler
[ ] 30-дневен анализ                             → SQL + Claude

POST-CAMPAIGN:
[ ] "NOT NOW" feedback processing               → DB analysis
[ ] 90-дневен re-engagement setup               → Railway scheduler
[ ] Task 4Г пълна имплементация (6-цифрен код) → SWE-1.6 + Kimi-2.6
```

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
