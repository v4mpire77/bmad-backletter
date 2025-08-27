#!/usr/bin/env bash
set -euo pipefail

: "${PORT:=8080}"
: "${NEXT_PORT:=3000}"
: "${API_PORT:=8000}"

# Render nginx config from template
envsubst '${PORT} ${NEXT_PORT} ${API_PORT}' < \
  /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Start FastAPI (Uvicorn). Use --app-dir since apps/ isn't a package.
uvicorn blackletter_api.main:app \
  --app-dir apps/api \
  --host 0.0.0.0 --port "${API_PORT}" --workers 2 &

# Start Next.js in production mode
npm run start --prefix apps/web -- --port "${NEXT_PORT}" --hostname 0.0.0.0 &

term_handler() {
  echo "Shutting down..."
  pkill -TERM -P $$ || true
  exit 0
}
trap term_handler SIGTERM SIGINT

# Start Nginx in foreground
nginx -g 'daemon off;' &
wait -n || true

