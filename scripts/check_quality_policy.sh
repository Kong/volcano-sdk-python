#!/usr/bin/env bash
set -euo pipefail

mkdir -p reports
git ls-files --cached --others --exclude-standard -z > reports/policy-tracked.bin
ruff check --show-files --config pyproject.toml . > reports/policy-ruff-files.txt
python -m scripts.check_quality_policy \
  reports/policy-tracked.bin reports/policy-ruff-files.txt
