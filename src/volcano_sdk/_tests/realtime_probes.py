"""Typed state probes for the realtime facades used by runtime tests."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Never, TypeVar

import pytest

from volcano_sdk import _realtime_connection as connection_module
from volcano_sdk import client as client_module
from volcano_sdk import realtime as realtime_module
from volcano_sdk._realtime_channel import ChannelState
from volcano_sdk._realtime_connection import RealtimeState
from volcano_sdk._realtime_fetch_worker import PostgresFetchWorker
from volcano_sdk.realtime import Channel, Realtime

if TYPE_CHECKING:
    from volcano_sdk._realtime_callbacks import ConnectionDelivery, DynamicCallback
    from volcano_sdk._realtime_fetch_worker import (
        PostgresFetchJob,
        PostgresFetchOutcome,
        PostgresFetchRequest,
        StopWorker,
    )
    from volcano_sdk._realtime_messages import (
        CallbackDelivery,
        CentrifugeSubscription,
        PostgresChange,
        PostgresDelivery,
        PostgresDeliveryIdentity,
        RealtimeConnectContext,
        RealtimeDisconnectContext,
        RealtimeErrorContext,
    )
    from volcano_sdk._realtime_transport import VolcanoCentrifugeConnection
    from volcano_sdk._session_operations import SessionOperations
    from volcano_sdk.models import Session


class InspectableChannel(Channel):
    @property
    def state(self) -> ChannelState:
        state = self._state
        assert isinstance(state, ChannelState)
        return state


class InspectableRealtime(Realtime):
    @property
    def state(self) -> RealtimeState[Channel]:
        return self._state


def channel_state(channel: Channel) -> InspectedChannelState:
    if not isinstance(channel, InspectableChannel):
        message = "expected a realtime channel with a typed state probe"
        raise TypeError(message)
    state = channel.state
    assert isinstance(state, InspectedChannelState)
    return state


def realtime_state(realtime: Realtime) -> InspectedRealtimeState:
    if not isinstance(realtime, InspectableRealtime):
        message = "expected a realtime facade with a typed state probe"
        raise TypeError(message)
    state = realtime.state
    assert isinstance(state, InspectedRealtimeState)
    return state


@pytest.fixture(autouse=True)
def realtime_state_probes(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(client_module, "Realtime", InspectableRealtime)
    monkeypatch.setattr(realtime_module, "Channel", InspectableChannel)
    monkeypatch.setattr(realtime_module, "RealtimeState", InspectedRealtimeState)
    monkeypatch.setattr(connection_module, "ChannelState", InspectedChannelState)


WorkerValueT = TypeVar("WorkerValueT")


class InspectableFetchWorker(PostgresFetchWorker[WorkerValueT]):
    @property
    def background_task(self) -> asyncio.Task[None] | None:
        return self._task

    @property
    def stop_task(self) -> asyncio.Task[None] | None:
        return self._stop_task

    @property
    def queue(self) -> asyncio.Queue[PostgresFetchJob[WorkerValueT] | StopWorker]:
        return self._queue

    @queue.setter
    def queue(
        self, value: asyncio.Queue[PostgresFetchJob[WorkerValueT] | StopWorker]
    ) -> None:
        self._queue: asyncio.Queue[PostgresFetchJob[WorkerValueT] | StopWorker] = value

    async def put_while_running(
        self, job: PostgresFetchJob[WorkerValueT], task: asyncio.Task[None]
    ) -> None:
        await self._put_while_running(job, task)

    async def next_before(
        self, deadline: float
    ) -> PostgresFetchJob[WorkerValueT] | StopWorker | None:
        return await self._next_before(deadline)


class InspectedChannelState(ChannelState):
    def rotate_postgres_epoch(self) -> None:
        return self._rotate_postgres_epoch()

    def capture_postgres_delivery_identity(self) -> PostgresDeliveryIdentity:
        return self._capture_postgres_delivery_identity()

    async def end_postgres_epoch(self) -> None:
        return await self._end_postgres_epoch()

    async def stop_postgres_worker(self) -> None:
        return await self._stop_postgres_worker()

    def postgres_delivery_is_current(self, identity: PostgresDeliveryIdentity) -> bool:
        return self._postgres_delivery_is_current(identity)

    def has_postgres_listener(self, change: PostgresChange) -> bool:
        return self._has_postgres_listener(change)

    def postgres_fetch_request(
        self, change: PostgresChange
    ) -> PostgresFetchRequest | None:
        return self._postgres_fetch_request(change)

    def postgres_delivery(self, data: object) -> PostgresDelivery | None:
        return self._postgres_delivery(data)

    async def deliver_postgres(
        self, outcome: PostgresFetchOutcome[PostgresDelivery]
    ) -> None:
        return await self._deliver_postgres(outcome)

    def report_postgres_fetch_failure(
        self,
        change: PostgresChange,
        request: PostgresFetchRequest,
        error: Exception | None,
    ) -> None:
        return self._report_postgres_fetch_failure(change, request, error)

    def queue_callback(self, delivery: CallbackDelivery) -> bool:
        return self._queue_callback(delivery)

    def start_callback_dispatcher(self) -> None:
        return self._start_callback_dispatcher()

    def callback_dispatcher_finished(self, task: asyncio.Task[None]) -> None:
        return self._callback_dispatcher_finished(task)

    async def dispatch_callbacks(self) -> None:
        return await self._dispatch_callbacks()

    def callback_delivery_is_current(self, delivery: CallbackDelivery) -> bool:
        return self._callback_delivery_is_current(delivery)

    def callback_epoch(self, event: str) -> object:
        return self._callback_epoch(event)

    def enqueue_pending_presence_sync(self) -> None:
        return self._enqueue_pending_presence_sync()

    async def run_callback(
        self, callback: DynamicCallback, delivery: CallbackDelivery
    ) -> None:
        return await self._run_callback(callback, delivery)

    def discard_callbacks(self, *, presence_only: bool = False) -> None:
        return self._discard_callbacks(presence_only=presence_only)


class InspectedRealtimeState(RealtimeState[Channel]):
    async def connect(self) -> VolcanoCentrifugeConnection:
        return await self._connect()

    def connection_delivery(
        self,
        context: RealtimeConnectContext
        | RealtimeDisconnectContext
        | RealtimeErrorContext,
    ) -> ConnectionDelivery:
        return self._connection_delivery(context)

    async def drain_connection_callbacks(self) -> None:
        return await self._drain_connection_callbacks()

    async def remove_registered_channel(
        self, wire_name: str, channel: ChannelState
    ) -> Exception | None:
        return await self._remove_registered_channel(wire_name, channel)

    async def remove_channel_state(self, channel: ChannelState) -> None:
        return await self._remove_channel_state(channel)

    async def discard_subscription(self, channel: ChannelState) -> None:
        return await self._discard_subscription(channel)

    async def token(self) -> str:
        return await self._token()

    def session_for_lineage(self, expected_lineage: SessionOperations) -> Session:
        return self._session_for_lineage(expected_lineage)

    def address(self) -> str:
        return self._address()

    async def connect_locked(self) -> VolcanoCentrifugeConnection:
        return await self._connect_locked()

    @classmethod
    async def resume_subscription(
        cls, channel: ChannelState, subscription: CentrifugeSubscription
    ) -> None:
        return await cls._resume_subscription(channel, subscription)

    @classmethod
    async def wait_subscription_readiness(
        cls, channel: ChannelState, subscription: CentrifugeSubscription
    ) -> None:
        return await cls._wait_subscription_readiness(channel, subscription)

    async def cleanup_failed_subscription(
        self,
        channel: ChannelState,
        subscription: CentrifugeSubscription | None,
        error: BaseException,
    ) -> None:
        return await self._cleanup_failed_subscription(channel, subscription, error)

    async def prepare_subscription(
        self, channel: ChannelState, generation: object
    ) -> CentrifugeSubscription:
        return await self._prepare_subscription(channel, generation)


ResultT = TypeVar("ResultT")


def completed_operation(value: ResultT) -> asyncio.Future[ResultT]:
    result: asyncio.Future[ResultT] = asyncio.get_running_loop().create_future()
    result.set_result(value)
    return result


def failed_operation(error: BaseException) -> asyncio.Future[Never]:
    result: asyncio.Future[Never] = asyncio.get_running_loop().create_future()
    result.set_exception(error)
    return result
