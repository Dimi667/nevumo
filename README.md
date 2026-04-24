# Nevumo

A multilingual services marketplace platform where providers publish services and clients discover and connect with them.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Monorepo | Turborepo |
| Frontend | Next.js 16, React 19, TypeScript 5, Tailwind CSS 4 |
| Backend | FastAPI, Python 3.13, SQLAlchemy, Pydantic |
| Database | PostgreSQL |
| Cache | Redis |
| Shared UI | packages/ui |
| i18n | 34 languages (default: `en`) |

## Monorepo Structure

The project is structured as a unified monorepo using **Turborepo**. This ensures a clean decoupling between the frontend and backend while maintaining a consistent development environment.

```
nevumo/
├── apps/
│   ├── web/          # Next.js frontend (port 3000)
│   ├── api/          # FastAPI backend (port 8000)
│   └── docs/         # Documentation app (Next.js)
├── packages/
│   ├── ui/                  # Shared React component library
│   ├── eslint-config/       # Shared ESLint configuration
│   └── typescript-config/   # Shared TypeScript configuration
├── docs/                    # Architectural & context documentation
├── docker-compose.yml       # Root orchestration for all services
├── turbo.json               # Turborepo configuration
└── package.json             # Root dependencies & scripts
```

### Path Logic & Environment
- **Unified Root**: All development and orchestration (Docker, Turborepo) happens from the root.
- **Backend Venv**: The virtual environment is strictly located at `apps/api/.venv`. All local execution should point to this path.
- **Decoupled Apps**: `apps/api` and `apps/web` are independent but share the same root context for Docker builds to resolve shared packages.

## Prerequisites

- Node.js >= 18
- npm >= 11
- Python 3.13
- Docker & Docker Compose (for PostgreSQL + Redis)

## Setup

### 1. Install dependencies

```sh
# Project is archived locally on external SSD (not on GitHub)
cd nevumo
npm install
```

### 2. Configure environment variables

```sh
cp .env.example .env
# Fill in your values in .env
```

### 3. Start services (PostgreSQL + Redis)

```sh
docker-compose up -d
```

### 4. Set up the Python backend

```sh
cd apps/api
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Run development servers

**All apps (from root):**

```sh
npm run dev
```

**Individual apps:**

```sh
# Frontend only
npm run dev --filter=web

# Backend only
cd apps/api && uvicorn apps.api.main:app --reload --port 8000
```

## Docker & Containerization

The project uses a centralized Docker Compose orchestration from the root.

### Optimized Dockerfiles
We use multi-stage builds to:
- Reduce final image size.
- Improve build speed via layer caching.
- Ensure production-ready security.

### Orchestration
The root `docker-compose.yml` manages:
- **nevumo-api**: FastAPI backend.
- **nevumo-web**: Next.js frontend.
- **nevumo-postgres**: PostgreSQL database.
- **nevumo-redis**: Redis cache.

### Local Development (Hot-Reload)
Volumes are mapped from the root to the `/workspace` directory inside containers. This ensures that changes made locally are immediately reflected inside the containers (Hot-Reloading).

```sh
docker-compose up -d
```

## Local Development with OrbStack

For optimal performance on macOS, this project uses **OrbStack** instead of Docker Desktop. OrbStack provides significantly faster container startup and better resource utilization.

### Prerequisites
- OrbStack installed (recommended for macOS development)
- Docker context set to `orbstack`

### Starting the Project

```sh
# Ensure OrbStack context is active
docker context use orbstack

# Start all services
docker compose up -d

# Check container status
docker compose ps
```

### Important Notes

**Next.js 16 Routing**: This project uses `proxy.ts` instead of `middleware.ts` to comply with Next.js 16 requirements.

**Alembic Migration Status:** The database currently has multiple Alembic head revisions. When creating new migrations, you may encounter a "Multiple head revisions" error. To resolve this, you'll need to merge the heads before proceeding with new schema changes:

```sh
docker compose exec api alembic merge heads -m "merge migration"
docker compose exec api alembic upgrade head
```

### Local URLs

| Service | URL |
|---------|-----|
| Web (frontend) | http://localhost:3000 |
| API (FastAPI) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |

## Common Commands (Cheat Sheet)

### Database & Migrations
| Task | Command |
|------|---------|
| **Run Migrations** | `docker exec -it nevumo-api alembic upgrade head` |
| **Generate Migration** | `docker exec -it nevumo-api alembic revision --autogenerate -m "description"` |
| **Access DB Shell** | `docker exec -it nevumo-postgres psql -U nevumo -d nevumo_leads` |

### Cache Management
| Task | Command |
|------|---------|
| **Clear Redis Cache** | `docker exec nevumo-redis redis-cli FLUSHALL` |
| **Flush translation cache** | `docker exec nevumo-redis redis-cli KEYS "translations:*" | xargs docker exec -i nevumo-redis redis-cli DEL` |

### Backend Development
| Task | Command |
|------|---------|
| **Activate Venv** | `source apps/api/.venv/bin/activate` |
| **Run API Locally** | `python -m apps.api.main` (from root) |
| **Run Scripts** | `python -m apps.api.scripts.seed_ui_translations` |

### Frontend Development
| Task | Command |
|------|---------|
| **Next.js Logs** | `docker logs -f nevumo-web` |

## Supported Languages

`bg` `cs` `da` `de` `el` `en` `es` `et` `fi` `fr` `ga` `hr` `hu` `is` `it` `lb` `lt` `lv` `mk` `mt` `nl` `no` `pl` `pt` `pt-PT` `ro` `ru` `sk` `sl` `sq` `sr` `sv` `tr` `uk`

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start all apps in development mode |
| `npm run build` | Build all apps |
| `npm run lint` | Lint all packages |
| `npm run check-types` | TypeScript type checking |
| `npm run format` | Format code with Prettier |

## URLs

| Service | URL |
|---------|-----|
| Web (frontend) | http://localhost:3000 |
| API (FastAPI) | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
