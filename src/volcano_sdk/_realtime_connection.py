"""Shared connection ownership, credential scoping, and channel registry."""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import dataclass
from itertools import count
from typing import (
    TYPE_CHECKING,
    TypeAlias,
    TypeVar,
)
from urllib.parse import quote, urlencode, urlsplit, urlunsplit

from centrifuge import ClientEventHandler
from typing_extensions import override

import volcano_sdk._realtime_transport as _native

from ._database_response import database_rows
from ._realtime_callbacks import (
    CallbackBatch,
    ConnectionDelivery,
    Invocation,
    register_callback,
)
from ._realtime_messages import (
    BROADCAST_ONLY,
    CALLBACK_NOT_CALLABLE,
    CALLBACK_QUEUE_LIMIT,
    CENTRIFUGE_ERROR,
    CHANNEL_NOT_MANAGED,
    CHANNEL_NOT_SUBSCRIBED,
    CHANNEL_REMOVAL_IN_PROGRESS,
    CONNECTION_SESSION_CHANGED,
    CONNECTION_SESSION_UNAVAILABLE,
    NO_ACTIVE_SESSION,
    POSTGRES_BATCH_WINDOW_MS,
    POSTGRES_MAX_BATCH_SIZE,
    POSTGRES_QUERY_UNAVAILABLE,
    CentrifugeFactory,
    CentrifugeSubscription,
    ChannelType,
    RealtimeConnectContext,
    RealtimeContext,
    RealtimeDisconnectContext,
    RealtimeErrorContext,
    UnsubscribeCallback,
    checked_postgres_row,
    postgres_fetch_config,
    validate_channel_type,
)
from ._transport import (
    AsyncDatabaseSelectTransport,
    invoke_async,
    response_payload,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Iterator, Mapping

    from ._realtime_fetch_worker import (
        PostgresFetchRequest,
    )
    from ._session_operations import SessionOperations
    from .models import JSONValue, Session

from typing import Generic

from ._realtime_channel import (
    ChannelEvents,
    ChannelState,
    reset_realtime_channels,
    wait_subscription,
)

FacadeT = TypeVar("FacadeT")
ConnectionContext: TypeAlias = (
    RealtimeConnectContext | RealtimeDisconnectContext | RealtimeErrorContext
)


@dataclass(frozen=True, slots=True)
class ManagedChannel(Generic[FacadeT]):
    state: ChannelState
    facade: FacadeT


class ClientEvents(ClientEventHandler):
    def __init__(self, enqueue: Callable[[ConnectionContext], None]) -> None:
        self.enqueue: Callable[[ConnectionContext], None] = enqueue

    @override
    async def on_connected(self, ctx: object) -> None:
        client = _native.native_attribute(ctx, "client")
        self.enqueue(
            RealtimeConnectContext(client=client if isinstance(client, str) else None),
        )

    @override
    async def on_disconnected(self, ctx: object) -> None:
        code = _native.native_attribute(ctx, "code")
        reason = _native.native_attribute(ctx, "reason")
        self.enqueue(
            RealtimeDisconnectContext(
                code=code if isinstance(code, int) else None,
                reason=reason if isinstance(reason, str) else None,
            ),
        )

    @override
    async def on_error(self, ctx: object) -> None:
        code = _native.native_attribute(ctx, "code")
        error = _native.native_attribute(ctx, "error")
        self.enqueue(
            RealtimeErrorContext(
                code=code if isinstance(code, int) else None,
                message=str(error) if error is not None else None,
                error=error if isinstance(error, Exception) else None,
            ),
        )


async def run_connection_callback(
    callback: Invocation,
) -> None:
    result = callback()
    if inspect.isawaitable(result):
        await result


class RealtimeState(Generic[FacadeT]):
    """Manage project realtime connections and channels."""

    def __init__(
        self,
        client: RealtimeContext,
        factory: Callable[[ChannelState], FacadeT],
        *,
        api_url: str,
        client_factory: CentrifugeFactory = _native.centrifuge_client,
    ) -> None:
        """Create a lazily connected realtime facade."""
        self.factory: Callable[[ChannelState], FacadeT] = factory
        self.client_context: RealtimeContext = client
        self.api_url: str = api_url
        self.client_factory: CentrifugeFactory = client_factory
        self.connection: _native.VolcanoCentrifugeConnection | None = None
        self.connection_session_lineage: SessionOperations | None = None
        self.connection_access_token: str | None = None
        self.connection_lock: asyncio.Lock = asyncio.Lock()
        self.channels: dict[str, ManagedChannel[FacadeT]] = {}
        self.callback_tasks: set[asyncio.Task[None]] = set()
        self.removing_channels: set[str] = set()
        self.connect_callbacks: dict[
            int, Callable[[RealtimeConnectContext], object]
        ] = {}
        self.disconnect_callbacks: dict[
            int, Callable[[RealtimeDisconnectContext], object]
        ] = {}
        self.error_callbacks: dict[int, Callable[[RealtimeErrorContext], object]] = {}
        self.callback_ids: Iterator[int] = count()
        self.connection_callback_queue: asyncio.Queue[ConnectionDelivery] = (
            asyncio.Queue(maxsize=CALLBACK_QUEUE_LIMIT)
        )
        self.connection_callback_task: asyncio.Task[None] | None = None
        self.bound_database_name: str | None = None

    @property
    def database_name(self) -> str | None:
        """Database bound to lightweight Postgres changes, or None if unbound."""
        return self.bound_database_name

    def set_database_name(self, name: str | None) -> None:
        """Bind lightweight Postgres changes to a project database."""
        self.bound_database_name = name

    async def fetch_postgres_rows(
        self,
        requests: tuple[PostgresFetchRequest, ...],
    ) -> tuple[Mapping[str, JSONValue] | None, ...]:
        first = requests[0]
        row_ids = [request.row_id for request in requests]
        transport = self.client_context.transport()
        if not isinstance(transport, AsyncDatabaseSelectTransport):
            raise TypeError(POSTGRES_QUERY_UNAVAILABLE)
        response = await invoke_async(
            transport.query_database_select_async,
            authorization=first.access_token,
            database_name=first.database_name,
            body={
                "table": first.table,
                "filters": [{"column": "id", "operator": "in", "value": row_ids}],
                "limit": len(row_ids),
            },
        )
        rows = tuple(
            checked_postgres_row(row)
            for row in database_rows(response_payload(response, 200))
        )
        return tuple(
            next(
                (row for row in rows if row.get("id") == request.row_id),
                None,
            )
            for request in requests
        )

    def on_connect(
        self, callback: Callable[[RealtimeConnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a connection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self.connect_callbacks, self.callback_ids, callback, CALLBACK_NOT_CALLABLE
        )

    def on_disconnect(
        self, callback: Callable[[RealtimeDisconnectContext], object]
    ) -> UnsubscribeCallback:
        """Register a disconnection callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self.disconnect_callbacks,
            self.callback_ids,
            callback,
            CALLBACK_NOT_CALLABLE,
        )

    def on_error(
        self, callback: Callable[[RealtimeErrorContext], object]
    ) -> UnsubscribeCallback:
        """Register a transport-error callback.

        Returns
        -------
        UnsubscribeCallback
            An idempotent function that removes this callback.

        """
        return register_callback(
            self.error_callbacks, self.callback_ids, callback, CALLBACK_NOT_CALLABLE
        )

    def _connection_delivery(
        self,
        context: RealtimeConnectContext
        | RealtimeDisconnectContext
        | RealtimeErrorContext,
    ) -> ConnectionDelivery:
        if isinstance(context, RealtimeConnectContext):
            return CallbackBatch(
                "connect",
                self.connect_callbacks,
                tuple(self.connect_callbacks),
                context,
            )
        if isinstance(context, RealtimeDisconnectContext):
            return CallbackBatch(
                "disconnect",
                self.disconnect_callbacks,
                tuple(self.disconnect_callbacks),
                context,
            )
        return CallbackBatch(
            "error", self.error_callbacks, tuple(self.error_callbacks), context
        )

    def enqueue_connection_callbacks(
        self,
        context: RealtimeConnectContext
        | RealtimeDisconnectContext
        | RealtimeErrorContext,
    ) -> None:
        batch = self._connection_delivery(context)
        if batch.empty:
            return
        try:
            self.connection_callback_queue.put_nowait(batch)
        except asyncio.QueueFull:
            asyncio.get_running_loop().call_exception_handler(
                {"message": "Volcano realtime connection callback queue is full"}
            )
            return
        task = self.connection_callback_task
        if task is None or task.done():
            self.connection_callback_task = asyncio.create_task(
                self._drain_connection_callbacks()
            )

    async def _drain_connection_callbacks(self) -> None:
        while not self.connection_callback_queue.empty():
            batch = self.connection_callback_queue.get_nowait()
            try:
                for callback in batch.invocations():
                    (error,) = await asyncio.gather(
                        run_connection_callback(callback),
                        return_exceptions=True,
                    )
                    if isinstance(error, BaseException):
                        asyncio.get_running_loop().call_exception_handler(
                            {
                                "message": (
                                    "Volcano realtime connection callback failed"
                                ),
                                "exception": error,
                                "event": batch.event,
                            }
                        )
            finally:
                self.connection_callback_queue.task_done()

    def channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
        auto_fetch: bool = True,
        fetch_batch_window_ms: int = POSTGRES_BATCH_WINDOW_MS,
        fetch_max_batch_size: int = POSTGRES_MAX_BATCH_SIZE,
    ) -> FacadeT:
        """Get a stable channel facade for a realtime name and configuration.

        Returns
        -------
        ChannelState
            The existing channel for this type and name, or a newly created one.

        Raises
        ------
        ValueError
            The type or fetch settings are invalid, or the existing channel
            uses different fetch settings.
        RuntimeError
            Removal of this channel is still in progress.

        """
        channel_type = validate_channel_type(channel_type)
        fetch_config = postgres_fetch_config(
            auto_fetch=auto_fetch,
            fetch_batch_window_ms=fetch_batch_window_ms,
            fetch_max_batch_size=fetch_max_batch_size,
        )
        wire_name = f"{channel_type}:{name}"
        if wire_name in self.removing_channels:
            raise RuntimeError(CHANNEL_REMOVAL_IN_PROGRESS)
        entry = self.channels.get(wire_name)
        if entry is None:
            channel = ChannelState(
                self,
                wire_name,
                channel_type,
                fetch_config=fetch_config,
            )
            entry = ManagedChannel(channel, self.factory(channel))
            self.channels[wire_name] = entry
        elif entry.state.fetch_config != fetch_config:
            message = (
                f"channel {wire_name!r} already uses a different fetch configuration"
            )
            raise ValueError(message)
        return entry.facade

    @property
    def is_connected(self) -> bool:
        """Whether the realtime transport is connected."""
        return self.connection is not None and self.connection.is_connected

    async def remove_channel(
        self,
        name: str,
        *,
        channel_type: ChannelType = "broadcast",
    ) -> None:
        """Unsubscribe and forget one broadcast or presence channel."""
        channel_type = validate_channel_type(channel_type)
        wire_name = f"{channel_type}:{name}"
        async with self.connection_lock:
            entry = self.channels.get(wire_name)
            if entry is None:
                return
            channel = entry.state
            self.removing_channels.add(wire_name)
            try:
                await self._remove_channel_state(channel)
                del self.channels[wire_name]
            finally:
                self.removing_channels.remove(wire_name)

    async def remove_all_channels(self) -> None:
        """Unsubscribe and forget every managed channel."""
        async with self.connection_lock:
            first_error: Exception | None = None
            for wire_name, entry in tuple(self.channels.items()):
                error = await self._remove_registered_channel(wire_name, entry.state)
                first_error = first_error or error
            if first_error is not None:
                raise first_error

    async def _remove_registered_channel(
        self,
        wire_name: str,
        channel: ChannelState,
    ) -> Exception | None:
        self.removing_channels.add(wire_name)
        try:
            await self._remove_channel_state(channel)
        except CENTRIFUGE_ERROR as error:
            return error
        else:
            entry = self.channels.get(wire_name)
            if entry is not None and entry.state is channel:
                del self.channels[wire_name]
        finally:
            self.removing_channels.remove(wire_name)
        return None

    async def _remove_channel_state(self, channel: ChannelState) -> None:
        channel.supersede_subscribe_intent()
        await self._discard_subscription(channel)
        await channel.reset()

    async def _discard_subscription(self, channel: ChannelState) -> None:
        subscription = channel.subscription
        channel.subscription_events = None
        channel.pause_delivery()
        try:
            if subscription is not None:
                # Native state must change before any cancellable local cleanup.
                await _native.unsubscribe_native(subscription)
        finally:
            await channel.transport_lost()
        if subscription is not None and self.connection is not None:
            self.connection.remove_subscription(subscription)
        channel.subscription = None

    async def _token(self) -> str:
        lineage = self.connection_lineage()
        session = self._session_for_lineage(lineage)
        self.connection_access_token = session.access_token
        return session.access_token

    def _session_for_lineage(self, expected_lineage: SessionOperations) -> Session:
        _generation, lineage, session = self.client_context.capture_session_binding()
        if session is None:
            raise RuntimeError(NO_ACTIVE_SESSION)
        if lineage != expected_lineage:
            raise RuntimeError(CONNECTION_SESSION_CHANGED)
        return session

    def connection_lineage(self) -> SessionOperations:
        lineage = self.connection_session_lineage
        if lineage is None:
            raise RuntimeError(CONNECTION_SESSION_UNAVAILABLE)
        return lineage

    def connection_token(self) -> str:
        token = self.connection_access_token
        if token is None:
            raise RuntimeError(CONNECTION_SESSION_UNAVAILABLE)
        return token

    def _address(self) -> str:
        parsed = urlsplit(self.api_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        query = urlencode({"apikey": self.client_context.anon_token()}, quote_via=quote)
        return urlunsplit((scheme, parsed.netloc, "/realtime/v1/websocket", query, ""))

    async def _connect(self) -> _native.VolcanoCentrifugeConnection:
        async with self.connection_lock:
            return await self._connect_locked()

    async def _connect_locked(self) -> _native.VolcanoCentrifugeConnection:
        if self.connection is not None:
            _ = self._session_for_lineage(self.connection_lineage())
            return self.connection
        _generation, lineage, session = self.client_context.capture_session_binding()
        if session is None:
            raise RuntimeError(NO_ACTIVE_SESSION)
        connection = _native.VolcanoCentrifugeConnection(
            self.client_factory(
                self._address(),
                events=ClientEvents(self.enqueue_connection_callbacks),
                token=session.access_token,
                get_token=self._token,
            )
        )
        self.connection_session_lineage = lineage
        self.connection_access_token = session.access_token
        try:
            await connection.connect()
        except BaseException:
            self.connection_session_lineage = None
            self.connection_access_token = None
            raise
        try:
            current_session = self._session_for_lineage(lineage)
        except RuntimeError:
            self.connection = connection
            await connection.disconnect()
            self.connection = None
            self.connection_session_lineage = None
            self.connection_access_token = None
            raise
        self.connection_access_token = current_session.access_token
        self.connection = connection
        return connection

    async def subscribe(self, channel: ChannelState) -> None:
        # A later stop supersedes this request, including time spent waiting for locks.
        generation = channel.subscribe_generation
        async with channel.subscribe_lock:
            subscription = None
            try:
                async with self.connection_lock:
                    subscription = await self._prepare_subscription(channel, generation)
                    if channel.subscribed:
                        return
                    await self._resume_subscription(channel, subscription)
                await self._wait_subscription_readiness(channel, subscription)
            except BaseException as error:
                await self._cleanup_failed_subscription(channel, subscription, error)
                raise

    @staticmethod
    async def _resume_subscription(
        channel: ChannelState, subscription: CentrifugeSubscription
    ) -> None:
        channel.paused = False
        await subscription.subscribe()

    @staticmethod
    async def _wait_subscription_readiness(
        channel: ChannelState, subscription: CentrifugeSubscription
    ) -> None:
        channel.readiness_task = asyncio.create_task(
            wait_subscription(channel, subscription)
        )
        try:
            await channel.readiness_task
        finally:
            channel.clear_readiness_task()

    async def _cleanup_failed_subscription(
        self,
        channel: ChannelState,
        subscription: CentrifugeSubscription | None,
        error: BaseException,
    ) -> None:
        if (
            subscription is None
            or channel.subscription is not subscription
            or channel.paused
        ):
            # An explicit pause or removal owns the newer subscription intent.
            return
        channel.supersede_subscribe_intent()
        channel.subscription_events = None
        channel.pause_delivery()
        try:
            async with self.connection_lock:
                if channel.subscription is subscription:
                    await self._discard_subscription(channel)
        except CENTRIFUGE_ERROR:
            error.add_note("Failed to clean up the realtime subscription")

    async def _prepare_subscription(
        self, channel: ChannelState, generation: object
    ) -> CentrifugeSubscription:
        if generation is not channel.subscribe_generation:
            raise asyncio.CancelledError
        entry = self.channels.get(channel.name)
        if entry is None or entry.state is not channel:
            raise RuntimeError(CHANNEL_NOT_MANAGED)
        connection = await self._connect_locked()
        if channel.subscription is not None and channel.subscription_events is None:
            await self._discard_subscription(channel)
        if channel.subscription is None:
            channel.subscription_events = ChannelEvents(channel)
            channel.subscription = connection.new_subscription(
                channel.name,
                events=channel.subscription_events,
                join_leave=channel.type == "presence",
                recoverable=channel.type != "postgres",
            )
        return channel.subscription

    async def sync_presence(self, channel: ChannelState) -> None:
        if channel.subscription is None:
            return
        await channel.presence.begin_presence_sync()
        try:
            # Native replies must settle even after the roster refresh is cancelled.
            query = asyncio.create_task(channel.subscription.presence())
            query.add_done_callback(_native.consume_presence_result)
            result = await asyncio.shield(query)
        except CENTRIFUGE_ERROR as error:
            await self.report_presence_sync_failure(channel, error)
            return
        except BaseException:
            await channel.presence.abort_presence_sync()
            raise
        clients = _native.native_presence_clients(
            _native.native_attribute(result, "clients")
        )
        if clients is not None:
            await channel.presence.complete_presence_sync(clients)
        else:
            await channel.presence.abort_presence_sync()

    async def report_presence_sync_failure(
        self, channel: ChannelState, error: Exception
    ) -> None:
        try:
            await channel.presence.fail_presence_sync()
        except BaseException:
            await channel.presence.abort_presence_sync()
            raise
        code = _native.native_attribute(error, "code")
        self.enqueue_connection_callbacks(
            RealtimeErrorContext(
                code=code if isinstance(code, int) else None,
                message=str(error),
                error=error,
            ),
        )

    async def publish(self, channel: ChannelState, data: object) -> None:
        async with self.connection_lock:
            if channel.type != "broadcast":
                raise ValueError(BROADCAST_ONLY)
            subscription = channel.subscription
            if not channel.subscribed or subscription is None:
                raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
            _ = await subscription.publish(data)

    async def unsubscribe(self, channel: ChannelState) -> None:
        async with self.connection_lock:
            channel.supersede_subscribe_intent()
            if not channel.paused:
                channel.pause_delivery()
            if channel.subscription is not None:
                await _native.unsubscribe_native(channel.subscription)

    async def disconnect(self) -> None:
        """Disconnect and reset every channel managed by this facade."""
        async with self.connection_lock:
            connection = self.connection
            self.connection = None
            channels = tuple(entry.state for entry in self.channels.values())
            for channel in channels:
                channel.supersede_subscribe_intent()
                channel.invalidate()
            try:
                cancelled = await reset_realtime_channels(channels)
            finally:
                try:
                    if connection is not None:
                        await connection.disconnect()
                finally:
                    self.connection_session_lineage = None
                    self.connection_access_token = None
            if cancelled is not None:
                raise cancelled
