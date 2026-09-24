"""Realtime broadcast, presence, and Postgres public facades."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypeAlias, TypeVar

import volcano_sdk._realtime_messages as _messages
import volcano_sdk._realtime_transport as _native

from ._client_context import ClientContextSource, facade_context
from ._realtime_connection import RealtimeState

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from ._realtime_channel import ChannelOperations
    from .models import JSONValue

_MessageT = TypeVar("_MessageT")
CentrifugeConnection: TypeAlias = _messages.CentrifugeConnection
CentrifugeFactory: TypeAlias = _messages.CentrifugeFactory
CentrifugeSubscription: TypeAlias = _messages.CentrifugeSubscription
Publication: TypeAlias = _messages.Publication
PublicationContext: TypeAlias = _messages.PublicationContext
RealtimeContext: TypeAlias = _messages.RealtimeContext
MessageCallback: TypeAlias = _messages.MessageCallback[_MessageT]
RealtimeCallback: TypeAlias = _messages.RealtimeCallback[_MessageT]
UnsubscribeCallback: TypeAlias = _messages.UnsubscribeCallback
ChannelType: TypeAlias = _messages.ChannelType
PostgresEvent: TypeAlias = _messages.PostgresEvent
PostgresListenerEvent: TypeAlias = _messages.PostgresListenerEvent
PostgresChangeCallback: TypeAlias = _messages.PostgresChangeCallback
RealtimeConnectContext: TypeAlias = _messages.RealtimeConnectContext
RealtimeDisconnectContext: TypeAlias = _messages.RealtimeDisconnectContext
RealtimeErrorContext: TypeAlias = _messages.RealtimeErrorContext
RealtimePresenceInfo: TypeAlias = _messages.RealtimePresenceInfo
PostgresChange: TypeAlias = _messages.PostgresChange
POSTGRES_EVENTS = _messages.POSTGRES_EVENTS
POSTGRES_CHANNEL_SEGMENTS = _messages.POSTGRES_CHANNEL_SEGMENTS
POSTGRES_PUBLICATION_SEGMENTS = _messages.POSTGRES_PUBLICATION_SEGMENTS
CENTRIFUGE_ERROR: type[Exception] = _messages.CENTRIFUGE_ERROR
CALLBACK_QUEUE_LIMIT = _messages.CALLBACK_QUEUE_LIMIT
POSTGRES_QUEUE_LIMIT = _messages.POSTGRES_QUEUE_LIMIT
POSTGRES_BATCH_WINDOW_MS = _messages.POSTGRES_BATCH_WINDOW_MS
POSTGRES_MAX_BATCH_SIZE = _messages.POSTGRES_MAX_BATCH_SIZE
NO_PENDING_CALLBACK = _messages.NO_PENDING_CALLBACK
CALLBACK_QUEUE_FULL_MESSAGE = _messages.CALLBACK_QUEUE_FULL_MESSAGE
CHANNEL_NOT_SUBSCRIBED = _messages.CHANNEL_NOT_SUBSCRIBED
CHANNEL_REMOVAL_IN_PROGRESS = _messages.CHANNEL_REMOVAL_IN_PROGRESS
CHANNEL_NOT_MANAGED = _messages.CHANNEL_NOT_MANAGED
PRESENCE_ONLY = _messages.PRESENCE_ONLY
BROADCAST_ONLY = _messages.BROADCAST_ONLY
POSTGRES_ONLY = _messages.POSTGRES_ONLY
CALLBACK_NOT_CALLABLE = _messages.CALLBACK_NOT_CALLABLE
SUBSCRIPTION_REGISTRY_UNAVAILABLE = _messages.SUBSCRIPTION_REGISTRY_UNAVAILABLE
NO_ACTIVE_SESSION = _messages.NO_ACTIVE_SESSION
CONNECTION_SESSION_UNAVAILABLE = _messages.CONNECTION_SESSION_UNAVAILABLE
CONNECTION_SESSION_CHANGED = _messages.CONNECTION_SESSION_CHANGED
POSTGRES_FETCH_FAILED_MESSAGE = _messages.POSTGRES_FETCH_FAILED_MESSAGE


class Channel:
    """Realtime broadcast, presence, or Postgres channel."""

    def __init__(self, state: ChannelOperations) -> None:
        """Wrap an owned internal channel lifecycle."""
        self._state: ChannelOperations = state

    @property
    def name(self) -> str:
        """Canonical channel name sent to realtime."""
        return self._state.name

    def on(self, event: str, callback: Callable[[_MessageT], object]) -> Channel:
        """Register a callback for messages or presence events.

        Returns
        -------
        Channel
            This channel, for chaining listener registrations.

        Unsupported events raise ValueError.

        """
        _ = self._state.on(event, callback)
        return self

    def on_postgres_changes(
        self,
        event: PostgresListenerEvent,
        *,
        schema: str,
        table: str,
        callback: PostgresChangeCallback,
    ) -> UnsubscribeCallback:
        """Observe Postgres changes filtered by event, schema, and table.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this listener.

        Non-Postgres channels and unsupported events raise ValueError.

        """
        return self._state.on_postgres_changes(
            event, schema=schema, table=table, callback=callback
        )

    def on_presence_sync(
        self, callback: Callable[[Mapping[str, RealtimePresenceInfo]], object]
    ) -> UnsubscribeCallback:
        """Observe immutable snapshots of a presence channel's current state.

        Requires a presence channel.

        Returns
        -------
        UnsubscribeCallback
            A function that removes this listener.

        """
        return self._state.on_presence_sync(callback)

    async def track(self, state: Mapping[str, JSONValue] | None = None) -> None:
        """Store local presence state while server identity remains authoritative.

        Requires a presence channel.

        An unsubscribed channel raises RuntimeError.

        """
        await self._state.presence.track(state)

    def get_presence_state(self) -> Mapping[str, RealtimePresenceInfo]:
        """Read the clients currently present.

        Requires a presence channel.

        Returns
        -------
        Mapping[str, RealtimePresenceInfo]
            An immutable snapshot indexed by client identifier.

        """
        return self._state.presence.get_presence_state()

    @property
    def tracked_state(self) -> Mapping[str, JSONValue]:
        """Immutable snapshot of this client's local presence state."""
        return self._state.presence.tracked_state

    async def subscribe(self) -> None:
        """Wait until this channel is subscribed and ready for use."""
        await self._state.subscribe()

    async def send(self, data: object) -> None:
        """Publish a broadcast payload to this channel."""
        await self._state.send(data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self._state.unsubscribe()


class Realtime:
    """Manage project realtime connections and channels."""

    def __init__(
        self,
        client: RealtimeContext | ClientContextSource,
        *,
        api_url: str,
        client_factory: CentrifugeFactory = _native.centrifuge_client,
    ) -> None:
        """Create a lazily connected realtime facade."""
        self._state: RealtimeState[Channel] = RealtimeState(
            facade_context(client),
            Channel,
            api_url=api_url,
            client_factory=client_factory,
        )

    @property
    def database_name(self) -> str | None:
        """Database bound to lightweight Postgres changes, or None if unbound."""
        return self._state.database_name

    def set_database_name(self, name: str | None) -> None:
        """Bind lightweight Postgres changes to a project database."""
        self._state.set_database_name(name)

    def on_connect(
        self, callback: Callable[[RealtimeConnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a connection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return self._state.on_connect(callback)

    def on_disconnect(
        self, callback: Callable[[RealtimeDisconnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a disconnection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return self._state.on_disconnect(callback)

    def on_error(
        self, callback: Callable[[RealtimeErrorContext], object]
    ) -> UnsubscribeCallback:
        """Register a transport-error callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return self._state.on_error(callback)

    def channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
        auto_fetch: bool = True,
        fetch_batch_window_ms: int = POSTGRES_BATCH_WINDOW_MS,
        fetch_max_batch_size: int = POSTGRES_MAX_BATCH_SIZE,
    ) -> Channel:
        """Get a stable channel facade for a realtime name and configuration.

        Returns
        -------
        Channel
            The existing channel for this type and name, or a newly created one.

        Invalid or conflicting channel settings raise ValueError.
        A channel being removed raises RuntimeError.

        """
        return self._state.channel(
            name,
            channel_type=channel_type,
            auto_fetch=auto_fetch,
            fetch_batch_window_ms=fetch_batch_window_ms,
            fetch_max_batch_size=fetch_max_batch_size,
        )

    @property
    def is_connected(self) -> bool:
        """Whether the realtime transport is connected."""
        return self._state.is_connected

    async def remove_channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
    ) -> None:
        """Unsubscribe and forget one broadcast or presence channel."""
        await self._state.remove_channel(name, channel_type=channel_type)

    async def remove_all_channels(self) -> None:
        """Unsubscribe and forget every managed channel."""
        await self._state.remove_all_channels()

    async def disconnect(self) -> None:
        """Disconnect and reset every channel managed by this facade."""
        await self._state.disconnect()
