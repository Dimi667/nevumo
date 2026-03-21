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
| i18n | 32 languages (default: `en`) |

## Monorepo Structure

```
nevumo/
├── apps/
│   ├── web/          # Next.js frontend (port 3000)
│   ├── api/          # FastAPI backend (port 8000)
│   └── docs/         # Next.js docs app
├── packages/
│   ├── ui/                  # Shared React component library
│   ├── eslint-config/       # Shared ESLint config
│   └── typescript-config/   # Shared tsconfig
├── docs/                    # Architecture & context docs
├── docker-compose.yml       # PostgreSQL + Redis
├── turbo.json
└── package.json
```

## Prerequisites

- Node.js >= 18
- npm >= 11
- Python 3.13
- Docker & Docker Compose (for PostgreSQL + Redis)

## Setup

### 1. Clone & install dependencies

```sh
git clone https://github.com/dimitardimitrov/nevumo.git
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
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
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
cd apps/api && uvicorn main:app --reload --port 8000
```

## Supported Languages

`bg` `cs` `da` `de` `el` `en` `es` `et` `fi` `fr` `ga` `hr` `hu` `it` `lt` `lv` `mk` `mt` `nl` `no` `pl` `pt` `pt-PT` `ro` `sk` `sl` `sq` `sr` `sv` `tr`

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
