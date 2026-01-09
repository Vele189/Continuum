# Use Python 3.12 slim image as base
FROM python:3.12-slim

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
RUN cat > /app/container-start.sh << 'EOF' && chmod +x /app/container-start.sh
#!/bin/bash
set -e
echo "Running database migrations..."
if [ -n "$DATABASE_URL" ]; then
  alembic upgrade head || echo "Warning: Migrations failed, continuing anyway..."
else
  echo "Warning: DATABASE_URL not set, skipping migrations"
fi
echo "Starting application server on port $PORT..."
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
EOF

# Start the application using the startup script
CMD ["/app/container-start.sh"]
