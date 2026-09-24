from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from types import MappingProxyType
from typing import TYPE_CHECKING

import httpx
import pytest
from transport_fixtures import RejectingTransport
from typing_extensions import override

from volcano_sdk import (
    NotFoundError,
    ServerError,
    VolcanoClient,
    VolcanoError,
    _function_resolution,
)
from volcano_sdk import functions as functions_module
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk.functions import Functions

if TYPE_CHECKING:
    from volcano_sdk.models import JSONValue


@dataclass(frozen=True)
class FakeResponse:
    status_code: int
    payload: object
    headers: dict[str, str] | None
    content: bytes = b""


class FakeFunctionsTransport(RejectingTransport):
    def __init__(self, *, invoke_url: str | None = None) -> None:
        self.calls: list[tuple[str, dict[str, object]]] = []
        self.invoke_url: str | None = invoke_url
        self.cache_ttl_seconds: object = 60
        self.resolve_response: FakeResponse | None = None
        self.invoke_responses: list[FakeResponse] = []
        self.invoke_response: FakeResponse = FakeResponse(
            200,
            {"message": "hello", "items": [1, 2]},
            {"X-Volcano-Version": "staging-v1", "X-Trace": "trace-1"},
        )

    def resolve_function_for_invocation(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("resolveFunctionForInvocation", kwargs))
        if self.resolve_response is not None:
            return self.resolve_response
        payload: dict[str, object] = {
            "name": kwargs["name"],
            "function_id": "00000000-0000-4000-8000-000000000040",
            "cache_ttl_seconds": self.cache_ttl_seconds,
        }
        if self.invoke_url is not None:
            payload["invoke_url"] = self.invoke_url
        return FakeResponse(200, payload, {})

    def invoke_function(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("invokeFunction", kwargs))
        return self._next_invoke_response()

    def invoke_function_url(self, **kwargs: object) -> FakeResponse:
        self.calls.append(("invokeFunctionUrl", kwargs))
        return self._next_invoke_response()

    def _next_invoke_response(self) -> FakeResponse:
        if self.invoke_responses:
            return self.invoke_responses.pop(0)
        return self.invoke_response

    @property
    def resolve_calls(self) -> int:
        return sum(
            1
            for operation, _ in self.calls
            if operation == "resolveFunctionForInvocation"
        )


def functions_client(
    transport: FakeFunctionsTransport,
    *,
    anon_key: str = "anon-key",
    service_key: str | None = "service-key",
) -> VolcanoClient:
    return VolcanoClient(
        anon_key=anon_key,
        service_key=service_key,
        _transport=transport,
    )


def test_functions_requires_a_transport_with_invocation_methods() -> None:
    client = VolcanoClient(
        anon_key="anon-key", service_key="service-key", _transport=RejectingTransport()
    )

    with pytest.raises(
        TypeError, match="Transport does not support function invocation"
    ):
        _ = client.functions.invoke("send-welcome")


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
    # The dispatch marker is what makes this the function's answer rather than
    # a platform refusal; the version stamp is on every response either way.
    transport.invoke_response = FakeResponse(
        422,
        {"error": "invalid order"},
        {"x-volcano-version": "v2", "x-volcano-function-invoked": "true"},
    )

    result = functions_client(transport).functions.invoke("validate-order")

    assert result.status == 422
    assert result.data == {"error": "invalid order"}
    assert result.version == "v2"


def test_functions_raise_when_the_platform_refuses_the_invocation() -> None:
    """A refusal before dispatch is an SDK error, not the function's answer.

    The version stamp is present here because the server puts it on every
    response. Classifying on it would hand this back as though the function had
    replied, which is what happened before the dispatch marker existed.
    """
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(
        400,
        {"error": "function cannot be invoked (status: failed)"},
        {"x-volcano-version": "v2"},
    )

    with pytest.raises(VolcanoError) as caught:
        _ = functions_client(transport).functions.invoke("validate-order")

    assert "function cannot be invoked" in str(caught.value)


