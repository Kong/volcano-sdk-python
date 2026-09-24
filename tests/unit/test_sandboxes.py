from __future__ import annotations

import base64
import binascii
import json
from collections import deque
from typing import TYPE_CHECKING, cast
from uuid import UUID, uuid4

import httpx
import pytest

from volcano_sdk import (
    AuthenticationError,
    ConflictError,
    RateLimitedError,
    SandboxCommandResult,
    Sandboxes,
    SandboxSession,
    Session,
    TransportError,
    ValidationError,
    VolcanoClient,
)
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Mapping

    from volcano_sdk.sandbox_models import SandboxExecOptions

PROJECT = "00000000-0000-4000-8000-000000000001"
SESSION = "00000000-0000-4000-8000-000000000002"
SUBJECT = "00000000-0000-4000-8000-000000000003"
KEY = "00000000-0000-4000-8000-000000000004"


def session_body(state: str = "running") -> dict[str, object]:
    return {
        "id": SESSION,
        "project_id": PROJECT,
        "region": "aws-us-east-1",
        "state": state,
        "expires_at": "2026-09-25T00:00:00Z",
    }


def command_body() -> dict[str, object]:
    return {
        "stdout": "hello",
        "stderr": "err",
        "exit_code": 7,
        "timed_out": False,
        "stdout_truncated": False,
        "stderr_truncated": True,
    }


class SandboxHTTP:
    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.responses: deque[httpx.Response] = deque()
        self.failure: Exception | None = None
        self.client = VolcanoClient(
            anon_key="anon",
            service_key="service",
            _transport=GeneratedTransport(
                api_url="https://sandbox.test",
                httpx_transport=httpx.MockTransport(self.handle),
            ),
        )

    def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        if self.failure is not None:
            raise self.failure
        return self.responses.popleft()

    def reply(
        self,
        payload: object = None,
        status: int = 200,
        headers: Mapping[str, str] | None = None,
    ) -> None:
        self.responses.append(httpx.Response(status, json=payload, headers=headers))


def test_sandbox_selectors_and_mutation_identity() -> None:
    server = SandboxHTTP()
    assert isinstance(server.client.sandboxes, Sandboxes)
    for _ in range(2):
        server.reply(session_body(), 201)
        session = server.client.sandboxes.create(
            PROJECT,
            region="aws-us-east-1",
            sandbox_id=SUBJECT,
            request_id=KEY,
            max_duration_seconds=300,
            idle_timeout_seconds=30,
        )
        assert session.id == SESSION
    first, second = server.requests
    assert first.headers["Idempotency-Key"] == second.headers["Idempotency-Key"] == KEY
    assert first.headers["Authorization"] == "Bearer service"
    assert first.url.path == f"/projects/{PROJECT}/sandbox-sessions"
    assert json.loads(first.content) == {
        "sandbox_id": SUBJECT,
        "region": "aws-us-east-1",
        "max_duration_seconds": 300,
        "idle_timeout_seconds": 30,
    }
    assert first.extensions["timeout"]["read"] >= 180


def test_sandbox_one_shot_and_session_execution() -> None:
    server = SandboxHTTP()
    server.reply(
        command_body()
        | {"session_id": SESSION, "region": "aws-us-east-1", "duration_ms": 42}
    )
    result = server.client.sandboxes.exec(
        PROJECT,
        "exit 7",
        preset="python3.12",
        region="aws-us-east-1",
        memory_mb=2048,
        environment={"X": "value"},
        timeout_seconds=30,
    )
    assert result.exit_code == 7
    assert result.stderr_truncated
    assert result.session_id == SESSION
    assert result.duration_ms == 42
    assert (
        str(UUID(server.requests[0].headers["Idempotency-Key"]))
        == server.requests[0].headers["Idempotency-Key"]
    )
    assert json.loads(server.requests[0].content) == {
        "region": "aws-us-east-1",
        "preset": "python3.12",
        "command": "exit 7",
        "memory_mb": 2048,
        "environment": {"X": "value"},
        "timeout_seconds": 30,
    }
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    server.reply(command_body())
    command = session.exec("exit 7", request_id=KEY, timeout_seconds=3600)
    assert command == SandboxCommandResult(
        "hello",
        "err",
        7,
        timed_out=False,
        stdout_truncated=False,
        stderr_truncated=True,
    )
    assert server.requests[-1].extensions["timeout"]["read"] == 3720
    assert server.requests[-1].headers["Idempotency-Key"] == KEY


