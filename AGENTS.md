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

## i18n
- 32 supported languages, default: English
- Translations in PostgreSQL, cached in Redis
- New keys must be generated for ALL 32 languages