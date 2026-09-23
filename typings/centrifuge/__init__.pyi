import asyncio
from collections.abc import Awaitable, Callable
from enum import Enum

class CentrifugeError(Exception): ...

class ClientState(Enum):
    DISCONNECTED = "disconnected"
    CONNECTING = "connecting"
    CONNECTED = "connected"

class SubscriptionState(Enum):
    UNSUBSCRIBED = "unsubscribed"
    SUBSCRIBING = "subscribing"
    SUBSCRIBED = "subscribed"

class Subscription:
    state: SubscriptionState
    _recover: bool
    _epoch: str
    _offset: int

    async def subscribe(self) -> None: ...
    async def ready(self) -> None: ...
    async def publish(self, data: object) -> object: ...
    async def unsubscribe(self) -> None: ...
    async def presence(self) -> object: ...
    async def _process_publication(self, pub: object) -> None: ...
    async def _move_subscribing(
        self, code: int, reason: str, skip_schedule_resubscribe: bool = False
    ) -> None: ...

class Client:
    state: ClientState
    events: object
    _connected_future: asyncio.Future[object]
    _inflight_commands: dict[int, object]
    _timeout: float

    def __init__(
        self,
        address: str,
        events: object | None = None,
        token: str = "",
        get_token: Callable[[], Awaitable[str]] | None = None,
        *,
        loop: asyncio.AbstractEventLoop | None = None,
    ) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    def new_subscription(
        self,
        channel: str,
        /,
        events: object | None = None,
        *,
        recoverable: bool = False,
        join_leave: bool = False,
    ) -> Subscription: ...
    def get_subscription(self, channel: str) -> Subscription | None: ...
    def remove_subscription(self, sub: object, /) -> None: ...
    async def _send_commands(self, commands: list[dict[str, object]]) -> None: ...
    async def _process_reply(self, reply: dict[str, object]) -> None: ...
    async def _unsubscribe(self, channel: str) -> None: ...
    def _construct_subscribe_command(
        self, sub: Subscription, cmd_id: int
    ) -> dict[str, object]: ...
