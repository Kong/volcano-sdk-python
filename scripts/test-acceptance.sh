#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo 'usage: test-acceptance.sh package-file sdk-acceptance.tar.gz' >&2; exit 1; fi
artifact="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
bundle="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
tar -xzf "$bundle" -C "$work"
cd "$work"
cp "$artifact" .
python3 -c 'import hashlib,json,pathlib; a=json.loads(pathlib.Path("acceptance.json").read_text()); assert hashlib.sha256(pathlib.Path(a["filename"]).read_bytes()).hexdigest()==a["sha256"], "Package differs from acceptance bundle"'
uv sync --frozen --no-build
uv run --no-sync python -I -c 'from pathlib import Path; import volcano_sdk; assert Path(volcano_sdk.__file__).resolve().is_relative_to(Path.cwd()/".venv")'
bash scripts/smoke-wheel.sh "$(basename "$artifact")"
