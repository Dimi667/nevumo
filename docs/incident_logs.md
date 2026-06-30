# Incident Logs

---

## 2026-06-30 — Timezone Comparison Error in verify_claim_code()

**Симптом:** 500 Internal Server Error при verify_claim_code() — TypeError: can't compare offset-naive and offset-aware datetimes

**Root cause:** Migration ff8bc78d912a (commit 925f091, Profile Strength Email задача) умишлено/инцидентно сменила pending_claim_verifications timestamp полета от timezone-aware на naive, без да обнови кода в verify_claim_code(), който още сравняваше с datetime.now(timezone.utc). Кодът използваше timezone-aware datetime.now(timezone.utc) за expires_at сравнение, но базата имаше naive timestamps след миграцията.

**Импакт:** 0 реални потребители засегнати — открито само от Б11 функционален тест с @mcp-playwright срещу production, преди bulk кампанията.

**Решение:** datetime.now(timezone.utc) → datetime.utcnow() на двата места в providers.py (commit 6b08f51):
- Line 459: expires_at calculation за pending_claim_verifications
- Line 701: expires_at comparison в verify_claim_code()

Това align-ва с установената конвенция в codebase-а, където pending_claim_verifications използва naive timestamps (match-ващи други подобни таблици като magic_link_tokens, password_reset_tokens, pending_lead_claims).

**Файлове:**
- apps/api/routes/providers.py (2 реда променени)

**Правила за бъдещето:**
- Migrations да съдържат САМО промени, свързани с конкретната задача — не комбинирай несвързани schema промени в една migration
- При промяна на timestamp типове (aware ↔ naive) винаги проверявай всички места в кода, където се прави datetime сравнение

---

## 2026-05-30 — Production Site Down After First Deployment

**Симптом:** nevumo.com не се зарежда. Vercel връща 504 GATEWAY_TIMEOUT на всички SSR страници.

**Root causes (4 проблема в каскада):**

1. **Cloudflare DNS сочеше към стар Railway URL** — при новия deploy Railway генерира нов service URL (`api-production-7631.up.railway.app`), а Cloudflare CNAME сочеше към стария (`ntkked5p.up.railway.app`). Допълнително Cloudflare proxy (оранжев облак) беше включен, което Railway не поддържа.

2. **Липсваше `API_URL` environment variable във Vercel** — Next.js SSR fetch-овете използват `API_URL` за server-side заявки. Без нея SSR не можеше да достигне API-то и timeout-ваше след 300 секунди.

3. **`API_URL` липсваше в `turbo.json` env масива** — Turbo не я подаваше към build процеса, което причиняваше build failure.

4. **SQLAlchemy connection pool изчерпваше Neon free tier лимита** — при static generation Vercel генерира 210 страници едновременно, всяка правеше множество DB заявки. Neon free tier позволява 5 едновременни връзки, SQLAlchemy default pool (size=5, overflow=10) отваряше 15. Резултат: `QueuePool limit of size 5 overflow 10 reached`.

**Решения:**

1. **DNS fix:** Cloudflare CNAME за `api` → `api-production-7631.up.railway.app`, Proxy status → DNS only (сив облак). Използван Railway "One-click DNS Setup" за автоматично управление занапред.

2. **Vercel env fix:** Добавена `API_URL=https://api.nevumo.com` в Vercel → Environment Variables → All Environments.

3. **turbo.json fix:** Добавен `"API_URL"` в `tasks.build.env` масива в `turbo.json`.

4. **NullPool fix:** В `apps/api/database.py` заменен default SQLAlchemy pool с `NullPool` — всяка връзка се отваря и веднага затваря, без pooling. Подходящо за Neon free tier и serverless среди.

**Правила за бъдещи deployments:**
- Cloudflare CNAME за Railway винаги трябва да е **DNS only** (не Proxied)
- Всяка нова environment variable трябва да се добавя и в `turbo.json` env масива
- Neon free tier = NullPool задължително
- GitHub свързан с Vercel — всеки `git push origin main` тригерира автоматичен Vercel deploy

---

