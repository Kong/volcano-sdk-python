"""Function invocation over the real HTTP stack.

These exercise httpx end to end against two local servers on different ports:
one standing in for the API, one for the resolved function endpoint. Running
them apart is the point -- an invocation that reached the API port would prove
the SDK derived the host instead of using the resolved `invoke_url`.
"""

from __future__ import annotations

import json
import threading
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

import pytest

from volcano_sdk import NotFoundError, VolcanoClient

FUNCTION_ID = "00000000-0000-4000-8000-000000000040"

Responder = Callable[[str], "tuple[int, Any]"]


@dataclass
class RecordedRequest:
    path: str
    body: Any
    authorization: str | None


@dataclass
class Recorder:
    requests: list[RecordedRequest] = field(default_factory=list["RecordedRequest"])
    lock: threading.Lock = field(default_factory=threading.Lock)

    def record(self, request: RecordedRequest) -> None:
        with self.lock:
            self.requests.append(request)

    def paths(self) -> list[str]:
        with self.lock:
            return [request.path for request in self.requests]


class _Server:
    """A local HTTP server that answers from a caller-supplied handler."""

    def __init__(self, respond: Responder, recorder: Recorder) -> None:
        self.recorder = recorder
        outer = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def _handle(self) -> None:
                length = int(self.headers.get("Content-Length") or 0)
                raw = self.rfile.read(length) if length else b""
                body = json.loads(raw) if raw else None
                outer.recorder.record(
                    RecordedRequest(
                        path=self.path,
                        body=body,
                        authorization=self.headers.get("Authorization"),
                    )
                )
                status, payload = respond(self.path)
                encoded = json.dumps(payload).encode()
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def do_GET(self) -> None:
                self._handle()

            def do_POST(self) -> None:
                self._handle()

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
                """Keep the test output free of per-request server logging."""

        self._httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._thread = threading.Thread(target=self._httpd.serve_forever, daemon=True)
        self._thread.start()

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self._httpd.server_address[1]}"

    def close(self) -> None:
        self._httpd.shutdown()
        self._httpd.server_close()
        self._thread.join(timeout=5)


@pytest.fixture
def function_server() -> Iterator[tuple[_Server, Recorder]]:
    recorder = Recorder()

    def respond(_path: str) -> tuple[int, Any]:
        return 200, {"ok": True}

    server = _Server(respond, recorder)
    try:
        yield server, recorder
    finally:
        server.close()


def _api_server(recorder: Recorder, resolve_payload: Any, status: int = 200) -> _Server:
    def respond(path: str) -> tuple[int, Any]:
        if path.startswith("/functions/resolve"):
            return status, resolve_payload
        return 200, {"ok": "via-api"}

    return _Server(respond, recorder)


def _client(api_url: str) -> VolcanoClient:
    return VolcanoClient(
        anon_key="anon-key", service_key="service-key", api_url=api_url
    )


def test_repeated_invocations_resolve_once_and_reach_the_resolved_host(
    function_server: tuple[_Server, Recorder],
) -> None:
    functions, function_requests = function_server
    api_requests = Recorder()
    invoke_url = f"{functions.url}/"
    api = _api_server(
        api_requests,
        {
            "name": "send-welcome",
            "function_id": FUNCTION_ID,
            "invoke_url": invoke_url,
            "cache_ttl_seconds": 300,
        },
    )
    try:
        client = _client(api.url)
        for _ in range(3):
            result = client.functions.invoke("send-welcome", {"user_id": "u-1"})
            assert result.status == 200

        assert api_requests.paths() == ["/functions/resolve?name=send-welcome"]
        assert function_requests.paths() == ["/", "/", "/"]
        invoked = function_requests.requests[0]
        assert invoked.body == {"payload": {"user_id": "u-1"}}
        assert invoked.authorization == "Bearer service-key"
    finally:
        api.close()


def test_invocation_falls_back_to_the_api_path_without_an_invoke_url(
    function_server: tuple[_Server, Recorder],
) -> None:
    _functions, function_requests = function_server
    api_requests = Recorder()
    api = _api_server(
        api_requests,
        {
            "name": "send-welcome",
            "function_id": FUNCTION_ID,
            "cache_ttl_seconds": 300,
        },
    )
    try:
        result = _client(api.url).functions.invoke("send-welcome")

        assert result.status == 200
        assert api_requests.paths() == [
            "/functions/resolve?name=send-welcome",
            f"/functions/{FUNCTION_ID}/invoke",
        ]
        assert function_requests.paths() == []
    finally:
        api.close()


def test_an_unknown_name_is_not_re_resolved_on_every_attempt() -> None:
    api_requests = Recorder()
    api = _api_server(api_requests, {"error": "function not found"}, status=404)
    try:
        client = _client(api.url)
        for _ in range(3):
            with pytest.raises(NotFoundError):
                client.functions.invoke("missing-function")

        assert api_requests.paths() == ["/functions/resolve?name=missing-function"]
    finally:
        api.close()
