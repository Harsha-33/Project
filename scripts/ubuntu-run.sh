#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT_DIR/backend/.env"
ENV_EXAMPLE="$ROOT_DIR/backend/.env.example"

cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Install Docker Engine and Docker Compose plugin first."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin is not available. Install docker-compose-plugin first."
  exit 1
fi

if [ ! -f "$ENV_FILE" ]; then
  cp "$ENV_EXAMPLE" "$ENV_FILE"
  cat <<MSG
Created backend/.env from backend/.env.example.
Edit backend/.env and set DATABASE_URL before starting the app.
Remember to URL-encode special characters in the password, for example # becomes %23.
MSG
  exit 1
fi

docker compose up --build -d

echo "WeCareForYou is starting..."
echo "Frontend: http://localhost:4200"
echo "Backend health: http://localhost:5000/api/health"