## 2026-04-28 — Provider Dashboard Stats Excluded Retro-Matched Leads

**Проблем:** Новорегистрирани провайдери виждат 0 на KPI картите (Общо/Нови запитвания) въпреки retro-matched leads.

**Root cause:** get_dashboard_stats() в apps/api/services/provider_service.py броеше само Lead.provider_id == provider.id. Retro-matched leads живеят в lead_matches таблицата и не се брояха.

**Fix:** total_leads заменен с UNION SQL заявка (leads + lead_matches). new_leads и contacted_leads обновени да включват LeadMatch.status 'invited'/'contacted'.

**Файл:** apps/api/services/provider_service.py → get_dashboard_stats()

---

## 2026-04-28 — Client Dashboard Showed Wrong Role State

**Проблем:** Потребител с JWT role="provider" попадаше на client dashboard и получаваше ALREADY_IN_ROLE при клик на "Стани доставчик".

**Root cause:** Client dashboard layout нямаше JWT role guard — не проверяваше дали токенът вече е provider.

**Fix:** Добавен useEffect guard в apps/web/app/[lang]/client/dashboard/layout.tsx — декодира JWT, ако role="provider" redirect-ва към /[lang]/provider/dashboard.

**Тестван — PASS**

## 2026-04-28 — Retro-Matching Widget Lead Leak

**Проблем:** Нови провайдери получаваха widget leads от чужди провайдери при retro-matching.

**Root cause:** retro_match_provider() не филтрираше по Lead.provider_id — widget leads с provider_id != NULL се матчваха към всички нови провайдери в категорията.

**Fix:** Добавен филтър Lead.provider_id == None в retro_match_provider() в apps/api/services/provider_service.py.

**Тестван с @mcp-playwright — PASS**

## 2026-04-28 — Mass SEO Title Duplicate Correction

**Symptom:** Duplicated brand name "Nevumo" in page titles (e.g., "Home | Nevumo | Nevumo").

**Root cause:** The `meta_title` keys in the database contained the suffix " | Nevumo", which was also being appended by the global Metadata Template in `layout.tsx`.

**Fix:**
1. Cleaned up the `translations` table by removing " | Nevumo" and " | Nevumo.com" suffixes from all `meta_title` keys across all 34 languages.
2. Synchronized database state with the programmatically added brand name in the Next.js `layout.tsx`.
3. Flush Redis: `docker exec nevumo-redis redis-cli FLUSHALL`
4. Verified titles on homepage, category pages, and city pages via Playwright + Phoenix.

**Rule:** Database translations for metadata must be "clean" (brand-agnostic) as the brand is managed at the layout level.

## 2026-04-27 — Widget Namespace Missing Nudge Translation Keys

**Symptom:** ProviderWidget showed English text for post-lead nudge despite correct Bulgarian translations in category namespace.

**Root cause:** get_widget_translations() in providers.py fetches only widget.* keys. Nudge keys existed only in category namespace — not copied to widget.

**Fix:**
1. Created apps/api/scripts/seed_widget_nudge_translations.py — copies 13 nudge keys from category → widget namespace for all 34 languages
2. ON CONFLICT clause must be (lang, key) — translations table has NO separate namespace column
3. Flush Redis: docker exec nevumo-redis redis-cli KEYS "translations:*" | xargs docker exec -i nevumo-redis redis-cli DEL
4. docker restart nevumo-web

**Rule:** After every translation seed → always run docker restart nevumo-web.

## 2026-04-26 - Docker Network Interface Loss

**Problem:** Next.js (nevumo-web) experienced `fetch failed` errors with `ConnectTimeoutError` when attempting to reach the API at `nevumo-api:8000`.

**Root Cause:** The nevumo-api container lost its network interface in the Docker network after the host machine was put to sleep. The container was connected to the `nevumo_default` network but had no IP address assigned (IPAddress and EndpointID were empty).

