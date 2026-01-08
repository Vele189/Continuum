#!/bin/bash

# Navigate to the project root (one level up from this script)
cd "$(dirname "$0")/.."

echo "Starting Backend Container..."
docker compose up -d --build backend db mailpit

echo "Backend container started. Following logs (Ctrl+C to exit logs)..."
docker compose logs -f backend
