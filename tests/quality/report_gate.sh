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

for mode in reportless failing; do
  if [[ $mode == failing ]]; then
    for executable in pytest uv; do
      cat > "$fixture_dir/$executable" <<'SH'
#!/bin/sh
for argument do
  case "$argument" in
    --junitxml=*) printf 'fresh' > "${argument#--junitxml=}" ;;
    --cov-report=json:*) printf 'fresh' > "${argument#--cov-report=json:}" ;;
  esac
done
exit 7
SH
    done
  fi
  for task in test coverage; do
    shell_command="$(python3 - "$repo_dir/pyproject.toml" "$task" <<'PY'
import sys
import tomllib

with open(sys.argv[1], "rb") as source:
    print(tomllib.load(source)["tool"]["poe"]["tasks"][sys.argv[2]]["shell"])
PY
)"
    if PATH="$fixture_dir:$PATH" /bin/bash -c "$shell_command"; then
      echo "$mode $task task unexpectedly succeeded" >&2
      exit 1
    else
      status=$?
    fi
    if [[ $mode == reportless ]]; then
      test "$status" -eq 1
      test "$(cat reports/unit.xml)" = stale
      test "$(cat reports/coverage.json)" = stale
    else
      test "$status" -eq 7
      test "$(cat reports/unit.xml)" = fresh
      if [[ $task == coverage ]]; then
        test "$(cat reports/coverage.json)" = fresh
        test "$(cat reports/coverage-unit.xml)" = fresh
      fi
    fi
  done
done