def test_sandbox_lifecycle_files_access_and_grants() -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    for operation, state in [
        (session.suspend, "suspending"),
        (session.resume, "resuming"),
        (session.terminate, "terminating"),
    ]:
        server.reply(session_body(state), 202)
        assert operation() is session
        assert session.state == state
    server.reply(session_body("running"))
    assert session.refresh().state == "running"
    data = bytes(range(256))
    server.reply(status=204)
    session.files.write("/workspace/data", data)
    assert (
        json.loads(server.requests[-1].content)["data"]
        == base64.b64encode(data).decode()
    )
    server.reply({"data": base64.b64encode(data).decode()})
    assert session.files.read("/workspace/data") == data
    server.reply(
        {
            "url": "https://sandbox.test/access",
            "token": "secret",
            "expires_at": "tomorrow",
        }
    )
    access = session.access(8080)
    assert access.token == "secret"
    assert "secret" not in repr(access)
    server.reply(status=204)
    server.client.sandboxes.grant(SESSION, SUBJECT, "2026-09-25T00:00:00Z")
    assert server.requests[-1].method == "PUT"
    assert server.requests[-1].url.path.endswith(f"/grants/{SUBJECT}")
    server.reply(status=204)
    server.client.sandboxes.revoke(SESSION, SUBJECT)
    assert server.requests[-1].method == "DELETE"


def test_sandbox_credentials_and_typed_failures() -> None:
    server = SandboxHTTP()
    _ = server.client.auth.set_session(Session("user-access", "refresh", "user"))
    server.reply(session_body())
    _ = server.client.sandboxes.get(SESSION)
    assert server.requests[-1].headers["Authorization"] == "Bearer user-access"
    for status, error in [(409, ConflictError), (429, RateLimitedError)]:
        server.reply(
            {"error": "denied", "code": "sandbox_denied"}, status, {"Retry-After": "7"}
        )
        with pytest.raises(error) as caught:
            _ = server.client.sandboxes.get(SESSION)
        assert caught.value.code == "sandbox_denied"
        assert caught.value.status == status
        assert caught.value.retry_after == (7 if status == 429 else None)
    server.failure = httpx.ReadTimeout("lost response")
    before = len(server.requests)
    with pytest.raises(TransportError):
        _ = server.client.sandboxes.exec(
            PROJECT, "run", region="aws-us-east-1", preset="python3.12", request_id=KEY
        )
    assert len(server.requests) == before + 1
    client = VolcanoClient(anon_key="anon")
    with pytest.raises(AuthenticationError) as missing:
        _ = client.sandboxes.get(SESSION)
    assert missing.value.status == 401
    assert str(missing.value) == "No service key configured"


def test_sandbox_rejects_invalid_local_inputs() -> None:
    server = SandboxHTTP()
    for options in [
        {"region": "aws-us-east-1"},
        {"region": "aws-us-east-1", "preset": "python3.12", "sandbox_id": SUBJECT},
        {"region": "aws-us-east-1", "sandbox_id": "bad"},
        {"region": "aws-us-east-1", "preset": "python3.12", "request_id": "bad"},
    ]:
        with pytest.raises(ValidationError):
            _ = server.client.sandboxes.exec(
                PROJECT, "run", **cast("SandboxExecOptions", options)
            )
    with pytest.raises(ValidationError):
        _ = server.client.sandboxes.get("../escape")
    assert not server.requests
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    with pytest.raises(ValidationError, match=r"^Sandbox files are limited to 8 MiB$"):
        session.files.write("/workspace/large", bytes(8 * 1024 * 1024 + 1))


def test_sandbox_context_requests_cleanup_and_checks_identity() -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    server.reply(session_body("terminating"), 202)
    with pytest.raises(ValueError, match="body failed"):
        fail_inside_session(session)
    server.reply(session_body("terminated"))
    _ = session.refresh()
    with session:
        pass
    count = len(server.requests)
    server.reply(session_body() | {"id": str(uuid4())})
    with pytest.raises(TypeError, match=r"^Sandbox session identity changed$"):
        _ = session.refresh()
    assert len(server.requests) == count + 1
    assert session.state == "terminated"


