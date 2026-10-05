#!/usr/bin/env python3
"""Generate the internal Python client from the bundled OpenAPI document."""

from __future__ import annotations

import argparse
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import] - fixed argv; no shell.
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "openapi" / "openapi.yaml"
CONFIG = ROOT / "openapi-python-client.yaml"
TEMPLATES = ROOT / "openapi" / "templates"
DEFAULT_OUTPUT = ROOT / "src" / "volcano_sdk" / "_generated"
REQUIRED_OPERATION_MODULES = {
    "acquire_project_lock.py",
    "auth_signin.py",
    "copy_storage_object.py",
    "delete_storage_object.py",
    "download_storage_object.py",
    "get_durable_execution.py",
    "force_release_project_lock.py",
    "get_project_log_activity.py",
    "get_project_lock.py",
    "invoke_function.py",
    "list_durable_executions.py",
    "list_storage_objects.py",
    "move_storage_object.py",
    "query_database_select.py",
    "release_project_lock.py",
    "renew_project_lock.py",
    "resolve_function_for_invocation.py",
    "search_project_logs.py",
    "start_durable_execution_from_application.py",
    "stop_durable_execution.py",
    "update_storage_object_visibility.py",
    "upload_storage_object.py",
}


def generate(output: Path) -> None:
    """Generate the OpenAPI client into ``output`` and validate required operations.

    Raises:
        RuntimeError: If the generated client omits a required operation.

    """
    if output.exists():
        shutil.rmtree(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    _ = subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true] - argv and executable are controlled by this script.
        [
            sys.executable,
            "-I",
            "-m",
            "openapi_python_client",
            "generate",
            "--path",
            str(SPEC),
            "--config",
            str(CONFIG),
            "--custom-template-path",
            str(TEMPLATES),
            "--meta",
            "none",
            "--output-path",
            str(output),
            "--overwrite",
            "--fail-on-warning",
        ],
        cwd=ROOT,
        check=True,
    )
    generated_operations = {path.name for path in (output / "api").rglob("*.py")}
    missing = REQUIRED_OPERATION_MODULES - generated_operations
    if missing:
        message = f"required OpenAPI operations were not generated: {sorted(missing)}"
        raise RuntimeError(message)


def main() -> None:
    """Parse command-line options and generate the internal client.

    Raises:
        TypeError: The output argument is not a path.

    """
    parser = argparse.ArgumentParser(description="Generate the internal OpenAPI client")
    _ = parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    output = cast("object", args.output)
    if not isinstance(output, Path):
        message = "--output must be a path"
        raise TypeError(message)
    generate(output.resolve())


if __name__ == "__main__":
    main()
