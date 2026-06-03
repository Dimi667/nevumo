---
name: backup-db
description: Archive the database from Docker container to external SSD
---

Create a gzip archive of the active PostgreSQL database from the Docker container and save it to the external SSD.

## Steps

1. Use pg_dump to export the database nevumo_leads from Docker container nevumo-postgres (user: nevumo)
2. Compress the dump with gzip
3. Save to external SSD: /Volumes/Transcend ESD310C 128GB/Nevumo_DB_Backups/
4. Use timestamp in filename: nevumo_leads_backup_YYYYMMDD_HHMMSS.sql.gz
5. Verify the archive was created and report: file name, location, and size

## Command to execute

```bash
docker exec nevumo-postgres pg_dump -U nevumo -d nevumo_leads | gzip > "/Volumes/Transcend ESD310C 128GB/Nevumo_DB_Backups/nevumo_leads_backup_$(date +%Y%m%d_%H%M%S).sql.gz"
```
