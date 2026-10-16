"""Ordered, once-each delivery of the messages a durable execution publishes."""

from __future__ import annotations

import asyncio
from bisect import insort
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ._durable_message_response import broadcast_prev_seq, durable_message

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from .models import DurableMessage, DurableMessagePage

_FIRST_RETRY_SECONDS = 0.5
_MAX_RETRY_SECONDS = 30.0
# Live messages held past this are dropped, oldest first. Each one held after
# a dropped one names a predecessor at or past it, so it waits for a read that
# lists the dropped one.
_HELD_LIMIT = 128
_SESSION_CHANGED = (
    "The session that subscribed to the execution's messages has changed; "
    "the subscription has ended"
)
_ENDED = "The durable message subscription has ended"
_HANDLER_FAILED = "Volcano durable message handler failed"


@dataclass(frozen=True)
class _Held:
    message: DurableMessage
    prev_seq: int


def _published(data: object) -> _Held | None:
    message = durable_message(data)
    if message.direction != "out":
        return None
    return _Held(message, broadcast_prev_seq(data))


def _report_failed_catch_up(task: asyncio.Task[None]) -> None:
    if task.cancelled() or (error := task.exception()) is None:
        return
    asyncio.get_running_loop().call_exception_handler(
        {"message": "Volcano durable message catch-up failed", "exception": error}
    )


def retry_delay(failures: int) -> float:
    """Wait half a second after the first failure, doubling to 30 seconds.

    Returns
    -------
    float
        Seconds to wait before the next catch-up.

    """
    delay = _FIRST_RETRY_SECONDS
    for _ in range(failures):
        delay = min(delay * 2, _MAX_RETRY_SECONDS)
    return delay


