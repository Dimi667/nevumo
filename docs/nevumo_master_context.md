# Nevumo Master Context

## Project Overview
Nevumo е уеб платформа за marketplace на услуги.
- Доставчици публикуват услуги
- Клиенти търсят и се свързват с доставчици
- Платформата е мултиезична (34 езика)
- Основен фокус: scalability, SEO, conversion

### Фирмени данни
- **Юридическо наименование:** „ФИЛИПС ЦЕНТЬР БЪЛГАРИЯ" ООД
- **ЕИК:** 175369610
- **Адрес:** бул. Петко Каравелов бл. 77, вх. А, ап. 19, р-н Триадица, п.к. 1408, гр. София, България
- **Privacy email:** privacy@nevumo.com
- **Бранд:** Nevumo
- **Забележка:** Предстои преименуване — при промяна актуализирай всички правни документи

---

## Tech Stack

### Architecture
- Monorepo: Turborepo
  - apps/web (frontend)
  - apps/api (backend)
  - apps/docs

### Frontend
- Next.js 16
- React 19
- TypeScript 5 (strict mode)
- Tailwind CSS 4
- PostCSS

### Backend
- FastAPI
- Python 3.13.12
- SQLAlchemy (ORM)
- Pydantic v2 + pydantic-settings (validation + config)
- bcrypt 4.2.1 (password hashing)
- python-jose (JWT — HS256, 30-day tokens)
- Alembic (migrations)
- python-slugify (URL slug generation)
- qrcode[pil] (QR code generation for provider growth tools)
- python-multipart (file upload support)
- apscheduler>=3.10.0 (background jobs for magic link delivery)
- tzlocal>=3.0 (timezone support for APScheduler)
- boto3>=1.34.0 (Cloudflare R2 S3-compatible storage for images)
- Backend packaging/runtime: absolute `apps.api.*` imports with module-based startup/scripts
- STATIC_FILES_BASE_URL: Environment variable for proper static file URL generation (images, etc.)
- R2 Integration: Image uploads (profile and gallery) use Cloudflare R2 with automatic fallback to local disk when R2_BUCKET_NAME is empty (local dev)

### Database & Caching
- PostgreSQL (nevumo_leads)
- Redis (caching layer)

### Хостинг инфраструктура (deployment в прогрес — 2026-05-29)
| Компонент | Доставчик | Цена старт |
|-----------|-----------|------------|
| Frontend | Vercel Inc. | $0 (free tier) |
| Backend API | Railway Corp. | $5/мес |
| PostgreSQL | Neon Inc. | $0 (free tier) |
| Redis кеш | Upstash Inc. | $0 (free tier) |
| Снимки/Storage | Cloudflare Inc. (R2) | $0 (free tier) |
| **Общо** | | **$0–5/мес при launch** |

Бележка: Всички са в USA — трансфери покрити с SCCs. Cloudflare + DPF.
Миграция от локален Docker: В ПРОГРЕС (2026-05-29)

#### Deployment правила (от инцидент 2026-05-30)
- **Cloudflare CNAME за Railway** → винаги **DNS only** (сив облак), никога Proxied
- **Railway URL** → използвай service URL (`api-production-7631.up.railway.app`), не deployment URL — service URL е постоянен
- **Environment Variables**:
  - **Backend variables** (Railway): `APP_URL`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `OAUTH_REDIRECT_BASE` - добавят се само в Railway environment variables
  - **Frontend variables** (Vercel): `NEXT_PUBLIC_SITE_URL`, `NEXT_PUBLIC_API_URL` - добавят се във Vercel Environment Variables И в `turbo.json` tasks.build.env масива
  - **Important**: `APP_URL` е backend-only variable, не се добавя във Vercel или turbo.json
- **Neon free tier** → задължително `NullPool` в `apps/api/database.py` (от `sqlalchemy.pool import NullPool`)
- **Auto-deploy** → Vercel е свързан с GitHub (`Dimi667/nevumo`); всеки `git push origin main` тригерира автоматичен production deploy

#### Deployment статус (2026-05-29)
| Компонент | Статус | Бележки |
|-----------|--------|---------|
| Neon (PostgreSQL) | ✅ ГОТОВО | 27 таблици мигрирани от локален PostgreSQL. Alembic heads merge-нати (revision: 988cd791c762). |
| Upstash (Redis) | ✅ ГОТОВО | Акаунт и база създадени, URL запазен |
| Cloudflare | ✅ ГОТОВО | nevumo.com прехвърлен, R2 bucket `nevumo-images` създаден, API token запазен |
| Railway (API) | ✅ ГОТОВО | api.nevumo.com |
| Vercel (Frontend) | ✅ ГОТОВО | www.nevumo.com |
| DNS (Cloudflare) | ✅ ГОТОВО | — |
| Custom domain api.nevumo.com | ✅ ГОТОВО | — |

#### Deployment код промени (2026-05-29)

**Frontend (apps/web)**
- `app/[lang]/LayoutShell.tsx` — нов Client Component. Чете modal и embed от URL чрез useSearchParams(). Заменя searchParams prop в layout (несъвместим с Next.js 16).
- `app/[lang]/layout.tsx` — премахнат searchParams prop, използва LayoutShell.
- `lib/api.ts` — добавени verification_level: number и gallery: GalleryImage[] в ProviderDetail интерфейса.
- `app/[lang]/[city]/[category]/[providerPage]/page.tsx` — подава verification_level, gallery, cities: [] към ProviderFullPage.
- `app/[lang]/terms/page.tsx` и `cookies/page.tsx` — fetch cache сменен от no-store на { next: { revalidate: 3600 } }.

**Backend (apps/api)**
- `Dockerfile` — CMD използва ${PORT:-8000} за Railway PORT env variable.

**Deployment конфигурация**
- `.vercelignore` (root) — добавен за изключване на node_modules, apps/api, .turbo.
- `apps/web/vercel.json` — опростен до framework: nextjs и outputDirectory: .next.

#### Production инфраструктура (2026-05-29)

**Environment Variables (Vercel)**
- NEXT_PUBLIC_API_URL = https://api.nevumo.com
- NEXT_PUBLIC_STATIC_URL = https://images.nevumo.com
- NEXT_PUBLIC_SITE_URL = https://nevumo.com
- NEXT_PUBLIC_GA_ID = G-3PYNQ1Y2V9
- GOOGLE_CLIENT_ID = [Google OAuth Client ID from Google Cloud Console]

**Railway variables**
- SECRET_KEY — добавен
- CORS_ORIGINS=https://www.nevumo.com,https://nevumo.com,https://nevumo.vercel.app
- PORT = 8000
- GOOGLE_CLIENT_ID = [Google OAuth Client ID from Google Cloud Console]
- GOOGLE_CLIENT_SECRET = [Google OAuth Client Secret from Google Cloud Console]
- OAUTH_REDIRECT_BASE = https://www.nevumo.com

**Cloudflare DNS**
- api.nevumo.com CNAME → ntkked5p.up.railway.app (DNS only, не Proxied)
- _railway-verify.api TXT запис добавен

**Cloudflare R2**
- Custom domain: images.nevumo.com

#### Предстои
- Тестване на www.nevumo.com

### Tracking
- Google Analytics 4 (GA4) — G-3PYNQ1Y2V9
- Custom DB events — page_events таблица + /api/v1/page-events endpoint
- Shared utility: lib/tracking.ts — trackPageEvent()

### Auth (Phase 1 — COMPLETE)
- Email-based: register, login, forgot password, reset password
- Backend: 6 endpoints на /api/v1/auth/, bcrypt hashing, JWT tokens
- Frontend: lib/auth-api.ts (typed API calls), lib/auth-store.ts (localStorage)
- Security: rate limiting, no email enumeration, token hashing, password policy
- **Robustness**: BFCache support and auto-login recovery for duplicate registration attempts (back button flow). Replaced legacy hidden iframe hacks with the **Credential Management API** (`navigator.credentials.store`) for robust password saving, including iOS Safari.
- **Password save robustness**: Credential Management API replaces legacy iframe hack. Hidden email input in register form ensures Safari associates email+password. onInput handler fixes browser autofill not triggering React state. Native browser strong password suggestion replaces custom generator.
- Phase 2 (future): OAuth Google + Facebook, email sending via Resend/SendGrid ✅ COMPLETE
- Phase 3 (COMPLETE June 24, 2026): Magic Link Login + Add/Change Password
  - Passwordless authentication via magic links (POST /api/v1/auth/request-magic-link)
  - Password management via POST /api/v1/auth/password (set/change password)
  - Single source of truth for password status via GET /api/v1/auth/me
  - Works parallel with email/password and Google OAuth authentication

### Email Service (Resend) — COMPLETE (June 5, 2026)
- Provider: Resend (resend>=2.0.0)
- Railway env var: RESEND_API_KEY
- From address: Nevumo <noreply@nevumo.com>
- Domain verified: nevumo.com (SPF + DKIM verified in Resend)
- Fallback: console.log when RESEND_API_KEY is empty

### 12 transactional emails implemented in apps/api/services/email_service.py:
1. send_password_reset_email — forgot password (auth.py:223)
2. send_welcome_email — new registration (auth.py:136)
3. send_magic_link_email — anonymous lead claim (send_magic_links.py:43)
4. send_new_lead_notification — provider receives new lead (leads.py:107)
5. send_lead_status_notification — status change to client (provider.py:379)
6. send_lead_status_notification — status change to provider (client.py:123)
7. send_new_review_notification — provider receives new review (client.py:223)
8. send_review_reply_notification — client receives provider reply (email_service.py)
9. send_withdrawal_form_email — legal@nevumo.com (legal.py:86)
10. send_article14_notification — GDPR Art.14 on claimed profile (provider.py:621)
11. send_welcome_email — covers both client and provider roles
12. send_login_magic_link_email — passwordless login (auth.py + email_service.py)

### Claimed Profiles Email Templates
- **Outreach template:** `apps/api/scripts/templates/outreach_email_pl.html`
  - Език: полски (единствен outreach език — Варшава)
  - Изпраща се от: `support@nevumo.com` via Resend
  - Jinja2 templating
  - Лого: при deploy качи `nevumo-logo.png` на `images.nevumo.com/nevumo-logo.png` и замени base64 src
  - **Competitor branding (June 19, 2026):** Премахнати всички споменавания на "Fixly/Oferteo" от имейла. Заменени с generic "Tradycyjne platformy". Причина: правен риск + стратегическо позициониране. Засегнати: heading, intro paragraph, right column label.
  - **BG review template:** `apps/api/scripts/templates/outreach_email_bg_review.html` — същата промяна приложена (Fixly → Традиционни платформи)
  - **Test utility:** `apps/api/scripts/test_outreach_send.py` — изпраща имейла до 2 тестови адреса с реалистични данни
- **Gravatar:** настроен за `support@nevumo.com` с Nevumo иконка (apple-touch-icon 120×120px)
- **FROM_EMAIL:** хардкоднат в кода (не е env var в Railway) — при следваща рефакторинг да се извади като `RESEND_FROM_EMAIL` env var

### Email Notification Fixes (June 9, 2026) — COMPLETE:
- **Root cause diagnosed:** `except Exception: pass` silently swallowed all email errors in provider.py, client.py, and leads.py — replaced with `[EMAIL_WARNING]` logging in all 3 files
- **Direct lead fix:** `send_new_lead_notification` was never called for direct leads (with provider_slug). Added email notification block AFTER db.commit() in leads.py for direct provider assignment.
- **Marketplace lead fix:** `send_new_lead_notification` for marketplace leads was called BEFORE db.commit(), so LeadMatch records were not yet visible in the DB query. Fixed by moving the notification block AFTER db.commit() and iterating directly over `matching_providers` list instead of re-querying LeadMatch.
- **Silent error fix:** All `except Exception: pass` blocks around email_service calls in provider.py, client.py, leads.py replaced with `print(f"[EMAIL_WARNING] ...", flush=True)`. Push notification except blocks remain as `pass`.

### Shared
- packages/ui (shared UI components)
- packages/typescript-config (shared TS config)

---

## GDPR / Правни документи

### Privacy Policy (завършено 2026-05-11)
- Route: `/[lang]/privacy` — SSG, 34 езика
- Текст: EN + BG + PL
- Компонент: `apps/web/app/[lang]/privacy/page.tsx`
- Seed: `apps/api/scripts/seed_privacy_translations.py` (121 ключа — включва всички таблични стрингове в секции 3.1–3.4, 4, 5, 8). Допълнителни скриптове: seed_privacy_table_part1-5.py (сийдват EN+BG+PL), seed_privacy_corrections.py (коригира 8 правни citation ключа), seed_privacy_last_url.py (1 ключ × 3 езика = 3 rows) — t4_purpose_pwa_redirect. Таблиците са напълно преводими на всички 34 езика; BG и PL имат пълни преводи, останалите 31 fallback-ват към EN.
- Namespace: `privacy` (54 ключа)

### Terms & Conditions (завършено 2026-05-15)
- Route: `/[lang]/terms` — SSG, 34 езика
- Текст: EN + BG + PL (15 статии + Annex 1)
- Компонент: `apps/web/app/[lang]/terms/page.tsx`
- Seed: Множество скриптове за terms преводи:
  - seed_terms_p1.py - Article 1 titles and buttons
  - seed_terms_p1_bodies.py through seed_terms_p15_bodies.py - Article bodies (15 articles)
  - seed_terms_annex_bodies.py - Annex 1 content
  - seed_terms_buttons.py - Button translations
- Namespace: `terms`
- Keys: page_title, meta_description, effective_date, version, pl_notice, art1_title through art15_title, art1_body through art15_body, annex1_title, annex1_body, download_pdf, online_form, back_to_home
- PDF download: Links to `/api/v1/legal/withdrawal-form/{lang}` for downloadable PDF withdrawal form

### Withdrawal Form (завършено 2026-05-15)
- Route: `/[lang]/withdrawal` — Client component, 34 езика
- Компонент: `apps/web/app/[lang]/withdrawal/page.tsx`
- Backend: `POST /api/v1/legal/withdrawal` endpoint in `apps/api/routes/legal.py`
- Seed: `apps/api/scripts/seed_withdrawal_translations_4.py` (19 ключа × 34 езика = 646 rows)
- Namespace: `withdrawal`
- Keys: page_title, page_description, label_service_description, label_contract_date, label_consumer_name, label_consumer_address, label_account_id, label_email, label_submission_date, optional, cancel, submit, submitting, error_* (7 error keys), success_title, success_message, back_to_home
- Email integration: Sends withdrawal form data to legal@nevumo.com via email service
- Validation: All required fields validated for non-empty values and proper format

### Cookie Policy (завършено 2026-05-16)
- Route: `/[lang]/cookies` — Server component, 34 езика
- Компонент: `apps/web/app/[lang]/cookies/page.tsx`
- Seed: Множество скриптове за cookies преводи:
  - seed_cookies_p11.py (4 ключа × 34 езика = 136 rows) — page_title, effective_date, s1_title, s2_title, s3_title
  - seed_cookies_p12.py (4 ключа × 34 езика = 136 rows) — s3_1_title, s3_2_title, s3_3_title, s3_4_title (Cookie Categories)
  - seed_cookies_p21.py (11 ключа × 34 езика = 374 rows)
  - seed_cookies_p22.py (9 ключа × 34 езика = 306 rows)
  - seed_cookies_p23.py (8 ключа × 34 езика = 272 rows)
  - seed_cookies_p24.py (12 ключа × 34 езика = 408 rows)
  - seed_cookies_table_data_p1.py (12 ключа EN only = 23 rows)
  - seed_cookies_browser_paths_p2.py (4 ключа × 17 езика = 68 rows)
  - seed_cookies_browser_paths_p3.py (4 ключа × 17 езика = 68 rows)
  - seed_cookies_last_url.py (1 ключ × 34 езика = 34 rows) — s5_p_last_url
- Namespace: `cookies`
- Keys: page_title, effective_date, s1_title, s1_text, s2_title, s2_text, s3_title, s3_text, s3_1_title, s3_2_title, s3_3_title, s3_4_title, s4_title, s4_text, s5_title, s5_text, s5_p_consent, s5_p_lang, s5_p_ga, s5_p_ga_id, s5_p_stripe_mid, s5_p_stripe_sid, s5_p_auth_token, s5_p_auth_user, s5_p_phone, s5_p_intent, s5_p_city, s5_p_auth_email, s5_type_cookie_1p, s5_type_cookie_3p, s5_type_localstorage, s5_type_sessionstorage, s5_ret_12mo, s5_ret_13mo, s5_ret_1y, s5_ret_30d, s5_ret_30min, s5_ret_sess_30d, s5_ret_cleared, s5_ret_session, s5_ret_session_tab, s6_chrome_path, s6_firefox_path, s6_safari_path, s6_edge_path, s7_role_google, s7_role_stripe, s7_role_vercel, s7_role_railway, s7_role_neon, s7_role_upstash, s7_role_cloudflare, s8_safeguard_sccs_dpf, s8_safeguard_sccs, s8_country_usa, s9_title, s9_text, s10_title, s10_text, s11_title, s11_authority_bg, s11_authority_pl, last_updated, back_to_home
- Total: 1,848 rows (50 ключа × 34 езика + 12 ключа EN only + 4 ключа × 34 езика)
- Note: s1_title values have "1. " prefix removed (e.g., "1. What Are Cookies" → "What Are Cookies") — updated in both DB and seed file (2026-05-16)
- Note: s3_1_title, s3_2_title, s3_3_title, s3_4_title Bulgarian translations corrected from Latin to Cyrillic (e.g., "Zadulzhitelno neobhodimi" → "Задължително необходими") — seed_cookies_p12.py updated (2026-05-16)

### Terms & Conditions for Service Providers (завършено 2026-05-17)
- Route: `/[lang]/provider-terms` — Server component, 34 езика
- Текст: EN + BG + PL (18 статии + Annex 1 + Annex 2)
- Компонент: `apps/web/app/[lang]/provider-terms/page.tsx`
- Seed: 23 скрипта за provider_terms преводи:
  - seed_provider_terms_p1_meta.py (4 ключа × 34 езика = 136 rows) — page_title, meta_description, effective_date, version
  - seed_provider_terms_p2_ui.py (1 ключ × 34 езика = 34 rows) — pl_notice (Polish-specific notice)
  - seed_provider_terms_p3_titles1.py (5 ключа × 34 езика = 170 rows) — art1_title through art5_title
  - seed_provider_terms_p4_titles2.py (5 ключа × 34 езика = 170 rows) — art6_title through art10_title
  - seed_provider_terms_p5_titles3.py (5 ключа × 34 езика = 170 rows) — art11_title through art15_title
  - seed_provider_terms_p6_titles4.py (3 ключа × 34 езика = 102 rows) — art16_title through art18_title
  - seed_provider_terms_p7_titles5.py (2 ключа × 34 езика = 68 rows) — annex1_title, annex2_title
  - seed_provider_terms_p8_art1_body.py through seed_provider_terms_p22_art17_18_body.py — Article bodies (18 articles, 1-2 keys per script)
  - seed_provider_terms_p23_footer.py (3 ключа × 34 езика = 102 rows) — annex1_body, annex2_body, footer
- Namespace: `provider_terms`
- Keys: page_title, meta_description, effective_date, version, pl_notice, art1_title through art18_title, art1_body through art18_body, annex1_title, annex1_body, annex2_title, annex2_body, footer
- Total: 50+ keys × 34 languages = 1,700+ rows
- Documentation: Full legal content in docs/terms_conditions_providers_nevumo.md (EN + BG + PL versions with 18 articles + Annex 1 + Annex 2)
- Legal content structure:
  - English version: 18 articles covering General Provisions, Definitions, Registration, Profile, Ranking, Commission, Provider Obligations, Account Suspension, KYC, Amendments, Data Access, Complaints, Mediation, Liability, IP, Data Protection, Applicable Law, Final Provisions
  - Polish version (WERSJA POLSKA): Complete translation with Polish-specific legal terminology and structure
  - Bulgarian version: Complete translation with Bulgarian-specific legal terminology and structure
- P2B Regulation compliance: Document drawn up in compliance with Regulation (EU) 2019/1150 on promoting fairness and transparency for business users of online intermediation services
- **Update (May 25, 2026)**: Fixed Polish typo in seed_provider_terms_p24_art5_badge_b.py (poşrednictwem → pośrednictwem) and re-seeded badge sections (art5_body, badge_a, badge_b)

### Privacy Policy — достъпност (2026-05-11)
- Футър: `GlobalFooter.tsx` — линк `footer.privacy_policy_link` (namespace `footer`) ✅
- Регистрация: `LoginClient.tsx` — линк под бутона за регистрация ✅
- Cookie Banner: `CookieConsentBanner.tsx` — линк в описанието ✅

### Cookie/Storage Registry
| Ключ | Тип | Цел | Retention | Основа |
|------|-----|-----|-----------|--------|
| `lang` | Cookie | Избран език от dropdown | 30 дни | Functional |
| `nevumo_city_preference` | localStorage | Предпочитан град | Indefinite | Functional |
| `nevumo_last_url` | localStorage | Последна посетена чиста URL за PWA smart redirect | Indefinite | Functional |
| `nevumo_pwa_ctx` | Cookie | Дублира nevumo_last_url за iOS PWA isolated storage — последна посетена чиста URL | 30 дни (max-age=2592000) | Functional |
| `nevumo_auth_email` | sessionStorage | Email при auth flow | Session (tab) | Договор |