**Resolution:** 
1. Ran `docker network prune -f` to clean up unused networks
2. Restarted containers with `docker-compose up -d --build`
3. After restart, nevumo-api was properly assigned IP 192.168.97.4 in the network
4. Verified connectivity with ping from nevumo-web container (0% packet loss)
5. Cleared Redis cache with `docker exec nevumo-redis redis-cli FLUSHALL`
6. Confirmed API responding with 200 OK on /docs endpoint

**Status:** Resolved

## След всеки seed на преводи → docker restart nevumo-web

## 2026-05-05 — LightningCSS Build Error in Docker Container

**Проблем:** `Error: Cannot find module '../lightningcss.linux-x64-musl.node'` в apps/web Docker контейнер при зареждане на http://localhost:3000/pl/warszawa/cleaning

**Root cause:** Alpine Linux (node:22-alpine) използва musl libc, но lightningcss-linux-x64-musl пакетът не се инсталираше правилно поради конфликти между host (macOS) и container (Linux) node_modules чрез Docker volume mounts. LightningCSS модулът очакваше .node файла на специфична позиция относно своята директория.

**Решение:**
1. **package.json** — Премахнах `lightningcss-linux-x64-musl` от `dependencies` и добавих `lightningcss` и `lightningcss-linux-x64-musl` в `optionalDependencies` за да се инсталира правилната архитектура автоматично
2. **docker-compose.yml** — Промених volumes да монтират само конкретни директории (`./apps/web`, `./packages`, `.env.local`) вместо целия workspace, и добавих named volume `web_node_modules:/workspace/node_modules` за да се предотврати override на container-ните node_modules от host-а
3. **Dockerfile** — Смених base image от `node:22-alpine` на `node:22-slim` (Debian с glibc libc), което позволи на npm да инсталира правилната платформено-специфична версия (lightningcss-linux-x64-gnu вместо musl)

**Файлове:**
- `/Users/dimitardimitrov/nevumo/package.json`
- `/Users/dimitardimitrov/nevumo/docker-compose.yml`
- `/Users/dimitardimitrov/nevumo/apps/web/Dockerfile`

**Тестван — PASS** (http://localhost:3000/pl/warszawa/cleaning се зарежда коректно)

**Урок:** Alpine Linux (musl libc) не е съвместим с всички npm native modules. За сложни native dependencies като lightningcss, Debian (glibc) е по-надежден избор.

---

## 2026-05-24 — Provider Dashboard Translation Keys Missing

**Проблем:** 13 translation keys от `LeadsClient.tsx` и `LeadDetailModal.tsx` липсваха от `provider_dashboard` namespace след изтриване на translation записи от базата.

**Root cause:** Инцидент с изтриване на translation записи от базата данни.

**Диагностика:** Сравнение на три архива установи времевата линия:
- Архив 23.05.2026 — 12 от 13 ключа липсват (след инцидента)
- Архив 16.05.2026 — 12 от 13 ключа липсват (след инцидента)
- Архив 07.05.2026 — 11 ключа налични с 34 езика (преди инцидента)
- 2 ключа никога не са съществували в базата

**Restore:**
- 11 ключа извлечени от архив `nevumo_leads_20260507_155146.sql.gz` чрез `grep` + Python генератор на INSERT SQL
- 2 нови ключа създадени чрез seed скрипт: `apps/api/scripts/seed_leads_missing_keys.py`

**Засегнати ключове (13):**
`aria_close`, `btn_close`, `btn_save_notes`, `label_cancelled_leads`, `label_client_message`, `label_notes_privacy_disclaimer`, `label_private_notes`, `lead_detail_title`, `msg_no_description`, `msg_notes_save_failed`, `msg_notes_saved`, `msg_saving`, `placeholder_private_notes`

**Резултат:** Всички 13 ключа верифицирани с `lang_count = 34`. Redis cache изчистен за `provider_dashboard` namespace.

**Файлове:**
- `/tmp/restore_11_keys_raw.txt` — извлечени данни от архива
- `/tmp/generate_restore_sql.py` — генератор на INSERT SQL
- `/tmp/restore_11_keys.sql` — генериран SQL за restore
- `apps/api/scripts/seed_leads_missing_keys.py` — seed скрипт за 2 нови ключа
