# Incident Logs

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
