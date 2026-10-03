#!/usr/bin/env bash
# build.sh — CI-equivalent gate, RUN INSIDE the container shell (see shell.sh).
# `jekyll build` only, no server/ports. Run before pushing;
# exit code is Jekyll's (0 = deploy-safe). For preview use serve.sh.

set -euo pipefail
cd "$(dirname "$0")/.."
cd docs && bundle exec jekyll build
