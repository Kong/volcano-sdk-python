#!/usr/bin/env bash
# Run the full test suite against the built wheel as a new consumer installs it:
# runtime dependencies resolved from PyPI without uv.lock. See
# maintainers/dependency-ranges.md.
set -euo pipefail
cd "$(dirname "$0")/.."

package_dir="$1"
wheels=("$package_dir"/*.whl)
test "${#wheels[@]}" -eq 1
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
venv="$work/venv"
venv_python="$venv/bin/python"

uv venv --quiet "$venv"
# --refresh revalidates cached index pages so today's releases are candidates.
uv pip install --refresh --python "$venv_python" "${wheels[0]}[durable]"
uv pip list --quiet --python "$venv_python" --format freeze --exclude volcano-sdk-python > "$work/resolved.txt"

# Test tools come from uv.lock. Every package the wheel resolved is left out of
# that export and constrained to its fresh version instead.
no_emit=()
while IFS='=' read -r name _; do
  no_emit+=(--no-emit-package "$name")
done < "$work/resolved.txt"
uv export --quiet --locked --only-group dev --no-emit-project --no-hashes "${no_emit[@]}" > "$work/tools.txt"
uv pip install --python "$venv_python" --requirements "$work/tools.txt" --constraints "$work/resolved.txt"
uv pip list --quiet --python "$venv_python" --format freeze --exclude volcano-sdk-python > "$work/tested.txt"

report_status=0
python -m scripts.dependency_drift uv.lock "$work/resolved.txt" "$work/tested.txt" || report_status=$?

# The wheel omits the in-package tests. Put them beside the installed SDK so
# their imports resolve to it; tests/package/installed_sdk.py checks that.
site="$("$venv_python" -I -c 'import sysconfig; print(sysconfig.get_path("purelib"))')"
test ! -e "$site/volcano_sdk/_tests"
cp -R src/volcano_sdk/_tests "$site/volcano_sdk/_tests"
test_status=0
VIRTUAL_ENV="$venv" PATH="$venv/bin:$PATH" PYTHONPATH="$PWD/tests/package" \
  "$venv/bin/pytest" -c pyproject.toml -q -p installed_sdk || test_status=$?

if [[ $report_status -ne 0 || $test_status -ne 0 ]]; then
  exit 1
fi
