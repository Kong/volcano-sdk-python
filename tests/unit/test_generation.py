import os
import subprocess
import sys
from pathlib import Path
from runpy import run_path
from uuid import UUID

import httpx
import pytest

from volcano_sdk._generated.api.projects import get_project_logo
from volcano_sdk._generated.api.storage_objects import download_public_file
from volcano_sdk._generated.client import Client
from volcano_sdk._generated.types import File

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
        "get_project_log_activity.py",
        "get_project_lock.py",
        "invoke_function.py",
        "release_project_lock.py",
        "resolve_function_for_invocation.py",
        "search_project_logs.py",
        "renew_project_lock.py",
    }


@pytest.mark.parametrize(
    "content_type",
    ["image/png", "image/jpeg", "image/gif", "image/webp", "image/svg+xml"],
)
def test_generated_logo_response_preserves_bytes(content_type: str) -> None:
    payload = b"\x00\xff\x80binary response"
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(
            200, content=payload, headers={"Content-Type": content_type}
        )
    )
    with Client(
        base_url="https://api.test",
        httpx_args={"transport": transport},
        raise_on_unexpected_status=True,
    ) as client:
        response = get_project_logo.sync_detailed(UUID(int=1), client=client)

    assert response.content == payload
    assert response.headers["Content-Type"] == content_type
    assert isinstance(response.parsed, File)
    assert response.parsed.payload.read() == payload


@pytest.mark.parametrize(
    "content_type", ["application/octet-stream", "application/zip", "image/png"]
)
def test_generated_public_download_preserves_bytes(content_type: str) -> None:
    payload = b"\x00\xff\x80binary response"
    transport = httpx.MockTransport(
        lambda _request: httpx.Response(
            200, content=payload, headers={"Content-Type": content_type}
        )
    )
    with Client(
        base_url="https://api.test",
        httpx_args={"transport": transport},
        raise_on_unexpected_status=True,
    ) as client:
        response = download_public_file.sync_detailed(
            UUID(int=1), "assets", "file.bin", client=client
        )

    assert response.content == payload
    assert response.headers["Content-Type"] == content_type
    assert isinstance(response.parsed, File)
    assert response.parsed.payload.read() == payload


def test_generate_rejects_unsupported_response_warnings(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    spec = tmp_path / "unsupported.yaml"
    spec.write_text(
        """openapi: 3.0.3
info: {title: Unsupported, version: '1.0'}
paths:
  /binary:
    get:
      operationId: unsupportedBinary
      responses:
        '200':
          description: Binary response
          content:
            application/x-unsupported:
              schema: {type: string, format: binary}
""",
        encoding="utf-8",
    )
    script = run_path(str(ROOT / "scripts" / "generate_openapi.py"))
    generate = script["generate"]
    monkeypatch.setitem(generate.__globals__, "SPEC", spec)

    with pytest.raises(subprocess.CalledProcessError):
        generate(tmp_path / "_generated")


@pytest.mark.parametrize(
    "missing_operation",
    [
        "force_release_project_lock.py",
        "invoke_function.py",
        "search_project_logs.py",
        "update_storage_object_visibility.py",
    ],
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
