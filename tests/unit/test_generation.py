import os
import sys
from pathlib import Path
from runpy import run_path

ROOT = Path(__file__).resolve().parents[2]


def test_generate_emits_all_six_contract_operations(tmp_path: Path) -> None:
    script = run_path(str(ROOT / "scripts" / "generate_openapi.py"))
    generate = script["generate"]
    output = tmp_path / "_generated"

    generate(output)

    assert {path.name for path in (output / "api").rglob("*.py")} >= {
        "auth_signin.py",
        "query_database_select.py",
        "upload_storage_object.py",
        "download_storage_object.py",
        "acquire_project_lock.py",
        "release_project_lock.py",
    }


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
