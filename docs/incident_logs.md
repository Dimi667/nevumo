# Incident Logs

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
