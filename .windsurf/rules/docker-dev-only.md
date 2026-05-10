# Docker Development Only Rule

**Never run `npm run dev` or `next dev` locally on Mac.**
All dev servers run only in Docker containers.

**Troubleshooting black screen or ERR_CONNECTION_REFUSED:**
First check with:
```bash
lsof -i :3000 | grep -v OrbStack
```

If there's a result — kill the process with:
```bash
kill <PID>
```

**Only this!**
