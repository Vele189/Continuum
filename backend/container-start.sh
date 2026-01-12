#!/bin/bash
set -e

# Detect Python command (python3 on host, python in container)
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "Error: Python not found. Please install Python 3."
    exit 1
fi

echo "Running database migrations..."
if [ -n "$DATABASE_URL" ]; then
  $PYTHON_CMD -m alembic upgrade head || echo "Warning: Migrations failed, continuing anyway..."
else
  echo "Warning: DATABASE_URL not set, skipping migrations"
fi
echo "Starting application server on port ${PORT:-8000}..."
exec $PYTHON_CMD -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