Пълният актуален списък (11 entries) е в `docs/gdpr_compliance_plan.md` ЗАДАЧА 4.

---

## AI Development Tools

- Windsurf IDE + Cascade (SWE-1.5)
- Codex CLI (gpt-5.1-codex-mini)
- Continue extension (Groq, Gemini, DeepSeek)
- GitHub Copilot

---

## Config Files

- .windsurfrules
- ~/.codeium/windsurf/memories/global_rules.md
- .github/copilot-instructions.md
- ~/.continue/config.yaml
- AGENTS.md

---

## Translations Workflow

- Claude генерира преводите
- Codex CLI ги записва в PostgreSQL
- Redis кешира преводите
- UI copy за homepage и category страниците вече се подава от PostgreSQL през namespaced endpoint (`homepage.*`, `category.*`)
- **Source of Truth за езици**: `apps/web/lib/locales.ts` (34 поддържани езика)

### Важно правило за t() функцията
- Ключовете се подават БЕЗ namespace префикс
- Правилно: `t(dict, 'heading')`
- ГРЕШНО: `t(dict, 'privacy.heading')`
- Причина: API-то връща ключовете без namespace префикс (strips автоматично)
- Това важи за ВСИЧКИ namespaces в проекта

### Namespace `footer` (seed: `seed_footer_translations.py`)
- Глобален namespace за футър линкове и правни бележки
- Текущи ключове: `privacy_policy_link`, `cookies_link`, `terms_link`, `register_privacy_note`, `register_privacy_link`, `provider_terms_link`, `withdrawal_link`, `contact_dsa_link` (8 ключа общо)
- 34 езика с реални преводи
- seed_footer_translations_p2.py съдържа provider_terms_link и withdrawal_link (2 ключа × 34 езика = 68 rows, добавен 2026-05-19)
- seed_footer_translations_p3.py съдържа contact_dsa_link (1 ключ × 34 езика = 34 rows, добавен 2026-05-20)

### Namespace `contact_dsa` (seed: `seed_contact_dsa_p1.py + seed_contact_dsa_p2.py`)
- DSA Contact Point страница (DSA чл. 11)
- 17 ключа, seed скриптове: seed_contact_dsa_p1.py + seed_contact_dsa_p2.py
- EN/BG/PL имат пълни преводи; останалите 31 езика fallback към EN за body текстове

### Namespace `cookie_banner` (seed: `seed_cookie_banner_translations_1/2/3.py`)
- Добавен ключ `cookie_privacy_link` (2026-05-11) — 34 езика

### SEO & Internationalization Infrastructure
- **Автоматизация**: Автоматично генериране на `hreflang` за всички 34 езика чрез `generateHreflangAlternates`.
- **Метаданни**: Използване на Metadata Template (`%s | Nevumo`). Преводите в БД са без бранд суфикси.
- **Structured Data**: JSON-LD схеми (`Organization`, `WebSite`, `LocalBusiness`) през `lib/seo.ts`. Динамична адаптация според езика.
- **Валидация**: Playwright + Phoenix за SEO одит на рендериран код.
- **Canonical Tags**: Автоматично генериране на абсолютни canonical URLs за всички City Landing страници чрез `NEXT_PUBLIC_SITE_URL`.
- **Universal Slug Logic**: Унифицирана логика за генериране на slugs между Frontend (`apps/web/lib/slug-utils.ts`) и Backend (`apps/api/services/provider_service.py`), поддържаща специални символи за 34 езика (Turkish İ/ı, German ü/ö, Icelandic ð/þ, Cyrillic).

### SEO Audit & Fixes (June 9, 2026)

**Trigger:** Google Search Console notification — "Duplicate without user-selected canonical"

**Root cause discovered:** Vercel was configured with `www.nevumo.com` as Primary domain,
causing `nevumo.com` to 307-redirect to `www`. Google saw both as duplicates.

**Fixes applied:**

1. **Vercel Domain Config** (no code change):
   - `nevumo.com` → changed from "Redirect to www" to **Primary Production**
   - `www.nevumo.com` → changed from Production to **301 Permanent Redirect → nevumo.com**

2. **Cloudflare DNS** (no code change):
   - `www.nevumo.com` CNAME record → changed from DNS only to **Proxied** (orange cloud)

3. **terms/page.tsx** — `apps/web/app/[lang]/terms/page.tsx`:
   - Was missing: canonical, hreflang (34 languages), OpenGraph tags
   - Added: `generateHreflangAlternates('/terms')`, canonical, OG block
   - Added modal noindex: `robots: isModal ? { index: false } : { index: true }`

4. **Legal pages modal noindex** — added `?modal=true` → noindex pattern to all 6 legal pages:
   - `apps/web/app/[lang]/privacy/page.tsx`
   - `apps/web/app/[lang]/cookies/page.tsx`
   - `apps/web/app/[lang]/terms/page.tsx`
   - `apps/web/app/[lang]/terms-provider/page.tsx`
   - `apps/web/app/[lang]/contact-dsa/page.tsx`
   - `apps/web/app/[lang]/withdrawal/page.tsx` — required server wrapper pattern
     (renamed to WithdrawalClient.tsx + new page.tsx server component)

5. **robots.ts** — `apps/web/app/robots.ts`:
   - Added to disallow array: `/*/provider/dashboard`, `/*/client/dashboard`, `/*/auth`

**Verification:** All 5 automated Playwright tests PASSED (June 9, 2026):
- robots.txt dashboard blocking ✅
- terms canonical + 34 hreflang tags ✅
- modal noindex on all 6 legal pages ✅
- non-modal legal pages indexable ✅
- www redirect chain working ✅

**Google Search Console:** "Validate Fix" submitted for both issues (June 9, 2026).

**Known remaining items (next sprint):**
- og:url missing on city and category pages
- JSON-LD missing on legal pages

### Google Search Console — Excluded by 'noindex' tag (June 14, 2026) — RESOLVED

**Trigger:** GSC email notification — "New reason preventing your pages from being indexed: Excluded by 'noindex' tag"

**Investigation:**
- 1 URL affected: `https://www.nevumo.com/en/auth?category=cleaning` (last crawled: Jun 7, 2026)
- URL is on `www.nevumo.com` — stale crawl from before the June 9 domain fix (www → nevumo.com).
- The `/auth` page is intentionally noindexed — login/registration pages must not appear in search results.
- The `?category=cleaning` parameter is a post-lead-submission redirect parameter. Google followed this link and reached the auth page.

**Conclusion:** Intentional and correct behavior. No bug.

**Fix applied (June 14, 2026):**
- `apps/web/app/robots.ts` — Added `/*/auth` to the disallow array to prevent Googlebot from crawling auth pages entirely, saving crawl budget and eliminating future GSC noise.
- Disallow array is now: `/*/provider/dashboard`, `/*/client/dashboard`, `/*/auth`

**Action taken:** "Validate Fix" to be submitted in GSC after deploy.

### Category Page Visual Breadcrumb (June 9, 2026) — COMPLETE

**Файл:** `apps/web/app/[lang]/[city]/[category]/page.tsx`

**Проблем:** Category listing страниците имаха breadcrumb само като JSON-LD Schema.org — видим за ботове, но не и за потребителите.

**Решение:** Добавен визуален `<nav>` breadcrumb между `</header>` и `<main>`. Стилът съвпада с `ProviderFullPage.tsx` breadcrumb (city › category › provider). `<main>` padding сменен от `py-12` на `pt-4 pb-12` за мобилен.

**Структура:** `[CityName] › [CategoryName]` — cityName от getCityBySlug, categoryName от homepageT. Без нови translation keys, без seed скрипт, без backend промени.

### Global Language Switcher (May 2026)

Имплементиран глобален превключвател на езика достъпен на всички страници.

**Архитектура:**
- `proxy.ts` — вече съдържаше пълна language detection логика (без промени):
  - URL сегмент → cookie `lang` → Accept-Language header → fallback `en` 
- `apps/web/lib/locales.ts` — добавени два нови обекта:
  - `LANGUAGE_DISPLAY_NAMES` — имена на 34 езика на собствения им език
  - `LANGUAGE_FLAGS` — emoji флагове за всеки език
- `apps/web/components/GlobalFooter.tsx` — нов компонент с props `{ lang: string; minimal?: boolean }`:
  - Пълна версия: copyright + Language Switcher
  - Минимална версия: само Language Switcher
  - Dropdown: searchable, отваря се нагоре (bottom-full), показва флаг + име
  - При смяна: записва cookie `lang` (30 дни) + router.push() към новия URL
- `apps/web/components/SmartGlobalFooter.tsx` — wrapper компонент:
  - Автоматично избира minimal=true за /dashboard URLs, minimal=false за останалите
- `apps/web/app/[lang]/layout.tsx` — нов файл, рендерира SmartGlobalFooter за всички публични страници
- Dashboard layouts (provider и client) — НЕ съдържат собствен Footer; покриват се от [lang]/layout.tsx

**GDPR:** Cookie `lang` е strictly necessary functional storage — не изисква consent.

**Скейлинг:** Нов език = един ред в SUPPORTED_LANGUAGES + LANGUAGE_DISPLAY_NAMES + LANGUAGE_FLAGS.

### Production Ready Status (April 30, 2026)
- **Technical SEO**: Системата е напълно готова за производство по отношение на техническото SEO
- **Scalability**: Архитектурата поддържа мащабиране до 10,000+ локации без ръчна интервенция
- **Automation**: Всички SEO елементи (canonical tags, JSON-LD, hreflang, slugs) се генерират автоматично
- **Performance**: JSON-LD и canonical tags се генерират server-side (SSR) за оптимална скорост
- **Compliance**: Следва напълно Google's structured data guidelines и SEO best practices

### Supported languages (34):
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, is, it, lb, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, ru, sk, sl, sq, sr, sv, tr, uk

- Default language: en
- UI translation seed status (April 30, 2026):
  - `43` homepage keys per language
  - `26` category-page keys per language (includes preposition keys added May 2026)
  - `69` total UI keys per language
  - `2,856` rows in `translations` for homepage/category namespaces across 34 languages (includes preposition keys: +68 rows)
  - `351` provider_dashboard keys per language (navigation, labels, messages, status, buttons, analytics, QR code, profile setup, settings, reviews, services, lead search & notes, lead details modal, TikTok share button)
  - `39` city-page keys per language (hero, search, CTA, empty state, how it works, SEO, prepositions)
  - `11,866` rows in `translations` for provider_dashboard namespace across 34 languages
  - `1,326` rows in `translations` for city namespace across 34 languages (includes preposition keys: +102 rows; full 34-language support added June 1, 2026 - previously only EN, BG, PL)
  - `2,856` rows in `translations` for `client_dashboard` namespace across 34 languages (includes Client Notes feature: 10 keys × 34 languages = 340 rows)
  - `1,020` rows in `translations` for `provider_dashboard` namespace across 34 languages (includes Widget page: 25 keys × 34 languages = 850 rows)
  - `340` rows in `translations` for `widget` namespace across 34 languages (relative time translations: 8 keys × 34 languages = 272 rows; error messages: 2 keys × 34 languages = 68 rows)
  - `646` rows in `translations` for `withdrawal` namespace across 34 languages (19 keys × 34 languages) — seed script: `seed_withdrawal_translations_4.py` (May 15, 2026)
    - New error keys: `widget.phone_error` (phone validation error message) and `widget.error_message` (general form error message)
  - **Dynamic Preposition & Declension Logic (May 2026)**: Added preposition and grammatical declension support (e.g., PL: w/we, Warszawa → Warszawie/Warszawy)
    - City namespace: preposition_base, preposition_modified, footer_in, locative_form, genitive_form
    - Category namespace: preposition_base, preposition_modified
    - Helper function: `apps/web/lib/cityHelpers.ts` - `getLocalizedCityText()`
    - **Applied to**: metadata titles, descriptions, headings, and footer links in homepage, city and category pages, ensuring grammatically correct output for Polish and other languages.

---

## Engineering Rules (CRITICAL)

- Никога не рефакторирай код извън текущата задача
- Никога не добавяй функционалност, която не е поискана
- Никога не модифицирай .env файлове
- Никога не използвай hardcoded localhost или портове в кода. Винаги използвай `config.settings` в Backend и `API_BASE` във Frontend.
- Скриптовете за сийдване трябва да използват централизираната база данни и Redis чрез `apps.api.database` и `apps.api.dependencies`.
- **Валидация на преводи**: Всички ключове в `translations` таблицата ЗАДЪЛЖИТЕЛНО трябва да следват патърна `namespace.key` (напр. `auth.login_title`). Валидацията е на ниво SQLAlchemy модел и Pydantic схема.
- Винаги спазвай текущата архитектура
- **API URL Configuration (May 28, 2026)**: Client-side API calls should use relative URLs by default (`process.env.NEXT_PUBLIC_API_URL || ''`) to support automatic local network access. Only set `NEXT_PUBLIC_API_URL` to an absolute URL for cross-domain production scenarios.

### TypeScript
- Strict mode задължително
- Забранен any тип

### Python
- Type hints задължителни
- Използвай Pydantic за validation

### Financial Logic
- Използвай Decimal (Python)
- Никога float за пари

### Mobile & CSS Rules (CRITICAL)
- **Android Chrome touch routing rule:** Any element with onClick that overlaps a scroll container MUST have touch-pan-y class. Without it, Chrome delays scroll activation waiting to distinguish tap vs scroll. iOS Safari is unaffected.
- **Dashboard layout rules (КРИТИЧНО):**
  - Outer wrapper MUST be h-screen (not min-h-screen) + overflow-hidden
  - Flex-col wrapper MUST have min-h-0
  - main scroll container MUST have overflow-auto + min-h-0 + touch-pan-y
  - SmartGlobalFooter MUST NOT render globally on dashboard pages 
    (isDashboardPath() guard in SmartGlobalFooter.tsx returns null by default)
  - SmartGlobalFooter MUST be rendered INSIDE <main> with force={true} 
    in each dashboard layout so footer is visible on scroll
  - Adding a new dashboard section = add SmartGlobalFooter inside its <main>

---

## AI Behavior Rules (IMPORTANT)

- Отговорите трябва да са practically oriented (без теория)
- Да се съобразяват със съществуващия stack
- Да не предлагат технологии извън stack-а, освен ако не е изрично поискано
- Да мислят в контекста на marketplace (clients + providers)
- Да приоритизират performance и scalability
- Да предлагат production-ready решения

---

## Priority Focus

1. SEO (critical for growth)
2. Conversion (landing → signup → action)
3. Scalable architecture
4. Clean DX (developer experience)

### Current Go-To-Market Focus (April 2026)
- Single-city launch playbook first: Warsaw before multi-city rollout
- Single-country proof with limited categories before expansion
- Provider-first homepage to acquire supply
- Client-first category pages to capture SEO demand and convert leads

---

## Roadmap Status

### ✅ Complete
- **Language Switch City Persistence Fix (June 7, 2026)** — COMPLETE:
  - **Problem**: Switching the display language changed the Hero city (e.g., switching to `pl` showed Warsaw even if the user was browsing Sofia in Bulgarian).
  - **Root cause**: `resolveDefaultCity()` reaches Priority 3 (`LANGUAGE_TO_CITY` mapping) when no `nevumo_city` cookie exists. Changing language changes the lang code, which changes the mapped city.
  - **Fix**: `handleLanguageChange` in `GlobalFooter.tsx` now reads the current city and locks it into `nevumo_city` cookie before navigating to the new language URL. Read priority inside the handler: (1) `nevumo_city` cookie → (2) `nevumo_ctx` localStorage → (3) `LANGUAGE_TO_CITY[currentLang]` fallback.
  - **TypeScript fix**: `cookieMatch?.[1]` instead of `cookieMatch[1]` to satisfy strict null checks in production build.
  - **Affected files**:
    - `apps/web/lib/default-city.ts` — added `getDefaultCityForLang(lang: string): string` export
    - `apps/web/components/GlobalFooter.tsx` — added `readCurrentCity(currentLang)` helper + city-lock logic as first two lines of `handleLanguageChange`
  - **Result**: Hero city is unchanged when user switches language. City changes only on explicit selection via `/izberi-grad`.
- **Web Push Notifications (June 7, 2026)** — COMPLETE: pywebpush backend, VAPID keys, push_subscriptions table, push service, 3 API endpoints, Service Worker push/notificationclick handlers, usePushNotifications hook, provider settings toggle. Full coverage: providers notified on new leads + new reviews; clients notified on lead status changes + review replies.
- **Outreach email Jinja2 fix — FIXED (June 18, 2026):**
  send_outreach_bulk.py създаден в apps/api/scripts/.
  Template в apps/api/scripts/templates/outreach_email_pl.html.
  jinja2>=3.1.0 добавен в requirements.txt.
  Bulk скриптът чете outreach_ready.csv (email, business_name, claim_token),
  рендерира с Jinja2 Template.render(), изпраща чрез Resend (support@nevumo.com),
  rate limit 37s между имейли (100/час), idempotent via outreach_sent_log.csv.
  Следваща стъпка: Task 2A seed_unclaimed_providers.py → произвежда outreach_ready.csv.
- **Claimed Profiles — Task 3Б Art. 14 GDPR Confirmation Email (June 20, 2026):** ✅ ЗАВЪРШЕНА
  Template: apps/api/services/templates/article14_confirmation_pl.html.
  send_article14_notification() updated in email_service.py — new signature:
  (to_email, business_name, dashboard_link, nip=None, provider_phone=None,
  scraped_email=None, provider_website=None, category_label="usługi").
  Renders Jinja2 template, sends via noreply@nevumo.com, non-blocking (try/except + [EMAIL_WARNING]).
  Call site updated in apps/api/routes/provider.py ~line 675.
  Test script: apps/api/scripts/test_article14_send.py.
  Email tested ✅ — correct design, data table, legal blocks, links verified.
  GDPR compliance: layered approach (EDPB approved) — key info inline, details via Privacy Policy link.
  Automated processing disclosed: ranking + badge systems (no legal effects, commercial visibility impact).
  Supervisory authorities: UODO (Poland) + КЗЛД (Bulgaria) both mentioned.
  URL bug fixed (June 20, 2026): /pl/terms-providers → /pl/terms-provider in both
  apps/api/services/templates/article14_confirmation_pl.html AND
  apps/api/scripts/templates/outreach_email_pl.html.
  Next: Task 2A seed_unclaimed_providers.py → outreach_ready.csv (Kimi-2.6).
- **Claimed Profiles — Data Collection (June 14 2026):** Warsaw CEIDG scraper complete (`apps/scripts/collect_ceidg_providers.py`). Collected 2,375 unique providers (701 with email, 257 with phone). PKD codes: cleaning 81.21.Z/81.22.Z/81.29.Z, massage 96.04.Z/96.23.Z/86.90.A/86.99.D, plumbing 43.22.Z/43.21.Z. Multi-layer acquisition planned: CEIDG website re-scrape → email extractor → Panoramafirm.pl scraper (Fixly отхвърлен — no browsable directory) → Bing API → SMS campaign. Full roadmap: `docs/claimed_profiles_plan.md`. Target: 3,000+ emails → 240-450 claimed profiles for Warsaw launch.
- **Claimed Profiles — CSV Clean + CEIDG Re-scrape (June 15-16 2026):**
  - CSV cleaning complete: 2,375 → 2,122 rows, script: clean_ceidg_csv.py
  - Result: 633 emails, 230 phones, all NIPs valid
  - IMPORTANT for seed script (2A): column "address" is broken (contains emails) → load as empty
  - IMPORTANT for seed script (2A): 176 partnership names "1. X, 2. Y" → take only first one
  - CEIDG re-scrape complete (June 16 2026): 51 websites from 2,122 rows (2.4%)
  - Output: apps/scripts/warszawa_providers_with_websites.csv
  - Next step: 1Ж — Bing API for remaining 2,071 firms without website
- **Claimed Profiles — Panoramafirm.pl Scraper (June 15-17 2026):** ✅ ЗАВЪРШЕНА
  - Fixly.pl отхвърлен: no browsable directory, GraphQL само count
  - Скриптове: scrape_panoramafirm.py (Playwright за листинг) + panoramafirm_requests_only.py (requests за профили)
  - Output: panoramafirm_emails_final.csv — 19,147 записа | 612 уникални имейла | 967 уебсайта
  - Ключово откритие: data-popup-param-email атрибут в статичен HTML → не е нужен Playwright
  - requests-only подход: 10x по-бързо, без Playwright memory leak
  - 233 фирми с уебсайт без имейл → Task 1З email extractor
  - Телефоните са call-tracking номера (unusable)
  - CEIDG re-scrape (1В): завършен — само 51 уебсайта (2.4%), Task 1Г пропусната
  - Общо имейли преди 1З: ~1,200 уникални (CEIDG 633 + Panoramafirm 612)
