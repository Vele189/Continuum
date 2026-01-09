#!/bin/bash
set -e
echo "Running database migrations..."
if [ -n "$DATABASE_URL" ]; then
  python -m alembic upgrade head || echo "Warning: Migrations failed, continuing anyway..."
else
  echo "Warning: DATABASE_URL not set, skipping migrations"
fi
echo "Starting application server on port ${PORT:-8000}..."
exec python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