class DurableMessageStream:
    """Deliver messages in `seq` order, once each, from the channel and the list.

    A live message can only be delivered once everything before it has been,
    or the missed ones would fall below the last delivered `seq` and be
    skipped. Each broadcast names the publish before it, so a live message is
    held, with that name, until the first catch-up starts, while any catch-up
    is reading, while it does not follow the last delivered `seq`, and behind
    any message already held. A catch-up that fails, or that leaves a held
    message still short of its predecessor, is tried again until one reads it.

    The channel itself drops publications while it is not subscribed, or
    while its callback queue is full, and reports each resubscription and
    each drop, which start a catch-up of what it dropped. A publication that
    does not read as a message starts one too.
    """

    def __init__(
        self,
        deliver: Callable[[DurableMessage], Awaitable[None]],
        list_after: Callable[[int], Awaitable[DurableMessagePage]],
        in_session: Callable[[], bool],
    ) -> None:
        """Deliver through `deliver`, reading missed messages with `list_after`.

        `in_session` says whether the session that subscribed is still the
        client's. Once it is not, the stream closes rather than read or
        deliver another user's messages.
        """
        self._handler: Callable[[DurableMessage], Awaitable[None]] = deliver
        self._list_after: Callable[[int], Awaitable[DurableMessagePage]] = list_after
        self._in_session: Callable[[], bool] = in_session
        self._leave: Callable[[], Awaitable[None]] | None = None
        self._last_seq: int = 0
        self._started: bool = False
        self._catch_ups: int = 0
        self._held: list[_Held] = []
        self._failures: int = 0
        self._retry: asyncio.TimerHandle | None = None
        self._closed: bool = False
        self._reads: asyncio.Lock = asyncio.Lock()
        self._handling: asyncio.Lock = asyncio.Lock()
        self._tasks: set[asyncio.Task[None]] = set()

    async def live(self, data: object) -> None:
        """Deliver a channel publication, or hold it until a catch-up releases it."""
        held = self._readable(data)
        if held is None:
            return
        if not self._started or self._catch_ups > 0 or self._held:
            self._hold(held)
            return
        if held.prev_seq > self._last_seq:
            self._hold(held)
            self._catch_up_in_background()
            return
        await self._deliver(held.message, report=True)

    def _readable(self, data: object) -> _Held | None:
        if self._closed:
            return None
        try:
            return _published(data)
        except TypeError:
            # Still one the execution published, so the list is read for it,
            # by the first catch-up when that has yet to start.
            if self._started:
                self._catch_up_in_background()
            return None

    def _hold(self, held: _Held) -> None:
        insort(self._held, held, key=lambda each: each.message.seq)
        if len(self._held) > _HELD_LIMIT:
            del self._held[0]

    def resubscribed(self) -> None:
        """Catch up on what the channel dropped while it was not subscribed."""
        self._catch_up_in_background()

    def dropped(self) -> None:
        """Catch up on a publication the channel's full callback queue dropped."""
        self._catch_up_in_background()

    def _catch_up_in_background(self) -> None:
        # One catch-up waiting its turn reads whatever more are asked for
        # meanwhile, so a burst of dropped publications reads once. Of those
        # counted, only the one reading holds `_reads`.
        reading = 1 if self._reads.locked() else 0
        if self._catch_ups > reading:
            return
        # The stream retries a failed catch-up itself; each failure is reported.
        self._start_catch_up(first=False).add_done_callback(_report_failed_catch_up)

    def catch_up(self) -> asyncio.Task[None]:
        """Read what was missed, then release the held messages that follow on.

        The first catch-up, which subscribing waits for. Should it fail, the
        stream closes before anything held is delivered. Later catch-ups
        report what a handler raises and go on.

        Returns
        -------
        asyncio.Task[None]
            The read, which fails with the list's or the handler's error, or
            with `RuntimeError` when the stream closed while it read.

        """
        return self._start_catch_up(first=True)

    def _start_catch_up(self, *, first: bool) -> asyncio.Task[None]:
        # Counted before the task starts, so nothing is delivered live while a
        # read waits its turn.
        self._started = True
        self._cancel_retry()
        self._catch_ups += 1
        task = asyncio.create_task(self._read_missed(first=first))
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def end_with(self, leave: Callable[[], Awaitable[None]]) -> None:
        """Call `leave` too once the session changes.

        Until then, leaving the channel is up to whoever subscribes.
        """
        self._leave = leave

    def close(self) -> None:
        """Deliver nothing more; a catch-up still reading stops after its page.

        Not cancelled: the handler a catch-up is running may be what closed it.
        """
        self._closed = True
        self._held.clear()
        self._cancel_retry()

    async def _read_missed(self, *, first: bool) -> None:
        # Past the first read, a handler that raises is reported and the read
        # goes on, as live delivery does; backing off is for failed reads.
        # The first read's handler errors end the subscription instead.
        report = not first
        try:
            async with self._reads:
                try:
                    await self._read_pages(report=report)
                    await self._release_if_last(read=True, report=report)
                except BaseException:
                    if first:
                        self.close()
                    await self._release_if_last(read=False, report=report)
                    raise
                if first and self._closed:
                    raise RuntimeError(_ENDED)
        finally:
            self._catch_ups -= 1

    async def _release_if_last(self, *, read: bool, report: bool) -> None:
        # Released by the last catch-up only, and while still counted, so a
        # live message that arrives meanwhile is held behind the ones being
        # released.
        if self._catch_ups == 1:
            await self._release(read=read, report=report)

    async def _read_pages(self, *, report: bool) -> None:
        while not self._closed:
            await self._require_session()
            after = self._last_seq
            page = await self._list_after(after)
            # An empty page delivers nothing that would check it.
            await self._require_session()
            for message in page.messages:
                await self._deliver(message, report=report)
            # A page that delivered nothing would be asked for again unchanged.
            if not page.has_more or self._last_seq == after:
                return

    async def _release(self, *, read: bool, report: bool) -> None:
        # One a handler raises on is already delivered, so a retry resumes
        # after it.
        try:
            while self._held and self._held[0].prev_seq <= self._last_seq:
                await self._deliver(self._held.pop(0).message, report=report)
        finally:
            if read and not self._held:
                self._failures = 0
            else:
                self._retry_later()

    def _retry_later(self) -> None:
        self._cancel_retry()
        if self._closed:
            return
        delay = retry_delay(self._failures)
        self._failures += 1
        self._retry = asyncio.get_running_loop().call_later(delay, self._retry_now)

    def _retry_now(self) -> None:
        self._retry = None
        self._catch_up_in_background()

    def _cancel_retry(self) -> None:
        if self._retry is not None:
            self._retry.cancel()
            self._retry = None

    async def _deliver(self, message: DurableMessage, *, report: bool) -> None:
        # Live messages and catch-ups are delivered from different tasks, so a
        # catch-up waits for a handler still running on a live message.
        async with self._handling:
            if self._closed or message.seq <= self._last_seq:
                return
            await self._require_session()
            self._last_seq = message.seq
            if not report:
                await self._handler(message)
                return
            (error,) = await asyncio.gather(
                self._handle_if_current(message), return_exceptions=True
            )
            if isinstance(error, BaseException):
                asyncio.get_running_loop().call_exception_handler(
                    {"message": _HANDLER_FAILED, "exception": error}
                )

    async def _handle_if_current(self, message: DurableMessage) -> None:
        # Runs as a task of its own, which an unsubscribe or a session change
        # can get to first. The next delivery or read ends a changed session.
        if not self._closed and self._in_session():
            await self._handler(message)

    async def _require_session(self) -> None:
        if not self._in_session():
            self.close()
            if self._leave is not None:
                await self._leave()
            raise RuntimeError(_SESSION_CHANGED)
