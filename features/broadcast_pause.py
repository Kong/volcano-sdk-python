from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from contract_support import ContractWorld

    from volcano_sdk.realtime import Channel


async def _publish_and_receive(
    publisher: Channel, received: asyncio.Queue[Any], message: dict[str, Any]
) -> Any:
    async with asyncio.timeout(10):
        await publisher.send(message)
        while True:
            delivered = await received.get()
            if delivered == message:
                return delivered


async def verify_broadcast_pause(world: ContractWorld) -> Any:
    subscriber, publisher = world.subscriber, world.publisher
    assert subscriber is not None
    assert publisher is not None
    received: asyncio.Queue[Any] = asyncio.Queue()
    delivered: list[Any] = []

    def on_message(message: Any) -> None:
        delivered.append(message)
        received.put_nowait(message)

    subscriber.on("message", on_message)
    baseline = {
        **world.realtime_message,
        "value": world.realtime_message["value"] + "-baseline",
    }
    await _publish_and_receive(publisher, received, baseline)
    await subscriber.unsubscribe()
    delivered.clear()
    await publisher.send(
        {**world.realtime_message, "value": world.realtime_message["value"] + "-paused"}
    )
    await asyncio.sleep(1)
    assert not delivered, "subscriber delivered a message while paused"
    await subscriber.subscribe()
    return await _publish_and_receive(publisher, received, world.realtime_message)
