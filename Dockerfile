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

# Default port (Railway will override with $PORT env var)
ENV PORT=8000

# Start the uvicorn server
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