def test_functions_rejects_a_platform_redirect_before_dispatch() -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(300, {"error": "redirected"}, {})

    with pytest.raises(VolcanoError, match="redirected"):
        _ = functions_client(transport).functions.invoke("send-welcome")


@pytest.mark.parametrize(
    ("content", "expected"),
    [(b'{"ok":true}', {"ok": True}), (b"[1,2]", (1, 2))],
)
def test_functions_recognizes_json_containers_without_content_type(
    content: bytes, expected: object
) -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(200, None, {}, content)

    assert functions_client(transport).functions.invoke("send-welcome").data == expected


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
        (b"\xff", "text/plain", "\ufffd"),
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
            headers={
                "Content-Type": content_type,
                "X-Volcano-Version": "v2",
                # The function ran and chose this status, including the 422.
                # Without the marker the platform would own the failure.
                "X-Volcano-Function-Invoked": "true",
            },
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
        _ = functions_client(transport).functions.invoke("daily-rollup")

    assert raised.value.status == 503
    assert raised.value.code == "function_not_ready"


@pytest.mark.parametrize("name", ["", " Invalid ", "-leading", "a" * 64])
def test_functions_rejects_invalid_names_before_transport(name: str) -> None:
    transport = FakeFunctionsTransport()

    with pytest.raises(ValueError, match="DNS-safe"):
        _ = functions_client(transport).functions.invoke(name)

    assert transport.calls == []


def test_functions_uses_the_local_anon_key_without_a_session_or_service_key() -> None:
    transport = FakeFunctionsTransport()
    anon_key = "ak-0000000000000000000000000000000000000000"

    _ = functions_client(
        transport,
        anon_key=anon_key,
        service_key=None,
    ).functions.invoke("public-health")

    assert transport.calls[0][1]["authorization"] == anon_key
    assert transport.calls[1][1]["authorization"] == anon_key


def test_functions_invokes_the_resolved_url_rather_than_the_api_path() -> None:
    invoke_url = "https://00000000-0000-4000-8000-000000000040.functions.test.run/"
    transport = FakeFunctionsTransport(invoke_url=invoke_url)

    _ = functions_client(transport).functions.invoke("send-welcome", {"user_id": "u-1"})

    assert [operation for operation, _ in transport.calls] == [
        "resolveFunctionForInvocation",
        "invokeFunctionUrl",
    ]
    assert transport.calls[1][1] == {
        "authorization": "service-key",
        "invoke_url": invoke_url,
        "payload": {"user_id": "u-1"},
    }


def test_functions_falls_back_to_the_api_path_without_an_invoke_url() -> None:
    transport = FakeFunctionsTransport(invoke_url=None)

    _ = functions_client(transport).functions.invoke("send-welcome")

    assert [operation for operation, _ in transport.calls] == [
        "resolveFunctionForInvocation",
        "invokeFunction",
    ]


@pytest.mark.parametrize(
    "invoke_url",
    [
        "",
        "not-a-url",
        "ftp://example.test/",
        "/relative",
        "https:///nohost",
        # Malformed authorities. urlsplit raises on some of these rather than
        # reporting them, and the fallback still has to hold.
        "https://[",
        "https://[::1",
        "https://example.test:99999/",
        "https://exa mple.test/",
    ],
)
def test_functions_ignores_an_unusable_invoke_url(invoke_url: str) -> None:
    transport = FakeFunctionsTransport(invoke_url=invoke_url)

    _ = functions_client(transport).functions.invoke("send-welcome")

    assert transport.calls[1][0] == "invokeFunction"


def test_functions_refuses_to_send_the_token_to_a_plaintext_endpoint() -> None:
    """An https API must not be downgraded to http by a resolve response."""
    transport = FakeFunctionsTransport(invoke_url="http://functions.test.run/")

    _ = functions_client(transport).functions.invoke("send-welcome")

    assert transport.calls[1][0] == "invokeFunction"


