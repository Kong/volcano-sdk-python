"""Owned subscription, delivery, and presence lifecycle for one channel."""

from __future__ import annotations

import asyncio
import inspect
from dataclasses import replace
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    TypeVar,
)

from centrifuge import SubscriptionEventHandler
from typing_extensions import override

import volcano_sdk._realtime_transport as _native

from ._realtime_fetch_worker import (
    PostgresFetchJob,
    PostgresFetchOutcome,
    PostgresFetchRequest,
    PostgresFetchWorker,
)
from ._realtime_messages import (
    CALLBACK_QUEUE_FULL_MESSAGE,
    CALLBACK_QUEUE_LIMIT,
    NO_PENDING_CALLBACK,
    POSTGRES_EVENTS,
    POSTGRES_FETCH_FAILED_MESSAGE,
    POSTGRES_ONLY,
    POSTGRES_QUEUE_LIMIT,
    CallbackDelivery,
    CentrifugeSubscription,
    ChannelType,
    PostgresChange,
    PostgresChangeCallback,
    PostgresDelivery,
    PostgresDeliveryIdentity,
    PostgresFetchConfig,
    PostgresListenerEvent,
    PublicationContext,
    RealtimeContext,
    RealtimePresenceInfo,
    UnsubscribeCallback,
    filter_postgres_changes,
    normalize_postgres_delete,
    postgres_change,
)
from ._realtime_presence import ChannelPresence

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from centrifuge import PublicationContext as NativePublicationContext

    from ._realtime_callbacks import (
        DynamicCallback,
    )
    from ._session_operations import SessionOperations
    from .models import JSONValue

from typing import Protocol

_MessageT = TypeVar("_MessageT")


class RealtimeOperations(Protocol):
    client_context: RealtimeContext
    callback_tasks: set[asyncio.Task[None]]

    @property
    def database_name(self) -> str | None: ...
    def connection_lineage(self) -> SessionOperations: ...
    def connection_token(self) -> str: ...
    async def fetch_postgres_rows(
        self, requests: tuple[PostgresFetchRequest, ...]
    ) -> tuple[Mapping[str, JSONValue] | None, ...]: ...
    async def subscribe(self, channel: ChannelState) -> None: ...
    async def publish(self, channel: ChannelState, data: object) -> None: ...
    async def unsubscribe(self, channel: ChannelState) -> None: ...
    async def sync_presence(self, channel: ChannelState) -> None: ...


class ChannelEvents(SubscriptionEventHandler):
    def __init__(self, channel: ChannelState) -> None:
        self.channel: ChannelState = channel

    def is_current(self) -> bool:
        return self.channel.subscription_events is self

    @override
    async def on_publication(
        self, ctx: PublicationContext | NativePublicationContext
    ) -> None:
        if not self.is_current() or self.channel.paused or not self.channel.subscribed:
            return
        if self.channel.type == "postgres":
            await self.channel.receive_postgres_change(ctx.pub.data)
            return
        await self.channel.emit("message", ctx.pub.data)

    @override
    async def on_subscribing(self, ctx: object) -> None:
        del ctx
        if self.is_current():
            await self.channel.transport_lost()

    @override
    async def on_subscribed(self, ctx: object) -> None:
        del ctx
        if not self.is_current() or self.channel.paused:
            return
        self.channel.subscribed = True
        await self.channel.begin_postgres_epoch()
        if self.channel.type == "presence":
            self.channel.presence.schedule_presence_sync()

    @override
    async def on_unsubscribed(self, ctx: object) -> None:
        del ctx
        if self.is_current():
            await self.channel.transport_lost()

    @override
    async def on_join(self, ctx: object) -> None:
        if self.is_current():
            await self.channel.presence.presence_join(
                _native.native_attribute(ctx, "info")
            )

    @override
    async def on_leave(self, ctx: object) -> None:
        if self.is_current():
            await self.channel.presence.presence_leave(
                _native.native_attribute(ctx, "info")
            )


