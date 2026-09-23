#!/usr/bin/env bash
set -euo pipefail

git ls-files -z --cached --others --exclude-standard |
  python -m scripts.check_quality_policy
