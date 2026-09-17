#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."

version="${1:-$(uv run python -c 'import tomllib; print(tomllib.load(open("pyproject.toml", "rb"))["project"]["version"])')}"
export PACKAGE_VERSION="$version"
uv run python -c 'import os, tomllib; p = tomllib.load(open("pyproject.toml", "rb"))["project"]; assert p["name"] == "volcano-sdk-python"; assert p["version"] == os.environ["PACKAGE_VERSION"]'

# Check the exact artifacts that will be uploaded, including sdist rebuilds.
artifacts=(dist/*)
test "${#artifacts[@]}" -eq 2
test -f "dist/volcano_sdk_python-$version-py3-none-any.whl"
test -f "dist/volcano_sdk_python-$version.tar.gz"
smoke_dir="$(mktemp -d)"
trap 'rm -rf "$smoke_dir"' EXIT
for artifact in "${artifacts[@]}"; do
  uv venv --clear "$smoke_dir/venv"
  uv pip install --python "$smoke_dir/venv/bin/python" "$artifact"
  "$smoke_dir/venv/bin/python" -I - <<'PY'
import os
from importlib.metadata import distribution
from volcano_sdk import VolcanoClient

package = distribution("volcano-sdk-python")
assert package.metadata["Name"] == "volcano-sdk-python"
assert package.version == os.environ["PACKAGE_VERSION"]
assert VolcanoClient
assert package.read_text("WHEEL")
print(f"Installed {package.metadata['Name']} {package.version}; volcano_sdk import OK")
PY
done
