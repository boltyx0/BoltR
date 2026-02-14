#!/usr/bin/env bash
# BoltR toolchain integrity check
# Run after 'make up' when all containers are healthy.
# Usage: ./scripts/health_check.sh   (from project root, or cd to project root)

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Load .env for COMPOSE_PROJECT_NAME
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi
PROJECT="${COMPOSE_PROJECT_NAME:-rengine}"
CELERY_CONTAINER="${PROJECT}-celery-1"

echo "=== BoltR Toolchain Health Check ==="
echo "Celery container: $CELERY_CONTAINER"
echo ""

if ! docker ps --format '{{.Names}}' | grep -qx "$CELERY_CONTAINER"; then
  echo "Error: Celery container '$CELERY_CONTAINER' is not running."
  echo "Start BoltR first: make up"
  exit 1
fi

check_tool() {
  local name="$1"
  local cmd="$2"
  if docker exec "$CELERY_CONTAINER" sh -c "command -v $name >/dev/null 2>&1 && $cmd" 2>/dev/null; then
    echo "[OK] $name"
    return 0
  else
    echo "[FAIL] $name (not found or error)"
    return 1
  fi
}

FAIL=0

# Core recon tools (version or help)
check_tool "nuclei" "nuclei -version" || FAIL=1
check_tool "naabu" "naabu -version" || FAIL=1
check_tool "subfinder" "subfinder -version" || FAIL=1
check_tool "amass" "amass -version" || FAIL=1
check_tool "httpx" "httpx -version" || FAIL=1

echo ""
if [ $FAIL -eq 0 ]; then
  echo "Result: All core tools are present and executable."
  exit 0
else
  echo "Result: One or more tools failed. Check container: docker exec -it $CELERY_CONTAINER bash"
  exit 1
fi
