import os
import subprocess
import sys
from pathlib import Path
from runpy import run_path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_generate_emits_required_contract_operations(tmp_path: Path) -> None:
    script = run_path(str(ROOT / "scripts" / "generate_openapi.py"))
    generate = script["generate"]
    output = tmp_path / "_generated"

    generate(output)

    assert {path.name for path in (output / "api").rglob("*.py")} >= {
        "auth_signin.py",
        "copy_storage_object.py",
        "query_database_select.py",
        "upload_storage_object.py",
        "download_storage_object.py",
        "delete_storage_object.py",
        "list_storage_objects.py",
        "move_storage_object.py",
        "update_storage_object_visibility.py",
        "acquire_project_lock.py",
        "force_release_project_lock.py",
        "get_project_lock.py",
        "release_project_lock.py",
        "renew_project_lock.py",
    }


@pytest.mark.parametrize(
    "missing_operation",
    ["force_release_project_lock.py", "update_storage_object_visibility.py"],
)
def test_generate_rejects_a_missing_required_operation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    missing_operation: str,
) -> None:
    script = run_path(str(ROOT / "scripts" / "generate_openapi.py"))
    generate = script["generate"]
    output = tmp_path / "_generated"

    def generate_without_required_operation(
        *_args: object,
        **_kwargs: object,
    ) -> None:
        operations = output / "api" / "storage_objects"
        operations.mkdir(parents=True)
        for name in script["REQUIRED_OPERATION_MODULES"]:
            if name != missing_operation:
                (operations / name).touch()

    monkeypatch.setattr(subprocess, "run", generate_without_required_operation)

    with pytest.raises(RuntimeError, match=missing_operation.replace(".", r"\.")):
        generate(output)


def test_generated_comparison_reads_file_bytes(
    tmp_path: Path,
) -> None:
    scripts_path = str(ROOT / "scripts")
    sys.path.insert(0, scripts_path)
    try:
        script = run_path(str(ROOT / "scripts" / "check_openapi.py"))
    finally:
        sys.path.remove(scripts_path)
    compared_files = script["compared_files"]
    expected = tmp_path / "expected"
    actual = tmp_path / "actual"
    expected.mkdir()
    actual.mkdir()
    (expected / "client.py").write_text("first\n", encoding="utf-8")
    (actual / "client.py").write_text("other\n", encoding="utf-8")
    timestamp = 1_800_000_000
    os.utime(expected / "client.py", (timestamp, timestamp))
    os.utime(actual / "client.py", (timestamp, timestamp))

    missing, extra, changed = compared_files(expected, actual)

    assert missing == []
    assert extra == []
    assert changed == ["client.py"]


def test_generated_comparison_ignores_runtime_bytecode(tmp_path: Path) -> None:
    script = run_path(str(ROOT / "scripts" / "check_openapi.py"))
    compared_files = script["compared_files"]
    expected = tmp_path / "expected"
    actual = tmp_path / "actual"
    (expected / "__pycache__").mkdir(parents=True)
    actual.mkdir()
    (expected / "client.py").write_text("source\n", encoding="utf-8")
    (actual / "client.py").write_text("source\n", encoding="utf-8")
    (expected / "__pycache__" / "client.pyc").write_bytes(b"runtime cache")

    assert compared_files(expected, actual) == ([], [], [])
