#!/bin/bash

# Navigate to the project root (one level up from this script)
cd "$(dirname "$0")/.."

echo "Starting Frontend Container..."
docker compose up -d --build frontend

echo "Frontend container started. Following logs (Ctrl+C to exit logs)..."
docker compose logs -f frontend
