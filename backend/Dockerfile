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

# Start the uvicorn server
# --host 0.0.0.0 is needed to expose the server to the network
# Note: Using shell form to allow $PORT variable expansion
CMD bash -c "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
