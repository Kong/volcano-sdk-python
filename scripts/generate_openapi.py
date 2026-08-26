#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "openapi" / "openapi.yaml"
CONFIG = ROOT / "openapi-python-client.yaml"
DEFAULT_OUTPUT = ROOT / "src" / "volcano_sdk" / "_generated"
REQUIRED_OPERATION_MODULES = {
    "acquire_project_lock.py",
    "auth_signin.py",
    "download_storage_object.py",
    "query_database_select.py",
    "release_project_lock.py",
    "upload_storage_object.py",
}


def generate(output: Path) -> None:
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            sys.executable,
            "-m",
            "openapi_python_client",
            "generate",
            "--path",
            str(SPEC),
            "--config",
            str(CONFIG),
            "--meta",
            "none",
            "--output-path",
            str(output),
            "--overwrite",
        ],
        cwd=ROOT,
        check=True,
    )
    generated_operations = {path.name for path in (output / "api").rglob("*.py")}
    missing = REQUIRED_OPERATION_MODULES - generated_operations
    if missing:
        raise RuntimeError(f"required OpenAPI operations were not generated: {sorted(missing)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the internal OpenAPI client")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    generate(args.output.resolve())


if __name__ == "__main__":
    main()
