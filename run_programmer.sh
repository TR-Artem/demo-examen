#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
export DEMOEXAM_COURSE=programmer
exec ./run.sh programmer
