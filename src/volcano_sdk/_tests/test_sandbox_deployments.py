from __future__ import annotations

import httpx
import pytest

from volcano_sdk import ValidationError

from .test_sandboxes import KEY, PROJECT, SUBJECT, SandboxHTTP

_DEPLOYMENT = {
    "id": KEY,
    "status": "building",
    "created_at": "2026-10-07T00:00:00Z",
    "updated_at": "2026-10-07T00:00:00Z",
}


def test_custom_deployment_preserves_archive_and_retry_identity() -> None:
    server = SandboxHTTP()
    source = bytes([31, 139, 0, 255])
    server.reply(_DEPLOYMENT, 202)
    result = server.client.sandboxes.deploy(
        PROJECT,
        SUBJECT,
        source,
        name="custom",
        memory_mb=2048,
        ports=[8080],
        request_id=KEY,
    )
    assert result.id == KEY
    assert result.status == "building"
    request = server.requests[0]
    assert request.url.path == f"/projects/{PROJECT}/sandboxes/{SUBJECT}/deployments"
    assert request.headers["Idempotency-Key"] == KEY
    assert source in request.content
    assert b"[8080]" in request.content
    assert b"2048" in request.content


def test_custom_deployment_history_source_logs_and_cleanup() -> None:
    server = SandboxHTTP()
    server.reply(
        {
            "data": [_DEPLOYMENT],
            "pagination": {"has_more": True, "limit": 1, "next_cursor": "next"},
        }
    )
    page = server.client.sandboxes.deployments(PROJECT, SUBJECT, cursor="first")
    assert page.data[0].id == KEY
    assert page.next_cursor == "next"
    assert server.requests[-1].url.params["cursor"] == "first"
    server.reply(_DEPLOYMENT)
    assert server.client.sandboxes.deployment(PROJECT, SUBJECT, KEY).id == KEY
    source = bytes([31, 139, 0, 255])
    server.responses.append(
        httpx.Response(
            200, content=source, headers={"content-type": "application/gzip"}
        )
    )
    assert server.client.sandboxes.source(PROJECT, SUBJECT, KEY) == source
    server.reply(
        {
            "data": [{"timestamp": _DEPLOYMENT["created_at"], "message": "Building"}],
            "next_cursor": "more",
        }
    )
    logs = server.client.sandboxes.logs(
        PROJECT, SUBJECT, KEY, region="aws-us-east-1", limit=10
    )
    assert logs.data[0].message == "Building"
    assert logs.next_cursor == "more"
    server.reply(None, 202)
    server.client.sandboxes.delete_template(PROJECT, SUBJECT)
    assert server.requests[-1].method == "DELETE"


def test_custom_deployment_rejects_invalid_ports_before_transport() -> None:
    server = SandboxHTTP()
    with pytest.raises(ValidationError, match="ports"):
        _ = server.client.sandboxes.deploy(
            PROJECT, SUBJECT, b"source", name="custom", ports=[65536]
        )
    assert not server.requests
