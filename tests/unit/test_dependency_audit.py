from __future__ import annotations

import os
import subprocess  # ruff: ignore[suspicious-subprocess-import] - fixed argv; no shell.
from pathlib import Path

import pytest

FAKE_UV = """#!/bin/sh
case "$1" in
  export)
    expected="export --locked --all-groups --all-extras --no-emit-project"
    expected="$expected --format requirements-txt"
    test "$*" = "$expected" || exit 99
    printf 'fixture==1.0 --hash=sha256:fixture\n'
    exit "$EXPORT_STATUS"
    ;;
  run)
    expected="run --frozen --no-sync python -I -m pip_audit --strict --disable-pip"
    expected="$expected --require-hashes --progress-spinner off"
    expected="$expected --requirement /dev/stdin"
    test "$*" = "$expected" || exit 98
    read -r requirement
    test "$requirement" = "fixture==1.0 --hash=sha256:fixture" || exit 97
    exit "$AUDIT_STATUS"
    ;;
  *) exit 96 ;;
esac
"""


@pytest.mark.parametrize(
    ("export_status", "audit_status", "expected"),
    [(0, 0, 0), (7, 0, 7), (0, 1, 1), (0, 9, 9)],
)
def test_audit_preserves_export_and_scanner_failures(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    export_status: int,
    audit_status: int,
    expected: int,
) -> None:
    executable = tmp_path / "uv"
    _ = executable.write_text(FAKE_UV)
    executable.chmod(0o700)
    monkeypatch.setenv("PATH", f"{tmp_path}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("EXPORT_STATUS", str(export_status))
    monkeypatch.setenv("AUDIT_STATUS", str(audit_status))
    result = subprocess.run(
        ["/bin/bash", "scripts/audit_dependencies.sh"],
        cwd=Path(__file__).parents[2],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == expected, result.stdout + result.stderr
