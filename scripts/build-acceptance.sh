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
uv add --no-sync --no-build "./$(basename "$artifact")"
python3 - "$(basename "$artifact")" <<'PYTHON'
import email, hashlib, json, sys, zipfile
from pathlib import Path
artifact = Path(sys.argv[1])
with zipfile.ZipFile(artifact) as wheel:
    names = [name for name in wheel.namelist() if name.endswith(".dist-info/METADATA")]
    assert len(names) == 1
    metadata = email.message_from_bytes(wheel.read(names[0]))
assert metadata["Name"] == "volcano-sdk-python"
Path("acceptance.json").write_text(json.dumps({"schema": 1, "language": "python", "package": metadata["Name"], "version": metadata["Version"], "filename": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest()}, indent=2))
PYTHON
rm "$(basename "$artifact")"
tar -czf "$output/sdk-acceptance.tar.gz" .
