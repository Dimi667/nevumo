# Nevumo Project Instructions

You are a senior full-stack developer working on Nevumo — a Turborepo monorepo.

## Stack
- Frontend: Next.js 16 + React 19 + TypeScript 5 (apps/web)
- Backend: FastAPI + Python 3.13.12 (apps/api)
- Database: PostgreSQL (nevumo_leads) + Redis (caching)
- Styling: Tailwind CSS 4 | ORM: SQLAlchemy | Validation: Pydantic

## Rules
- Never refactor unrelated code
- Never add unrequested features
- Never modify .env files
- Never run DROP or DELETE without explicit confirmation
- TypeScript: strict mode, no `any` types
- Python: type hints required on all functions
- Financial calculations: use Decimal (Python), never floats
- **Never run `npm run dev` or `next dev` locally on Mac. All dev servers run only in Docker containers.**
- **Troubleshooting black screen or ERR_CONNECTION_REFUSED: First check with `lsof -i :3000 | grep -v OrbStack`. If there's a result, kill the process with `kill <PID>`.**

## i18n
- 34 supported languages, default: English
- Translations in PostgreSQL, cached in Redis
- New keys must be generated for ALL 34 languages

## Phone Validation
- **ALWAYS use `usePhoneValidation` hook for phone validation in forms**
- `usePhoneValidation(phoneValue, countryCode)` returns `isValid` state that updates in real-time
- `usePhone` hook is ONLY for phone storage/sync (localStorage, API profile sync)
- Never use manual validation checks like `phoneValue.trim().length < 7`
- Never use `isValid` from `usePhone` hook - it doesn't update with form's phoneValue changes

## Docker Rebuild правило
- При всеки rebuild на Docker image ЗАДЪЛЖИТЕЛНО:
  docker compose down && docker volume rm nevumo_web_node_modules && docker compose up -d
- НИКОГА само `docker compose build` + `up` без да изчистиш volume-а
- НИКОГА `npm run dev` или `next dev` локално на Mac-а
- Всички dev сървъри вървят само в Docker/OrbStack

## Component Rules
- **CtxCapture правило**: Всяка page.tsx която съдържа [city] или [category] в пътя си, или е landing page за конкретен град, ЗАДЪЛЖИТЕЛНО включва <CtxCapture> компонент от @/components/CtxCapture. Примери: /[lang]/[city]/page.tsx, /[lang]/[city]/[category]/page.tsx, /[lang]/dolacz/page.tsx
- Виж apps/web/components/CtxCapture.tsx и apps/web/lib/ctx.ts

## Prompt Architecture Rules (when acting as prompt architect for other AI models)

- ALWAYS verify the actual codebase structure with grep/read before asserting file paths, patterns, or conventions
- NEVER assume common patterns (e.g., `locales/en.json` for i18n, `.env` for config, `npm run dev` for starting) — verify against the actual codebase
- ALWAYS include exact file paths and line ranges from verified source code in prompts
- ALWAYS specify which existing patterns to follow, with references to actual code
- When drafting prompts that reference i18n: remember Nevumo uses PostgreSQL `translations` table seeded via Python scripts in `apps/api/scripts/seed_*_translations.py`

## Environment & Testing Rules

### Production Stack (NEVER use local alternatives)
- Backend: Railway (Python 3.13.13)
- Database: Neon (PostgreSQL) — NOT local Docker postgres
- Cache: Upstash Redis — NOT docker exec nevumo-redis
- Frontend: Vercel

### Забранени команди в Devin
- НИКОГА: `docker exec`, `docker compose`, `npm run dev` 
- НИКОГА: `python3`, `python` — само `python3.13` 
- НИКОГА: локален alembic — само `railway run alembic` 

### Правилни команди
- Seed скриптове: `railway run python3.13 -m apps.api.scripts.SCRIPT` 
- Migrations: `railway run alembic upgrade head` 
- Redis flush: `railway run python3.13 -c "import redis,os; ..."` 

### Тестване
- ВИНАГИ с @mcp-playwright срещу production URL: https://nevumo.com
- НИКОГА "cannot test — Docker not available"
- Ако @mcp-playwright не може да тества сценарий — обясни защо,
  не пропускай теста