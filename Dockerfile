# Railway Dockerfile - builds from repo root
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements file first to leverage cache
COPY backend/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend application code
COPY backend/app ./app
COPY backend/alembic.ini ./alembic.ini
COPY backend/migrations ./migrations

# Default port (Railway will override with $PORT env var)
ENV PORT=8000

# Create a startup script that runs migrations then starts the server
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Running database migrations..."\n\
if [ -n "$DATABASE_URL" ]; then\n\
  alembic upgrade head || echo "Warning: Migrations failed, continuing anyway..."\n\
else\n\
  echo "Warning: DATABASE_URL not set, skipping migrations"\n\
fi\n\
echo "Starting application server on port $PORT..."\n\
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}\n\
' > /app/start.sh && chmod +x /app/start.sh

# Start the application using the startup script
CMD ["/app/start.sh"]
