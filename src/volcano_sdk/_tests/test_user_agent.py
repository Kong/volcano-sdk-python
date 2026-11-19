from __future__ import annotations

import asyncio
import platform
import sys
from http import HTTPStatus
from importlib import metadata
from typing import TYPE_CHECKING, cast

import httpx
import pytest
from websockets.asyncio.server import serve

from volcano_sdk import _user_agent
from volcano_sdk._durable_platform_request import PlatformRequest, post_to_platform
from volcano_sdk._realtime_transport import centrifuge_client
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk._transport_sandbox import SandboxHTTPTransport, SandboxRequest
from volcano_sdk._user_agent import USER_AGENT, build_user_agent, user_agent_headers

from .fixtures.durable_platform import install_platform
from .user_agent_support import USER_AGENT_PATTERN

if TYPE_CHECKING:
    from websockets.asyncio.server import ServerConnection
    from websockets.http11 import Request, Response


def test_the_user_agent_names_the_sdk_version_and_runtime() -> None:
    assert USER_AGENT_PATTERN.fullmatch(USER_AGENT)
    assert (
        build_user_agent(
            version=metadata.version("volcano-sdk-python"),
            implementation=sys.implementation.name,
            python_version=platform.python_version(),
            system=sys.platform,
            machine=platform.machine(),
        )
        == USER_AGENT
    )


def test_each_caller_gets_its_own_header_mapping() -> None:
    first = user_agent_headers()
    first["Authorization"] = "Bearer token"

    assert user_agent_headers() == {"User-Agent": USER_AGENT}


@pytest.mark.parametrize(
    ("system", "machine", "expected"),
    [
        ("darwin", "arm64", "volcano-sdk-python/1.4.0 (cpython/3.12.4; darwin/arm64)"),
        ("linux", "x86_64", "volcano-sdk-python/1.4.0 (cpython/3.12.4; linux/x86_64)"),
        ("win32", "AMD64", "volcano-sdk-python/1.4.0 (cpython/3.12.4; windows/amd64)"),
        (
            "freebsd14",
            "",
            "volcano-sdk-python/1.4.0 (cpython/3.12.4; freebsd14/unknown)",
        ),
        ("linux", "\u00e4rm", "volcano-sdk-python/1.4.0 (cpython/3.12.4; linux/?rm)"),
    ],
)
def test_the_runtime_is_normalised(system: str, machine: str, expected: str) -> None:
    assert (
        build_user_agent(
            version="1.4.0",
            implementation="cpython",
            python_version="3.12.4",
            system=system,
            machine=machine,
        )
        == expected
    )


def test_an_uninstalled_sdk_reports_an_unknown_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    seen: list[str] = []

    def missing(distribution: str) -> str:
        seen.append(distribution)
        raise metadata.PackageNotFoundError(distribution)

    monkeypatch.setattr(metadata, "version", missing)

    assert _user_agent.sdk_version() == "unknown"
    assert seen == ["volcano-sdk-python"]


def test_a_versionless_install_reports_an_unknown_version(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def versionless(_distribution: str) -> None:
        return None

    monkeypatch.setattr(metadata, "version", versionless)

    assert _user_agent.sdk_version() == "unknown"


def _single_user_agent(request: httpx.Request) -> str:
    agents = request.headers.get_list("user-agent")
    assert len(agents) == 1
    return agents[0]


def test_generated_requests_identify_the_sdk() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": []})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    _ = transport.query_database_select(
        authorization="access-token",
        database_name="app",
        body={"table": "messages", "limit": 1},
    )

    assert _single_user_agent(requests[0]) == USER_AGENT
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_asynchronous_generated_requests_identify_the_sdk() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": []})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    async def query() -> object:
        return await transport.query_database_select_async(
            authorization="access-token",
            database_name="app",
            body={"table": "messages", "limit": 1},
        )

    _ = asyncio.run(query())

    assert _single_user_agent(requests[0]) == USER_AGENT
    assert requests[0].headers["authorization"] == "Bearer access-token"


def test_unauthenticated_generated_requests_identify_the_sdk() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"presets": []})

    transport = SandboxHTTPTransport(
        api_url="https://api.test.volcano.dev",
        httpx_transport=httpx.MockTransport(handle),
    )

    _ = transport.sandbox_request(
        authorization=None, request=SandboxRequest("list_sandbox_presets")
    )

    assert _single_user_agent(requests[0]) == USER_AGENT
    assert "authorization" not in requests[0].headers


def test_durable_platform_requests_identify_the_sdk(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake = install_platform(monkeypatch, httpx.Response(200, json={"ok": True}))

    _ = post_to_platform(
        "https://api.test.volcano.dev",
        PlatformRequest(
            path="/durable-approvals",
            body={},
            headers={"user-agent": "replaced", "X-Volcano-Callback": "token"},
        ),
    )

    assert _single_user_agent(fake.requests[0]) == USER_AGENT
    assert fake.requests[0].headers["x-volcano-callback"] == "token"


@pytest.mark.allow_hosts(["127.0.0.1"])
async def test_the_realtime_handshake_identifies_the_sdk() -> None:
    received: asyncio.Queue[list[str]] = asyncio.Queue()

    def refuse(connection: ServerConnection, request: Request) -> Response:
        received.put_nowait(request.headers.get_all("User-Agent"))
        return connection.respond(HTTPStatus.FORBIDDEN, "")

    async def unreachable(_connection: ServerConnection) -> None:
        await asyncio.sleep(0)
        raise AssertionError

    async def token() -> str:
        return await asyncio.sleep(0, "access")

    async with serve(unreachable, "127.0.0.1", 0, process_request=refuse) as server:
        address = cast("tuple[str, int]", next(iter(server.sockets)).getsockname())
        native = centrifuge_client(
            f"ws://127.0.0.1:{address[1]}/realtime/v1/websocket",
            events=None,
            token="access",
            get_token=token,
        )
        try:
            await native.connect()
            agents = await asyncio.wait_for(received.get(), timeout=5)
        finally:
            await native.disconnect()

    assert agents == [USER_AGENT]
