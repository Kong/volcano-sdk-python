from __future__ import annotations

import httpx
import pytest

from volcano_sdk import NotFoundError, ValidationError
from volcano_sdk._sandbox import SandboxRequests
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk._transport_sandbox import SandboxRequest
from volcano_sdk._transport_types import GeneratedTransportResponse
from volcano_sdk.sandbox_deployments import SandboxDeployments

from .test_sandboxes import KEY, PROJECT, SUBJECT, SandboxHTTP

_DEPLOYMENT = {
    "id": KEY,
    "status": "building",
    "created_at": "2026-10-07T00:00:00Z",
    "updated_at": "2026-10-07T01:00:00Z",
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
    assert result.created_at == _DEPLOYMENT["created_at"]
    assert result.updated_at == _DEPLOYMENT["updated_at"]
    request = server.requests[0]
    assert request.url.path == f"/projects/{PROJECT}/sandboxes/{SUBJECT}/deployments"
    assert request.headers["Idempotency-Key"] == KEY
    assert source in request.content
    assert b'name="name"\r\nContent-Type: text/plain\r\n\r\ncustom' in request.content
    assert b'filename="source.tar.gz"' in request.content
    assert b"Content-Type: application/gzip" in request.content
    assert request.headers["Authorization"] == "Bearer service"
    assert request.method == "POST"
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
    assert page.has_more is True
    assert page.limit == 1
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
    assert logs.data[0].timestamp == _DEPLOYMENT["created_at"]
    assert dict(server.requests[-1].url.params) == {
        "region": "aws-us-east-1",
        "limit": "10",
    }
    assert (
        server.requests[-1].url.path
        == f"/projects/{PROJECT}/sandboxes/{SUBJECT}/deployments/{KEY}/logs"
    )
    assert logs.next_cursor == "more"
    server.reply(None, 202)
    server.client.sandboxes.delete_template(PROJECT, SUBJECT)
    assert server.requests[-1].method == "DELETE"
    assert server.requests[-1].url.path == f"/projects/{PROJECT}/sandboxes/{SUBJECT}"


def test_custom_deployment_rejects_invalid_ports_before_transport() -> None:
    server = SandboxHTTP()
    with pytest.raises(ValidationError, match="ports"):
        _ = server.client.sandboxes.deploy(
            PROJECT, SUBJECT, b"source", name="custom", ports=[65536]
        )
    assert not server.requests


@pytest.mark.parametrize("port", [0, -1, 65536, True, False])
def test_custom_deployment_invalid_port_boundaries(port: int) -> None:
    server = SandboxHTTP()
    with pytest.raises(
        ValidationError, match=r"^Sandbox ports must be between 1 and 65535$"
    ):
        _ = server.client.sandboxes.deploy(
            PROJECT, SUBJECT, b"source", name="custom", ports=[port]
        )
    assert not server.requests


def test_custom_deployment_source_size_boundaries_and_defaults() -> None:
    server = SandboxHTTP()
    source = b"x" * (32 * 1024 * 1024)
    server.reply(_DEPLOYMENT, 202)
    _ = server.client.sandboxes.deploy(PROJECT, SUBJECT, source, name="custom")
    request = server.requests[-1]
    assert source in request.content
    assert (
        b'name="memory_mb"\r\nContent-Type: text/plain\r\n\r\n1024' in request.content
    )
    assert b'name="ports"\r\nContent-Type: text/plain\r\n\r\n[]' in request.content
    with pytest.raises(
        ValidationError, match=r"^Sandbox source archives are limited to 32 MiB$"
    ):
        _ = server.client.sandboxes.deploy(
            PROJECT, SUBJECT, source + b"x", name="custom"
        )
    assert len(server.requests) == 1


def test_custom_deployment_accepts_port_boundaries() -> None:
    server = SandboxHTTP()
    server.reply(_DEPLOYMENT, 202)
    _ = server.client.sandboxes.deploy(
        PROJECT, SUBJECT, b"source", name="custom", ports=[1, 65535]
    )
    assert b"[1, 65535]" in server.requests[-1].content


@pytest.mark.parametrize("more", [None, 0, "true"])
def test_deployment_history_rejects_invalid_pagination(more: object) -> None:
    server = SandboxHTTP()
    server.reply({"data": [], "pagination": {"has_more": more, "limit": 1}})
    with pytest.raises(TypeError, match=r"^Invalid Sandbox pagination$"):
        _ = server.client.sandboxes.deployments(PROJECT, SUBJECT)


@pytest.mark.parametrize("rows", [None, {}, "rows"])
def test_deployment_history_rejects_invalid_rows(rows: object) -> None:
    server = SandboxHTTP()
    server.reply({"data": rows, "pagination": {"has_more": False, "limit": 1}})
    with pytest.raises(TypeError, match=r"^Invalid Sandbox list$"):
        _ = server.client.sandboxes.deployments(PROJECT, SUBJECT)


def test_deployment_empty_pages_and_log_cursor() -> None:
    server = SandboxHTTP()
    server.reply({"data": [], "pagination": {"has_more": False, "limit": 20}})
    page = server.client.sandboxes.deployments(PROJECT, SUBJECT)
    assert page.data == ()
    assert page.has_more is False
    assert page.limit == 20
    assert page.next_cursor is None
    assert "cursor" not in server.requests[-1].url.params
    server.reply({"data": []})
    logs = server.client.sandboxes.logs(
        PROJECT, SUBJECT, KEY, region="aws-us-west-2", cursor="next-page"
    )
    assert logs.data == ()
    assert logs.next_cursor is None
    assert dict(server.requests[-1].url.params) == {
        "region": "aws-us-west-2",
        "cursor": "next-page",
        "limit": "100",
    }


def test_deployment_source_http_failure_is_not_returned_as_archive() -> None:

    server = SandboxHTTP()
    server.reply({"message": "not found"}, 404)
    with pytest.raises(NotFoundError):
        _ = server.client.sandboxes.source(PROJECT, SUBJECT, KEY)
    assert (
        server.requests[-1].url.path
        == f"/projects/{PROJECT}/sandboxes/{SUBJECT}/deployments/{KEY}/source"
    )


def test_deployment_source_rejects_non_binary_transport_payload() -> None:

    deployments = SandboxDeployments(
        SandboxRequests(
            lambda _request: GeneratedTransportResponse(
                status_code=200, payload="not bytes", content=b"", headers={}
            )
        )
    )
    with pytest.raises(TypeError, match=r"^Invalid Sandbox source archive$"):
        _ = deployments.source(PROJECT, SUBJECT, KEY)


def test_generated_deployment_transport_defaults_omitted_ports() -> None:
    server = SandboxHTTP()
    server.reply(_DEPLOYMENT, 202)
    transport = GeneratedTransport(
        api_url="https://sandbox.test",
        httpx_transport=httpx.MockTransport(server.handle),
    )
    response = transport.sandbox_request(
        authorization="Bearer service",
        request=SandboxRequest(
            "deploy_sandbox",
            PROJECT,
            SUBJECT,
            body={"name": "custom", "memory_mb": 1024},
            request_id=KEY,
            archive=b"archive",
        ),
    )
    assert response.status_code == 202
    assert (
        b'name="ports"\r\nContent-Type: text/plain\r\n\r\n[]'
        in server.requests[-1].content
    )
