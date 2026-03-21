#!/bin/bash
set -e

echo "Starting Nevumo local development..."

if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
fi

echo "Starting PostgreSQL and Redis..."
docker compose up -d postgres redis

echo "Waiting for services..."
until docker compose exec postgres pg_isready -q 2>/dev/null; do sleep 1; done
echo "PostgreSQL ready"
until docker compose exec redis redis-cli ping -q 2>/dev/null; do sleep 1; done
echo "Redis ready"

echo "Running database migrations..."
cd apps/api
pip install -r requirements.txt -q
alembic upgrade head
cd ../..

echo "Starting API on port 8000..."
cd apps/api
uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!
cd ../..

echo "Starting frontend on port 3000..."
cd apps/web
npm install -q
npm run dev &
WEB_PID=$!
cd ../..

echo ""
echo "Nevumo is running!"
echo "   Frontend: http://localhost:3000"
echo "   API:      http://localhost:8000"
echo "   API docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

trap "kill $API_PID $WEB_PID 2>/dev/null; docker compose stop" EXIT
wait
