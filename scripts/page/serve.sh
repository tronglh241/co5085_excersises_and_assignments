#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/../.."

# Gems live in the container layer: reinstall if a recreate wiped them
cd docs && (bundle check || bundle install)
bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload
