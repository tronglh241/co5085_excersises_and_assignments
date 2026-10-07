#!/usr/bin/env bash
# build.sh [texfile] — build a report PDF (default: reports/exercises.tex).
# RUN INSIDE the latex container shell (see ../shell/latex.sh).

set -euo pipefail
cd "$(dirname "$0")/../.."
texfile="${1:-reports/exercises.tex}"
latexmk -lualatex -shell-escape -silent -interaction=batchmode -cd "$texfile"
