# Nevumo API

FastAPI backend for Nevumo platform.

## Environment Setup

### Python Path Standard

The API uses `PYTHONPATH` to ensure proper module imports. This is critical for scripts and the main application to resolve imports correctly.

#### Docker Environment
- `PYTHONPATH` is automatically set to `/app` in `docker-compose.yml`
- No manual configuration needed for containerized deployment

#### Local Development
- `run-local.sh` automatically exports `PYTHONPATH` to the `apps/api` directory
- When running scripts manually, always set:
  ```bash
  cd apps/api
  export PYTHONPATH=$(pwd)
  python your_script.py
  ```

## Running Scripts

### Using run-local.sh (Recommended)
```bash
./run-local.sh
```
This script handles:
- PYTHONPATH configuration
- Database migrations
- Starting API and web services

### Running Individual Scripts
```bash
cd apps/api
export PYTHONPATH=$(pwd)
python scripts/your_script.py
```

### Database Migrations
```bash
cd apps/api
export PYTHONPATH=$(pwd)
alembic upgrade head
```

## Development

### Install Dependencies
```bash
cd apps/api
pip install -r requirements.txt
```

### Run API Server
```bash
cd apps/api
export PYTHONPATH=$(pwd)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

- `main.py` - Application entry point
- `models.py` - Database models
- `schemas.py` - Pydantic schemas
- `routes/` - API endpoints
- `services/` - Business logic
- `scripts/` - Utility scripts
- `jobs/` - Background jobs