def test_functions_allows_a_plaintext_endpoint_for_a_plaintext_api() -> None:
    transport = FakeFunctionsTransport(invoke_url="http://127.0.0.1:9/")
    client = VolcanoClient(
        anon_key="anon-key",
        service_key="service-key",
        api_url="http://127.0.0.1:8000",
        _transport=transport,
    )

    _ = client.functions.invoke("send-welcome")

    assert transport.calls[1][0] == "invokeFunctionUrl"


def test_functions_resolves_a_name_once_for_repeated_invocations() -> None:
    transport = FakeFunctionsTransport(
        invoke_url="https://00000000-0000-4000-8000-000000000040.functions.test.run/"
    )
    client = functions_client(transport)

    for _ in range(3):
        _ = client.functions.invoke("send-welcome")

    assert transport.resolve_calls == 1
    operations = [operation for operation, _ in transport.calls]
    assert operations.count("invokeFunctionUrl") == 3


def test_functions_resolves_again_once_the_advertised_lifetime_expires(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = _FakeClock()
    monkeypatch.setattr(_function_resolution, "_now", clock)
    transport = FakeFunctionsTransport()
    transport.cache_ttl_seconds = 60
    client = functions_client(transport)

    _ = client.functions.invoke("send-welcome")
    clock.advance(59)
    _ = client.functions.invoke("send-welcome")
    assert transport.resolve_calls == 1

    clock.advance(2)
    _ = client.functions.invoke("send-welcome")
    assert transport.resolve_calls == 2


def test_functions_does_not_share_a_resolution_across_credentials() -> None:
    transport = FakeFunctionsTransport()

    first = functions_client(transport, service_key="service-key")
    second = functions_client(transport, service_key="other-key")
    _ = first.functions.invoke("send-welcome")
    _ = second.functions.invoke("send-welcome")

    assert transport.resolve_calls == 2


def test_functions_shares_a_resolution_across_clients_with_one_credential() -> None:
    transport = FakeFunctionsTransport()

    _ = functions_client(transport).functions.invoke("send-welcome")
    _ = functions_client(transport).functions.invoke("send-welcome")

    assert transport.resolve_calls == 1


@pytest.mark.parametrize("cache_ttl_seconds", [0, -1, None, "60", 1.5])
def test_functions_rejects_a_resolve_without_a_usable_lifetime(
    cache_ttl_seconds: object,
) -> None:
    transport = FakeFunctionsTransport()
    transport.cache_ttl_seconds = cache_ttl_seconds

    with pytest.raises(TypeError, match="complete function response"):
        _ = functions_client(transport).functions.invoke("send-welcome")


def test_functions_accepts_a_one_second_resolution_lifetime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(_function_resolution, "_now", _FakeClock())
    transport = FakeFunctionsTransport()
    transport.cache_ttl_seconds = 1
    client = functions_client(transport)

    assert client.functions.invoke("send-welcome").status == 200
    assert client.functions.invoke("send-welcome").status == 200
    assert transport.resolve_calls == 1


def test_functions_cache_hit_does_not_wait_for_a_resolve_lock(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    transport = FakeFunctionsTransport()
    client = functions_client(transport)
    _ = client.functions.invoke("send-welcome")

    def unexpected_resolve_lock(api_url: str, authorization: str, name: str) -> None:
        _ = (api_url, authorization, name)
        pytest.fail("cache hit tried to acquire a resolve lock")

    monkeypatch.setattr(functions_module, "resolve_lock", unexpected_resolve_lock)
    assert client.functions.invoke("send-welcome").status == 200
    assert transport.resolve_calls == 1


def test_functions_preserves_a_response_without_headers() -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(200, {"ok": True}, None)

    result = functions_client(transport).functions.invoke("send-welcome")

    assert result.status == 200
    assert result.headers == {}
    assert result.version is None
    assert result.data == {"ok": True}


@pytest.mark.parametrize("invalid", [{1, 2}, math.nan, math.inf, -math.inf])
def test_functions_rejects_non_json_response_payloads(invalid: object) -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(200, {"bad": invalid}, {})

    with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
        _ = functions_client(transport).functions.invoke("send-welcome")


@pytest.mark.parametrize("mode", ["mapping", "list", "tuple-list"])
def test_functions_rejects_cyclic_payloads_before_resolution(mode: str) -> None:
    payload: dict[str, JSONValue] = {}
    if mode == "mapping":
        payload["cycle"] = payload
    else:
        linked: list[JSONValue] = []
        payload["cycle"] = linked
        linked.append(linked if mode == "list" else (linked,))
    transport = FakeFunctionsTransport()

    with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
        _ = functions_client(transport).functions.invoke("send-welcome", payload)

    assert transport.calls == []


@pytest.mark.parametrize("payload", [{"bad": "\ud800"}, {"\udfff": "bad"}])
def test_functions_rejects_surrogates_before_resolution(
    payload: dict[str, JSONValue],
) -> None:
    transport = FakeFunctionsTransport()

    with pytest.raises(TypeError, match=r"Function (data|JSON object keys)"):
        _ = functions_client(transport).functions.invoke("send-welcome", payload)

    assert transport.calls == []


def test_functions_rejects_escaped_surrogates_in_response_json() -> None:
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(
        200, None, {"Content-Type": "application/json"}, b'{"bad":"\\ud800"}'
    )

    with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
        _ = functions_client(transport).functions.invoke("send-welcome")


def test_functions_accepts_shared_acyclic_values_and_unicode() -> None:
    shared: dict[str, JSONValue] = {"text": "🌋"}
    payload: dict[str, JSONValue] = {"first": shared, "second": shared}
    transport = FakeFunctionsTransport()

    result = functions_client(transport).functions.invoke("send-welcome", payload)
    assert result.status == 200
    assert transport.calls[-1][1]["payload"] == {
        "first": {"text": "🌋"},
        "second": {"text": "🌋"},
    }


def test_functions_accepts_nested_acyclic_sequences() -> None:
    transport = FakeFunctionsTransport()

    result = functions_client(transport).functions.invoke(
        "send-welcome", {"grid": [[1], [2]]}
    )

    assert result.status == 200
    assert transport.calls[-1][1]["payload"] == {"grid": ((1,), (2,))}


def test_functions_rejects_subclass_spoofed_surrogates() -> None:
    class ForgedString(str):
        __slots__ = ()

        @override
        def encode(self, encoding: str = "utf-8", errors: str = "strict") -> bytes:
            _ = (encoding, errors)
            return b"ok"

    transport = FakeFunctionsTransport()
    invalid = ForgedString("\ud800")
    payloads: tuple[dict[str, JSONValue], ...] = (
        {"bad": invalid},
        {invalid: "bad"},
    )
    for payload in payloads:
        with pytest.raises(TypeError, match=r"Function (data|JSON object keys)"):
            _ = functions_client(transport).functions.invoke("send-welcome", payload)

    assert transport.calls == []


def test_functions_rejects_integers_the_json_encoder_cannot_render() -> None:
    limit = sys.get_int_max_str_digits()
    value = 10 ** (limit or 4300)
    transport = FakeFunctionsTransport()
    client = functions_client(transport)

    if limit:
        with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
            _ = client.functions.invoke("send-welcome", {"value": value})
        assert transport.calls == []
    else:
        assert client.functions.invoke("send-welcome", {"value": value}).status == 200


def test_functions_rejects_excessively_nested_payloads_before_resolution() -> None:
    root: list[JSONValue] = []
    current = root
    for _ in range(sys.getrecursionlimit()):
        nested: list[JSONValue] = []
        current.append(nested)
        current = nested
    transport = FakeFunctionsTransport()

    with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
        _ = functions_client(transport).functions.invoke("send-welcome", {"deep": root})

    assert transport.calls == []


def test_functions_rejects_excessively_nested_response_values() -> None:
    root: list[JSONValue] = []
    current = root
    for _ in range(sys.getrecursionlimit()):
        nested: list[JSONValue] = []
        current.append(nested)
        current = nested
    transport = FakeFunctionsTransport()
    transport.invoke_response = FakeResponse(200, root, {})

    with pytest.raises(TypeError, match="Function data must be JSON-compatible"):
        _ = functions_client(transport).functions.invoke("send-welcome")


def test_functions_remembers_an_unknown_name_briefly() -> None:
    transport = FakeFunctionsTransport()
    transport.resolve_response = FakeResponse(404, {"error": "function not found"}, {})
    client = functions_client(transport)

    for _ in range(3):
        with pytest.raises(NotFoundError):
            _ = client.functions.invoke("missing-function")

    assert transport.resolve_calls == 1


def test_functions_reresolves_once_when_the_cached_identity_is_gone() -> None:
    """A recreated function gets a new id, so the cached one answers 404."""
    transport = FakeFunctionsTransport()
    transport.invoke_responses = [
        # A platform 404 still carries the version stamp — every response does.
        # Only the dispatch marker is missing.
        FakeResponse(404, {"error": "function not found"}, {"X-Volcano-Version": "v1"}),
        FakeResponse(
            200,
            {"ok": True},
            {"X-Volcano-Version": "v1", "X-Volcano-Function-Invoked": "true"},
        ),
    ]
    client = functions_client(transport)

    result = client.functions.invoke("send-welcome")

    assert result.status == 200
    assert [operation for operation, _ in transport.calls] == [
        "resolveFunctionForInvocation",
        "invokeFunction",
        "resolveFunctionForInvocation",
        "invokeFunction",
    ]


def test_functions_returns_a_function_owned_404_without_invoking_twice() -> None:
    transport = FakeFunctionsTransport()
    # What the server sends once the function has run: the dispatch marker
    # alongside the version stamp every response carries.
    transport.invoke_response = FakeResponse(
        404,
        {"error": "no such route"},
        {"X-Volcano-Version": "v1", "X-Volcano-Function-Invoked": "true"},
    )
    client = functions_client(transport)

    result = client.functions.invoke("send-welcome")

    assert result.status == 404
    assert [operation for operation, _ in transport.calls].count("invokeFunction") == 1


class _FakeClock:
    def __init__(self) -> None:
        self._now: float = 1000.0

    def __call__(self) -> float:
        return self._now

    def advance(self, seconds: float) -> None:
        self._now += seconds


def test_functions_preserves_owned_error_metadata_in_negative_cache() -> None:
    transport = FakeFunctionsTransport()
    transport.resolve_response = FakeResponse(
        404, {"error": "Unknown function", "code": "function_missing"}, {}
    )
    client = functions_client(transport)
    with pytest.raises(NotFoundError) as first:
        _ = client.functions.invoke("missing-function")
    assert (
        str(first.value),
        first.value.status,
        first.value.code,
        first.value.retry_after,
    ) == ("Unknown function", 404, "function_missing", None)
    first.value.args = ("changed",)
    first.value.code = "changed"
    first.value.retry_after = 99
    with pytest.raises(NotFoundError) as second:
        _ = client.functions.invoke("missing-function")
    assert (
        str(second.value),
        second.value.status,
        second.value.code,
        second.value.retry_after,
    ) == ("Unknown function", 404, "function_missing", None)
    assert second.value is not first.value
    assert transport.resolve_calls == 1


def test_functions_negative_cache_preserves_retry_metadata() -> None:
    api_url = "https://api.cache.test.volcano.dev"
    authorization = "cache-test-key"
    name = "missing-function"
    _function_resolution.store_missing(
        api_url,
        authorization,
        name,
        NotFoundError(
            "Try again later", status=404, code="function_missing", retry_after=7
        ),
    )

    with pytest.raises(NotFoundError) as caught:
        _ = Functions._cached(api_url, authorization, name)

    assert caught.value.status == 404
    assert caught.value.code == "function_missing"
    assert caught.value.retry_after == 7
