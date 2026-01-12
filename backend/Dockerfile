# Use Python 3.12 slim image as base
FROM python:3.12-slim

# Install git and Node.js (required for pre-commit and frontend checks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Default port (Railway will override with $PORT env var)
ENV PORT=8000

# Create a startup script that runs migrations then starts the server
# This script runs INSIDE the container, not on the host
# Note: The local container-start.sh will be used when volume is mounted
RUN cat > /app/container-start.sh << 'EOF' && chmod +x /app/container-start.sh
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
EOF

# Start the application using the startup script
CMD ["/app/container-start.sh"]