async def wait_subscription(
    channel: ChannelState, subscription: CentrifugeSubscription
) -> None:
    await subscription.ready()
    if channel.type == "presence":
        await channel.presence.wait_presence_sync()
    if channel.subscription is not subscription or not channel.subscribed:
        message = "realtime subscription was interrupted"
        raise RuntimeError(message)


class ChannelState:
    """Own channel subscription and ordered message delivery."""

    def __init__(
        self,
        realtime: RealtimeOperations,
        name: str,
        channel_type: ChannelType,
        *,
        fetch_config: PostgresFetchConfig,
    ) -> None:
        """Create a channel managed by a realtime facade."""
        self.realtime: RealtimeOperations = realtime
        self.presence: ChannelPresence = ChannelPresence(
            self, lambda: realtime.sync_presence(self)
        )
        self.wire_name: str = name
        self.type: ChannelType = channel_type
        self.fetch_config: PostgresFetchConfig = fetch_config
        self.callbacks: dict[str, list[DynamicCallback]] = {}
        self.presence_state: dict[str, RealtimePresenceInfo] = {}
        self.presence_events: list[tuple[str, RealtimePresenceInfo]] = []
        self.presence_syncing: bool = False
        self.tracked_value: Mapping[str, JSONValue] = MappingProxyType({})
        self.subscribe_lock: asyncio.Lock = asyncio.Lock()
        # Fresh identities invalidate stale work without implying an order.
        self.subscribe_generation: object
        self.supersede_subscribe_intent()
        self.readiness_task: asyncio.Task[None] | None = None
        self.subscription: CentrifugeSubscription | None = None
        self.subscription_events: ChannelEvents | None = None
        self.subscribed: bool
        self.paused: bool
        self.delivery_epoch: object
        self.presence_epoch: object
        self.presence_lock: asyncio.Lock = asyncio.Lock()
        self.presence_sync_task: asyncio.Task[None] | None = None
        self.presence_sync_pending: bool = False
        self.callback_queue: asyncio.Queue[CallbackDelivery] = asyncio.Queue(
            maxsize=CALLBACK_QUEUE_LIMIT
        )
        self.callback_task: asyncio.Task[None] | None = None
        self.pending_presence_sync: object
        self.postgres_epoch: object
        self._rotate_postgres_epoch()
        self.postgres_session_lineage: SessionOperations | None = None
        self.postgres_lock: asyncio.Lock = asyncio.Lock()
        self.postgres_worker: PostgresFetchWorker[PostgresDelivery] | None = None
        self.postgres_filters: dict[
            int,
            tuple[PostgresListenerEvent, str, str],
        ] = {}
        self.pause_delivery()

    def supersede_subscribe_intent(self) -> None:
        self.subscribe_generation = object()

    def _rotate_postgres_epoch(self) -> None:
        self.postgres_epoch = object()

    def clear_readiness_task(self) -> None:
        self.readiness_task = None

    @property
    def name(self) -> str:
        """Canonical channel name sent to realtime."""
        return self.wire_name

    def on(self, event: str, callback: Callable[[_MessageT], object]) -> ChannelState:
        """Register a callback for messages or presence events.

        Returns
        -------
        ChannelState
            This channel, for chaining listener registrations.

        Raises
        ------
        ValueError
            The event is not supported by this channel type.

        """
        allowed_events = {
            "broadcast": {"message"},
            "presence": {"message", "join", "leave", "presence_sync"},
            "postgres": {"*"},
        }[self.type]
        if event not in allowed_events:
            message = f"unsupported realtime event: {event}"
            raise ValueError(message)
        self.callbacks.setdefault(event, []).append(callback)
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

        Raises
        ------
        ValueError
            The channel is not a Postgres channel or the event is unsupported.

        """
        if self.type != "postgres":
            raise ValueError(POSTGRES_ONLY)
        if event not in {*POSTGRES_EVENTS, "*"}:
            message = f"unsupported Postgres change event: {event}"
            raise ValueError(message)

        filtered = filter_postgres_changes(event, schema, table, callback)

        self.callbacks.setdefault("*", []).append(filtered)
        self.postgres_filters[id(filtered)] = (event, schema, table)

        def unsubscribe() -> None:
            callbacks = self.callbacks["*"]
            if filtered in callbacks:
                callbacks.remove(filtered)
            _ = self.postgres_filters.pop(id(filtered), None)

        return unsubscribe

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
        self.presence.ensure_presence()
        self.callbacks.setdefault("presence_sync", []).append(callback)

        def unsubscribe() -> None:
            callbacks = self.callbacks["presence_sync"]
            if callback in callbacks:
                callbacks.remove(callback)

        return unsubscribe

    def _capture_postgres_delivery_identity(self) -> PostgresDeliveryIdentity:
        return PostgresDeliveryIdentity(
            session_lineage=self.postgres_session_lineage,
            subscription_epoch=self.postgres_epoch,
        )

    async def begin_postgres_epoch(self) -> None:
        if self.type != "postgres":
            return
        await self._stop_postgres_worker()
        self._rotate_postgres_epoch()
        self.postgres_session_lineage = self.realtime.connection_lineage()

    async def _end_postgres_epoch(self) -> None:
        if self.type != "postgres":
            return
        self._rotate_postgres_epoch()
        await self._stop_postgres_worker()

    async def _stop_postgres_worker(self) -> None:
        async with self.postgres_lock:
            worker = self.postgres_worker
            self.postgres_worker = None
        if worker is not None:
            await worker.abort()

    def _postgres_delivery_is_current(
        self,
        identity: PostgresDeliveryIdentity,
    ) -> bool:
        _generation, lineage, session = (
            self.realtime.client_context.capture_session_binding()
        )
        return (
            self.subscribed
            and session is not None
            and identity.subscription_epoch is self.postgres_epoch
            and identity.session_lineage == lineage
        )

    def _has_postgres_listener(self, change: PostgresChange) -> bool:
        for callback in self.callbacks.get("*", []):
            listener_filter = self.postgres_filters.get(id(callback))
            if listener_filter is None:
                return True
            event, schema, table = listener_filter
            if (
                event in {"*", change.type}
                and schema == change.schema
                and table == change.table
            ):
                return True
        return False

    def _postgres_fetch_request(
        self,
        change: PostgresChange,
    ) -> PostgresFetchRequest | None:
        database_name = self.realtime.database_name
        if (
            not self.fetch_config.enabled
            or change.mode != "lightweight"
            or change.type == "DELETE"
            or change.id is None
            or database_name is None
        ):
            return None
        return PostgresFetchRequest(
            database_name=database_name,
            access_token=self.realtime.connection_token(),
            table=(
                change.table
                if change.schema == "public"
                else f"{change.schema}.{change.table}"
            ),
            row_id=change.id,
        )

    def _postgres_delivery(self, data: object) -> PostgresDelivery | None:
        change = postgres_change(data)
        if change is None or not self._has_postgres_listener(change):
            return None
        change = normalize_postgres_delete(change)
        identity = self._capture_postgres_delivery_identity()
        if not self._postgres_delivery_is_current(identity):
            return None
        return PostgresDelivery(change=change, identity=identity)

    async def postgres_delivery_worker(
        self,
        identity: PostgresDeliveryIdentity,
    ) -> PostgresFetchWorker[PostgresDelivery] | None:
        async with self.postgres_lock:
            if not self._postgres_delivery_is_current(identity):
                return None
            if self.postgres_worker is None:
                self.postgres_worker = PostgresFetchWorker(
                    self.realtime.fetch_postgres_rows,
                    self._deliver_postgres,
                    queue_limit=POSTGRES_QUEUE_LIMIT,
                    batch_window_seconds=self.fetch_config.batch_window_seconds,
                    max_batch_size=self.fetch_config.max_batch_size,
                )
            return self.postgres_worker

    async def receive_postgres_change(self, data: object) -> None:
        delivery = self._postgres_delivery(data)
        if delivery is None:
            return
        request = self._postgres_fetch_request(delivery.change)
        worker = await self.postgres_delivery_worker(delivery.identity)
        if worker is None:
            return
        try:
            await worker.enqueue(PostgresFetchJob(request=request, fallback=delivery))
        except RuntimeError:
            if self._postgres_delivery_is_current(delivery.identity):
                raise

    async def _deliver_postgres(
        self,
        outcome: PostgresFetchOutcome[PostgresDelivery],
    ) -> None:
        delivery = outcome.job.fallback
        if not self._postgres_delivery_is_current(delivery.identity):
            return
        change = delivery.change
        if outcome.record is not None:
            change = replace(change, record=outcome.record, id=None, mode=None)
        elif outcome.job.request is not None:
            self._report_postgres_fetch_failure(
                change,
                outcome.job.request,
                outcome.error,
            )
        if self._postgres_delivery_is_current(delivery.identity):
            await self.emit(
                "*",
                change,
                postgres_identity=delivery.identity,
            )

    def _report_postgres_fetch_failure(
        self,
        change: PostgresChange,
        request: PostgresFetchRequest,
        error: Exception | None,
    ) -> None:
        if error is None:
            identifier = f"{change.schema}.{change.table}:{request.row_id}"
            message = f"Postgres row not found: {identifier}"
            error = LookupError(message)
        asyncio.get_running_loop().call_exception_handler(
            {
                "message": POSTGRES_FETCH_FAILED_MESSAGE,
                "exception": error,
                "channel": self.name,
            }
        )

    async def subscribe(self) -> None:
        """Wait until this channel is subscribed and ready for use."""
        await self.realtime.subscribe(self)

    async def send(self, data: object) -> None:
        """Publish a broadcast payload to this channel."""
        await self.realtime.publish(self, data)

    async def unsubscribe(self) -> None:
        """Unsubscribe from this channel."""
        await self.realtime.unsubscribe(self)

    async def emit(
        self,
        event: str,
        data: object,
        *,
        postgres_identity: PostgresDeliveryIdentity | None = None,
    ) -> None:
        if not self.callbacks.get(event):
            return
        if event == "presence_sync":
            self.pending_presence_sync = NO_PENDING_CALLBACK
        delivery = CallbackDelivery(
            event,
            data,
            postgres_identity,
            self._callback_epoch(event) if postgres_identity is None else None,
        )
        if not self._queue_callback(delivery):
            return
        task = self.callback_task
        if task is None or task.done():
            self._start_callback_dispatcher()

    def _queue_callback(self, delivery: CallbackDelivery) -> bool:
        try:
            self.callback_queue.put_nowait(delivery)
        except asyncio.QueueFull:
            if delivery.event == "presence_sync":
                self.pending_presence_sync = delivery.data
                return False
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": CALLBACK_QUEUE_FULL_MESSAGE,
                    "channel": self.name,
                }
            )
        return True

    def _start_callback_dispatcher(self) -> None:
        task = asyncio.create_task(self._dispatch_callbacks())
        self.callback_task = task
        # Retain running application work even if its channel is removed.
        self.realtime.callback_tasks.add(task)
        task.add_done_callback(self._callback_dispatcher_finished)

    def _callback_dispatcher_finished(self, task: asyncio.Task[None]) -> None:
        self.realtime.callback_tasks.discard(task)
        if self.callback_task is task:
            self.callback_task = None
        if not task.cancelled() and (error := task.exception()) is not None:
            asyncio.get_running_loop().call_exception_handler(
                {
                    "message": "Volcano realtime callback dispatcher failed",
                    "exception": error,
                    "channel": self.name,
                }
            )

    async def _dispatch_callbacks(self) -> None:
        try:
            # Register the worker before user code can re-enter through eager tasks.
            await asyncio.sleep(0)
            while not self.callback_queue.empty():
                delivery = self.callback_queue.get_nowait()
                try:
                    await self.dispatch_delivery(delivery)
                finally:
                    self.callback_queue.task_done()
                    self._enqueue_pending_presence_sync()
        finally:
            # Event-loop cancellation must not leave queued delivery to restart.
            self._discard_callbacks()

    async def dispatch_delivery(self, delivery: CallbackDelivery) -> None:
        if not self._callback_delivery_is_current(delivery):
            return
        for callback in tuple(self.callbacks.get(delivery.event, [])):
            if not self._callback_delivery_is_current(delivery):
                return
            # Isolate a callback's own cancellation from later delivery.
            (error,) = await asyncio.gather(
                self._run_callback(callback, delivery),
                return_exceptions=True,
            )
            if isinstance(error, BaseException):
                asyncio.get_running_loop().call_exception_handler(
                    {
                        "message": "Volcano realtime callback failed",
                        "exception": error,
                        "channel": self.name,
                    }
                )

    def _callback_delivery_is_current(self, delivery: CallbackDelivery) -> bool:
        if delivery.delivery_epoch is not None:
            return (
                not self.paused or delivery.event == "presence_sync"
            ) and delivery.delivery_epoch is self._callback_epoch(delivery.event)
        identity = delivery.postgres_identity
        return identity is None or self._postgres_delivery_is_current(identity)

    def _callback_epoch(self, event: str) -> object:
        if event in {"join", "leave", "presence_sync"}:
            return self.presence_epoch
        return self.delivery_epoch

    def _enqueue_pending_presence_sync(self) -> None:
        pending = self.pending_presence_sync
        if pending is NO_PENDING_CALLBACK or self.callback_queue.full():
            return
        self.pending_presence_sync = NO_PENDING_CALLBACK
        self.callback_queue.put_nowait(
            CallbackDelivery(
                "presence_sync", pending, delivery_epoch=self.presence_epoch
            )
        )

    async def _run_callback(
        self,
        callback: DynamicCallback,
        delivery: CallbackDelivery,
    ) -> None:
        if not self._callback_delivery_is_current(delivery):
            return
        result = callback(delivery.data)
        if inspect.isawaitable(result):
            await result

    async def reset(self) -> None:
        self.invalidate()
        await self._end_postgres_epoch()
        await self.presence.cancel_presence_sync()
        self.presence_state.clear()
        self.presence.discard_presence_sync()
        self.tracked_value = MappingProxyType({})
        self.subscribed = False

    def invalidate(self) -> None:
        if self.readiness_task is not None:
            _ = self.readiness_task.cancel()
        self.subscription = None
        self.subscription_events = None
        self.pause_delivery()

    def pause_delivery(self) -> None:
        self.paused = True
        self.subscribed = False
        self._discard_callbacks()

    def _discard_callbacks(self, *, presence_only: bool = False) -> None:
        self.presence_epoch = object()
        if not presence_only:
            self.delivery_epoch = object()
        # Free capacity before recovered publications arrive behind a slow callback.
        for _ in range(self.callback_queue.qsize()):
            delivery = self.callback_queue.get_nowait()
            if presence_only and delivery.event == "message":
                # Requeue before task_done so queue.join cannot finish prematurely.
                self.callback_queue.put_nowait(delivery)
            self.callback_queue.task_done()
        self.pending_presence_sync = NO_PENDING_CALLBACK

    async def transport_lost(self) -> None:
        self.subscribed = False
        # Recoverable channels already include queued messages in their offsets.
        if not self.paused and self.type != "broadcast":
            self._discard_callbacks(presence_only=self.type == "presence")
        await self._end_postgres_epoch()
        await self.presence.presence_unsubscribed()


async def reset_realtime_channels(
    channels: tuple[ChannelState, ...],
) -> asyncio.CancelledError | None:
    cancelled: asyncio.CancelledError | None = None
    for channel in channels:
        try:
            await channel.reset()
        except asyncio.CancelledError as error:
            cancelled = error
    return cancelled
