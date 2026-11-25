#!/usr/bin/env bash
# Запуск тренажёра:
#   ./run.sh              — веб-квалификация (09.02.07-3)
#   ./run.sh programmer   — «Программист» (09.02.07-2)
set -e
cd "$(dirname "$0")"

COURSE="${1:-web}"
export DEMOEXAM_COURSE="$COURSE"

if command -v python3 >/dev/null 2>&1; then
  exec python3 trainer.py
else
  exec python trainer.py
fi
