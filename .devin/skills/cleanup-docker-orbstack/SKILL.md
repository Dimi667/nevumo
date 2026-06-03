---
name: cleanup-docker-orbstack
description: Clean Docker system in OrbStack to free disk space
---

Изпълни пълно почистване на Docker системата в OrbStack, за да освободиш дисково пространство.

## Steps

1. Изпълни `docker system prune -a --volumes -f`. Това ще изтрие всички спрени контейнери, неизползвани мрежи, "висящи" изображения и неизползвани обеми (volumes).
2. Изчисти кеша на build-системата с `docker builder prune -f`.
3. След почистването, изпълни `df -h`, за да видим колко свободно място има на диска в момента.
4. Провери статуса на контейнерите за Nevumo (nevumo-api, nevumo-web, nevumo-postgres, nevumo-redis), за да се увериш, че всичко необходимо работи коректно.

## Important

Не променяй никакви конфигурационни файлове или код по проекта по време на този процес!
