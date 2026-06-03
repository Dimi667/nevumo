## Docker Rebuild правило
- При всеки rebuild на Docker image ЗАДЪЛЖИТЕЛНО:
  docker compose down && docker volume rm nevumo_web_node_modules && docker compose up -d
- НИКОГА само `docker compose build` + `up` без да изчистиш volume-а
- НИКОГА `npm run dev` или `next dev` локално на Mac-а
- Всички dev сървъри вървят само в Docker/OrbStack
