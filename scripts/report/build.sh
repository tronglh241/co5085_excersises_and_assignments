#!/usr/bin/env bash

set -euo pipefail
cd "$(dirname "$0")/../.."
texfile="${1:-reports/exercises.tex}"
latexmk -lualatex -shell-escape -silent -interaction=batchmode -cd "$texfile"
