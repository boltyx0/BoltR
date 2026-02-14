#!/bin/bash
# Restart web and proxy so the proxy re-resolves the web backend (avoids 502 after web restart).
# Run from project root: ./scripts/restart_web.sh

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

COMPOSE_FILE="docker/docker-compose.yml"
if command -v docker-compose &>/dev/null; then
  docker-compose -f "$PROJECT_ROOT/$COMPOSE_FILE" restart web proxy
elif docker compose version &>/dev/null; then
  docker compose -f "$PROJECT_ROOT/$COMPOSE_FILE" restart web proxy
else
  echo "Error: docker-compose or 'docker compose' required." >&2
  exit 1
fi
echo "Web and proxy restarted."
