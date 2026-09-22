"""Function invocation over the real HTTP stack.

These exercise httpx end to end against two local servers on different ports:
one standing in for the API, one for the resolved function endpoint. Running
them apart is the point -- an invocation that reached the API port would prove
the SDK derived the host instead of using the resolved `invoke_url`.
"""

from __future__ import annotations

import json
import threading
import time
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from functools import partial
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from socket import socket
    from socketserver import BaseServer

import pytest

from volcano_sdk import NotFoundError, VolcanoClient

FUNCTION_ID = "00000000-0000-4000-8000-000000000040"

# (status, payload) or (status, payload, extra response headers).
Responder = Callable[[str], "tuple[int, object] | tuple[int, object, dict[str, str]]"]


@dataclass
class RecordedRequest:
    path: str
    body: object
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


class Handler(BaseHTTPRequestHandler):
    def __init__(
        self,
        request: socket,
        client_address: tuple[str, int],
        server: BaseServer,
        *,
        respond: Responder,
        recorder: Recorder,
    ) -> None:
        self.respond = respond
        self.recorder = recorder
        super().__init__(request, client_address, server)

    protocol_version = "HTTP/1.1"

    def _handle(self) -> None:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b""
        body = json.loads(raw) if raw else None
        self.recorder.record(
            RecordedRequest(
                path=self.path,
                body=body,
                authorization=self.headers.get("Authorization"),
            )
        )
        answer = self.respond(self.path)
        status, payload = answer[0], answer[1]
        extra: dict[str, str] = answer[2] if len(answer) > 2 else {}
        encoded = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        # The server stamps this on every response, errors included, so
        # a test that omits it would accept a client keying the stale
        # mapping retry off its absence.
        self.send_header("X-Volcano-Version", "test-build")
        for name, value in extra.items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()


class Server(ThreadingHTTPServer):
    # The default backlog of 5 resets connections when a test opens
    # several at once, which reads as a transport failure in the SDK.
    request_queue_size = 128
    daemon_threads = True


class _Server:
    """A local HTTP server that answers from a caller-supplied handler."""

    def __init__(self, respond: Responder, recorder: Recorder) -> None:
        self.recorder = recorder
        handler = partial(Handler, respond=respond, recorder=recorder)
        self._httpd = Server(("127.0.0.1", 0), handler)
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

    def respond(_path: str) -> tuple[int, object]:
        return 200, {"ok": True}

    server = _Server(respond, recorder)
    try:
        yield server, recorder
    finally:
        server.close()


def _api_server(
    recorder: Recorder,
    resolve_payload: object,
    status: int = 200,
    resolve_delay: float = 0.0,
) -> _Server:
    def respond(path: str) -> tuple[int, object]:
        if path.startswith("/functions/resolve"):
            if resolve_delay:
                time.sleep(resolve_delay)
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


def test_concurrent_first_invocations_share_one_resolve(
    function_server: tuple[_Server, Recorder],
) -> None:
    """A cold cache must not let every caller open its own resolve."""
    functions, function_requests = function_server
    api_requests = Recorder()
    api = _api_server(
        api_requests,
        {
            "name": "send-welcome",
            "function_id": FUNCTION_ID,
            "invoke_url": f"{functions.url}/",
            "cache_ttl_seconds": 300,
        },
        resolve_delay=0.2,
    )
    try:
        client = _client(api.url)
        with ThreadPoolExecutor(max_workers=8) as executor:
            futures = [
                executor.submit(client.functions.invoke, "send-welcome")
                for _ in range(8)
            ]
            statuses = [future.result(timeout=30).status for future in futures]

        assert statuses == [200] * 8
        assert api_requests.paths() == ["/functions/resolve?name=send-welcome"]
        assert len(function_requests.paths()) == 8
    finally:
        api.close()


def test_a_recreated_function_is_resolved_again_after_a_platform_404() -> None:
    api_requests = Recorder()
    invoked: list[str] = []

    def respond(path: str) -> tuple[int, object] | tuple[int, object, dict[str, str]]:
        if path.startswith("/functions/resolve"):
            return 200, {
                "name": "send-welcome",
                "function_id": FUNCTION_ID,
                "cache_ttl_seconds": 300,
            }
        invoked.append(path)
        # The first invocation finds the cached identity gone. The platform
        # answers without the dispatch marker, which is the only thing telling
        # this apart from the function itself returning 404.
        if len(invoked) == 1:
            return 404, {"error": "function not found"}
        return 200, {"ok": True}, {"X-Volcano-Function-Invoked": "true"}

    api = _Server(respond, api_requests)
    try:
        result = _client(api.url).functions.invoke("send-welcome")

        assert result.status == 200
        assert api_requests.paths() == [
            "/functions/resolve?name=send-welcome",
            f"/functions/{FUNCTION_ID}/invoke",
            "/functions/resolve?name=send-welcome",
            f"/functions/{FUNCTION_ID}/invoke",
        ]
    finally:
        api.close()


def test_a_function_authored_404_is_returned_without_invoking_twice() -> None:
    api_requests = Recorder()

    def respond(path: str) -> tuple[int, object] | tuple[int, object, dict[str, str]]:
        if path.startswith("/functions/resolve"):
            return 200, {
                "name": "send-welcome",
                "function_id": FUNCTION_ID,
                "cache_ttl_seconds": 300,
            }
        # The function ran and chose 404. Retrying would repeat whatever it did
        # on the way to deciding that.
        return 404, {"error": "no such record"}, {"X-Volcano-Function-Invoked": "true"}

    api = _Server(respond, api_requests)
    try:
        result = _client(api.url).functions.invoke("send-welcome")

        assert result.status == 404
        assert api_requests.paths() == [
            "/functions/resolve?name=send-welcome",
            f"/functions/{FUNCTION_ID}/invoke",
        ]
    finally:
        api.close()
