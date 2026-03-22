# Nevumo Master Context

## Project Overview
Nevumo е уеб платформа за marketplace на услуги.
- Доставчици публикуват услуги
- Клиенти търсят и се свързват с доставчици
- Платформата е мултиезична (32 езика)
- Основен фокус: scalability, SEO, conversion

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
- Pydantic (validation)

### Database & Caching
- PostgreSQL (nevumo_leads)
- Redis (caching layer)

### Tracking
- Google Analytics 4 (GA4) — G-HKW6GBJJCK
- Custom DB events — page_events таблица + /api/v1/page-events endpoint
- Shared utility: lib/tracking.ts — trackPageEvent()

### Shared
- packages/ui (shared UI components)
- packages/typescript-config (shared TS config)

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

### Supported languages (32):
bg, cs, da, de, el, en, es, et, fi, fr, ga, hr, hu, it, lt, lv, mk, mt, nl, no, pl, pt, pt-PT, ro, sk, sl, sq, sr, sv, tr

- Default language: en

---

## Engineering Rules (CRITICAL)

- Никога не рефакторирай код извън текущата задача
- Никога не добавяй функционалност, която не е поискана
- Никога не модифицирай .env файлове
- Винаги спазвай текущата архитектура

### TypeScript
- Strict mode задължително
- Забранен any тип

### Python
- Type hints задължителни
- Използвай Pydantic за validation

### Financial Logic
- Използвай Decimal (Python)
- Никога float за пари

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