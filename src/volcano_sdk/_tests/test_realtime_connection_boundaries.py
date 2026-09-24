from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import TYPE_CHECKING

import pytest
from typing_extensions import override

from volcano_sdk import (
    RealtimeConnectContext,
    RealtimeDisconnectContext,
    RealtimeErrorContext,
    Session,
    VolcanoClient,
)
from volcano_sdk import _realtime_transport as realtime_transport
from volcano_sdk._realtime_transport import (
    VolcanoCentrifugeConnection,
    centrifuge_client,
    native_presence_clients,
)
from volcano_sdk.realtime import (
    _ClientEvents,
    _presence_info,
    _wait_subscription,
)

from .test_realtime import FakeCentrifugeClient, FakeCentrifugeFactory, FakeSubscription

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


async def test_readiness_reports_an_interrupted_subscription() -> None:
    channel = VolcanoClient(anon_key="anon").realtime.channel("messages")
    native = FakeSubscription(channel.name, None, join_leave=False, recoverable=True)
    native.subscribed.set()

    with pytest.raises(RuntimeError, match=r"^realtime subscription was interrupted$"):
        await _wait_subscription(channel, native)


async def test_connection_token_is_available_during_native_connect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    observed: list[str] = []
    connect = native.connect

    async def inspect_connect() -> None:
        observed.append(client.realtime._connection_token())
        await connect()

    monkeypatch.setattr(native, "connect", inspect_connect)
    try:
        await client.realtime.channel("messages").subscribe()
        assert observed == ["access"]
    finally:
        await client.realtime.disconnect()


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
        _ = VolcanoCentrifugeConnection(native)


def test_native_adapter_rejects_non_string_subscription_keys(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    native = FakeCentrifugeClient()
    monkeypatch.setattr(native, "_subs", {1: object()})

    with pytest.raises(TypeError, match="subscription registry"):
        _ = VolcanoCentrifugeConnection(native)


def test_native_presence_rejects_non_string_client_keys() -> None:
    assert native_presence_clients({"known": object(), 1: object()}) is None


def test_native_presence_sanitizes_missing_client_and_invalid_user() -> None:
    presence = _presence_info(SimpleNamespace(user=42, conn_info={}))

    assert presence.client == ""
    assert presence.user is None


async def test_default_factory_constructs_the_installed_centrifuge_client() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    native = centrifuge_client(
        "wss://realtime.example.test/realtime/v1/websocket",
        events=_ClientEvents(realtime),
        token="access",
        get_token=realtime._token,
    )
    connection = VolcanoCentrifugeConnection(native)

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

    monkeypatch.setattr(realtime_transport, "Client", construct)

    assert (
        centrifuge_client(
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


async def test_recovering_channel_drops_publications_before_acknowledgement() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    received: list[object] = []
    channel = client.realtime.channel("messages").on("message", received.append)
    try:
        await channel.subscribe()
        subscription = native.subscription
        assert subscription is not None

        await subscription.emit_subscribing()
        await subscription.emit("before acknowledgement")
        await asyncio.wait_for(channel._callback_queue.join(), timeout=0.2)

        assert received == []
    finally:
        await client.realtime.disconnect()


async def test_stale_acknowledgement_cannot_revive_a_recovering_channel() -> None:
    native = FakeCentrifugeClient()
    client = VolcanoClient(
        anon_key="anon",
        access_token="access",
        _realtime_client_factory=FakeCentrifugeFactory(native),
    )
    channel = client.realtime.channel("messages")
    try:
        await channel.subscribe()
        stale_events = channel._subscription_events
        assert stale_events is not None
        await client.realtime.disconnect()
        await channel.subscribe()
        current_events = channel._subscription_events
        assert current_events is not None
        assert current_events is not stale_events

        await current_events.on_subscribing(object())
        assert not channel._subscribed
        await stale_events.on_subscribed(object())

        assert not channel._subscribed
    finally:
        await client.realtime.disconnect()


async def test_malformed_native_connection_contexts_are_sanitized() -> None:
    realtime = VolcanoClient(anon_key="anon").realtime
    connected: list[RealtimeConnectContext] = []
    disconnected: list[RealtimeDisconnectContext] = []
    errors: list[RealtimeErrorContext] = []
    _ = realtime.on_connect(connected.append)
    _ = realtime.on_disconnect(disconnected.append)
    _ = realtime.on_error(errors.append)
    events = _ClientEvents(realtime)

    await events.on_connected(SimpleNamespace(client=42))
    await events.on_disconnected(SimpleNamespace(code="invalid", reason=5))
    await events.on_error(SimpleNamespace(code="invalid", error=None))
    await events.on_error(SimpleNamespace(code="invalid", error="wire error"))
    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=0.2)

    assert connected == [RealtimeConnectContext(client=None)]
    assert disconnected == [RealtimeDisconnectContext(code=None, reason=None)]
    assert errors == [
        RealtimeErrorContext(code=None, message=None, error=None),
        RealtimeErrorContext(code=None, message="wire error", error=None),
    ]


async def test_presence_failure_reports_a_non_numeric_native_code_as_absent() -> None:
    class InvalidCodeError(RuntimeError):
        code: str = "invalid"

    realtime = VolcanoClient(anon_key="anon").realtime
    channel = realtime.channel("lobby", channel_type="presence")
    errors: list[RealtimeErrorContext] = []
    _ = realtime.on_error(errors.append)
    failure = InvalidCodeError("presence failed")

    await realtime._report_presence_sync_failure(channel, failure)
    await asyncio.wait_for(realtime._connection_callback_queue.join(), timeout=0.2)

    assert errors == [
        RealtimeErrorContext(code=None, message="presence failed", error=failure)
    ]