def test_sandbox_catalog() -> None:
    server = SandboxHTTP()
    server.reply(
        {
            "data": [
                {"id": "python3.12", "memory_mb": 2048, "regions": ["aws-us-east-1"]}
            ]
        }
    )
    (preset,) = server.client.sandboxes.presets()
    assert (preset.id, preset.memory_mb, preset.regions) == (
        "python3.12",
        2048,
        ("aws-us-east-1",),
    )


def fail_inside_session(session: SandboxSession) -> None:
    with session as owned:
        assert owned is session
        message = "body failed"
        raise ValueError(message)


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"data": {}},
        {"data": [{"id": "python3.12", "memory_mb": 2048, "regions": "bad"}]},
    ],
)
def test_sandbox_rejects_invalid_catalog(payload: object) -> None:
    server = SandboxHTTP()
    server.reply(payload)
    with pytest.raises(TypeError):
        _ = server.client.sandboxes.presets()


@pytest.mark.parametrize(
    ("field", "value"), [("stdout", 1), ("exit_code", True), ("timed_out", "false")]
)
def test_sandbox_rejects_invalid_command_response(field: str, value: object) -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    server.reply(command_body() | {field: value})
    with pytest.raises(TypeError):
        _ = session.exec("run")


@pytest.mark.parametrize(
    ("field", "value"), [("state", "invalid"), ("expires_at", None)]
)
def test_sandbox_refresh_preserves_state_on_invalid_response(
    field: str, value: object
) -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    server.reply(session_body("terminated") | {field: value})
    with pytest.raises(TypeError):
        _ = session.refresh()
    assert session.state == "running"


def test_sandbox_create_preserves_server_lifecycle_defaults() -> None:
    server = SandboxHTTP()
    server.reply(session_body(), 201)
    _ = server.client.sandboxes.create(
        PROJECT, region="aws-us-east-1", preset="python3.12"
    )
    assert json.loads(server.requests[-1].content) == {
        "region": "aws-us-east-1",
        "preset": "python3.12",
    }


@pytest.mark.parametrize(
    ("payload", "message"),
    [
        (None, "Invalid Sandbox response"),
        ({}, "Invalid Sandbox preset catalog"),
        ({"data": [{"regions": None}]}, "Invalid Sandbox regions"),
    ],
)
def test_sandbox_catalog_reports_invalid_wire_shape(
    payload: object, message: str
) -> None:
    server = SandboxHTTP()
    server.reply(payload)
    with pytest.raises(TypeError) as caught:
        _ = server.client.sandboxes.presets()
    assert str(caught.value) == message


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("stdout", 1, "Invalid Sandbox text field"),
        ("exit_code", True, "Invalid Sandbox integer field"),
        ("timed_out", "false", "Invalid Sandbox flag"),
    ],
)
def test_sandbox_command_reports_invalid_wire_field(
    field: str, value: object, message: str
) -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    server.reply(command_body() | {field: value})
    with pytest.raises(TypeError) as caught:
        _ = session.exec("run")
    assert str(caught.value) == message
    assert server.requests[-1].extensions["timeout"]["read"] == 180


def test_sandbox_invalid_identity_and_state_are_actionable() -> None:
    server = SandboxHTTP()
    with pytest.raises(
        ValidationError, match=r"^Sandbox resource and request IDs must be UUIDs$"
    ):
        _ = server.client.sandboxes.get("bad")
    server.reply(session_body("invalid"))
    with pytest.raises(TypeError, match=r"^Invalid Sandbox state$"):
        _ = server.client.sandboxes.get(SESSION)
    with pytest.raises(
        ValidationError, match=r"^Choose exactly one preset or sandbox_id$"
    ):
        _ = server.client.sandboxes.create(PROJECT, region="aws-us-east-1")


def test_sandbox_file_boundary_and_invalid_encoding() -> None:
    server = SandboxHTTP()
    server.reply(session_body())
    session = server.client.sandboxes.get(SESSION)
    data = bytes(8 * 1024 * 1024)
    server.reply(status=204)
    session.files.write("/workspace/boundary", data)
    assert base64.b64decode(json.loads(server.requests[-1].content)["data"]) == data
    server.reply({"data": "!!!!"})
    with pytest.raises(binascii.Error):
        _ = session.files.read("/workspace/invalid")
