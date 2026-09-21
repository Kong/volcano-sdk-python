#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 1 ]; then echo 'usage: smoke-wheel.sh sdk.whl' >&2; exit 1; fi
artifact="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
uv venv "$work/venv"
uv pip install --python "$work/venv/bin/python" --only-binary :all: "$artifact"
cd "$work"
env -i PATH="$PATH" HOME="$work" "$work/venv/bin/python" -I "$repo_dir/tests/package/quickstart.py"
