#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL is required. In Jenkins, add it as a Secret text credential."
  exit 1
fi

cat > backend/.env <<EOF
SECRET_KEY=${SECRET_KEY:-change-me-in-jenkins}
JWT_SECRET_KEY=${JWT_SECRET_KEY:-change-me-too-in-jenkins}
DATABASE_URL=${DATABASE_URL}
FLASK_DEBUG=false
EOF

docker compose down --remove-orphans
docker compose build --pull
docker compose up -d

echo "Waiting for backend health check..."
for attempt in $(seq 1 30); do
  if curl -fsS http://localhost:5000/api/health >/dev/null; then
    echo "Backend is healthy."
    exit 0
  fi
  sleep 2
done

echo "Backend did not become healthy in time."
docker compose logs --tail=80 backend
exit 1
