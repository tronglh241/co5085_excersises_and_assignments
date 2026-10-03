#!/usr/bin/env bash
# tensorboard.sh [logdir] — TensorBoard, RUN INSIDE the container shell (see shell.sh).
# Open http://localhost:6006/ ; Ctrl-C stops.

set -euo pipefail
cd "$(dirname "$0")/.."
tensorboard --logdir "${1:-logs}" --host 0.0.0.0 --port 6006
