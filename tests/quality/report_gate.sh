#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/../.." && pwd)"
fixture_dir="$(mktemp -d)"
trap 'rm -rf "$fixture_dir"' EXIT
printf '#!/bin/sh\nexit 0\n' > "$fixture_dir/pytest"
printf '#!/bin/sh\nexit 0\n' > "$fixture_dir/uv"
chmod +x "$fixture_dir/pytest" "$fixture_dir/uv"
cd "$fixture_dir"
mkdir reports
printf 'stale' > reports/unit.xml
printf 'stale' > reports/coverage.json

for task in test coverage; do
  shell_command="$(python3 - "$repo_dir/pyproject.toml" "$task" <<'PY'
import sys
import tomllib

with open(sys.argv[1], "rb") as source:
    print(tomllib.load(source)["tool"]["poe"]["tasks"][sys.argv[2]]["shell"])
PY
)"
  if PATH="$fixture_dir:$PATH" /bin/bash -c "$shell_command"; then
    echo "Reportless $task task unexpectedly succeeded" >&2
    exit 1
  fi
  test "$(cat reports/unit.xml)" = stale
  test "$(cat reports/coverage.json)" = stale
done