- **Claimed Profiles — Task 1З Website Email Extractor (June 17 2026):** ✅ ЗАВЪРШЕНА
  - Script: apps/scripts/extract_emails_from_websites.py
  - 308 уникални домейна посетени от 233 target реда
  - 160 нови имейла извлечени (51.9% success rate)
  - Техника: requests + BeautifulSoup, homepage + /kontakt + /contact
  - Cleanup: regex двустъпков fix за мръсни имейли → 0 мръсни
  - Общо уникални имейли след 1З: ~1,360 (CEIDG 633 + Panoramafirm 612 + websites 160)
  - Следваща: Task 1Д — SMS кампания (230 телефона, SMSapi.pl, ~4 EUR)
  - CEIDG technical facts (critical for future scripts):
    * API dead, direct NIP URL doesn't work
    * Search by NIP (#MainContentForm_txtNip) + PKD (#MainContentForm_txtPkd) → button #MainContentForm_btnInputSearch
    * headless=False required (Akamai blocks headless)
    * Website label: "Adres strony internetowej" (not "Strona")
    * sync_playwright, headless=False, viewport 1920x1080, real Chrome UA
- **Claimed Profiles — Task 1Ж DuckDuckGo Website Finder (June 17 2026):** ✅ ЗАВЪРШЕНА
  - Script: apps/scripts/bing_website_finder.py
  - Targets: 1,473 реда (без email + без website)
  - Намерени уебсайтове: 562 (38% success rate)
  - Encoding fix: utf-8-sig (BOM)
  - Blocklist: social media + directories
  - Output: warszawa_providers_with_websites.csv (website колона обновена)
- **Claimed Profiles — Task 1Ж-ext Email Extractor CEIDG (June 17 2026):** ✅ ЗАВЪРШЕНА
  - Script: apps/scripts/extract_emails_ceidg.py
  - Targets: 568 реда (website != "" AND email == "")
  - Намерени имейли: 231 (40.7% success rate)
  - Стратегия: homepage + /kontakt + /contact, https с http fallback
  - Output: warszawa_providers_with_websites.csv (email колона обновена)
  - CEIDG CSV финален резултат: 864 имейла | 613 уебсайта | 2,122 реда
- **Claimed Profiles — Backend (Task 2B, June 14 2026)** — COMPLETE: Claim endpoint pair added to apps/api/routes/providers.py:
  - GET /api/v1/providers/claim/{token} — public profile preview for claim landing page
  - POST /api/v1/providers/claim/{token} — authenticated claim action; validates role, deletes registration draft (detected by slug prefix "draft" + business_name = user email), links user_id to unclaimed profile, sets is_claimed=TRUE, clears claim_token, recalculates verification_level, sends Art. 14 GDPR email (non-blocking)
  - Draft detection: dual condition (slug.startswith("draft") AND business_name == user.email) to prevent accidental deletion of real profiles
- **Related Links Category Names Fix (June 7, 2026)** — COMPLETE:
  - **Problem**: "Виж също" section on category pages showed category names in English on all languages. Root cause: `category.h1_cleaning/massage/plumbing` keys existed in `translations` table but were empty strings — falsy in JS, always triggering English fallback.
  - **Root cause (architectural)**: Using `translations` table for category names is wrong. The correct source is `category_translations` table (102 rows: 3 categories × 34 languages).
  - **Fix**: `apps/web/app/[lang]/[city]/[category]/page.tsx`
    - Added `getCategories(lang)` import from `@/lib/api`
    - Replaced hardcoded `relatedLinksByCategory` Record with dynamic logic:
      - Calls `getCategories(lang)` → fetches from `GET /api/v1/categories?lang={lang}`
      - Filters out current category by slug
      - Builds labels: `${cat.name} ${prepBaseCat} {city}` → passed to `getLocalizedCityText()`
  - **Scalability**: Adding a new category to DB automatically appears in related links. Zero code changes needed.
  - **Note**: `category.h1_cleaning/massage/plumbing` keys remain in DB (empty) — not removed, not used.
- **Provider CTA with City/Category Pre-fill (May 2026)** — COMPLETE:
  - **Category page header CTA**: Replaced static "Become a specialist" link with 2-line dynamic CTA using new translation keys `nav_cta_line1` and `nav_cta_line2` (category namespace, 68 rows × 34 languages). Href updated to `/${lang}/auth?mode=register&role=provider&city=${citySlug}&category=${categorySlug}`
  - **Auth flow**: `LoginClient.tsx` now saves `city` and `category` query params to localStorage (`nevumo_selected_city`, `nevumo_selected_category`) after successful provider registration
  - **Onboarding Step 2**: `profile/page.tsx` reads `nevumo_selected_city` from localStorage in a separate `useEffect([cities])` and pre-fills city dropdown. Fix: city.id cast to `String()` to match `cityOptions` value type (string[])
  - **Onboarding City Dropdown Fix (June 7, 2026)**: `profile/page.tsx` previously called `getCities('BG', lang)`, `getCities('RS', lang)`, `getCities('PL', lang)` separately. Replaced with single `getAllCities(lang)` call using `GET /api/v1/cities/all?lang={lang}`. Both `/izberi-grad` and the onboarding city dropdown now use the same data source and show all cities from the database.
  - **Seed script**: `apps/api/scripts/seed_nav_cta_translations.py`
- **Legal & Compliance (May 2026)** — COMPLETE:
  - /[lang]/terms страница с онлайн форма и PDF изтегляне на withdrawal form
  - /[lang]/provider-terms страница (Общи условия за доставчици)
  - /[lang]/cookies страница (Cookie Policy)
  - LegalModal компонент (apps/web/components/auth/LegalModal.tsx) — преглед на документи без напускане на текущата страница, iframe подход с ?modal=true параметър
  - **Namespace Standardization (May 27, 2026):** Fixed namespace mismatches in LegalModal integration:
    - `terms-provider` → `provider_terms` (matches document page namespace)
    - `contact-dsa` → `contact_dsa` (matches document page namespace)
  - **Dismiss Button Translation (May 27, 2026):** Added `dismiss_button` key to `auth` namespace for all 34 languages (seeded from `pwa.dismiss_button`)
  - **Integration Points:**
    - ProviderWidget: Terms & Privacy links open modal
    - GlobalFooter: All 6 legal links open modal instead of page navigation
    - LoginClient: Terms link uses `provider_terms` namespace
    - OAuthTermsClient: Terms link uses `provider_terms` namespace
  - **Embed Mode Support (May 27, 2026):** GlobalFooter hidden in embed mode via `[data-global-footer] { display: none !important; }` CSS rule
  - Checkbox за T&C при email регистрация в LoginClient.tsx — различни документи за client/provider
  - oauth-terms страница и OAuthTermsClient.tsx — приемане на условия при Google OAuth преди създаване на акаунт
- **Provider Dashboard Language Context Propagation (May 27, 2026)** — COMPLETE:
  - Fixed language context propagation in provider dashboard to ensure widget preview and public profile links use the current dashboard language
  - Backend: Added `lang` query parameter to `/api/v1/provider/dashboard` endpoint, passed to `build_public_url()` and `build_qr_public_url()`
  - Frontend: Updated `getProviderDashboard()` to accept and forward `lang` parameter from dashboard layout
  - Result: `/bg/provider/dashboard/widget` now shows Bulgarian widget preview, public profile link opens `/bg/...` instead of `/en/...`
  - Google OAuth flow обновен: state параметърът носи lang|intent|category|city, backend проверява дали user съществува преди създаване, новите провайдъри получават автоматично providers запис
  - OAUTH_REDIRECT_BASE добавен в root .env и apps/api/config.py като конфигурируема променлива
- **Google OAuth City/Category Pre-fill Fix (May 2026)** — COMPLETE:
  - OAuthTermsClient.tsx: reads `city` and `category` from searchParams, saves to localStorage before redirect
  - oauth-callback/page.tsx: reads `city` and `category` from searchParams, saves to localStorage before redirect
  - Both email and Google OAuth registration now correctly pre-fill city and category dropdowns in onboarding Step 2
  - Root cause: city/category params were passed through OAuth flow but never written to localStorage on frontend
- **N+1 Fix — Category Page Performance** — COMPLETE:
  - `GET /api/v1/providers` обогатен с batch данни: profile_image_url, description, jobs_completed, leads_received, review_count, latest_lead_preview, services[]
  - Redis cache key обновен: `providers:{category_slug}:{city_slug}:{lang}`, TTL 3600s
  - Category page: премахнат Promise.all с N x getProviderBySlug() извиквания
  - apps/web/lib/api.ts: API_BASE обновен да използва API_URL (Docker SSR) преди NEXT_PUBLIC_API_URL
  - .env: добавен API_URL=http://nevumo-api:8000 за SSR в Docker
- **Provider Image Hydration Mismatch Fix (May 10, 2026)** — COMPLETE:
  - Fixed React hydration mismatch for provider images by implementing `resolveStaticUrl()` utility in `apps/web/lib/urlUtils.ts`
  - Utility uses relative URLs for local development (works on localhost:3000 and 192.168.0.15:3000)
  - Absolute URLs for production CDN (when backend returns them via `STATIC_FILES_BASE_URL`)
- **Google OAuth Onboarding Fix (May 31, 2026)** — COMPLETE:
  - /pl/dolacz — всички 6 auth линка вече подават intent=provider
  - OAuthTermsClient.tsx — нови провайдъри (is_new_user=true) се redirect-ват към /provider/dashboard/profile
  - Backend /api/v1/auth/google/complete — добавен is_new_user флаг в response
  - Eliminates hydration mismatch by ensuring server and client render identical HTML
  - Added `NEXT_PUBLIC_STATIC_URL` to `.env.example` documentation
  - Backend `STATIC_FILES_BASE_URL` config supports CDN/S3 in production
- **Data Export Endpoint (GDPR Article 20 - Right to Portability) — May 8, 2026** — COMPLETE:
  - **Backend**: Implemented `GET /api/v1/user/export` endpoint in `apps/api/routes/user.py` with `apps/api/services/export_service.py`
  - **Rate Limiting**: 1 request per 24 hours per user (Redis key: `export_rl:{user_id}`, TTL 86400)
  - **Response Headers**: `Cache-Control: no-store` for Safari download fix
  - **Data Exported**: User profile, leads submitted, services listed (if provider), reviews, consent log
  - **Frontend**: "Download my data" buttons in client dashboard settings and provider dashboard settings
  - **Translations**: 7 keys in `settings` namespace × 34 languages = 238 rows seeded
  - **Keys**: export_title, export_description, export_button, export_success, export_error, export_rate_limited, export_format
  - **Error Handling**: 429 response displays `settings.export_rate_limited` translation key
- **Polish City Declension - Homepage & City Pages (May 2026)** — PARTIALLY COMPLETE:
  - **Completed**: Polish homepage (/pl) - All declension and dynamic prepositions working correctly
  - **Completed**: Polish city page (/pl/warszawa) - All declension and dynamic prepositions working correctly
  - **Completed**: Bulgarian and English regression tests - Passing
  - **Completed**: Seed script executed and database populated with declension forms for Warsaw
  - **Completed**: cityHelpers.ts extended with grammaticalCase parameter
  - **Completed**: Homepage and city page components updated
  - **Outstanding Issues**: Polish category pages (/pl/warszawa/sprzatanie, /pl/warszawa/hydraulik, /pl/warszawa/masaz):
    - Meta titles showing "we Warszawa" instead of "we Warszawie" (wrong case)
    - Hero headings showing English "in" instead of Polish prepositions
    - FAQ sections showing English text
    - Related links showing "w Warszawie" instead of "we Warszawie" (missing w→we)
    - Bottom CTA showing "w Warszawie" instead of "we Warszawie"
  - **Next Steps**: Category pages require separate task to integrate getLocalizedCityText with grammaticalCase parameter
  - **Scope**: Currently only Warsaw (Warszawa) has declension forms seeded
- **SEO City Grammatical Case Fix (June 1, 2026)** — COMPLETE:
  - **Problem**: Slavic languages (bg, cs, sk, ru, uk, sr, hr, mk, sl, pl) incorrectly used locative form for city names in SEO p1 paragraphs where city is sentence subject (e.g., "Warszawie oferuje..." instead of "Warszawa oferuje...")
  - **Solution**: Added conditional logic in `apps/web/app/[lang]/[city]/[category]/page.tsx` to use direct `.replace('{city}', cityName)` (nominative) for Slavic languages in p1 paragraphs while keeping `getLocalizedCityText()` for other SEO elements (h2, h3, p2, p3)
  - **Implementation**: Added `useDirectCityName` flag based on existing `slavicLanguagesWithDeclension` array
  - **Affected Keys**: `category.seo_massage_p1`, `category.seo_cleaning_p1`, `category.seo_plumbing_p1`
  - **No Database Changes**: Solution is frontend-only, no seed script or database modifications needed
  - **Commit**: de5e907
- **Hardcoded City Names Cleanup (June 1, 2026)** — COMPLETE:
  - **Problem**: All 34 languages in `seed_ui_translations.py` had hardcoded city names (Warsaw, Warszawa, Варшава, etc.) instead of `{city}` placeholder in 7 category keys, causing all city pages to display hardcoded city names
  - **Solution**: Deleted hardcoded values from Neon production database using SQL script and removed them from `seed_ui_translations.py` to allow code fallback logic to generate dynamic text with `{city}` placeholder
  - **SQL Script**: Created `delete_hardcoded_city_translations.sql` to delete 7 keys from all 34 languages (238 rows total)
  - **Affected Keys**: 7 category translation keys with hardcoded city names
  - **Result**: City names now display correctly on all pages using dynamic `{city}` placeholder replacement
  - **Polish Grammar Fix**: Also fixed "specjalistówe" → "specjalistów" grammatical error in Polish SEO content
- **SEO Translation Fixes (May 6, 2026)** — COMPLETE:
  - Added SEO cleaning keys for all 34 languages (not just bg/en/pl)
  - Added FAQ title key for all 34 languages
  - Added category.price_on_request key for all 34 languages
  - Fixed Polish SEO keys (removed pl from LANGUAGES_WITH_FULL_KEYS, deleted empty p3, re-seeded)
  - Removed duplicate FAQ section that was duplicating SEO content
  - Added {city} variable replacement to SEO section
  - All 34 languages now have complete SEO cleaning keys (6 keys each: h2, h3_1, h3_2, p1, p2, p3)
- **Phase 3B Part 1 SEO Translation Completion (May 7, 2026)** — COMPLETE:
  - Added missing SEO massage and plumbing keys for 15 languages (cs, da, de, el, es, et, fi, fr, ga, hr, hu, is, it, lb, lt)
  - Seed script: apps/api/scripts/seed_phase3b_part1_seo_keys.py
  - 136 translation rows inserted (9 keys per language: 5 massage + 4 plumbing)
  - All 34 languages now have complete SEO keys for cleaning, massage, and plumbing (18 keys total per category)
  - Redis cache cleared and servers restarted
- **FAQ Price Placeholder Fix (May 2, 2026)** — COMPLETE:
  - **Problem**: Users saw raw placeholders like `{min_price}` in FAQ answers when no price data was available.
  - **Fix**: Implemented aggressive placeholder removal and replacement with "Price on request" in `apps/web/app/[lang]/[city]/[category]/page.tsx`.
  - **Logic**: Any sentence containing price placeholders is replaced with localized "Price on request" when `hasValidPrice` is false.
  - **Safety**: Added a categorical cleanup step to ensure no placeholders remain in the final text.
  - **getPriceText**: Updated helper to always return `price_on_request` as a safe fallback.
- **Provider Page Optimization (April 30, 2026)** — COMPLETE:
  - **Error Fixes**: Eliminated "currency is not defined" ReferenceError and fixed HTML structure parsing errors in `page.tsx`.
  - **SEO**: Added `Service` Schema.org JSON-LD to provider widgets.
  - **Logic**: Robust multi-layer currency fallback (Provider Service -> City -> Country -> 'EUR').
- **Universal Currency Logic (April 30, 2026)** — COMPLETE:
  - **Logic**: Currency is now location-based (from `city.country_code`) rather than interface-language-based.
  - **BG Rule**: For Bulgaria (BG), currency is always "EUR" (active from 01.01.2026).
  - **Implementation**: `apps/web/lib/currency.ts` handles logic and formatting.
  - **Integration**: JSON-LD `LocalBusiness` and `ProviderWidget` UI updated to use the new logic.
- **Provider Page SEO Optimization (April 30, 2026)** — COMPLETE:
  - **Robots Logic**: Conditional `noindex, nofollow` for `?embed=1` views; `index, follow` for full pages.
  - **Canonical Tags**: Dynamic canonical URLs that prioritize the full page version.
  - **Localized Schema**: JSON-LD `LocalBusiness` now uses translated city names from the database.
  - **Universal City Map**: Replaced hardcoded `CITY_COUNTRY_MAP` with dynamic API-driven city data.
- **City Selection Page SEO Completion (April 30, 2026)** — COMPLETE:
  - Namespace: `city_selection` — 6 keys × 34 languages = 204 rows seeded
  - Keys: meta_title, meta_description, heading, empty_state, nav_link, footer_text
  - page.tsx updated: fetchTranslations, t(dict, key), generateStaticParams, JSON-LD CollectionPage
  - All hardcoded strings replaced with DB-backed translations
  - Tested: bg, en, pl — 42/42 PASS
- **Universal Slug Generation (April 30, 2026)** — SUCCESSFUL:
  - **Problem**: Inconsistent slug logic between Frontend and Backend, and limited support for special characters beyond Bulgarian.
  - **Solution**: Unified slug generation logic stack-wide.
  - **Frontend**: Removed hardcoded `locale: 'bg'` from `apps/web/lib/slug-utils.ts` and updated `apps/web/lib/slugify.ts` to use the robust `slugify` library.
  - **Backend**: Standardized `apps/api/services/provider_service.py` with a consistent `slugify` wrapper using pre-defined replacements to match Frontend behavior.
  - **Result**: Identical slug output across 34 languages, correctly handling Turkish (İ, ı), German (ü, ö), Icelandic (ð, þ), and Cyrillic characters.
- **City Fallback Chain Expansion (April 30, 2026)** — COMPLETE:
  - **Problem**: Providers with services in a specific city were seeing /izberi-grad instead of their city in the client dashboard
  - **Solution**: Expanded fallback chain in apps/api/services/client_service.py
  - **New fallback chain**:
    1. user.city_id
    2. Last lead as client
    3. City from provider's last service (if user is a provider)
    4. null → /izberi-grad
  - **Testing**: 4 scenarios tested — all passed successfully
- **City Context System (April 30, 2026)** — COMPLETE:
  - **Database**: Added `city_id INTEGER REFERENCES locations(id)` to users table (nullable, "last known context", not permanent residence)
  - **Index**: `idx_users_city_id` for efficient queries
  - **Architecture**: city_id represents "last known context", updated on registration from URL city parameter and on each new lead submission
  - **Fallback chain**: user.city_id → last lead (as client) → last service city (as provider) → null → /[lang]/izberi-grad
  - **New endpoint**: GET /api/v1/cities/active?lang={lang} — returns only cities with at least 1 active provider, Redis cached as `cities:active:{lang}`
  - **New page**: /[lang]/izberи-град — SSR city selection page with grid of active cities, SEO-indexable
  - **Client dashboard**: "Намери услуга" button redirects to /{lang}/{last_city_slug} if available, otherwise /{lang}/izberи-град
  - **Provider dashboard**: "Намери услуга" now redirects directly without switchRole API call if user already has client role
  - **Schema**: RegisterRequest updated with optional city_id field
- **Provider Dashboard "Find Service" Fix (April 29, 2026)** — SUCCESSFUL:
  - **Problem**: Clicking "Find Service" in the provider dashboard sidebar while already having a client role resulted in an `ALREADY_IN_ROLE` error (400) from the API.
  - **Fix**: Added a frontend check in `apps/web/components/dashboard/DashboardSidebar.tsx`.
  - **Logic**: If `user.role === 'client'`, the app now redirects directly to the client dashboard without calling the `switchRole` API.
- **Category Page Badge Update (May 25, 2026)** — COMPLETE:
  - Updated badge rendering in category page provider cards to use `verification_level` logic (0/1/2)
  - Level 0 (New): Changed from amber to blue (`bg-blue-50 text-blue-400`)
  - Level 1 (Verified): Green badge unchanged (`bg-green-100 text-green-700`)
- **Централизирана ctx система (nevumo_ctx) — May 31, 2026** — COMPLETE:
  - Нов файл: apps/web/lib/ctx.ts — getCtx(), setCtx(), clearCtx()
  - Нов компонент: apps/web/components/CtxCapture.tsx
  - Заменени: nevumo_selected_city, nevumo_selected_category, nevumo_city_preference → nevumo_ctx
  - CtxCapture добавен в: homepage, city page, dolacz page, CategoryPageClient
  - Правило: всяка page с [city]/[category] в пътя задължително включва CtxCapture
  - Seed fix: seed_onboarding_hero_v2.py и seed_delete_account_translations.py изпълнени срещу Neon
  - Sitemap fix: getCitiesActive() заменя getCities('BG') — Warsaw вече в sitemap
  - Google Search Console: верифициран, sitemap подаден (680 URLs, 31 май 2026)
  - Level 2 (Top Specialist): Changed from yellow to orange (`bg-orange-100 text-orange-700`)
  - Simplified Level 2 displayText logic to use ' – ' separator consistently
  - Badge colors now consistent across ProviderFullPage and category page provider cards
- **Provider Page Translation Fixes (May 23, 2026)** — COMPLETE:
  - **Problem**: Hardcoded Bulgarian texts appearing on provider page when Polish language was selected
  - **Solution**: Added provider_page.request_service translation key for all 34 languages to fix service card button text
- **Provider Page Service Selection Toggle (May 23, 2026)** — COMPLETE:
  - **Shared State Pattern**: Both service cards and chips use the same `selectedService` state with toggle logic
  - **Toggle Logic**: Click selected → deselect to null, click unselected → select
  - **Desktop Behavior**: Selected card + hover shows gray deselect button instead of orange select button
  - **Mobile Behavior**: Unselected shows `select_this_service`, selected shows `service_selected_confirm`
  - **Textarea Behavior**: Does NOT clear on deselect as per requirements
  - **Translation Keys**: Added 3 new keys in `provider_page` namespace (`select_this_service`, `service_selected_confirm`, `service_deselect`) for all 34 languages
  - **Seed Script**: `apps/api/scripts/seed_provider_page_service_select.py` (102 rows)
  - **API Note**: `get_namespaced_translations` in `apps/web/lib/ui-translations.ts` strips namespace prefix from keys, so frontend uses keys WITHOUT prefix (e.g., `select_this_service` NOT `provider_page.select_this_service`)
  - **Redis Cache Flush**: Required after seeding: `docker exec nevumo-redis redis-cli FLUSHALL`
  - **Seed script**: seed_provider_page_translations_p2.py (34 keys × 34 languages = 1,156 rows total including existing keys)
  - **Key pattern**: Translation keys must use namespace.prefix pattern (e.g., provider_page.request_service) to match frontend fetchTranslations() calls
  - **Solution**: Fixed translation namespace issue - API returns translations without namespace prefix (e.g., `price_per_hour`), but components were accessing them with full namespace (e.g., `provider_page.price_per_hour`)
  - **Changes**:
    - Changed translation keys in ProviderFullPage.tsx and LeadPanel.tsx from `provider_page.price_on_request`/`provider_page.price_per_hour` to `price_on_request`/`price_per_hour` (without namespace prefix)
    - Fixed merge order in page.tsx from `{ ...categoryT, ...providerPageT, ...widgetT }` to `{ ...categoryT, ...widgetT, ...providerPageT }` to ensure provider_page translations have priority
    - Added dynamic pricing logic based on service price_type (fixed, hourly, per_sqm, request) with proper currency and unit labels
    - Added `provider_page.price_per_hour` and `provider_page.price_on_request` translation keys for all 34 languages (seed script: seed_provider_page_price_units.py)
  - **Verification**: Spanish page (http://localhost:3000/es/belgrade/cleaning/et-lili) now correctly displays "A consultar" and "/h" instead of Bulgarian "По запитване" and "/ч"
  - **Fixed texts**: "✓ {jobsCompleted} завършени услуги", "Свържи ме с {providerName}", "Топ специалист в {city}", "За специалиста"
  - **Solution**: Replaced hardcoded texts with existing translation keys using dynamic injection
  - **Components updated**: `LeadPanel.tsx`, `StickyProviderCTA.tsx`, `ProviderFullPage.tsx`, `AboutSection.tsx`
  - **Translation keys used**: `provider_page.completed_jobs`, `provider_page.cta_button`, `widget.badge_top_specialist`, `provider_page.section_about`
  - **Additional fix**: Added `widget` namespace to translation fetching in provider page
  - **Badge logic**: Enhanced to handle both placeholder-based and direct city name appending
- **Docker Environment Variable Pattern Update (May 23, 2026)** — COMPLETE:
  - **Problem**: NEXT_PUBLIC_API_URL set to OrbStack internal IP (192.168.0.15:8000) which is not browser-accessible from Mac
  - **Solution**: Updated `.env` to production value (https://api.nevumo.com) and `.env.local` to host IP (http://192.168.0.15:8000)
  - **Benefit**: Enables local network access from other devices while maintaining production readiness
  - **Pattern**: `.env` contains production-ready value, `.env.local` (gitignored) contains local dev override

#### Provider Full Page (May 21, 2026) — В ПРОГРЕС
- Статус на задачите:
  - ✅ Задача A — Backend: Badge логика + DB migration
  - ✅ Задача B — Backend: Multi-image галерия
  - ✅ Задача C — Dashboard Gallery UI
  - ✅ Задача E — ShareButton интеграция в ProviderFullPage Hero секция → COMPLETE (May 22, 2026)
    - ShareButton добавен в HeroSection ActionRow (apps/web/components/provider/ProviderFullPage.tsx)
    - Translation keys share_button и link_copied вече заредени (seed_provider_page_translations_p2.py)
    - Fallback fix: navigator.clipboard + document.execCommand за HTTP/non-secure контексти
  - ✅ Задача F — Seed scripts за namespace provider_page и widget badge ключове
  - ✅ Задача D — ProviderFullPage компонент
  - ✅ Задача G — Lead submission flow restoration in LeadPanel.tsx — COMPLETE
    - LeadPanel.tsx contains full lead submission logic ported from ProviderWidget.tsx: lead API call, JWT linking, 429 handling, success screen Step1/Step2, email nudge, claim-email, localStorage, window.location.href redirect, phone validation, scrollIntoView, PWA install prompt
  - ⏳ Задача H — Правен текст: Badge система (предстои)
  - ⏳ Задача I — Category page badge актуализация (предстои)
  - ✅ Задача J — Mobile Sticky CTA за Provider страница — COMPLETE (May 22, 2026)
    - Нов компонент: apps/web/components/provider/StickyProviderCTA.tsx
    - Логика идентична с StickyLeadFormButton (md:hidden, isFormInView, paddingBottom)
    - Target: id="provider-lead-form" в ProviderFullPage.tsx
    - Translation key: cta_button (namespace: provider_page)
    - Seed скрипт: apps/api/scripts/seed_provider_cta_button.py (34 езика)
    - Изтрити грешно въведени zh преводи (24 реда)
    - Bugs fixed по време на имплементацията:
      - ProviderFullPage не зареждаше provider_page namespace (translations={} → translations={providerPageT})
      - t['provider_page.KEY'] → t['KEY'] в ProviderFullPage.tsx и LeadPanel.tsx (18 замени)
  - ✅ Задача K — Mobile Bottom Sheet Form — COMPLETE (May 23, 2026)
    - Нов компонент: apps/web/components/provider/BottomSheetForm.tsx
    - Slide-up анимация (translateY 100% → 0), overlay с click-to-close, X бутон горе дясно, body scroll lock
    - PhoneInput с usePhone hook (auto-fill за логнати, auto-prefix за анонимни)
    - Service chips, textarea за бележка, trust signal, submit бутон
    - Валидация: phone задължително + (услуга ИЛИ бележка) — грешка `error_service_or_note`
    - StickyProviderCTA.tsx обновен: onClick → onOpenSheet() prop вместо scroll
    - ProviderFullPage.tsx: isSheetOpen state, споделен selectedService между LeadPanel и BottomSheetForm
    - Pre-fill на notes при service card click: handleServicePreFill обвита в useCallback
    - useEffect dependency fix: onServicePreFill премахнат от deps, предотвратява двойно изпълнение
    - Select на услуга replace-ва notes (не append) — само една услуга активна едновременно
    - Deselect изчиства notes
    - Seed скрипт: apps/api/scripts/seed_provider_page_error_keys.py (1 ключ × 34 езика)
- Translation keys заредени в namespace provider_page: section_gallery, section_about, section_services, section_reviews, read_more, read_less, completed_jobs, meta_services, meta_cities, reviews_count, request_panel_title, request_panel_free, request_panel_no_commitment, or_general_request, phone_placeholder, notes_placeholder, cta_button, trust_verified, trust_free, trust_direct, share_button, link_copied, select_service, service_selected, meta_response_rate
- Translation keys заредени в namespace widget: badge_new_provider, badge_verified, badge_top_specialist
- Seed скриптове: seed_provider_page_translations_v2.py, seed_provider_page_translations_p2.py
- **Provider Dashboard Stats Fix (April 28, 2026)** — Retro-matched leads now counted:
  - **Problem**: Newly registered providers saw 0 on KPI cards (Total/New leads) despite retro-matched leads.
  - **Root cause**: `get_dashboard_stats()` in `apps/api/services/provider_service.py` only counted `Lead.provider_id == provider.id`. Retro-matched lives in `lead_matches` table.
  - **Fix**: `total_leads` replaced with UNION SQL query (leads + lead_matches). `new_leads` and `contacted_leads` updated to include `LeadMatch.status` 'invited'/'contacted'.
- **Delete Account — GDPR-compliant (April 25, 2026)**
  - Backend: `DELETE /api/v1/auth/account` (JWT required) in `apps/api/routes/auth.py` + `apps/api/services/auth_service.py`
  - Deletion order (single DB transaction):
    1. Nullify `leads.client_id` AND set `leads.phone = "deleted"` WHERE `client_id = user.id` (GDPR Art. 17 — phone is personal data)
    2. If provider exists: nullify `leads.provider_id`, delete `lead_matches`, `provider_cities`, `services`, then `providers` record
    3. Explicitly delete `reviews` WHERE `client_id = user.id` (NO ACTION FK — not cascaded)
    4. Explicitly delete `messages` WHERE `sender_id = user.id` (NO ACTION FK — preventive)
    5. Delete `user` record (cascade: `password_reset_tokens`, `magic_link_tokens`, `pending_lead_claims`, `providers`)
  - Handles all three cases: client-only, provider-only, both simultaneously
  - Frontend: inline confirmation panel (no modal) in both:
    - `apps/web/app/[lang]/provider/dashboard/settings/page.tsx`
    - `apps/web/app/[lang]/client/dashboard/settings/SettingsClient.tsx`
  - On success: `clearAuth()` + localStorage cleanup + redirect to `/${lang}`
  - Translations: 5 keys × 34 languages × 2 namespaces (`provider_dashboard`, `client_dashboard`) = 340 rows seeded
- **Issue 4 Fix — JWT Expiry Redirect Loop (June 23, 2026)** — RESOLVED:
  - **Problem**: Expired JWT caused infinite redirect loop between provider and client dashboard. `authFetch()` and `clientFetch()` did not handle 401 responses — provider layout redirected to client dashboard, client layout detected role=provider and redirected back, creating endless loop.
  - **Fix**: Added 401 interceptor in `apps/web/lib/provider-api.ts` (authFetch) and `apps/web/lib/client-api.ts` (clientFetch). On 401: `clearAuth()` removes cookie and localStorage, `window.location.replace()` redirects to `/{lang}/auth` with full page reload.
  - **Null safety**: Added `json.error?.code ?? 'UNKNOWN_ERROR'` in clientFetch to prevent crash when backend returns 401 with non-standard error body.
  - **Tested**: Manually verified in production on both provider and client dashboard.
- **Delete Account Bug Fix (June 16, 2026)**
  - **Root cause**: `reviews.client_id` FK is `NO ACTION` (not CASCADE). Users with reviews could not delete their account — PostgreSQL threw `ForeignKeyViolation: reviews_client_id_fkey`.
  - **Secondary issue**: `leads.phone` was not nullified on account deletion — personal data remained in DB after GDPR Art. 17 erasure request.
  - **Fix**: `apps/api/services/auth_service.py` — `delete_user_account()` updated:
    - `leads.phone` set to `"deleted"` alongside `client_id = None`
    - Explicit `Review` delete added before `db.delete(user)`
    - Explicit `Message` delete added before `db.delete(user)` (preventive — `messages.sender_id` also NO ACTION)
  - **Imports added**: `Review`, `Message` added to models import in `auth_service.py`
  - **Verified**: Account deletion confirmed working in production (June 16, 2026)
  - Translation keys: `delete_account_btn`, `delete_account_title`, `delete_account_warning`, `delete_account_confirm`, `delete_account_cancel`
- **Frontend Next.js 16 Compliance (April 21, 2026)** — Migrated from `middleware.ts` to `proxy.ts`:
  - **Reason**: Next.js 16 deprecated the `middleware.ts` convention in favor of `proxy.ts` for improved routing control.
  - **Fix**: Renamed `middleware.ts` to `proxy.ts` and updated the export to `export default function proxy`.
  - **Routing Restored**: Resolved a 404 error on `/bg/provider/dashboard/leads` caused by incompatible middleware handling in the new Next.js version.
- **Frontend Next.js 15+ Compliance (April 16, 2026)** — Completed full audit and remediation of Promise-based params:
  - **Audit Scope**: Reviewed all `page.tsx` and `layout.tsx` files in `apps/web/app/[lang]` for Next.js 15+ standards compliance
  - **Translation Consistency**: Verified `t()` function usage - all files correctly use keys without namespace prefixes (backend unpacks namespaces)
  - **Fix Applied**: Updated `apps/web/app/[lang]/auth/magic/page.tsx` to use `params: Promise<{ lang: string }>` and `searchParams: Promise<{ token?: string }>`
  - **Result**: All frontend pages now fully compliant with Next.js 15+ Promise-based params standard
- **Lead Submission Bug Fix (April 19, 2026)** — Fixed a critical issue where lead submissions failed with "Internal Server Error" (500):
  - **Root Cause**: PostgreSQL sequences for `lead_rate_limits` and `auth_rate_limits` were out of sync with existing data, causing `UniqueViolation` on the `id` column.
  - **Fix**: Synchronized all database sequences using `setval` to match current `MAX(id)` values.
- **Provider Profile Request Bottleneck Fix (April 20, 2026)** — Resolved request timeouts during profile updates:
  - **Fix**: Moved 34-language translation process to FastAPI `BackgroundTasks` for non-blocking immediate response.
  - **Robustness**: Improved `lib/provider-api.ts` with response validation and content-type checking.
- **Onboarding UX Fixes (April 19, 2026)**:
  - Added `noValidate` to forms to prevent browser-native interference.
  - Improved `slugifyText` for proper Bulgarian Cyrillic transliteration.
- **Auth Flow Robustness (April 19, 2026)** — Fixed back-button navigation issues:
    - Added `pageshow` listener to handle BFCache (back-button-restored pages)
    - Implemented session checks in all auth handlers to prevent redundant API calls
    - Added auto-login recovery in `handleRegister` to gracefully handle "Email already registered" errors by attempting a login with the same credentials
- **URL Audit & Centralized Networking (April 16, 2026)** — Completed a full audit and remediation of hardcoded URLs, IPs, and ports:
  - **Backend Centralization**: All URLs (magic links, QR codes, static files) now derive from `apps/api/config.py` settings. Hardcoded `localhost` fallbacks removed from `provider_service.py` and `main.py`.
  - **Frontend Consolidation**: `API_BASE` in `apps/web/lib/api.ts` is now the single source of truth for API communication. All API clients (`auth-api`, `provider-api`, `client-api`, `tracking`) use this shared constant.
  - **Seed Script Standardization**: Key seed scripts now use centralized DB/Redis connection logic from `apps.api.database`, ensuring consistency and avoiding redundant connection code.
  - **Docker Compose Alignment**: Updated configuration to use service names instead of `localhost` for inter-container communication.
- **Major Architectural Overhaul (April 14, 2026)** — Unified the project into a high-performance monorepo:
  - **New Monorepo Structure**: Unified root managed by Turborepo, decoupling `apps/api` and `apps/web` while sharing a consistent environment.
  - **Docker Strategy**: Implemented multi-stage builds and root `docker-compose.yml` orchestration for `nevumo-api`, `nevumo-web`, `nevumo-postgres`, and `nevumo-redis`.
  - **Path Logic**: Relocated backend virtual environment to `apps/api/.venv` and standardized absolute imports (`apps.api.*`).
  - **SQLAlchemy Fix**: Centralized `Base` in `apps/api/database.py` and ensured all models are imported to prevent 'table not found' errors.
  - **Next.js Metadata**: Fixed dynamic page titles using the Metadata API in `layout.tsx`.
  - **Namespaced Translations**: Standardized translation key prefixing (e.g., `provider_dashboard.*`) and documented Redis flush requirements.
  - **Documentation**: Finalized `README.md` and `docs/ARCHITECTURE.md` as the single source of truth for the new structure.
- **API Encoding & Middleware Hardening (April 14, 2026)** — Fixed Mojibake (double-encoding) and middleware redirection issues:
  - Added `UnescapedJSONResponse` as default response class in `apps/api/main.py` to ensure `charset=utf-8` and `ensure_ascii=False` globally.
  - Updated `apps/web/middleware.ts` to exclude all `/api/` paths from language redirection logic.
  - Updated `apps/web/next.config.mjs` to proxy all `/api/*` and `/:lang/api/*` routes to the backend, supporting paths without `/v1/` prefix.
  - Hardened Redis caching in `translations`, `categories`, and `cities` routes with `ensure_ascii=False`.
  - Verified `DATABASE_URL` uses `client_encoding=utf8`.
- **Phase 3 Absolute-Import Migration** — Backend import/package alignment completed across `apps/api`:
  - Added `apps/api/pyproject.toml` for package definition
  - Converted backend imports to absolute `apps.api.*` paths across routes, services, jobs, scripts, tests, and Alembic env
  - Removed remaining manual `sys.path` hacks from scripts/tests
  - Verified module-based script execution with `python3 -m apps.api.scripts.seed_ui_translations`
  - Runtime startup path verified with `python3 -m uvicorn apps.api.main:app` up to dependency loading
  - Docker runtime aligned to repo-root `PYTHONPATH` with `uvicorn apps.api.main:app`
- **Provider Description Auto-Translation (Langbly)** — Automatic translation of provider descriptions into all 34 languages:
  - New table: `provider_translations` (provider_id, field, lang, value, auto_translated)
  - Migration: `apps/api/alembic/versions/t1u2v3w4x5y6_add_provider_translations.py` 
  - Translation service: `apps/api/services/translation_service.py` (Langbly API, endpoint: https://api.langbly.com/language/translate/v2)
  - PATCH /api/v1/provider/profile now auto-translates description on save
  - GET /api/v1/providers/{slug}?lang={lang} now serves translated description from DB
  - Fallback: if Langbly returns 429 or times out, original text stored with auto_translated=False
  - Retry job: `apps/api/jobs/retry_translations.py` runs daily at 03:00 via APScheduler
  - Langbly free tier: 500K chars/month, no credit card required, ~98 providers/month capacity
- **Dynamic Price Range System** — Fully automated price display across all category pages:
  - New backend endpoint GET /api/v1/price-range?category_slug=X&city_slug=Y
    returns { min, max, currency, provider_count } or null, Redis cached TTL 3600
  - 3 display states: 0 providers → price_text_none, 1 provider → price_text_single,
    2+ providers → price_text_range
  - Applied in 4 SEO places: meta description, FAQ JSON-LD schema, SEO body paragraph
  - 9 translation keys × 34 languages = 306 rows seeded in translations table
    (namespace: category, keys: price_text_none/single/range, price_faq_none/single/range,
    price_meta_none/single/range)
  - Hardcoded price paragraphs removed from seo_cleaning_p3, seo_plumbing_p3,
    seo_massage_p3 (cleared to empty string for all languages)
  - SEO copy updated: seo_cleaning_h3_1, seo_cleaning_p1, seo_cleaning_p2
    now use 'specialist' instead of 'company/firm' across all 34 languages
    (102 rows upserted via update_cleaning_seo_translations.py)
- **Provider Card 4-State System (April 2026)** — Category/city listing page provider cards now render dynamically based on provider maturity:
  - **4 states implemented** in `apps/web/app/[lang]/[city]/[category]/page.tsx`:
    - State 1 (jobs=0, leads=0, rating=0): "✓ Проверен специалист • Безплатна заявка • Без ангажимент" + "✓ Директен контакт"
    - State 2 (leads>0, jobs=0, rating=0): "{N} души потърсиха този специалист" + "✓ Директен контакт"
    - State 3 (jobs>0, rating=0): "✅ {N} изпълнени задачи" + "⚡ {Име} наскоро направи заявка" (само ако < 90 дни) + "✓ Директен контакт"
    - State 4 (jobs>0, rating>0): "⭐ рейтинг • {N} ревюта" + "✅ {N} изпълнени задачи" + "⚡ {Име} наскоро направи заявка" (само ако < 90 дни) + "✓ Директен контакт"
  - **EnrichedProvider** extended with: `leadsReceived`, `reviewCount`, `latestLeadPreviewClientName`, `services[]`
  - **Services display** per card: до 2 услуги с цени (formatPrice helper: fixed/hourly/per_sqm/request), описание на услугата (line-clamp-1 ако има), "+ {n} още услуги" ако има повече от 2. Fallback текст само ако нито една услуга няма описание.
  - **Backend fix**: `_get_public_client_name()` в `apps/api/services/provider_service.py` вече връща само първото име (split()[0])
  - **Translation keys seeded** (namespace: category, 34 езика):
    - `provider_verified_specialist` — "Verified specialist"
    - `provider_free_no_obligation` — "Free request • No obligation"
    - `provider_people_sought` — "people sought this specialist"
    - `provider_recently_requested` — "recently made a request"
    - `provider_reviews` — "reviews"
    - `provider_on_request` — "On request"
    - `provider_more_services` — "and {n} more services"
    - `provider_desc_fallback` — "Send a free request. Response within 30 minutes."
  - **Redis cache key pattern**: `trans:{lang}:{namespace}` (НЕ `translations:*`) — важно за flush команди
  - **Seed scripts created**:
    - `apps/api/scripts/seed_provider_card_state_translations.py`
    - `apps/api/scripts/seed_provider_card_fixes.py`
    - `apps/api/scripts/seed_provider_more_services.py`
    - `apps/api/scripts/seed_provider_on_request.py`
- **Category Page Lead Form Redesign** — Converted LeadForm to marketplace broadcast model:
  - Pioneer framing banner when no providers: "Be the first to request this service in your area" / "Providers joining Nevumo will see your request and contact you"
  - How it works 3-step section (DB-backed translations)
  - Service chips from existing provider services + "Not sure" chip with solid border
  - Conditional textarea expands after chip selection, pre-fills with chip value
  - "Get offers" CTA replacing old "Submit request"
  - Trust signals: Free, No obligation, Sent to multiple providers, Response 30 min
  - Mobile sticky CTA button: md:hidden, isFormInView logic, shows when form is out of viewport in either direction
  - globals.css: overflow-x:clip fixes position:fixed on mobile (overflow:hidden auto browser quirk)
  - 15 new translation keys in category namespace × 34 languages = 510 new DB rows
- **Retro-matching** — при добавяне на първа услуга, новият доставчик автоматично получава всички съществуващи необработени заявки (status: created / pending_match) за същата категория + град. Имплементирано в `apps/api/services/provider_service.py` (функция `retro_match_provider`) и извиквано от `POST /api/v1/provider/services` в `apps/api/routes/provider.py`. Отговорът на endpoint-а съдържа `retro_matched_leads: int`.
  - Филтърът Lead.provider_id == None е задължителен — предотвратява retro-match на leads адресирани към конкретен провайдер
- SEO infrastructure (robots, sitemap, JSON-LD, hreflang, OG tags)
- Provider listing + detail pages
- Lead form (LeadForm component)
- Event tracking (GA4 + custom DB)
- Auth backend — Phase A (6 endpoints, bcrypt, JWT, rate limiting)
- Auth frontend — connected to real API (login, register, forgot, reset)
- Provider Dashboard backend — 10 endpoints, JWT auth, lead status management, image upload (HEIC/HEIF → WebP conversion, max 1200px resize, 85% quality), QR generation, onboarding support
- Provider Dashboard frontend — all pages (Overview, Leads, Services, Analytics, QR Code, Profile, Settings, Reviews)
- Android Chrome mobile scroll freeze fixed (June 2026): root cause was 5 onboarding overlay divs (absolute inset-0, onClick) covering 70% of viewport. Fix: touch-pan-y on overlays + h-screen/min-h-0 layout fixes + SmartGlobalFooter excluded from dashboard pages via isDashboardPath(). Footer restored inside <main> scroll container via force={true} prop pattern.
- Provider onboarding — 2-step wizard (profile info → first service), completeness check with auto-redirect
- Service CRUD — add/edit/delete with category, multi-city, price type, currency
- Client Dashboard — frontend + backend complete with guarded sidebar/topbar layout, Overview, My Requests, Reviews, Settings, inline review submission, review reply toggle preferences, role switch, and logout. Multi-provider review system: clients can review each provider who contacted them (LeadMatch.status IN contacted/done), one review per (lead_id, provider_id) pair. Badge count loads on initial mount (not only on tab click). Overview page lead cards have hover:shadow-md + "Write a Review" button for done leads. Fixes (April 2026): Resolved data inconsistencies and added real-time status updates for reviews and leads.
- Lead Rate Limiting UX Improvement (April 2026) — When a user is rate limited during lead submission, the API now returns the ID of their most recent lead. This allows the frontend to show the "Success" screen and allow the user to claim that lead via email, even if the new submission was blocked.
- Namespaced Translations Validator — Implemented strict `namespace.key` validation at the model layer to prevent incorrect translation keys.
- Warsaw Launch Data Seeded — Complete Warsaw marketplace setup:
  - City: Warszawa (PL) with coordinates 52.2297, 21.0122
  - Categories: cleaning, plumbing, massage
  - Category translation rows: 102 (`3` categories × `34` languages)
  - Seed script: apps/api/scripts/seed_warsaw_launch.py (idempotent)
- Warsaw Homepage — Provider-first landing page implemented at `apps/web/app/[lang]/page.tsx`:
  - SSR metadata and hreflang generation
  - Database-backed homepage copy via `fetchTranslations(lang, 'homepage')`
  - Hero with rotating categories, trust bullets, social proof and primary CTA to auth
  - Category cards for cleaning, plumbing, massage
  - Live activity feed, Why Nevumo section, footer service links, mobile sticky CTA
- Warsaw Category Pages — Client-first SEO pages implemented at `apps/web/app/[lang]/[city]/[category]/page.tsx`:
  - SSR metadata from DB translations
  - Provider listing cards enriched with provider details, rating, jobs completed and recent lead preview
  - Sticky sidebar lead form
  - SEO body blocks, FAQ schema, internal related links and provider acquisition CTA
- Namespaced UI Translations — Public DB-backed translation delivery is live:
  - Endpoint: `GET /api/v1/translations?lang={lang}&namespace={namespace}`
  - Backend file: `apps/api/routes/translations.py`
  - Router mounted in `apps/api/main.py`
  - Redis cache key pattern: `translations:{lang}:{namespace}` with 1 hour TTL
  - Per-key English fallback when requested language is missing part of a namespace payload
  - **Translation Key Validation (April 19, 2026)**: Completed audit of 712 unique keys (100% compliant). Implemented mandatory namespacing validation (`namespace.key`) at SQLAlchemy model level and Pydantic schema level to prevent "flat" keys.
- **Client Dashboard & Leads Enhancement (April 2026)**:
  - Implemented 8 new endpoints for client dashboard management.
  - Added review eligibility check and preference management.
  - Optimized leads listing with status filtering and pagination.
  - Fixed dashboard errors related to role switching and data loading.
  - **Leads Rate Limiting UX (April 21, 2026)**: Improved lead creation failure response to return the last successful lead ID, enabling the "claim" flow for rate-limited users.
  - **Client Dashboard Translation Fix (April 21, 2026)**: Fixed missing translation for "Recent Requests" in the client dashboard overview. Synced key `recent_requests_title` between frontend and backend and seeded 2,482 rows across 34 languages.
  - **Client Notes Feature (April 21, 2026)** — COMPLETE:
- **Mobile Sticky Footer Fix (May 2026)** — COMPLETE:
  - **Проблем:** Sticky бутоните на homepage, category и provider страниците покриваха GlobalFooter и dropdown-а за смяна на езици на мобилен екран.
  - **Решение:** Добавен динамичен paddingBottom на document.body равен на височината на sticky бутона — footer-ът се повдига и е достъпен при скрол до дъното.
  - **Засегнати файлове:**
    - apps/web/components/category/StickyLeadFormButton.tsx — добавен useEffect с paddingBottom логика
    - apps/web/components/ProviderWidget.tsx — добавен useRef + useEffect с paddingBottom логика; премахнат статичен pb-16
    - apps/web/components/homepage/MobileStickyCTA.tsx — добавен paddingBottom useEffect + заменен second-cta observer с hero-section observer (threshold: 0.1) + добавен footer observer (threshold: 0.01)
    - apps/web/app/[lang]/page.tsx — добавен id="hero-section" на hero секцията
  - **Логика на MobileStickyCTA:**
    - Hero-section видима → бутонът се скрива
    - Hero-section невидима → бутонът се показва
    - Footer видим → бутонът се показва (override)
- **Cookie Consent Banner (GDPR Compliance) — May 8, 2026** — COMPLETE:
  - **Frontend Component**: `apps/web/components/ui/CookieConsentBanner.tsx` with Accept All / Reject All / Customize buttons
  - **Cookie Storage**: First-party cookie `nevumo_consent` with versioned structure (v:2, timestamp, categories, policy_version)
  - **Footer Link**: "Cookie Settings" button in footer to reopen banner without page reload
  - **Localization**: Supported in EN, PL, BG (cookie_banner namespace with 14 keys)
  - **Backend Logging**: POST /api/v1/consent endpoint in `apps/api/routes/consent.py`
  - **Database**: New `consent_logs` table for GDPR audit trail (24-month retention)
  - **Migration**: Alembic migration `20260508_add_consent_logs` executed successfully
- **Provider Cancelled Status Translation Fix — May 13, 2026** — COMPLETE:
  - **Problem**: English text "Cancelled" displayed on provider dashboard leads page when Bulgarian language was selected
  - **Root Cause**: Missing translation key `status_cancelled` in PROVIDER_DASHBOARD_KEYS and RAW_PROVIDER_DATA
  - **Fix**: Added `status_cancelled` key to `apps/api/scripts/seed_status_translations.py` with full 34-language translations (including Bulgarian "Отказана")
  - **Component**: `apps/web/app/[lang]/provider/dashboard/leads/LeadsClient.tsx` uses `t('status_cancelled', 'Cancelled')`
  - **Verification**: Seed script executed successfully (782 rows seeded), Redis cache flushed, Bulgarian now displays "Отказана" instead of "Cancelled"
  - **Testing**: 7/7 automated Playwright tests passed (banner visibility, Reject All, Accept All, Customize, no banner on repeat visit, footer link, Polish language)
  - **GA4 Consent Mode v2 (May 8, 2026)**: gtag('consent','update') integrated in useCookieConsent.ts. Fires on acceptAll/rejectAll/savePreferences. PASS verified via Playwright.
  - **Pending Items**: Stripe.js conditional loading
  - **Status**: Core cookie consent functionality complete, backend audit trail operational. Advanced GA4 integration and Stripe management deferred to future tasks.
  - **Bug Fix (May 11, 2026)**: Cookie banner показваше English на /bg route от мобилни устройства в локална мрежа. Root cause: `useCookieConsent.ts` и `ui-translations.ts` използваха `process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'` като client-side apiBase — абсолютен localhost URL заобикаляше Next.js proxy и се чупеше на устройства различни от localhost. Fix: `apps/web/hooks/useCookieConsent.ts` ред 99 и `apps/web/lib/ui-translations.ts` ред 13 — client клоновете сетнати на `''` (относителен URL). Next.js rewrites в next.config.mjs проксират `/api/v1/*` към FastAPI — работи от всяко устройство.
- **Mobile Network API URL Configuration Fix (May 17, 2026)** — COMPLETE:
  - **Problem**: Frontend API calls failed when accessing from mobile devices in local network (e.g., http://192.168.0.15:3000/bg/auth) because `NEXT_PUBLIC_API_URL` was hardcoded to `http://localhost:8000` in docker-compose.yml
  - **Root cause**: `localhost` on mobile device refers to the mobile device itself, not the laptop running the API server
  - **Solution**: Made `NEXT_PUBLIC_API_URL` configurable via environment variable with fallback:
    - `.env`: Set `NEXT_PUBLIC_API_URL=http://192.168.0.15:8000` for local network testing
    - `docker-compose.yml`: Changed from hardcoded value to `${NEXT_PUBLIC_API_URL:-http://localhost:8000}`
  - **Benefits**: Global and scalable solution - works in all environments (dev, staging, production) via environment variables without code changes
    - **DB:** New column `leads.client_notes TEXT` (nullable) — migration r2s3t4u5v6w7
    - **Backend:**
      - New endpoint: `PATCH /api/v1/client/leads/{lead_id}/notes` (ownership check: lead.client_id == user.id)
      - `GET /api/v1/client/leads` and `GET /api/v1/client/dashboard` now accept `?lang=` param and return localized `category_name`
      - Schemas added: `ClientLeadNotesUpdate`, `ClientLeadNotesUpdateResponse`
      - `ClientLeadListItem` updated with `client_notes` field
    - **Frontend:**
      - New component: `apps/web/components/client/ClientLeadDetailModal.tsx`
        - Opens on card click in requests page
        - Shows: ДАТА, СПЕЦИАЛИСТ (provider link OR broadcast msg), STATUS, ВАШЕТО СЪОБЩЕНИЕ ДО СПЕЦИАЛИСТА
        - Private notes textarea: debounced 500ms autosave + blur save
        - Button: "Запази и затвори" (btn_save_and_close)
      - `RequestsClient.tsx`: cards clickable, description preview, note preview/CTA with SVG pencil icon, broadcast message instead of "Marketplace"
      - `OverviewClient.tsx`: recent lead cards clickable → navigate to /requests?open={lead_id} to auto-open modal; broadcast message instead of "Marketplace"
      - `client-api.ts`: ClientLead interface + updateClientLeadNotes() + lang param on getClientLeads() and getClientDashboard()
    - **Translations:** 10 keys in `client_dashboard` namespace × 34 languages = 340 rows
      - modal_title_request, label_specialist, label_your_message, msg_broadcast_lead
      - label_client_notes, placeholder_client_notes, btn_save_and_close, btn_add_note
      - (+ 2 existing reused: label_date, label_status)
      - Seed script: `apps/api/scripts/seed_client_notes_translations.py`
  - **Dual Role Architecture (April 2026)** — COMPLETE:
    - **PROBLEM:** One user can be both provider and client simultaneously (two tabs open)
    - **SOLUTION:** Removed role-based guards, kept ownership-based security
    - `apps/api/dependencies.py`: get_current_provider() now queries providers table by user_id instead of checking JWT role
    - `apps/api/routes/client.py`: _require_client_role() was already a no-op (confirmed by audit)
    - `apps/web/app/[lang]/provider/dashboard/layout.tsx`: guard now calls GET /api/v1/provider/dashboard to verify provider profile exists (not JWT role check)
    - **Result:** user with role='client' JWT can access provider dashboard if they have a provider profile, and vice versa
  - **Category Page Fix (April 2026)** — COMPLETE:
    - **PROBLEM:** CATEGORY_CONTENT keyed by Polish slugs (masaz, sprzatanie, hydraulik); URLs use English slugs (cleaning, massage, plumbing) → always showed cleaning content
    - **SOLUTION:** Re-keyed CATEGORY_CONTENT, CategoryKey type, relatedLinksByCategory from Polish to English slugs
    - Removed categorySlugMap and categoryKeyMap — getApiSlug() is now identity function
    - File: apps/web/app/[lang]/[city]/[category]/page.tsx
    - **Result:** /bg/warszawa/plumbing correctly shows plumbing content
  - **Client Dashboard Localization (April 2026)** — COMPLETE:
    - GET /api/v1/client/leads: added lang query param, category_name now localized
    - GET /api/v1/client/dashboard: added lang query param, category_name in recent_leads now localized
    - ClientLeadsQueryParams schema: added lang field (was causing 422 without it)
    - Frontend passes lang to both API calls
- **Provider Dashboard i18n Hardening** — provider dashboard shell and pages now share one `provider_dashboard` dictionary via `DashboardI18nProvider`, use locale-aware category/date loading, and ship DB-backed translations for the remaining shared dashboard UI copy
- **Verified UI Translation Coverage** — Homepage and category UI copy seeded for 34 languages:
  - Source script: `apps/api/scripts/seed_ui_translations.py`
  - Exact DB-backed UI key counts: `43` homepage + `24` category = `67` per language
  - Total namespace rows seeded/upserted: `2,278`
- **Client Dashboard Shell Upgrade** — `apps/web/app/[lang]/client/dashboard/layout.tsx` now includes:
  - Logout in topbar and sidebar
  - `Стани доставчик` role-switch CTA
  - `НАМЕРИ УСЛУГА` CTA after settings
- **Provider Widget UX Improvement (April 30, 2026)** — COMPLETE:
  - Filtering visible service tags by current category
  - Selecting a service tag to auto-fill the description
  - Expand-to-show-all services flow
  - **Relative Time Localization**: Fully localized relative time (e.g., "just now", "5m ago", "2 days ago") across all 34 languages using DB-backed translations (namespace: `widget`).
  - **Technical Refactor**: Replaced hardcoded Bulgarian/English logic in `getRelativeTime` with a universal translation function `t` and 8 new translation keys. All component UI strings in the widget now use the `t` function.
- **ProviderWidget State Updates (April 27, 2026)** — `apps/web/components/ProviderWidget.tsx` rendering logic changes:
  - **Verified badge**: Now renders unconditionally for ALL providers regardless of `provider.verified` value (condition changed from `{provider.verified && (...)}` to `{...}`)
  - **Top section waterfall**: Fallback state (`new_badge` + `no_reviews_yet`) removed; waterfall now ends with `null` when no conditions match
- **ProviderWidget UX Refactor (April 27, 2026)** — `apps/web/components/ProviderWidget.tsx` interactive improvements:
  - **Provider description**: Now renders between verified badge and services section (conditional, non-empty only)
  - **Services section**: Refactored from static list to interactive clickable cards — on click selects service, pre-fills notes textarea, smooth scrolls to #widget-form
  - **Service affordance**: Chevron (›) added to each service row as clickable indicator
  - **Chips removal**: Chips section removed from form entirely
  - **Dynamic form heading**: Changed from static "Заявете услуга" to dynamic "{t.send_request_to} {provider.business_name}"
  - **Translation key**: New `widget.send_request_to` key added (34 languages, seed script: apps/api/scripts/seed_widget_send_request_to.py)
  - **Backend fallback**: `get_widget_translations()` in apps/api/routes/providers.py refactored to three-layer fallback: hardcoded defaults → English DB → target language DB
  - **Hydration fix**: `suppressHydrationWarning` added to relative time elements in RecentRequestBlock and SocialProofBlock
- **Docker Environment Variable Pattern (April 27, 2026)** — Next.js in Docker requires two separate environment variables:
  - API_URL=http://nevumo-api:8000 — used server-side (SSR, Next.js rewrites) for container-to-container communication
  - NEXT_PUBLIC_API_URL=http://localhost:8000 — used client-side (browser)
  - Applied in: docker-compose.yml, apps/web/lib/api.ts, apps/web/lib/ui-translations.ts, apps/web/next.config.mjs
  - Ensures server-side rendering can reach backend via Docker network while client-side requests use localhost port forwarding
- **Мобилно тестване (локална мрежа)** — За тестване от телефон на същата WiFi мрежа:
  - `.env`: CORS_ORIGINS трябва да включва http://{LOCAL_IP}:3000
  - `docker-compose.yml`: NEXT_PUBLIC_API_URL трябва да е http://{LOCAL_IP}:8000
  - `apps/web/next.config.mjs`: allowedDevOrigins: ["{LOCAL_IP}"]
  - При смяна на IP адреса на лаптопа — обнови и трите места
  - Текущ IP: 192.168.0.15
- **ScrollIntoView on Phone Validation Error (April 27, 2026)** — When phone validation fails on form submit, viewport smoothly scrolls to the phone field:
  - Applied in: apps/web/components/provider/ProviderWidget.tsx, apps/web/components/category/LeadForm.tsx
  - Ensures users immediately see validation errors and can correct them without manual scrolling
- **Frontend API Shape Alignment** — `apps/web/lib/api.ts` `ServiceOut` now exposes `category_slug` for category-aware UI filtering
- **Global Phone Field System** — Complete phone persistence and UX:
  - users.phone column added (migration p1q2r3s4t5u6)
  - GET/PATCH /api/v1/user/profile endpoints
  - usePhone hook: sync between localStorage and DB
  - PhoneInput component: auto-prefix by country, soft validation
  - Auto-fill for anonymous (localStorage) and logged-in (DB) users
  - countryCode wired in: category pages, provider pages, 
    ProviderWidget, provider/client dashboard settings
  - Error display logic: Error only shows when `!isValid && phone && (touched || submitted)`
    - `touched`: Set to true when user interacts with the field (onChange or onBlur)
    - `submitted`: Prop passed from parent form, set to true on form submission attempt
    - This prevents premature error display on initial load with country code prefix
  - GDPR: Legitimate Interest basis, Privacy Policy update pending
- **Lead Form Success Screen with Email Capture** — Post-submission two-step success flow:
  - Step 1: Shows success message + "Want to track your request?" with Continue/Skip CTAs
  - Step 2: Email input captures lead claim intent, saves to localStorage (nevumo_pending_claim)
  - Rate limit exceeded (429) shows success screen instead of error
  - Redirects to /{lang}/auth?email=...&intent=client for account creation
  - All success screen strings are fully translated in 34 languages 
    via category namespace (15 new keys: success_title, success_subtitle,
    success_track_title, success_bullet_responses, success_bullet_manage,
    success_bullet_notifications, success_cta_email, success_free_label,
    success_skip_link, email_back_link, email_label, email_placeholder,
    email_cta_continue, error_phone_invalid, error_generic)
  - **City Name Translation Fix (April 19, 2026)**: Fixed an issue where the city name in the lead success message was not translated (e.g., showing "Warszawa" instead of "Варшава" on the Bulgarian site). The `LeadForm` now accepts and uses a translated `cityName` prop passed from the category page.
  - Trust signal keys fixed: form_free→form_trust_1, 
    form_no_obligation→form_trust_2
  - Seed script: apps/api/scripts/seed_success_screen_translations.py
- **Lead Submission Bug Fix (April 19, 2026)** — Fixed a critical issue where lead submissions failed with "Internal Server Error" (500):
  - **Root Cause**: PostgreSQL sequences for `lead_rate_limits` and `auth_rate_limits` were out of sync with existing data (likely due to manual imports/migrations during Phase 3), causing `UniqueViolation` on the `id` column.
  - **Fix**: Synchronized all database sequences using `setval` to match current `MAX(id)` values.
  - **Verification**: Confirmed successful lead creation and claim-email registration via API/Curl.
  - **Affected Areas**: All lead forms (category pages, provider pages, widgets) and auth-related rate limiting.
- **Pending Lead Claims System** — Anonymous lead → account linking bridge:
  - Table: pending_lead_claims (lead_id, email, phone, claimed, expires_at, magic_link_sent)
  - Endpoint: POST /api/v1/leads/{lead_id}/claim-email (no auth required)
  - Auth hooks: link_pending_claims() called in /register and /login
  - Links claims matching email OR phone to the authenticated user
  - Updates leads.client_id and marks claims as claimed
- **Magic Link System** — Passwordless authentication for lead claimers:
  - Table: magic_link_tokens (email, lead_id, token_hash, expires_at, used_at)
  - Background job: apps/api/jobs/send_magic_links.py runs every 5 minutes via APScheduler
  - Sends delayed magic links 30 min after claim registration (configurable)
  - Endpoint: POST /api/v1/auth/magic-link validates token, creates passwordless account
  - Frontend: /[lang]/auth/magic/page.tsx handles token validation + auto-login
  - Import path fix: apps/api/jobs/send_magic_links.py uses relative imports (from models import ..., from config import ...) — NOT absolute paths (from apps.api.models import ...) because uvicorn runs from inside apps/api/
- **Widget Translation System (provider detail pages)** — Full language consistency for provider widget across all 34 languages:
  - New `widget` namespace in `translations` table: 23 keys × 34 languages = 782 rows
  - Seed script: `apps/api/scripts/seed_widget_translations.py` (idempotent)
  - Backend: `GET /api/v1/providers/{slug}` now fetches widget translations from DB via `get_widget_translations(lang, db)` in `apps/api/routes/providers.py`
  - Frontend: `apps/web/components/ProviderWidget.tsx` — all hardcoded English strings replaced with `t.*` from `provider.translations`; `'use client'` directive confirmed
  - Frontend: `apps/web/lib/api.ts` `getProviderBySlug` — `lang` param now passed to API; `cache: 'no-store'` added
  - Keys: verified_label, rating_label, jobs_label, phone_label, phone_placeholder, notes_label, notes_placeholder, response_time, button_text, disclaimer, success_title, success_message, success_message_received, new_request_button, recent_request_label, city_leads_label, free_request_no_obligation, no_registration, direct_contact_with_provider, services_label, price_on_request
- **PWA Етап 1 — Install Prompt + Tracking** — Базова PWA инфраструктура и install prompt система:
  - `apps/web/public/manifest.json` — Web App Manifest (name, icons, theme_color: #f97316, display: standalone)
  - `apps/web/public/icons/icon-192x192.png` и `icon-512x512.png` — PWA иконки
  - `apps/web/next.config.mjs` — plain Next.js config (no PWA library — static sw.js in public/)
  - `apps/web/app/layout.tsx` — PWA meta тагове (manifest, theme-color, apple-mobile-web-app-*)
  - `apps/web/hooks/usePWAInstall.ts` — Hook: beforeinstallprompt (Android), iOS detection, localStorage anti-spam (спира при 2 отказа), canInstall/isIOS/showPrompt/handleDismiss/handleInstalled
  - `apps/web/components/pwa/PWAInstallPrompt.tsx` — Компонент: Android bottom banner + iOS bottom sheet с 2-стъпкови инструкции, различно копие за client/provider роли
  - Trigger точки:
    - Category page lead submit — LeadForm.tsx (2s delay)
    - Provider onboarding completion — provider dashboard (1.5s delay, useRef guard)
    - Provider page lead submit — ProviderWidget.tsx (2s delay)
    - Embedded widget lead submit — ProviderWidget.tsx (2s delay)
  - localStorage keys: pwa_installed, pwa_prompt_dismissed_count
  - Tracking: pwa_prompt_shown, pwa_install_accepted, pwa_install_dismissed, pwa_installed — всички през trackPageEvent() към page_events таблицата
- **Post-lead nudge flow added to ProviderWidget.tsx (April 27, 2026)** — Two-step account creation nudge (identical to LeadForm) shown to unauthenticated users after lead submission on provider profile pages. Nudge keys seeded into widget namespace via seed_widget_nudge_translations.py (442 rows copied from category namespace).
  - CORS fix: apps/api/.env добавен с CORS_ORIGINS, apps/api/main.py зарежда .env чрез load_dotenv()
  - PWA prompt не се показва на desktop (очаквано) — активира се само на мобилен Chrome (Android) и Safari (iOS 16.4+)
  - pwa namespace в translations таблицата: 6 ключа × 34 езика = 204 реда (install_title, client_subtitle, provider_subtitle, ios_step1, ios_step2, dismiss_button)
  - PWAInstallPrompt компонентът зарежда преводи от DB via GET /api/v1/translations?lang={lang}&namespace=pwa
  - lang prop се предава от layout.tsx (provider dashboard) и LeadForm.tsx (category pages)
  - iOS bottom sheet: текстовете са центрирани, бутонът е sticky
- **PWA Етап 2 — Footer AppBar (June 2026)** — COMPLETE:
  - **Нов компонент**: `apps/web/components/footer/FooterAppBar.tsx`
    - PWA install бутон (mobile only, md:hidden) — независим от usePWAInstall hook
    - Share бутон (всички устройства) — navigator.share() на mobile, clipboard на desktop
    - Inline iOS sheet — без dismiss count ограничение (копие на PWAInstallPrompt iOS JSX)
    - Собствен beforeinstallprompt listener — pwa_installed записва се само при accepted
    - pwa namespace преводи зареждат се независимо via fetch('/api/v1/translations/pwa')
  - **Role detection** (detectRole() helper в FooterAppBar):
    Йерархия: 1) getAuthUser().role → 2) nevumo_intent localStorage → 3) URL path (/dolacz, /provider/) → 4) default 'client'
  - **Нов seed скрипт**: `apps/api/scripts/seed_footer_translations.py`
    - 2 ключа × 34 езика = 68 реда в `footer` namespace
    - `footer.install_app` — "Инсталирай приложението"
    - `footer.share_page` — "Сподели"
  - **GlobalFooter.tsx промени**:
    - FooterAppBar добавен над legal links блока (вътре в !minimal)
    - Copyright и language dropdown преместени в bottom row: copyright ляво, dropdown дясно
  - **Важно решение**: FooterAppBar НЕ използва usePWAInstall — избягва анти-спам dismiss limit (2 отказа). Автоматичните PWA банери остават непроменени.
  - **Отхвърлена оптимизация**: navigator.share() при "Разбрах" на iOS — програматичният share sheet не съдържа "Add to Home Screen" (само Safari toolbar бутонът го показва). Reverted.
- **PWA Етап 3 — Smart Redirect (June 2026)** — COMPLETE:
  - **Проблем**: manifest.json start_url="/" отваряше homepage при всяко стартиране на PWA, независимо от контекста на потребителя.
  - **Решение**: Нова /pwa-start страница с интелигентна redirect логика.
  - **Нови файлове**:
    - apps/web/app/pwa-start/page.tsx — client компонент с redirect логика и оранжев spinner
    - apps/web/hooks/usePWALastUrl.ts — записва последната "чиста" URL в localStorage И в cookie nevumo_pwa_ctx
    - apps/web/components/PWAUrlTracker.tsx — невидим компонент, монтиран в [lang]/layout.tsx
  - **Промени по съществуващи файлове**:
    - apps/web/public/manifest.json — start_url сменен от "/" на "/pwa-start"
    - apps/web/app/[lang]/layout.tsx — добавен <PWAUrlTracker /> в LayoutShell
    - apps/web/proxy.ts — добавено изключение за /pwa-start от language normalization
  - **Redirect логика**:
    - Логнат провайдър → /{lang}/provider/dashboard
    - Логнат клиент + nevumo_ctx.city → /{lang}/{city}
    - Логнат клиент без град → /{lang}
    - Анонимен + nevumo_last_url (localStorage) → последната посетена страница
    - Анонимен + nevumo_pwa_ctx (cookie) → последната посетена страница (iOS fallback)
    - Анонимен + cookie `lang` → /{lang} (език от cookie)
    - Анонимен + navigator.language → /{lang} (системен език)
    - Анонимен без нищо → /en
  - **"Чисти" URL-и** (записват се в nevumo_last_url и nevumo_pwa_ctx): homepage, city pages, category pages, provider pages (1-4 сегмента)
  - **"Мръсни" URL-и** (не се записват): /auth/*, /dashboard/*, /pwa-start, /izberi-grad
  - **localStorage ключ**: nevumo_last_url — последната посетена чиста URL за PWA smart redirect
  - **Cookie**: nevumo_pwa_ctx — дублира nevumo_last_url като cookie (path=/; max-age=2592000; SameSite=Lax); решава iOS PWA isolated storage проблема — iOS PWA има напълно изолиран localStorage от Safari browser, но cookies се споделят
  - **iOS бъг (June 2026)**: При инсталиране на PWA от iOS Safari, PWA-то стартира с празен localStorage (изолиран от браузъра). nevumo_pwa_ctx cookie се чете успешно и redirect-ва към последната посетена страница.
- **PWA Етап 4 — Web Push Notifications (June 7, 2026)** — COMPLETE:
  - **Backend:**
    - Dependency: `pywebpush>=2.0.0` added to `apps/api/requirements.txt`
    - New DB table: `push_subscriptions` (id, user_id, endpoint, p256dh, auth, device_info, created_at) — Alembic migration `20260607_add_push_subscriptions`
    - VAPID keys: `VAPID_PRIVATE_KEY`, `VAPID_PUBLIC_KEY`, `VAPID_CLAIMS_EMAIL` added to Railway environment variables and `apps/api/config.py`
    - New service: `apps/api/services/push_service.py` — `send_push_notification(db, user_id, title, body, url)` — iterates all user subscriptions, auto-removes expired (404/410)
    - New route file: `apps/api/routes/push.py` — 3 endpoints mounted at `/api/v1/push/`:
      - `GET /vapid-public-key` — returns VAPID public key (unauthenticated)
      - `POST /subscribe` — saves subscription (authenticated)
      - `DELETE /unsubscribe` — removes subscription (authenticated)
    - Push triggers added:
      - `apps/api/routes/leads.py` — push to provider on new lead (after email notification)
      - `apps/api/routes/provider.py` — push to client on lead status update (after email notification)
      - `apps/api/routes/client.py` — push to provider on new review (only first review per lead)
      - `apps/api/routes/reviews.py` — push to client on provider review reply (only first reply, not edits)
    - **Import path rule**: all new files under `apps/api/routes/` and `apps/api/services/` must use `apps.api.*` absolute imports (Railway runs uvicorn from `/workspace` monorepo root)
  - **Frontend:**
    - New hook: `apps/web/hooks/usePushNotifications.ts` — `isSupported`, `isSubscribed`, `isLoading`, `subscribe()`, `unsubscribe()` — handles VAPID key fetch, PushManager subscription, API calls to `/api/v1/push/subscribe` and `/api/v1/push/unsubscribe`
    - New file: `apps/web/worker/index.js` — custom Service Worker handlers for `push` event (showNotification) and `notificationclick` event (focus/open window)
    - `apps/web/next.config.mjs` — added `customWorkerDir: 'worker'` to next-pwa config (later removed all PWA libraries on June 11, 2026 — static sw.js in public/)
    - `apps/web/app/[lang]/provider/dashboard/settings/page.tsx` — added Push Notifications toggle section (visible only when `isSupported === true`, i.e. PWA installed + browser supports push)
  - **iOS note**: Web Push requires PWA installed via Add to Home Screen + iOS 16.4+. Safari without PWA install does NOT support Web Push.
  - **Notification flow**: Provider receives push on new lead → Client receives push on lead status change
- **PWA Library Migration (June 11, 2026)** — COMPLETE:
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
- **Push & Email Notification Audit (June 11, 2026)** — COMPLETE:
  - **PushPermissionPrompt fix (frontend)**: Added PushPermissionPrompt to ALL return branches (success1 logged in, success1 not logged in, success2) in LeadPanel.tsx and BottomSheetForm.tsx. Previously only rendered in default (form) return, causing unmount before 2s setTimeout fired after lead submit.
  - **Direct lead push notification (backend)**: Added send_push_notification to direct lead block in leads.py (was missing, only marketplace leads had push).
  - **Client status change push notification (backend)**: Added send_push_notification to client.py when client changes lead status. Also moved email notification from before db.commit() to after db.commit() (timing bug fix).
  - **Review reply duplicate email fix (backend)**: Removed duplicate send_review_reply_notification call from reviews.py (already called in review_service.py line 395). Removed unused email_service import from reviews.py.
  - **Full notification matrix verified**:
    - New lead (direct) → provider: ✅ email (leads.py), ✅ push (leads.py)
    - New lead (marketplace) → provider: ✅ email (leads.py), ✅ push (leads.py)
    - Provider changes status → client: ✅ email (provider.py), ✅ push (provider.py)
    - Client changes status → provider: ✅ email (client.py), ✅ push (client.py)
    - Client submits review → provider: ✅ email (client.py), ✅ push (client.py)
    - Provider replies to review → client: ✅ email (review_service.py), ✅ push (reviews.py)
    - Provider edits reply → client: ❌ intentional (no notifications)
- **Push Notifications Hardening (June 11, 2026)** — COMPLETE:
  - **PushPermissionPrompt auth guard**: Added `isAuthenticated()` check to `shouldShow` condition — prompt never shown to anonymous users, protecting browser permission budget
  - **permissionState exposed**: `usePushNotifications.ts` now exposes `permissionState: NotificationPermission` — components can react to 'default'/'granted'/'denied' states
  - **Blocked state UI**: Both Provider and Client Settings show amber warning box with browser instructions when `permissionState === 'denied'` — no more silent failures
  - **Anonymous subscription auto-sync**: On mount, if browser has push subscription AND user is logged in, hook silently POSTs to `/push/subscribe` to create DB record for `user_id` — fixes "Disable" shown instead of "Enable" after anonymous → login flow
  - **unsubscribe() auth header**: Added Authorization header to DELETE /push/unsubscribe call
  - **Client Settings push toggle**: Added push notifications section to `SettingsClient.tsx` (before Review Preferences) — clients can now enable/disable push from their dashboard
  - **New translation keys**: `settings.push_blocked_title` + `settings.push_blocked_description` × 34 languages — seed script: `apps/api/scripts/seed_push_blocked_translations.py`
  - **Translation namespace fix**: Client Settings uses `tSettings` from `useTranslation('settings', lang)` for push keys — separate from `t` for `client_dashboard` namespace
  - **Missing push settings translations**: 5 keys (push_title, push_description, push_enable, push_disable, push_loading) were missing from `settings` namespace — seed script added: `apps/api/scripts/seed_push_settings_translations.py` (170 rows × 34 languages)
  - **Provider Settings namespace fix**: `useTranslation('settings', lang)` added as `tSettings` in provider settings page — push keys now correctly load from `settings` namespace instead of `provider_dashboard`
- **PushNotificationBanner (June 14, 2026)** — COMPLETE:
  - **New component**: `apps/web/components/pwa/PushNotificationBanner.tsx`
  - Persistent banner shown at the top of provider and client dashboards.
  - No X button, no dismiss logic — stays visible until user acts.
  - **4 states (checked in this order)**:
    1. isSubscribed === true → return null (hidden)
    2. isIOSWithoutPWA === true → blue banner, Smartphone icon, install CTA text only
    3. isSupported && !isSubscribed && permissionState === 'denied' → amber banner, BellOff icon, blocked instructions
    4. isSupported && !isSubscribed && permissionState !== 'denied' → amber banner, Bell icon, "Enable" CTA button
  - **iOS detection**:
    - isIOS: /iPad|iPhone|iPod/.test(navigator.userAgent)
    - isStandalone: Boolean(window.navigator.standalone)
    - isIOSWithoutPWA = isIOS && !isStandalone
  - **Translation sources (3 namespaces via Promise.all)**:
    - pwa namespace: install_for_notifications_provider, install_for_notifications_client (NEW — seeded June 14, 2026)
    - push_prompt namespace: title, provider_body, client_body, cta_button (existing)
    - settings namespace: push_blocked_title, push_blocked_description (existing)
  - **Props**: lang: string, role: 'provider' | 'client'
- **Provider dashboard layout changes (June 14, 2026)** — COMPLETE:
  - File: `apps/web/app/[lang]/provider/dashboard/layout.tsx`
  - PushNotificationBanner added before {children} in main content area
  - After nevumo:onboarding_complete event: second timer at 5000ms shows PushPermissionPrompt
    (existing PWA prompt fires at 1500ms, push prompt fires at 5000ms)
  - Onboarding sequence: 0ms event → 1500ms PWA banner → 5000ms Push prompt
- **Client dashboard layout changes (June 14, 2026)** — COMPLETE:
  - File: `apps/web/app/[lang]/client/dashboard/layout.tsx`
  - PushNotificationBanner added before {children} in main content area
- **New translation keys (June 14, 2026)** — COMPLETE:
  - Seed script: `apps/api/scripts/seed_pwa_install_notifications_translations.py`
  - 68 rows (2 keys × 34 languages), seeded June 14, 2026
  - Keys added to pwa namespace:
    - pwa.install_for_notifications_provider
    - pwa.install_for_notifications_client
- **Architecture decision: no separate Notifications menu item (June 14, 2026)** — COMPLETE:
  - Notifications toggle stays in Settings.
  - Separate menu item deferred until in-app notification inbox exists.
  - Dashboard banner is the primary visibility mechanism.
- **Onboarding Hero Banner i18n** — Hero banner texts on provider dashboard are now DB-backed and translated in all 34 languages:
  - 8 new keys in `provider_dashboard` namespace: `onboarding_hero_2steps_title`, `onboarding_hero_2steps_desc`, `onboarding_hero_2steps_cta`, `onboarding_hero_1step_title`, `onboarding_hero_1step_desc`, `onboarding_hero_1step_cta`, `onboarding_step_profile`, `onboarding_step_service` 
  - 272 new rows 
  - Seed script: `apps/api/scripts/seed_onboarding_hero_translations.py` 
- **City Page Launch (April 19, 2026)** — Implementation of the dynamic city landing page system (`/[lang]/[city]`):
  - **New Page Structure**: SSR landing page featuring a hero section with search, category grid, "How it works" section, and SEO content blocks.
  - **Dynamic Metadata**: SEO-optimized titles and descriptions using localized city names.
  - **Namespace: `city`**: 11 new translation keys per language (374 total rows) covering all UI elements.
  - **API Integration**: Frontend now consumes `GET /api/v1/cities/{slug}` for localized city context.
  - **Seed Script**: `apps/api/scripts/seed_city_translations.py` for idempotent deployment across 34 languages.
  - **UX**: Automatic category icon mapping and links to category-specific pages within the city.
- **Location Translations System** — Multilingual city name display (April 2026):
  - New table: location_translations (location_id, lang, city_name) — 102 rows seeded
  - locations.city_en added for English/admin fallback
  - GET /api/v1/cities?lang={lang} returns translated city_name as `city` field
  - Fallback chain: translated name → city_en → city
  - Seed script: apps/api/scripts/seed_location_translations.py (idempotent)
  - Frontend CityOut interface updated: city + city_en fields
  - getCities() updated with lang param
  - Provider dashboard fetches cities for BG + RS + PL with lang
  - Backend must run with --host 0.0.0.0 for SSR fetches to reach NEXT_PUBLIC_API_URL (network IP)
- **Auth Page i18n (April 11, 2026)** — Пълна i18n на auth страницата:
  - Seed script: apps/api/scripts/seed_auth_hero_translations.py обновен с 13 нови ключа
  - Нови ключове: checking_btn, logging_in_btn, registering_btn, sending_btn, error_wrong_password, error_generic, error_rate_limit, error_account_disabled, error_email_exists, register_success, coming_soon, page_title, meta_description
  - Общо: 27 ключа × 34 езика = 918 rows в translations таблицата (namespace: auth)
  - apps/web/app/[lang]/auth/page.tsx: заменен static metadata export с async generateMetadata({ params }) която използва fetchTranslations(lang, 'auth') за динамичен title, description, og:title, og:description
  - Claim state trigger: ?claim=1 URL параметър
  - Тествани и потвърдени: всички 18 state-а × 3 езика (pl, en, bg) = 54 проверки — нито един проблем
- **Provider Dashboard Lead Search Enhancement** — Enhanced search capabilities across 5 fields:
  - New search parameter in GET /api/v1/provider/leads endpoint
  - Searches across: client_name, client_email, client_phone, description, provider_notes
  - Case-insensitive partial matching
  - Frontend UI: Search input with placeholder "Search name, email, phone, description or notes..."
  - i18n keys: label_search, placeholder_search_leads
  - **Provider Notes Feature** — Private notes for providers on leads (COMPLETE):
  - New field: leads.provider_notes (TEXT, nullable) added via migration q1r2s3t4u5v6
  - New endpoint: PATCH /api/v1/provider/leads/{lead_id}/notes
  - Frontend: LeadDetailModal component with private notes textarea
  - Debounced auto-save (500ms) + blur save
  - i18n key: label_private_notes
  - Notes are provider-private and not visible to clients
  - Full module complete: DB schema, API endpoint, UI components, documentation synchronized
  - **Lead Status Bidirectional Fix (April 24, 2026)** — COMPLETE:
  - Root cause: get_ui_status() четеше match.status вместо lead.status → разминаване между DB и UI
  - Fix 1: get_ui_status() вече проверява lead.status ПЪРВО за терминални статуси (cancelled, done, contacted)
  - Fix 2: change_lead_status() не обновява match.status при cancelled (само lead.status)
  - Fix 3: Migration cdf063316609 добавя 'cancelled', 'contacted', 'done' в lead_matches CHECK constraint
  - Засегнати файлове: apps/api/services/provider_service.py, apps/api/alembic/versions/cdf063316609_add_cancelled_to_lead_matches_status.py

### Recent Changes (April 2026)
**Blocker 3 — Outreach Unsubscribe Mechanism (June 22, 2026)** — COMPLETE:
- New table: `outreach_unsubscribes` (email PK, unsubscribed_at TIMESTAMPTZ, reason CHECK)
- Alembic migration: `u1v2w3x4y5z6_add_outreach_unsubscribes.py`
- New model: `OutreachUnsubscribe` in `models.py`
- New config: `OUTREACH_HMAC_SECRET: str` in `Settings` (loaded from Railway env var)
- New router: `apps/api/routes/outreach.py` — `GET /api/v1/outreach/unsubscribe`
  - Verifies HMAC-SHA256 token, writes to DB, 302 redirect to confirmation page
  - Invalid token → 400 `{"detail": "invalid_token"}`
- New page: `apps/web/app/[lang]/outreach/unsubscribe/page.tsx`
  - async Server Component with `await searchParams` (Next.js 16 required)
  - Two states: confirmed (green checkmark) / invalid link (gray icon)
  - Static Polish text, no translation keys
- Updated: `apps/api/scripts/templates/outreach_email_pl.html`
  - Added `{{ unsubscribe_url }}` Jinja2 variable in footer
- Updated: `apps/api/scripts/send_outreach_bulk.py`
  - Added `_generate_unsubscribe_url()` — HMAC token generation
  - Added DB check against `outreach_unsubscribes` before every send
  - Added SQLAlchemy engine setup for DB queries
- E2E verified: invalid token → 400, valid token → 302, DB record created, bulk skip confirmed

**Blocker 4 — Resend Webhooks (June 22, 2026)** — COMPLETE:
- New table: `outreach_events` (UUID PK, resend_message_id, email, event_type, occurred_at TIMESTAMPTZ)
- Alembic migration: `v1w2x3y4z5a6_add_outreach_events.py`
- New model: `OutreachEvent` in `models.py`
- New config: `RESEND_WEBHOOK_SECRET: str` in `Settings` (loaded from Railway env var)
- New router: `apps/api/routes/webhooks.py` — `POST /api/v1/webhooks/resend`
  - Verifies Resend svix signature (svix-id, svix-timestamp, svix-signature headers)
  - Logs all events to outreach_events table
  - email.bounced → also writes to outreach_unsubscribes (reason='bounce')
  - email.complained → also writes to outreach_unsubscribes (reason='complaint')
  - Idempotent: duplicate events safely handled
  - Returns 200 for malformed payloads (prevents Resend retry loops)
- Registered in: `apps/api/main.py` (webhooks_router)
- New dependency: svix>=1.0.0 in requirements.txt
- Manual config: Webhook created in Resend Dashboard (Enabled), RESEND_WEBHOOK_SECRET added to Railway
- E2E verified: email.sent + email.delivered recorded in outreach_events (resend_message_id: 9764744d-5be9-4425-8a87-147535920076)

**Blocker 6 — Claim Verification (June 23, 2026)** — COMPLETE:
- email verification removed from token flow; wizard pre-fill for scraped providers; category_slug + data_source in API; photo upload fix pending
- DB: scraped_email + pending_claim_verifications table (migration b1c2d3e4f5g6)
- DB: category_slug column on providers (migration c1d2e3f4g5h6)
- Backend: data_source + category_slug added to get_provider_profile() response
- Frontend: AutoClaimTrigger redirect → /provider/dashboard/profile (wizard)
- Alembic current head: c1d2e3f4g5h6 (непроменен)

**Blocker 7A — Banner Flow Redesign (June 24, 2026)** — COMPLETE:
- claim_provider(): no JWT required for source=banner
- verify_claim_code(): get_or_create_claim_user(scraped_email) → returns JWT + redirect
- PendingClaimVerification: filtered by user_id==None (banner flow)
- IntegrityError catch → 409 USER_ALREADY_HAS_PROVIDER
- verify/page.tsx: auth guard removed
- VerifyCodeForm.tsx: saveAuth(token) after successful verify
- ClaimProcessor.tsx: sessionStorage guard replaces useRef
- sw.js: /_next/ exclusion prevents Application error on router.push()
- Art.14 email: dashboard_link uses lang parameter correctly
- Welcome email removed from verify flow → moved to Task 6A
- E2E verified: full banner flow working end-to-end

**Blocker 7B — Magic Link Login (June 24, 2026)** — COMPLETE:
- Backend: POST /api/v1/auth/request-magic-link endpoint (auth.py)
  - Rate limiting: 1 request/minute per email
  - Cleanup of unused tokens before generating new one
  - secrets.token_urlsafe(32) → SHA256 hash → MagicLinkToken record
  - 24h TTL, single-use, always returns 200 (no email enumeration)
- Backend: send_login_magic_link_email() method (email_service.py)
  - Separate from send_magic_link_email() (client leads flow)
  - PL/EN support (technical debt: other 32 languages → EN)
- Frontend: requestMagicLink() function (auth-api.ts)
- Frontend: LoginClient.tsx — "Brak hasła? Zaloguj się linkiem na email →"
  - Appears on step 2 (after email entry)
  - Click → sends link to already-entered email → success message
  - No second email field
- Translations: 8 keys × 34 languages (seed_magic_link_translations.py)
- Existing infrastructure: MagicLinkToken model + POST /auth/magic-link (consumes token, issues JWT) — untouched
- Tested: passwordless provider → magic link → provider dashboard ✅
- Known limitations (technical debt, not blocking campaign):
  - Email is PL/EN only; other 32 languages receive EN
  - Magic link login redirect is only partially role-aware

**Blocker 7В — Add/Change Password in Settings (June 24, 2026)** — COMPLETE:
- Backend: POST /api/v1/auth/password endpoint (auth.py)
  - Global endpoint works for all users regardless of role
  - Passwordless users: set new password (no current_password required)
  - Existing password users: change password (current_password required)
  - Rate limiting: 5 attempts per 15 minutes per user_id
  - Error codes: CURRENT_PASSWORD_REQUIRED, INVALID_CURRENT_PASSWORD, RATE_LIMIT_EXCEEDED, USER_NOT_FOUND
- Backend: GET /api/v1/auth/me endpoint (auth.py)
  - Returns current user info including has_password status
  - Single source of truth for password status
  - Response: id, email, role, has_password, locale
- Frontend: PasswordSection.tsx component
  - Shared component for both provider and client settings
  - Uses getMe() to fetch password status from /api/v1/auth/me on mount
  - Automatically shows 2-field form (set password) or 3-field form (change password)
  - Password visibility toggles, client-side validation
- Translations: account_settings namespace (14 keys × 34 languages = 476 rows)
  - seed_account_settings_translations.py
  - Keys: section_security, security_description_no_password, security_description_has_password, label_current_password, label_new_password, label_confirm_password, btn_set_password, btn_change_password, btn_save_password, msg_password_set, msg_password_changed, error_current_password_invalid, error_passwords_dont_match, error_password_too_short
- Architecture refactor: Removed has_password from provider profile and client dashboard responses
  - Centralized password status in /api/v1/auth/me endpoint
  - Eliminates stale context data issues
  - Simplifies component interface (no props needed)
- Tested: ✅ Works for provider settings, ✅ Works for client settings, ✅ Works parallel with magic link login, ✅ Works parallel with Google OAuth login
- Commits: 3c8cda9 (initial), a7f8344 (bug fix), 6c382ea (self-healing), 7602bb4 (/me endpoint), 5228cc3 (refactor)

**Blocker 7Г+7Е — Global Auth Architecture (June 25, 2026)** — COMPLETE:
- New endpoint: POST /api/v1/auth/check-email → returns {exists, has_password, role, oauth_connected}
- New function: determine_post_auth_redirect() — single source of truth for all post-auth redirects
- LoginClient.tsx: smart detection flow (check-email → passwordless auto magic link → magic_link_sent UI)
- Google OAuth fix: correct lang in redirect URL
- magic_link_tokens.lang column added (flows through full request chain)
- QA: ✅ check-email response, ✅ passwordless auto magic link, ✅ login redirect (correct lang), ✅ magic link redirect /bg/ → /bg/client/dashboard, ✅ register redirect, ✅ Google OAuth redirect
- Commits: feat: implement frontend for Blocker 7Г+7Е, fix: lang fixes за login/register/magic-link

**Blocker 7Д — Outreach Email Claim Flow Verification (June 26, 2026)** — COMPLETE:
- E2E verified: direct email claim flow (/pl/claim/{token}, no ?source=banner) still works after Blocker 7A
- T1 (Happy Path): POST /api/v1/providers/claim/{token} → 200 → nevumo_auth_token cookie → /pl/provider/dashboard/profile?claimed=success → wizard visible
- T2 (Already Claimed): same token → error UI (no crash, no unauthorized access)
- T3 (Invalid Token): fake token → error UI (no crash, clean error page)
- All 3 tests: 0 console errors
- Tool: SWE-1.6 + @mcp-playwright

**Blocker 7Ж — Onboarding Pre-fill Scraped Providers (June 26, 2026)** — COMPLETE:
- DB: scraped_phone TEXT column added to providers (migration d2e3f4g5h6i7)
- models.py: scraped_phone field added to Provider model
- provider_service.py: scraped_phone included in get_provider_profile() response
- auth_service.py: get_or_create_claim_user() pre-fills user.phone from scraped_phone if user.phone is None
- providers.py: both call sites pass scraped_phone=provider.scraped_phone
- E2E verified: claim flow → user.phone populated from scraped_phone ✅
- Alembic current head: d2e3f4g5h6i7

**Task 6A — Profile Strength Email** — PLANNED:
- Trigger: first service added (is_complete: False → True)
- Content: personalized advice based on missing profile fields
- Languages: 34 (provider.locale)

**Issue 5 Partial Implementation (June 24, 2026)** — PARTIAL:
- ClaimProfileBanner.tsx: scraped_email показан под business name (пълен, не masked)
- ClaimProfileBanner.tsx: ?source=banner добавен към claim href
- ClaimProcessor.tsx: 202 handler → redirect към /verify?sent_to=...
- ClaimProcessor.tsx: 401 handler → redirect към /auth (ще се промени в 7А)
- verify/page.tsx: sentTo prop → VerifyCodeForm
- VerifyCodeForm.tsx: "Kod wysłano na: {sentTo}" UI
- providers.py: source=banner → 401/422/202 сценарии + masked email
- E2E тест открил: flow изисква login преди код — архитектурен проблем
- Plan: 7 нови блокера (7А–7Ж) преди seed_unclaimed_providers

Next: Blocker 7 (seed_unclaimed_providers.py), Blocker 8 (Railway Scheduler).

**April 21 — City Page Enhancements, Leads Dashboard UX, Next.js 16 Proxy & Client Dashboard i18n**
  - **City Page Hero (4 States)**: Implemented `CityPageHero.tsx` with dynamic content based on provider count, request count, and ratings.
  - **City Stats API**: Added `GET /api/v1/cities/{slug}/stats` with Redis caching (1h TTL) to power the hero section.
  - **Lead Form Integration**: Integrated `LeadForm` directly into the city hero via `CityHeroChips.tsx`.
- **Homepage Hero Social Proof (June 2026)** — COMPLETE:
  - Fixed: hero was showing hardcoded "47 specialists • 120 requests" from seed script
  - Root cause: homepage did not call city stats API; numbers were hardcoded in translation value
  - Added: `getCityStats(citySlug)` function in `apps/web/lib/api.ts` using `API_BASE`
  - API discovery: `GET /api/v1/cities/{slug}/stats` returns flat JSON (no success/data wrapper)
  - Updated: `apps/web/app/[lang]/page.tsx` now fetches real stats via getCityStats()
  - 3-state social proof logic:
    - provider_count > 0 AND request_count > 0 → "{providers} specialists • {requests} requests this month"
    - provider_count > 0 AND request_count == 0 → "{providers} specialists have already registered"
    - provider_count == 0 → "And more: statistics, client reviews, Website Widget"
  - Changed translation key: `homepage.trust_1` from "No commission" → "Visibility in Google" (all 34 langs)
  - Updated: `homepage.social_proof` — now uses {providers} and {requests} placeholders
  - Added: `homepage.social_proof_providers_only` (new key, all 34 langs)
  - Added: `homepage.social_proof_pioneer` (new key, all 34 langs)
  - Affected files: apps/api/scripts/seed_ui_translations.py, apps/web/lib/api.ts, apps/web/app/[lang]/page.tsx
- **Homepage Hero City Fix (June 2026)** — COMPLETE:
  - Problem: Homepage Hero showed the language-default city even after user explicitly selected a different city on `/izberi-grad`.
  - Root cause: City preference was stored only in localStorage (`nevumo_ctx.city`), which is inaccessible during SSR. Priority 1 always failed server-side, falling through to language mapping.
  - Fix 1: `apps/web/app/[lang]/izberi-grad/CitySelectButton.tsx` (NEW) — client component that sets cookie `nevumo_city` + syncs localStorage + navigates on city card click.
  - Fix 2: `apps/web/lib/default-city.ts` — `resolveDefaultCity(lang, cookieCity?)` now accepts optional cookie value as Priority 1.
  - Fix 3: `apps/web/app/[lang]/page.tsx` — reads `nevumo_city` cookie via `next/headers` in both `generateMetadata` and `Homepage` component, passes to `resolveDefaultCity`.
  - Result: Homepage Hero correctly reflects user's city selection on every subsequent SSR visit.
  - Compatibility: No impact on provider registration pre-fill (uses URL params → localStorage), Google OAuth flow (uses state param), or CtxCapture mechanism.
- **Lead Cancellation Logic Improvement (April 24, 2026)** — COMPLETE:
  - Updated `provider_service.py` to correctly handle UI status for cancelled leads.
  - Modified `change_lead_status` to prevent `lead_match.status` update when lead is cancelled.
  - Added `cancelled` status to `lead_matches` check constraint via Alembic migration `cdf063316609`.
  - Updated documentation (`db_schema.md`, `models.py`) to reflect schema changes.
- **Client Dashboard Dynamic Redirect (April 29, 2026)** — COMPLETE:
  - Updated `getClientDashboard` (API + Frontend) to include `last_city_slug` based on the most recent lead.
  - Enhanced `OverviewClient.tsx` to dynamically redirect the "Find Service" button to `/[lang]/[city_slug]` instead of `/[lang]`.
  - Added fallback logic to `/[lang]` if the user has no previous requests.
  - Synchronized `api_contracts.md` and `client-api.ts` interfaces.
  - **LeadForm UX**: Set `showTextarea` to true by default and removed the "Not sure" chip for a more direct request flow on city pages.
  - **Leads Rate Limiting UX**: API now returns the last `lead_id` on 429 errors, allowing email claim for rate-limited users.
  - **Next.js 16 Compliance**: Migrated `middleware.ts` to `proxy.ts` and resolved 404 routing issues on dashboard leads.
  - **Auth Redirect Fix**: Fixed `LoginClient.tsx` to correctly redirect clients to `/client/dashboard`.
  - **Client Dashboard i18n**: Fixed missing translation for "Recent Requests" by syncing `recent_requests_title` key and re-seeding the `client_dashboard` namespace.
  - **Translations**: Seeded 10 new `city.hero_*` keys across 34 languages, 306 new `provider_dashboard` rows, and 2,482 `client_dashboard` rows.
**April 20 — Provider Profile Optimization, CORS Hardening & Static Routing**
  - **Background Translations**: Moved 34-language translation process to FastAPI `BackgroundTasks` to prevent proxy timeouts (>30s) during provider profile updates.
  - **CORS Hardening**: Implemented `CORS_ORIGINS` configuration in `apps/api/config.py` and `main.py` using `load_dotenv()` for secure cross-origin communication.
  - **Static Routing Update**: Relocated static file mount point to `/api/v1/static/provider_images` for architectural consistency and updated `STATIC_FILES_BASE_URL` to support relative paths.
  - **Sequence Synchronization**: Fixed critical 500 errors in lead submission by synchronizing PostgreSQL sequences (`lead_rate_limits`, `auth_rate_limits`) that were out of sync after Phase 3 migrations.
  - **Onboarding UX**: Added `noValidate` to forms to prevent browser-native interference and improved `slugifyText` for proper Bulgarian Cyrillic transliteration.
  - **API Robustness**: Enhanced `lib/provider-api.ts` with strict response validation and `Content-Type` checking to prevent frontend crashes on non-JSON responses.
  - **Location Translations**: Seeded `location_translations` table with 102 rows (3 cities × 34 languages) and updated `cities` API with a multi-level fallback chain.
**April 19 — Provider Onboarding Bug Fix**
  - Fixed "The string did not match the expected pattern" error during Step 1 of provider registration.
  - Added `noValidate` to onboarding forms to prevent browser-native validation from interfering with custom logic.
  - Improved `slugifyText` utility to properly support Bulgarian Cyrillic transliteration.
  - Ensured all submitted fields are properly trimmed and slug is forced to lowercase before API submission.
- **April 13 — UI Cleanup & Accessibility Improvements**
  - Removed inline styles in Dashboard section in favor of Tailwind 4 utility classes
  - Improved button accessibility standards across Dashboard components
  - Standardized styling approach for better maintainability and consistency
- **April 11 — Auth Page i18n**
  - 13 нови ключа добавени в auth namespace seed скрипта (checking_btn, logging_in_btn, registering_btn, sending_btn, error_wrong_password, error_generic, error_rate_limit, error_account_disabled, error_email_exists, register_success, coming_soon, page_title, meta_description)
  - Общо auth ключове: 27 × 34 езика = 918 rows
  - generateMetadata() в auth/page.tsx вече генерира title и description динамично от DB
  - Всички loading states, error messages, coming_soon тоаст са напълно преведени на 34 езика
- **April 11 — Location Translations + Bug Fixes**
  - location_translations table added with 102 rows (3 cities × 34 languages)
  - locations.city_en column added
  - cities API now lang-aware with translation fallback chain
  - Provider dashboard layout.tsx: fixed null user redirect (was redirecting to client dashboard instead of auth)
  - ProviderWidget.tsx: fixed cityInfo?.name → cityInfo?.city after CityOut schema update
  - Backend startup: must use --host 0.0.0.0 for SSR to reach NEXT_PUBLIC_API_URL
- **April 10 — Onboarding Hero i18n + API routing fix**
  - Onboarding hero banner fully translated in 34 languages via provider_dashboard namespace
  - Frontend API_BASE changed from hardcoded `http://localhost:8000` to empty string `""` across all lib files (api.ts, auth-api.ts, client-api.ts, provider-api.ts, tracking.ts, ui-translations.ts, locales.ts)
  - next.config.mjs rewrites added to proxy `/api/v1` requests to backend, enabling relative API paths
  - `httpx` package added to .venv (required by translation_service.py)
- **Provider Dashboard i18n Polish Translation Fix** — Complete remediation of Polish translations in provider dashboard:
  - Root cause: `row_bg(...)` seeding caused English fallback for non-Bulgarian locales
  - Fix: Centralized `POLISH_OVERRIDES` block in `apps/api/scripts/seed_provider_dashboard_translations.py`
  - Affected sections: Overview, Leads, Services, Analytics, Reviews, QR Code, Profile (Settings/Sidebar previously fixed)
  - Operational workflow: reseed script → clear Redis cache (`translations:*:provider_dashboard`) → validate UI pages
  - Branding exception: `logo_pro` remains untranslated as `"Pro"` in all 34 locales
  - No API contract changes, no database schema changes, no model changes
  - Validation required on: `/pl/provider/dashboard`, `/pl/provider/dashboard/leads`, `/pl/provider/dashboard/services`, `/pl/provider/dashboard/analytics`, `/pl/provider/dashboard/reviews`, `/pl/provider/dashboard/qr-code`, `/pl/provider/dashboard/profile`
- **April 4 Strategic Decisions — Warsaw launch operating model**
  - **Categories**: launch scope is intentionally constrained to `cleaning`, `plumbing`, and `massage` to validate supply-demand fit before adding more verticals
  - **Homepage strategy**: homepage is provider-first and optimized for specialist acquisition, not for client browsing
  - **Category-page strategy**: `/[lang]/[city]/[category]` pages are client-first and optimized for SEO capture + lead conversion
  - **SEO strategy**: build programmatic, multilingual city/category landing pages with SSR metadata, hreflang, internal linking, FAQ schema and text blocks
  - **Monetization strategy**: do not monetize early Warsaw launch traffic aggressively; validate liquidity first, keep primary long-term model as pay-per-lead, and treat featured placement as a later-stage monetization layer

- **April 4 Database Changes — launch market data + translation infrastructure**
  - **Locations**:
    - Added Warsaw launch city in `locations`: `Warszawa`, country `PL`, slug `warszawa`, coordinates `52.2297, 21.0122`
  - **Categories**:
    - Seeded/ensured root categories `cleaning`, `plumbing`, `massage`
  - **Category translations**:
    - Script: `apps/api/scripts/seed_warsaw_launch.py`
    - Exact rows: `102` category translation rows (`3` categories × `34` languages)
    - Stored in `category_translations`
  - **UI translations**:
    - Script: `apps/api/scripts/seed_ui_translations.py`
    - Namespace model stored in `translations` table as `namespace.key`
    - Exact final key counts per language: `43` homepage keys + `24` category keys = `67`
    - Exact seeded/upserted UI translation rows across all supported languages: `2,788`
  - **Language set expanded and normalized to 34 supported languages**:
    - `bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, is, it, lb, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, ru, sk, sl, sq, sr, sv, tr, uk`

- **April 4 Backend Changes**
  - **New public endpoint**: `GET /api/v1/translations?lang={lang}&namespace={namespace}`
    - File: `apps/api/routes/translations.py`
    - Returns flat translation payload without namespace prefix
    - Falls back to English if requested language namespace is missing
    - Caches successful payloads in Redis for 1 hour
  - **Router wiring**:
    - File: `apps/api/main.py`
    - `translations_router` mounted under `/api/v1`
  - **New seed scripts**:
    - `apps/api/scripts/seed_warsaw_launch.py` — idempotent Warsaw location/category/category-translation bootstrap
    - `apps/api/scripts/seed_ui_translations.py` — DB seed/upsert for homepage/category UI copy in 34 languages

- **April 4 Frontend Changes**
  - **`apps/web/app/[lang]/page.tsx`**
    - Homepage converted to DB-backed multilingual SSR page
    - Metadata now resolved via homepage namespace translations
    - Navigation/service links normalized around Warsaw launch URLs
    - Provider-first content structure finalized: hero, trust row, how-it-works, category cards, activity feed, why section, second CTA, footer, mobile sticky CTA
  - **`apps/web/components/homepage/RotatingCategory.tsx`**
    - Client component rotates translated category labels from DB-fed homepage data
  - **`apps/web/app/[lang]/[city]/[category]/page.tsx`**
    - Category page converted to DB-backed multilingual SSR page
    - Heading/subtitle/SEO copy/provider CTA now read from category/homepage translation namespaces
    - Provider cards enriched using provider detail fetches for better trust signals
    - FAQ JSON-LD retained for search visibility
    - Internal related-link structure created between the 3 Warsaw launch categories
  - **`apps/web/components/category/LeadForm.tsx`**
    - Lead form made reusable/translation-ready through prop-based title, subtitle, placeholders, button label and trust-item inputs
    - Continues to submit minimal conversion payload (`phone`, optional `description`, `source: 'seo'`)
  - **`apps/web/lib/ui-translations.ts`**
    - Added frontend helper for fetching namespace translations from the API with hourly revalidation
    - Supported-language guard now matches the 34-language rollout
  - **`apps/web/lib/api.ts`**
    - `ServiceOut` extended with `category_slug`, enabling category-aware UI behavior
  - **`apps/web/app/[lang]/client/dashboard/layout.tsx`**
    - Added logout, role switch and homepage CTA improvements in the client shell
  - **`apps/web/components/ProviderWidget.tsx`**
    - Added selectable service chips, auto-filled request description and expanded service-list behavior
  - **Asset cleanup**:
    - `apps/web/public/Nevumo_logo-2.svg` removed as unused duplicate asset

- **Design System Decisions Established**
  - **Primary brand action color**: orange remains the dominant CTA and emphasis color across homepage, category pages and dashboard actions
  - **Surface system**: white primary surfaces, light gray secondary sections, rounded-xl cards, soft borders and soft shadows
  - **Conversion-first UI**: one primary action per section, short trust bullets, friction-minimized forms, immediate CTA visibility on mobile via sticky controls
  - **Trust modules**: ratings, specialist counts, request velocity, FAQ content and proof snippets are reusable building blocks across SEO pages and widgets
  - **Responsive layout pattern**:
    - Homepage: stacked storytelling sections with repeated CTA opportunities
    - Category page: content/listing column + sticky conversion sidebar

- **Scale Principles Reaffirmed**
  - **Programmatic rollout over bespoke pages**: one reusable homepage pattern and one reusable category-page pattern should scale city-by-city and language-by-language
  - **DB as content source of truth**: UI copy moved out of hardcoded components and into PostgreSQL so new languages/markets can be rolled out without reworking page structure
  - **Cache multilingual payloads aggressively**: Redis namespaced caching keeps translation reads cheap while preserving server-rendered SEO output
  - **Launch narrow, then expand**: prove liquidity in one city and three categories before broadening the matrix of locations/categories
  - **Keep conversion payload minimal**: public lead capture remains intentionally simple to maximize completion rate and support future scaling

- **Homepage Implementation (Warsaw)** — Provider-first landing page:
  - DB-backed multilingual SSR content fetched by namespace
  - Rotating hero section with translated launch categories
  - Category cards with icons and counts
  - Live activity feed showing recent requests
  - Mobile-responsive design with Tailwind CSS
- **Category Page Implementation** — Client-first service discovery:
  - Server-side rendering with DB-backed translations
  - Two-column layout with lead form and provider listings
  - SEO text blocks for content marketing
  - FAQ schema markup for search visibility
  - Internal linking structure for navigation
- **Warsaw Launch** — Complete marketplace initialization:
  - 1 city: Warszawa (PL)
  - 3 categories: cleaning, plumbing, massage
  - 34 language translations for all categories
  - Idempotent seed script for safe re-running
- **Implemented Review/Rating System** — Closed trust conversation model:
  - Database migration for provider reply fields and user email preferences
  - Backend API endpoints for client and provider review flows
  - Email notification service with opt-out mechanism
  - Provider dashboard reviews section with reply/edit functionality
  - Client dashboard completed jobs with review CTA
  - Client email preferences toggle
  - Translation keys for all 34 languages
  - Updated documentation (api_contracts, db_schema, architecture)
- **Social Proof + Multi-Role Review Restore** — Root-cause fix and review hardening:
  - Applied `users.name` migration (`i8j9k0l1m2n3`) to restore embed/social-proof and authenticated dashboard queries
  - Provider dashboard route now loads provider profile through the correct `get_provider_profile(provider, db)` contract
  - Review surfaces now use canonical `users.name` display names with `Client` fallback, never email-derived names
  - Backend review eligibility, can-review checks, and create-review flow now block self-reviews via `Provider.user_id == client_id`
  - Public `POST /api/v1/leads` now links authenticated submissions to `lead.client_id`, enabling real review eligibility for logged-in users
- **Rating card** on provider dashboard clearly labeled as "Overall Rating" from all client reviews
- **Client Dashboard Backend Expansion** — Added authenticated `/api/v1/client/dashboard` and `/api/v1/client/leads` endpoints:
  - Dashboard overview now returns `active_leads`, `completed_leads`, `reviews_written`, and latest 3 leads for the current client
  - Leads inbox now supports `all|active|done|rejected` filters, provider metadata, English category fallback, and `has_review`
  - `main.py` already included the shared `client_router`, so no new router wiring was needed beyond extending `routes/client.py`
- **Client Dashboard Frontend** — Implemented provider-style client shell and pages:
  - New guarded layout at `/[lang]/client/dashboard/*` with dedicated sidebar/topbar, active nav state, email in topbar, and orange `НАМЕРИ УСЛУГА` CTA
  - `apps/web/lib/client-api.ts` adds strict typed wrappers for dashboard, leads, reviews, eligible leads, review submission, and review preferences
  - Overview page renders KPI cards + recent leads hero/empty state
  - My Requests page renders status tabs, lead cards, and inline review submission for completed provider-linked jobs without reviews
  - Reviews page now splits into `Написани` and `Чакащи ревю`, with collapsible provider replies and the shared review-reply email toggle
  - Settings page now contains readonly email, reset-password link, `Стани доставчик`, and logout
- **Dynamic Price Range** — Real-time pricing from provider services:
  - New `GET /api/v1/price-range?category_slug=X&city_slug=Y` endpoint
  - Queries MIN/MAX base_price from services with valid prices (excludes 'request' price_type)
  - Returns currency based on city's country_code (PL→PLN, BG→EUR, RS→RSD, CZ→CZK, GR→EUR)
  - Redis caching with TTL 3600s (key: `price_range:{category}:{city}`)
  - Frontend integration in category page: metadata, FAQ schema, SEO paragraph
  - Translation keys for price display: `price_text_none/single/range`, `price_faq_none/single/range`, `price_meta_none/single/range`

- **Client Dashboard Fixes (Review Flow)**:
  - Added `useEffect` in `reviews/page.tsx` to load pending leads count on mount without a loading spinner, ensuring the badge count is populated immediately.
  - Fixed SQL join logic in `get_eligible_leads_for_review()` service to correctly filter `LeadMatch` by both `provider_id` and `lead_id`, ensuring all reviewable providers for a given lead are returned instead of just one.
  - **Client Dashboard Review Eligibility Fix (May 25, 2026)** — COMPLETE:
    - **Problem:** After introducing the shared status change system (migration 0535f00974f4), completed requests were not showing the Review button and not appearing in the "Pending Review" tab. Root cause was that the client status change endpoint was not synchronizing status updates to the `LeadMatch` table, which is required for review eligibility.
    - **Solution:** Added `LeadMatch` synchronization in `apps/api/routes/client.py` (lines 132-143) to sync `match.status` with the new status when `lead.provider_id` exists. When a client changes a request status to "done", the corresponding `LeadMatch` record is also updated to "done", making the request eligible for review.
    - **Status Transitions:** Provider transitions: new → contacted/cancelled, contacted → cancelled. Client transitions: new → contacted → done, new/c → cancelled.
    - **Review Eligibility:** Only leads with `LeadMatch.status IN ('contacted', 'done')` are eligible for review.

## Production Deployment

### Инфраструктура (конфигурирана May 29, 2026)

| Компонент | Платформа | URL/Endpoint | Статус |
|-----------|-----------|--------------|--------|
| Backend API | Railway (Hobby $5/мес) | api-production-7631.up.railway.app | ✅ Online |
| Database | Neon (PostgreSQL 17, EU Frankfurt) | neon.com | ✅ Готов |
| Redis Cache | Upstash (EU West, Free) | upstash.com | ✅ Готов |
| Media Storage | Cloudflare R2 (EU, Free 10GB) | nevumo-images bucket | ✅ Готов |
| Domain | nevumo.com (Cloudflare DNS) | — | ✅ Прехвърлен |
| Frontend | Vercel | — | ⏳ Предстои |

### Railway Configuration
- **Service:** api
- **Builder:** Dockerfile
- **Dockerfile Path:** /apps/api/Dockerfile
- **Region:** EU West (Amsterdam)
- **Branch:** main (auto-deploy при push)
- **GitHub Repo:** Dimi667/nevumo

### Environment Variables (Railway)
- DATABASE_URL — Neon connection string
- REDIS_URL — Upstash Redis URL
- R2_ACCESS_KEY_ID — Cloudflare R2
- R2_SECRET_ACCESS_KEY — Cloudflare R2
- R2_BUCKET_NAME — nevumo-images
- R2_ENDPOINT_URL — Cloudflare R2 S3 endpoint

### Deployment Workflow
След всяка промяна на кода:
```bash
git add .
git commit -m "описание на промяната"
git push origin main
# Railway автоматично deploy-ва
git push nevumo-git main  # архив на SSD
```

### Предстои
- Миграция на база данни от локален Mac към Neon
- Deployment на frontend (Vercel)
- DNS настройки за nevumo.com → Vercel
- Custom domain за API: api.nevumo.com → Railway

### 🔮 Future
- AI lead matching
- Subscription / pay-per-lead billing
- Multi-region DB partitioning
- Advanced provider analytics
- **PWA Етап 2** — Push notifications само за провайдери: нова таблица push_subscriptions, Web Push протокол, интеграция с lead creation flow. Старт след валидиране на PWA install adoption от page_events данни.
- **PWA Етап 3** — Push notifications за клиенти: нотификация когато провайдер отговори на заявка.
- **Static Files URL Standardization** — Extend STATIC_FILES_BASE_URL pattern to other services that generate public URLs (e.g., QR codes, document uploads). Current implementation is specific to provider profile images; future services should use the same environment variable pattern for consistency across local and production environments.
- **sw.js generation rule** — `sw.js` is a static committed file in `apps/web/public/sw.js` — no PWA library needed; postbuild appends push handlers via `[NEVUMO-CUSTOM-SW]` marker on every build
- **Mobile tap zoom prevention** — `touch-action: manipulation` must be on all interactive elements globally in globals.css; input font-size must be `max(16px, 1em)` to prevent iOS auto-zoom; `max-width: 100%` on `*` prevents horizontal overflow. Do NOT revert these rules.
- **Claimed Profiles Warsaw launch:** Full roadmap in `docs/claimed_profiles_plan.md`. Фаза 1 данни в ход: ~1,200 уникални имейла събрани (CEIDG 633 + Panoramafirm 612). Следващи: email extractor от 233 уебсайта (1З), SMS кампания (1Д), Bing API (1Ж). Паралелно: seed (2А), claim landing page (4А). Target: 1,700-2,000 имейла → 136-300 claimed профила.

**Claimed Profiles — E2E Test Status (June 21, 2026):**
- E2E тест completed за dimitar.j.dimitroff@gmail.com → claimed "Hydraulik Testowy E2E" ✅
- Critical bugs found and fixed: auth cookie, draft detection, redirect flow, error handling
- Test scripts: e2e_outreach_full_setup.py, e2e_outreach_cleanup.py
- BEFORE bulk campaign (Task 5A): must fix auto-claim flow + Art. 14 email + test email/password + test error states

**Pre-Task 5A checklist:**
- ✅ Auto-claim after login (skip second visit to claim page) — ЗАВЪРШЕНО (22 юни 2026)
- 🔴 Test email/password login redirect flow
- ✅ Art. 14 GDPR email in providers.py POST endpoint — ЗАВЪРШЕНО (22 юни 2026)
- 🟡 Browser test all 5 error states
- 🟡 Test neli and nevumo.dev claim flows
- 🟡 Cleanup e2e_test providers from Neon DB

**Known gaps:**
- ✅ send_claim_welcome_email await bug — FIXED (22 юни 2026, Kimi-2.6): removed await from sync function call in providers.py

- **Claimed Profiles — Task 4Б Unclaimed Banner (June 21, 2026):** ✅ ЗАВЪРШЕНА
  - ClaimProfileBanner.tsx рефакториран (translations + correct claim URL)
  - Нова DB таблица city_category_search_volume (Warsaw: cleaning=7000, plumbing=5400, massage=6900)
  - Seed script: apps/api/scripts/seed_unclaimed_banner_translations.py (170 rows, 34 езика)
  - Backend: claim_token + search_volume добавени в GET /api/v1/providers/{slug} response
  - Frontend: ProviderDetail TypeScript interface обновен в lib/api.ts
  - Alembic migration: 20260620_add_city_category_search_volume.py
  - Next: Task 2A seed_unclaimed_providers.py → outreach_ready.csv

- **Claimed Profiles — Task 4В CTA Button Adaptive Layout (June 21, 2026):** ✅ ЗАВЪРШЕНА
  - Adaptive 2-line layout за имена > 22 символа
  - Засегнати: ProviderWidget.tsx, StickyProviderCTA.tsx, LeadPanel.tsx, ProviderMobileCTA.tsx
  - Root cause диагноза: ProviderMobileCTA.tsx рендерира се 2 пъти на iOS 26 (StickyBottomBar returns null)
  - Padding fix: StickyBottomBar fallback wrapper px-0 (без дублиран padding)

- **Claimed Profiles — Блокер 1 Auto-claim (June 22, 2026):** ✅ ЗАВЪРШЕНА
  - AutoClaimTrigger.tsx детектира ?from=auth в URL след auth redirect
  - и автоматично изпраща POST claim без втори клик от потребителя.
  - addFromAuthParam() добавен в LoginClient, oauth-callback, OAuthTermsClient.
  - Fix: ?role=provider се чете като intent при регистрация.
  - 10 нови translation ключа seeded в claim namespace.
  - Commit: 7394f73

### Known gap
- already_claimed state не работи: GET endpoint не различава claimed от not_found
- Email subject >50 chars: truncate-ва се на мобилен — нужни по-кратки варианти

## Email Notification Incident Log

**2026-06-09 — Email notifications fully operational:**
- All 11 transactional emails confirmed working
- Direct lead → provider email: FIXED
- Marketplace lead → all matched providers email: FIXED
- Lead status change → client email: CONFIRMED WORKING
- Lead status change → provider email: CONFIRMED WORKING
- Error visibility: [EMAIL_WARNING] logs now appear in Railway logs on any email failure

## Favicon Issue Log

**Status:** UNRESOLVED for Safari iOS. Working on: Chrome, Edge, Orion desktop, Safari desktop.

### What was tried (all failed for Safari iOS):

1. SVG favicon via `<link rel="icon" type="image/svg+xml">` — broke Safari desktop too
2. PNG favicons (32x32, 16x16) via manual `<head>` link tags — works only on full page load, disappears on client-side navigation
3. `favicon.ico` in `apps/web/app/` (Next.js file convention) — generates hashed URLs like `/icon.png?icon.d96e364e.png`, inconsistent
4. `icons` field in root layout `metadata` export — overridden by child pages with `generateMetadata`
5. Airbnb pattern: multiple apple-touch-icon sizes (76, 120, 152, 180) via manual `<head>` — same problem: disappears on client-side navigation
6. `FaviconManager` client component with `useEffect` + `usePathname` — did not fix Safari iOS
7. `baseIcons` shared helper + `metadata.icons` in `[lang]/layout.tsx` — caused duplicate icon tags (manual head + metadata), unstable React keys in RSC payload caused Safari to reset favicon on navigation
8. Stable React `key` props on manual `<head>` link tags (root layout) — Safari still resets favicon on client-side navigation
9. Removed duplicate metadata from `[lang]/layout.tsx`, kept only stable-key manual tags — still not working

### Root cause identified:
Next.js App Router: child pages with `generateMetadata` override `icons` from root layout metadata during client-side navigation. Manual `<head>` tags also disappear on client-side navigation.

### Current state (manual <head> in root layout.tsx):
- `<link key="apple-touch-icon">` + 4 sizes + `<link key="favicon-icon">` present in HTML on ALL pages (confirmed via curl)
- Tags present in server-rendered HTML AND RSC payload
- Safari iOS still resets favicon on client-side navigation
- Root cause unclear: iOS Safari may ignore favicon updates during SPA navigation regardless of implementation

### What works:
- Full page load (direct URL) → favicon shows
- Chrome, Edge, Orion: always show favicon regardless

### Files created/modified:
- `apps/web/public/favicon.ico` (5238 bytes, proper ICO)
- `apps/web/public/favicon-32x32.png`, `favicon-16x16.png`
- `apps/web/public/apple-touch-icon.png`, `apple-touch-icon-76x76.png`, `apple-touch-icon-120x120.png`, `apple-touch-icon-152x152.png`
- `apps/web/scripts/generate-favicons.js`
- `apps/web/components/FaviconManager.tsx`

### Known Issues — Pre-Launch (June 23, 2026)

✅ Issue 1: Magic link claim flow — ЗАВЪРШЕН (23 юни 2026)
   (claim token = proof of identity, auto-login/register, zero friction)
✅ Issue 2: Auth redirect → claim wizard — ЗАВЪРШЕН (23 юни 2026)
   (решен като част от Magic Link Flow)
✅ Issue 3: Photo upload — ЗАВЪРШЕН
✅ Issue 4: JWT expiry → безкраен loop — РЕШЕН (23 юни 2026)
   (401 interceptor в provider-api.ts + client-api.ts → clearAuth() + redirect)
🟡 Issue 5: Banner Claim Flow — частично имплементиран, нужен редизайн

Частично: scraped_email в банера, ?source=banner, 202 flow, masked sent_to,
VerifyCodeForm показва email
Проблем: изисква login ПРЕДИ код — грешна архитектура
План: Блокери 7А–7Ж в claimed_profiles_plan_2.md
Всички 7А–7Ж трябва да са завършени преди Блокер 8 (seed_unclaimed_providers)

Details: claimed_profiles_plan_2.md → секция KNOWN ISSUES