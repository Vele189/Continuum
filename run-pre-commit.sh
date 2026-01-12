#!/bin/bash
# Wrapper script to run pre-commit via Docker

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$REPO_ROOT"

docker compose run --rm \
    -v "$REPO_ROOT/.git:/app/.git:rw" \
    -v "$REPO_ROOT:/app:rw" \
    -w /app \
    -e SKIP=no-commit-to-branch \
    backend sh -c "git config --global --add safe.directory /app && pre-commit \"\$@\"" -- "$@"
