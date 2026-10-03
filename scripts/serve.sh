#!/usr/bin/env bash
# serve.sh — daily preview loop, RUN INSIDE the container shell (see shell.sh).
# Builds first, then serves with watch + livereload.
# Open http://localhost:4000/co5085_excersises_and_assignments/ ; Ctrl-C stops cleanly.

set -euo pipefail
cd "$(dirname "$0")/.."

# Gems live in the container layer: reinstall if a recreate wiped them
cd docs && (bundle check || bundle install)
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload
