#!/usr/bin/env bash
# latex.sh — open an interactive shell in the latex service container (RUNS ON HOST).
# Starts the service first if it isn't running. Exits back to host on `exit`.
set -euo pipefail
cd "$(dirname "$0")/../.."
service="latex"
cid="$(docker compose ps -q "$service")"
if [ -z "$cid" ] || [ "$(docker inspect -f '{{.State.Running}}' "$cid")" != "true" ]; then
  docker compose up -d "$service"
fi
docker compose exec "$service" bash
