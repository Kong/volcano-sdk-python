#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo 'usage: build-acceptance.sh sdk.whl output-directory' >&2; exit 1; fi
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
artifact="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
mkdir -p "$2"
output="$(cd "$2" && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
cp "$repo_dir/acceptance/pyproject.toml" "$work/"
cp "$artifact" "$work/"
cp -R "$repo_dir/features" "$work/"
mkdir -p "$work/tests/package" "$work/docs" "$work/scripts"
cp "$repo_dir/tests/package/quickstart.py" "$work/tests/package/"
cp "$repo_dir/docs/README.md" "$work/docs/"
cp "$repo_dir/scripts/smoke-wheel.sh" "$work/scripts/"
cd "$work"
uv add --no-sync "./$(basename "$artifact")"
uv sync --frozen
uv run --no-sync python -I - "$(basename "$artifact")" <<'PYTHON'
import hashlib, json, sys
from importlib.metadata import distribution
from pathlib import Path
import volcano_sdk
package = distribution("volcano-sdk-python")
assert Path(volcano_sdk.__file__).resolve().is_relative_to(Path.cwd() / ".venv")
artifact = Path(sys.argv[1])
Path("acceptance.json").write_text(json.dumps({"schema": 1, "language": "python", "package": "volcano-sdk-python", "version": package.version, "filename": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}, indent=2))
PYTHON
bash scripts/smoke-wheel.sh "$(basename "$artifact")"
rm -rf .venv "$(basename "$artifact")"
tar -czf "$output/sdk-acceptance.tar.gz" .
