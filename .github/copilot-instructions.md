## Project: Nevumo (my-monorepo)

### Architecture
- Turborepo monorepo with three apps: web, api, docs
- Frontend: Next.js 16 + React 19 + TypeScript 5 (apps/web)
- Backend: FastAPI + Python (apps/api)
- Database: PostgreSQL (nevumo_leads) + Redis (caching)
- Styling: Tailwind CSS 4 + PostCSS
- ORM: SQLAlchemy | Validation: Pydantic
- Shared UI: packages/ui | Shared types: packages/typescript-config

### Folder Conventions
- New frontend components → packages/ui or apps/web/components
- New API endpoints → apps/api (follow existing FastAPI router structure)
- Shared TypeScript types → packages/typescript-config
- Never put business logic in UI components

### Code Conventions
- TypeScript: strict mode, no `any` types
- Python: type hints required on all functions
- All Pydantic models must have field validation
- SQLAlchemy: never use raw SQL unless in migration files
- CSS: Tailwind utility classes only, no inline styles

### Financial Data Rules
- Never use floating-point for monetary/percentage calculations
- Use Decimal (Python) or number formatting utilities (TS) for financial values
- All financial calculations must have unit tests

### Database Rules
- Never modify schema without showing migration plan first
- All new tables need created_at, updated_at timestamps
- Never run DROP or DELETE without explicit confirmation

### Monorepo Rules
- Run builds/tests from root with Turbo, not from individual apps
- New dependencies: show package name and ask before installing
- Keep apps/web and apps/api dependencies separate — no cross-app imports

### Key Files (always consider these)
- apps/api/main.py - FastAPI entry point
- apps/web/package.json - Frontend dependencies  
- docker-compose.yml - Services configuration
- packages/ui/ - Shared UI components

### Runtime Versions
- Python: 3.13.12
- Node.js: 25.8.0
- API base URL: /api/v1

### Do NOT
- Refactor code not related to the current task
- Add features not explicitly requested
- Modify .env files
- Commit node_modules or .turbo cache

### Internationalization (i18n)
- 32 supported languages (see i18n.py for full list)
- Default language: en
- Translations stored in PostgreSQL, cached in Redis
- When adding new translation keys: generate for ALL 32 languages
- After translation changes: invalidate Redis cache for affected languages