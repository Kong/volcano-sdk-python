from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from contract_support import ContractWorld

    from volcano_sdk.realtime import Channel, RealtimePresenceInfo


class PresenceObserver:
    def __init__(self, channel: Channel, user_id: str) -> None:
        self.channel = channel
        self.user_id = user_id
        self.changed = asyncio.Event()
        self.snapshots: list[set[str]] = []
        self.unsubscribe = channel.on_presence_sync(self.record)

    def record(self, state: Mapping[str, RealtimePresenceInfo]) -> None:
        self.snapshots.append(set(state))
        self.changed.set()

    async def wait(self, predicate: Callable[[], bool]) -> None:
        async with asyncio.timeout(10):
            while True:
                self.changed.clear()
                if predicate():
                    return
                await self.changed.wait()

    async def roster(self, count: int) -> set[str]:
        await self.wait(lambda: len(self.channel.get_presence_state()) == count)
        state = self.channel.get_presence_state()
        assert all(info.user == self.user_id for info in state.values())
        assert all(key == info.client and key for key, info in state.items())
        return set(state)


async def verify_presence_membership(world: ContractWorld) -> list[int]:
    first, second = [
        client.realtime.channel(world.realtime_channel, channel_type="presence")
        for client in world.realtime_clients
    ]
    first_observer = PresenceObserver(first, world.fixture["user_id"])
    second_observer = PresenceObserver(second, world.fixture["user_id"])
    try:
        await first.subscribe()
        initial = await first_observer.roster(1)
        await second.subscribe()
        joined = await first_observer.roster(2)
        assert joined == await second_observer.roster(2)
        assert initial < joined
        await second.unsubscribe()
        assert await first_observer.roster(1) == initial
        await first_observer.wait(
            lambda: _observed_membership(first_observer.snapshots, initial, joined)
        )
        return [1, 2, 1]
    finally:
        first_observer.unsubscribe()
        second_observer.unsubscribe()
        await asyncio.gather(first.unsubscribe(), second.unsubscribe())


def _observed_membership(
    snapshots: list[set[str]], initial: set[str], joined: set[str]
) -> bool:
    expected = iter([initial, joined, initial])
    target: set[str] | None = next(expected)
    for state in snapshots:
        if state == target:
            target = next(expected, None)
            if target is None:
                return True
    return False
