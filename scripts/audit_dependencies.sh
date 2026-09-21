#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Audit the lock, including development tools and optional runtime dependencies.
# Exclude only this project's editable entry, which has no upstream advisory record.
uv export --locked --all-groups --all-extras --no-emit-project --format requirements-txt |
  uv run --frozen --no-sync python -m pip_audit \
    --strict --disable-pip --require-hashes --progress-spinner off --requirement /dev/stdin
