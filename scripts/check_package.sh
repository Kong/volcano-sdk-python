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
uvx --from twine==7.0.0 twine check --strict "${artifacts[@]}"
smoke_dir="$(mktemp -d)"
trap 'rm -rf "$smoke_dir"' EXIT
typechecker="$(uv run python -c 'import shutil; print(shutil.which("mypy"))')"
cat > "$smoke_dir/mypy.ini" <<'INI'
[mypy]
strict = True
INI
cat > "$smoke_dir/consumer.py" <<'PY'
from typing import assert_type
from volcano_sdk import Session, User, VolcanoClient

client = VolcanoClient(anon_key="example", access_token="supplied-access")
assert_type(client.auth.get_session(), Session | None)
session = client.auth.get_session()
if session is not None:
    assert_type(session.refresh_token, str | None)
    assert_type(session.user_id, str | None)
assert_type(client.auth.get_user(), User)
assert_type(client.storage.from_("assets").download("hello.txt"), bytes)
PY
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
  (
    cd "$smoke_dir"
    unset MYPYPATH
    "$typechecker" --no-incremental --python-executable "$smoke_dir/venv/bin/python" consumer.py
    cp consumer.py invalid.py
    echo 'client.auth.sign_in(email=42, password="example")' >> invalid.py
    echo 'VolcanoClient(anon_key="example", access_token=42)' >> invalid.py
    if "$typechecker" --no-incremental --python-executable "$smoke_dir/venv/bin/python" invalid.py > typing-error.log 2>&1; then
      echo "Installed SDK did not reject an invalid argument type" >&2
      exit 1
    fi
    grep -q '\[arg-type\]' typing-error.log
  )
done
