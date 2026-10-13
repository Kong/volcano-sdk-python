"""Ordered, once-each delivery of the messages a durable execution publishes."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from ._durable_message_response import durable_message

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .models import DurableMessage, DurableMessagePage


def _published(data: object) -> DurableMessage | None:
    try:
        message = durable_message(data)
    except TypeError:
        return None
    return message if message.direction == "out" else None


def _report_failed_catch_up(task: asyncio.Task[None]) -> None:
    if task.cancelled() or (error := task.exception()) is None:
        return
    asyncio.get_running_loop().call_exception_handler(
        {"message": "Volcano durable message catch-up failed", "exception": error}
    )


class DurableMessageStream:
    """Deliver messages in `seq` order, once each, from the channel and the list.

    A live message can only be delivered once everything before it has been
    listed, or the missed ones would fall below the last delivered `seq` and be
    skipped. So live messages are held until the first catch-up starts, and
    while any catch-up is reading, then released in order.

    The channel itself drops publications while it is not subscribed, and
    reports each resubscription, which starts a catch-up of what it dropped.
    """

    def __init__(
        self,
        deliver: Callable[[DurableMessage], Awaitable[None]],
        list_after: Callable[[int], Awaitable[DurableMessagePage]],
    ) -> None:
        """Deliver through `deliver`, reading missed messages with `list_after`."""
        self._handler: Callable[[DurableMessage], Awaitable[None]] = deliver
        self._list_after: Callable[[int], Awaitable[DurableMessagePage]] = list_after
        self._last_seq: int = 0
        self._started: bool = False
        self._catch_ups: int = 0
        self._held: list[DurableMessage] = []
        self._closed: bool = False
        self._reads: asyncio.Lock = asyncio.Lock()
        self._tasks: set[asyncio.Task[None]] = set()

    async def live(self, data: object) -> None:
        """Deliver a channel publication, or hold it until a catch-up releases it."""
        message = _published(data)
        if message is None:
            return
        if not self._started or self._catch_ups > 0:
            self._held.append(message)
            return
        await self._deliver(message)

    def resubscribed(self) -> None:
        """Catch up on what the channel dropped while it was not subscribed."""
        # A failed catch-up leaves the gap until the next one; live delivery
        # goes on.
        self.catch_up().add_done_callback(_report_failed_catch_up)

    def catch_up(self) -> asyncio.Task[None]:
        """Read what was missed, then release the held messages.

        Counted before the task starts, so nothing is delivered live while a
        read waits its turn.

        Returns
        -------
        asyncio.Task[None]
            The read, which fails with the list's or the handler's error.

        """
        self._started = True
        self._catch_ups += 1
        task = asyncio.create_task(self._read_missed())
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def close(self) -> None:
        """Deliver nothing more; a catch-up still reading stops after its page.

        Not cancelled: the handler a catch-up is running may be what closed it.
        """
        self._closed = True

    async def _read_missed(self) -> None:
        try:
            async with self._reads:
                try:
                    await self._read_pages()
                finally:
                    # Released by the last catch-up only, and while still
                    # counted, so a live message that arrives meanwhile is
                    # held behind the ones being released.
                    if self._catch_ups == 1:
                        await self._release()
        finally:
            self._catch_ups -= 1

    async def _read_pages(self) -> None:
        while not self._closed:
            page = await self._list_after(self._last_seq)
            for message in page.messages:
                await self._deliver(message)
            if not page.has_more or not page.messages:
                return

    async def _release(self) -> None:
        while self._held:
            held = sorted(self._held, key=lambda message: message.seq)
            self._held = []
            for message in held:
                await self._deliver(message)

    async def _deliver(self, message: DurableMessage) -> None:
        if self._closed or message.seq <= self._last_seq:
            return
        self._last_seq = message.seq
        await self._handler(message)
