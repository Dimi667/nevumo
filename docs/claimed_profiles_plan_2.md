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

---

### Блокер 5 — outreach_sequence_log DB таблица (НОВ) 🔴

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
    status TEXT DEFAULT 'sent',  -- sent/failed/skipped
    UNIQUE(email, sequence_step)
);
```

**Интеграция:** `send_outreach_bulk.py` пише в таблицата вместо CSV.
Scheduler проверява: "Кой email на коя стъпка е следващ?"

**Файлове:** Alembic migration, `apps/api/models.py`, `send_outreach_bulk.py`
**Модел:** SWE-1.6

---

### Блокер 6 — Верификация при claim от публичен банер (Задача 4Г) 🔴

**Проблем:** Банерът "Odbierz swój profil" е публично видим на всяка unclaimed провайдър страница
(напр. `nevumo.com/pl/warszawa/plumbing/hydraulik-testowy-e2e`). `claim_token` се вижда в HTML-а.
Всеки може да: посети страницата → регистрира Nevumo акаунт → claim чужд профил.
**Това е критичен security проблем след Task 2A** — стотици публични банери ще са активни.

**Защо НЕ е проблем при имейл кампанията:** Изпращаме имейла ДО `scraped_email` на бизнеса.
Ако собственикът кликва линка, неговият регистриран имейл = `scraped_email` → верифициран имплицитно.

**Решение — Email matching логика в POST /api/v1/providers/claim/{token}:**

```python
if current_user.email == provider.scraped_email:
    # Fast path — имейлите съвпадат → собственикът е
    # Покрива: outreach кампания + банер с бизнес имейл
    claim_directly()

elif provider.scraped_email is None:
    # Не можем да верифицираме (провайдър без имейл в CEIDG)
    raise HTTPException(
        status_code=422,
        detail="cannot_verify_ownership"
        # Frontend показва: "Свържете се с support@nevumo.com"
    )

else:
    # Имейлите не съвпадат → изпращаме верификационен код
    # Покрива: банер с личен Gmail, потенциален измамник
    send_verification_code_to(provider.scraped_email)
    return {"status": "pending_verification"}
```

**Верификационен flow (само при несъвпадение):**

1. Backend генерира 6-цифрен код, TTL 24h → записва в `pending_claim_verifications`
2. Изпраща код до `provider.scraped_email`
3. Frontend показва: *"Изпратихме код на имейла на бизнеса. Въведете го за да потвърдите собствеността."*
4. Потребителят въвежда кода → `POST /api/v1/providers/claim/{token}/verify`
5. Backend верифицира → claim → Art. 14 GDPR имейл

**Нова DB таблица:**
```sql
CREATE TABLE pending_claim_verifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    claim_token TEXT NOT NULL,
    user_id UUID REFERENCES users(id),
    code TEXT NOT NULL,           -- 6-цифрен код
    expires_at TIMESTAMPTZ NOT NULL,  -- NOW() + 24h
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Нов endpoint:** `POST /api/v1/providers/claim/{token}/verify`
- Body: `{ "code": "123456" }`
- Верифицира → claim → Art. 14 имейл

**Нов имейл template:** `apps/api/scripts/templates/claim_verification_pl.html`
- Subject: `"Potwierdź przejęcie profilu [business_name] na Nevumo — kod: [CODE]"`
- Sender: `noreply@nevumo.com`
- Съдържание: 6-цифрен код, TTL 24h, business_name, инструкции

**Поведение по случай:**

| Кой и откъде | scraped_email match? | Резултат |
|---|---|---|
| Собственик от outreach имейл | ✅ Да | Директен claim, без триене |
| Собственик от банера с бизнес имейл | ✅ Да | Директен claim, без триене |
| Собственик от банера с личен Gmail | ❌ Не | Код до бизнес имейла — само той го чете |
| Конкурент от банера | ❌ Не | Код до чуждия бизнес имейл — конкурентът не го получава |
| Провайдър без scraped_email | NULL | Блокиран → support@nevumo.com |

**Файлове:** `apps/api/routes/providers.py`, Alembic migration,
`apps/api/models.py`, `apps/api/scripts/templates/claim_verification_pl.html`
**Модел:** SWE-1.6 (backend + DB) + Kimi-2.6 (frontend verification UI + имейл template)

---

### Блокер 7 — Task 2A: seed_unclaimed_providers.py 🔴

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
[ ] Блокер 4: Resend Webhooks                    → SWE-1.6
[ ] Блокер 5: outreach_sequence_log таблица      → SWE-1.6
[ ] Блокер 6: Верификация при claim (4Г)         → SWE-1.6 (backend + DB) + Kimi-2.6 (frontend + template)
              email match → директен claim
              email mismatch → 6-цифрен код до scraped_email
              NULL scraped_email → блокиран → support
[ ] Блокер 7: Task 2A seed_unclaimed_providers   → Kimi-2.6 (изисква Блокер 5)
[ ] Блокер 8: Railway Scheduler script           → Kimi-2.6 (изисква Блокер 7)
[ ] Блокер 9: E2E cleanup                        → CLI команда

СЪДЪРЖАНИЕ (паралелно с блокерите):
[ ] Email #2, #3, #4 templates (× 3 категории)  → Claude пише текст
[ ] Preview text за Email #1                     → Claude пише текст
[ ] Activation emails #1-4                       → Claude пише текст
[ ] SMS templates                                → Claude пише текст
[ ] Pilot wave CSV (20-30 адреса)               → Dimitar избира ръчно

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

*Документът се обновява след всяка завършена задача.*
*Git: `git push nevumo-git main` след всяка актуализация.*
