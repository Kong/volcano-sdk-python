"""Presence membership and snapshot lifecycle for a realtime channel."""

from __future__ import annotations

import asyncio
from types import MappingProxyType
from typing import TYPE_CHECKING, Protocol

from ._realtime_messages import (
    CHANNEL_NOT_SUBSCRIBED,
    PRESENCE_ONLY,
    ChannelType,
    RealtimePresenceInfo,
    freeze_mapping,
    presence_info,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable, Mapping

    from .models import JSONValue


class PresenceChannel(Protocol):
    type: ChannelType
    subscribed: bool
    presence_state: dict[str, RealtimePresenceInfo]
    presence_events: list[tuple[str, RealtimePresenceInfo]]
    presence_syncing: bool
    tracked_value: Mapping[str, JSONValue]
    presence_lock: asyncio.Lock
    presence_sync_task: asyncio.Task[None] | None
    presence_sync_pending: bool

    async def emit(self, event: str, data: object) -> None: ...


class ChannelPresence:
    def __init__(
        self, channel: PresenceChannel, sync: Callable[[], Awaitable[None]]
    ) -> None:
        self.channel: PresenceChannel = channel
        self.sync: Callable[[], Awaitable[None]] = sync

    async def track(self, state: Mapping[str, JSONValue] | None = None) -> None:
        """Store local presence state while server identity remains authoritative.

        Requires a presence channel.

        Raises
        ------
        RuntimeError
            The channel is not subscribed.

        """
        self.ensure_presence()
        if not self.channel.subscribed:
            raise RuntimeError(CHANNEL_NOT_SUBSCRIBED)
        self.channel.tracked_value = freeze_mapping(state or {})

    def get_presence_state(self) -> Mapping[str, RealtimePresenceInfo]:
        """Read the clients currently present.

        Requires a presence channel.

        Returns
        -------
        Mapping[str, RealtimePresenceInfo]
            An immutable snapshot indexed by client identifier.

        """
        self.ensure_presence()
        return MappingProxyType(dict(self.channel.presence_state))

    @property
    def tracked_state(self) -> Mapping[str, JSONValue]:
        """Immutable snapshot of this client's local presence state."""
        self.ensure_presence()
        return MappingProxyType(dict(self.channel.tracked_value))

    def ensure_presence(self) -> None:
        if self.channel.type != "presence":
            raise ValueError(PRESENCE_ONLY)

    def replace_presence(self, clients: Mapping[str, object]) -> None:
        self.channel.presence_state = {
            client_id: presence_info(info) for client_id, info in clients.items()
        }

    async def begin_presence_sync(self) -> None:
        async with self.channel.presence_lock:
            self.channel.presence_syncing = True
            self.channel.presence_events.clear()

    async def complete_presence_sync(self, clients: Mapping[str, object]) -> None:
        async with self.channel.presence_lock:
            if not self.channel.subscribed:
                self.discard_presence_sync()
                return
            self.replace_presence(clients)
            for event, presence in self.channel.presence_events:
                self.apply_presence_event(event, presence)
            self.discard_presence_sync()
            await self.channel.emit("presence_sync", self.get_presence_state())

    async def abort_presence_sync(self) -> None:
        async with self.channel.presence_lock:
            self.discard_presence_sync()

    async def fail_presence_sync(self) -> None:
        async with self.channel.presence_lock:
            self.discard_presence_sync()
            if not self.channel.subscribed:
                return
            self.channel.presence_state.clear()
            await self.channel.emit("presence_sync", self.get_presence_state())

    def discard_presence_sync(self) -> None:
        self.channel.presence_syncing = False
        self.channel.presence_events.clear()

    def apply_presence_event(self, event: str, presence: RealtimePresenceInfo) -> None:
        if event == "join":
            self.channel.presence_state[presence.client] = presence
        if event == "leave":
            _ = self.channel.presence_state.pop(presence.client, None)

    async def presence_join(self, info: object) -> None:
        if self.channel.type != "presence" or info is None:
            return
        async with self.channel.presence_lock:
            if not self.channel.subscribed:
                return
            presence = presence_info(info)
            if self.channel.presence_syncing:
                self.channel.presence_events.append(("join", presence))
            self.apply_presence_event("join", presence)
            await self.channel.emit("join", presence)
            await self.channel.emit("presence_sync", self.get_presence_state())

    async def presence_leave(self, info: object) -> None:
        if self.channel.type != "presence" or info is None:
            return
        async with self.channel.presence_lock:
            if not self.channel.subscribed:
                return
            presence = presence_info(info)
            if self.channel.presence_syncing:
                self.channel.presence_events.append(("leave", presence))
            self.apply_presence_event("leave", presence)
            await self.channel.emit("leave", presence)
            await self.channel.emit("presence_sync", self.get_presence_state())

    async def presence_unsubscribed(self) -> None:
        if self.channel.type != "presence":
            return
        await self.cancel_presence_sync()
        async with self.channel.presence_lock:
            self.discard_presence_sync()
            self.channel.presence_state.clear()
            self.channel.tracked_value = MappingProxyType({})
            await self.channel.emit("presence_sync", self.get_presence_state())

    def schedule_presence_sync(self) -> None:
        task = self.channel.presence_sync_task
        if task is not None and (not task.done()):
            self.channel.presence_sync_pending = True
            return
        self.channel.presence_sync_pending = False
        self.channel.presence_sync_task = asyncio.create_task(self.run_presence_sync())

    async def run_presence_sync(self) -> None:
        try:
            while self.channel.subscribed:
                await self.sync()
                await asyncio.sleep(0)
                if not self.channel.presence_sync_pending:
                    return
                self.channel.presence_sync_pending = False
        finally:
            if asyncio.current_task() is self.channel.presence_sync_task:
                self.channel.presence_sync_task = None

    async def wait_presence_sync(self) -> None:
        task = self.channel.presence_sync_task
        if task is not None:
            await asyncio.shield(task)

    async def cancel_presence_sync(self) -> None:
        task = self.channel.presence_sync_task
        self.channel.presence_sync_task = None
        if task is None or task.done():
            return
        _ = task.cancel()
        _ = await asyncio.gather(task, return_exceptions=True)
