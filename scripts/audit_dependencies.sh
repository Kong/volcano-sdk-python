#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Audit the lock, including development tools and optional runtime dependencies.
# Local source packages have no upstream advisory record; the stub package's
# pinned durable-runtime dependency remains in the audited export.
uv export --locked --all-groups --all-extras --no-emit-project \
  --no-emit-package aws-durable-execution-sdk-python-stubs --format requirements-txt |
  uv run --frozen --no-sync python -I -m pip_audit \
    --strict --disable-pip --require-hashes --progress-spinner off --requirement /dev/stdin
