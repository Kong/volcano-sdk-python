"""Typed collaborators for the SDK contract binding tests."""

from __future__ import annotations

from dataclasses import dataclass

from volcano_sdk._tests.typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from volcano_sdk.realtime import RealtimePresenceInfo


class PauseSubscriber:
    def __init__(self) -> None:
        self.handler: Callable[[object], None] | None = None
        self.subscribed: bool = True
        self.on_count: int = 0

    def on(self, _event: str, handler: Callable[[object], None]) -> Callable[[], None]:
        self.handler = handler
        self.on_count += 1
        return lambda: None

    async def subscribe(self) -> None:
        self.subscribed = True

    async def unsubscribe(self) -> None:
        self.subscribed = False


class PausePublisher:
    def __init__(self, subscriber: PauseSubscriber, *, leak: bool) -> None:
        self.subscriber: PauseSubscriber = subscriber
        self.leak: bool = leak

    async def send(self, message: object) -> None:
        if self.leak or self.subscriber.subscribed:
            assert self.subscriber.handler is not None
            self.subscriber.handler(message)


@dataclass(frozen=True)
class BucketObject:
    name: str


@dataclass(frozen=True)
class BucketListing:
    objects: list[BucketObject]


class FailingBucket:
    def __init__(self, paths: list[str]) -> None:
        self.paths: list[str] = paths
        self.removed: list[str] = []

    def list(self, _path: str) -> BucketListing:
        return BucketListing([BucketObject(path) for path in self.paths])

    def remove(self, path: str) -> None:
        self.removed.append(path)
        if len(self.removed) == 1:
            message = "delete failed"
            raise RuntimeError(message)


class FailingPresenceChannel:
    def __init__(self, error: RuntimeError) -> None:
        self.error: RuntimeError = error

    @staticmethod
    def on_presence_sync(
        _callback: Callable[[Mapping[str, RealtimePresenceInfo]], None],
    ) -> Callable[[], None]:
        return lambda: None

    @staticmethod
    def get_presence_state() -> dict[str, RealtimePresenceInfo]:
        return {}

    async def subscribe(self) -> None:
        raise self.error

    async def unsubscribe(self) -> None:
        pass
