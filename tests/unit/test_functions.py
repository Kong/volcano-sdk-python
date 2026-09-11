from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING, Any, cast

import httpx
import pytest

from volcano_sdk import ServerError, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from volcano_sdk._transport import Transport


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: Any
    headers: dict[str, str]
    content: bytes = b""


class FakeFunctionsTransport:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.invoke_response = FakeResponse(
            200,
            {"message": "hello", "items": [1, 2]},
            {"X-Volcano-Version": "staging-v1", "X-Trace": "trace-1"},
        )

    def resolve_function_for_invocation(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("resolveFunctionForInvocation", kwargs))
        return FakeResponse(
            200,
            {
                "name": kwargs["name"],
                "function_id": "00000000-0000-4000-8000-000000000040",
                "cache_ttl_seconds": 60,
            },
            {},
        )

    def invoke_function(self, **kwargs: Any) -> FakeResponse:
        self.calls.append(("invokeFunction", kwargs))
        return self.invoke_response


def functions_client(
    transport: FakeFunctionsTransport,
    *,
    anon_key: str = "anon-key",
    service_key: str | None = "service-key",
) -> VolcanoClient:
    return VolcanoClient(
        anon_key=anon_key,
        service_key=service_key,
        _transport=cast("Transport", transport),
    )


def test_functions_resolves_and_invokes_by_name() -> None:
    transport = FakeFunctionsTransport()
    client = functions_client(transport)

    result = client.functions.invoke("send-welcome", {"user_id": "user-123"})

    assert result.status == 200
    assert result.version == "staging-v1"
    assert result.data == {"message": "hello", "items": (1, 2)}
    assert result.headers == {"X-Volcano-Version": "staging-v1", "X-Trace": "trace-1"}
    assert isinstance(result.data, MappingProxyType)
    assert isinstance(result.headers, MappingProxyType)
    assert [operation for operation, _ in transport.calls] == [
        "resolveFunctionForInvocation",
        "invokeFunction",
    ]
    assert transport.calls[0][1] == {
        "authorization": "service-key",
        "name": "send-welcome",
    }
    assert transport.calls[1][1] == {
        "authorization": "service-key",
        "function_id": "00000000-0000-4000-8000-000000000040",
        "payload": {"user_id": "user-123"},
    }


def test_functions_returns_a_function_owned_error_response() -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(
        422,
        {"error": "invalid order"},
        {"x-volcano-version": "v2"},
    )

    result = functions_client(transport).functions.invoke("validate-order")

    assert result.status == 422
    assert result.data == {"error": "invalid order"}
    assert result.version == "v2"


@pytest.mark.parametrize("version", [None, "v2"])
def test_functions_returns_none_for_an_empty_http_204(version: str | None) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/functions/resolve":
            return httpx.Response(
                200,
                json={
                    "name": "send-welcome",
                    "function_id": "00000000-0000-4000-8000-000000000040",
                    "cache_ttl_seconds": 60,
                },
            )
        headers = {} if version is None else {"X-Volcano-Version": version}
        return httpx.Response(204, headers=headers)

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    result = client.functions.invoke("send-welcome")

    assert result.status == 204
    assert result.data is None
    assert result.version == version
    assert result.headers.get("x-volcano-version") == version


@pytest.mark.parametrize("status", [200, 422])
@pytest.mark.parametrize(
    ("content", "content_type", "expected"),
    [
        (b'{"ok":true}', "application/json", {"ok": True}),
        (b'[1,{"ok":true}]', "application/json", (1, {"ok": True})),
        (b'"hello"', "application/json", "hello"),
        (b"42", "application/json", 42),
        (b"true", "application/json", True),
        (b"null", "application/json", None),
        (b"hello", "text/plain", "hello"),
        (b"\xef\xbb\xbf[1]", "application/json", (1,)),
        (b"\xef\xbb\xbfhello", "text/plain", "hello"),
        (b"\xef\xbb\xbf", "text/plain", None),
        (b"42", "text/plain", "42"),
        (b"[]", "text/plain", ()),
        (b"\n [1, 2]", "text/plain", "\n [1, 2]"),
        (b"broken json", "application/json", "broken json"),
        (b"NaN", "application/json", "NaN"),
        (b"", "text/plain", None),
    ],
)
def test_functions_preserve_json_values_and_text(
    content: bytes, content_type: str, expected: object, status: int
) -> None:
    def handle(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/functions/resolve":
            return httpx.Response(
                200,
                json={
                    "name": "send-welcome",
                    "function_id": "00000000-0000-4000-8000-000000000040",
                    "cache_ttl_seconds": 60,
                },
            )
        return httpx.Response(
            status,
            content=content,
            headers={"Content-Type": content_type, "X-Volcano-Version": "v2"},
        )

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )
    result = VolcanoClient(anon_key="anon", _transport=transport).functions.invoke(
        "send-welcome"
    )

    assert result.data == expected
    assert result.status == status
    assert result.version == "v2"
    assert result.headers["content-type"] == content_type


def test_function_response_has_a_stable_hash() -> None:
    result = functions_client(FakeFunctionsTransport()).functions.invoke("send-welcome")

    assert hash(result) == hash(result)


def test_functions_raises_for_a_platform_failure() -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(
        503,
        {"error": "function is provisioning", "code": "function_not_ready"},
        {},
    )

    with pytest.raises(ServerError, match="function is provisioning") as raised:
        functions_client(transport).functions.invoke("daily-rollup")

    assert raised.value.status == 503
    assert raised.value.code == "function_not_ready"


@pytest.mark.parametrize("name", ["", " Invalid ", "-leading", "a" * 64])
def test_functions_rejects_invalid_names_before_transport(name: str) -> None:
    transport = FakeFunctionsTransport()

    with pytest.raises(ValueError, match="DNS-safe"):
        functions_client(transport).functions.invoke(name)

    assert transport.calls == []


def test_functions_uses_the_local_anon_key_without_a_session_or_service_key() -> None:
    transport = FakeFunctionsTransport()
    anon_key = "ak-0000000000000000000000000000000000000000"

    functions_client(
        transport,
        anon_key=anon_key,
        service_key=None,
    ).functions.invoke("public-health")

    assert transport.calls[0][1]["authorization"] == anon_key
    assert transport.calls[1][1]["authorization"] == anon_key
