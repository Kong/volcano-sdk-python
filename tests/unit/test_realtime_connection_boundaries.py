from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory
from typing_extensions import override

from volcano_sdk import Session, VolcanoClient
from volcano_sdk import realtime as realtime_module
from volcano_sdk.realtime import (
    _centrifuge_client,
    _ClientEvents,
    _native_presence_clients,
    _VolcanoCentrifugeConnection,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class FailingFirstConnection(FakeCentrifugeClient):
    def __init__(self, failure: BaseException) -> None:
        super().__init__()
        self.failure: BaseException = failure
        self.attempts: int = 0

    @override
    async def connect(self) -> None:
        self.attempts += 1
        if self.attempts == 1:
            raise self.failure
        await super().connect()


@pytest.mark.parametrize(
    "failure", [RuntimeError("connect failed"), asyncio.CancelledError()]
)
async def test_failed_connect_clears_credentials_before_retry(
    failure: BaseException,
) -> None:
    native = FailingFirstConnection(failure)
    client = VolcanoClient(
        anon_key="anon",
        access_token="old-access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("messages")

    with pytest.raises(type(failure)) as caught:
        await channel.subscribe()

    assert caught.value is failure
    assert client.realtime._connection is None
    assert client.realtime._connection_session_lineage is None
    assert client.realtime._connection_access_token is None

    _ = client.auth.set_session(Session("new-access", "new-refresh", "new-user"))
    try:
        await channel.subscribe()
        assert native.attempts == 2
        assert client.realtime.is_connected
        assert await client.realtime._token() == "new-access"
    finally:
        await client.realtime.disconnect()


async def test_connection_requires_a_session_before_constructing_transport() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon", _realtime_client_factory=FakeCentrifugeFactory(native)
    )

    with pytest.raises(RuntimeError, match="No active session"):
        _ = await client.realtime._connect()

    assert native.calls == []
    assert client.realtime._connection is None


async def test_token_callback_requires_a_connection_identity() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    with pytest.raises(
        RuntimeError, match="Realtime connection has no session binding"
    ):
        _ = await realtime._token()


def test_connection_identity_cannot_supply_a_cleared_session() -> None:
    client = VolcanoClient(anon_key="anon")
    lineage = client._capture_session_binding()[1]

    with pytest.raises(RuntimeError, match="No active session"):
        _ = client.realtime._session_for_lineage(lineage)


def test_native_adapter_rejects_an_incompatible_subscription_registry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    native = FakeCentrifugeClient()
    monkeypatch.delattr(native, "_subs")

    with pytest.raises(TypeError, match="subscription registry"):
        _ = _VolcanoCentrifugeConnection(native)


def test_native_presence_rejects_non_string_client_keys() -> None:
    assert _native_presence_clients({"known": object(), 1: object()}) is None


async def test_default_factory_constructs_the_installed_centrifuge_client() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    native = _centrifuge_client(
        "wss://realtime.example.test/realtime/v1/websocket",
        events=_ClientEvents(realtime),
        token="access",
        get_token=realtime._token,
    )
    connection = _VolcanoCentrifugeConnection(native)

    assert not connection.is_connected
    await connection.disconnect()
    assert not connection.is_connected


def test_default_factory_passes_connection_settings_to_centrifuge(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    address = "wss://realtime.example.test/realtime/v1/websocket"
    events = object()
    native = FakeCentrifugeClient()
    received: list[object] = []

    async def refresh_token() -> str:
        return "refreshed-access"

    def construct(
        supplied_address: str,
        *,
        events: object,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> FakeCentrifugeClient:
        received.extend((supplied_address, events, token, get_token))
        return native

    monkeypatch.setattr(realtime_module, "Client", construct)

    assert (
        _centrifuge_client(
            address,
            events=events,
            token="initial-access",
            get_token=refresh_token,
        )
        is native
    )
    assert received == [address, events, "initial-access", refresh_token]


@pytest.mark.parametrize(
    ("api_url", "expected_address"),
    [
        (
            "https://api.example.test/base?ignored=yes",
            "wss://api.example.test/realtime/v1/websocket?apikey=X%2Fy",
        ),
        (
            "http://localhost:8000/base?ignored=yes",
            "ws://localhost:8000/realtime/v1/websocket?apikey=X%2Fy",
        ),
    ],
)
def test_realtime_address_preserves_scheme_and_escapes_anonymous_key(
    api_url: str,
    expected_address: str,
) -> None:
    realtime = VolcanoClient(anon_key="X/y", api_url=api_url).realtime

    assert realtime._address() == expected_address


async def test_server_subscription_events_do_not_dispatch_project_callbacks() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    received: list[object] = []
    _ = realtime.on_connect(received.append)
    _ = realtime.on_disconnect(received.append)
    _ = realtime.on_error(received.append)
    events = _ClientEvents(realtime)
    context = object()

    await events.on_connecting(context)
    await events.on_subscribed(context)
    await events.on_subscribing(context)
    await events.on_unsubscribed(context)
    await events.on_publication(context)
    await events.on_join(context)
    await events.on_leave(context)

    assert received == []
    assert realtime._connection_callback_queue.empty()
    assert realtime._connection_callback_task is None
