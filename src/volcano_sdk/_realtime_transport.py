"""Native realtime transport contracts and subscription lifecycle adapters."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable, Mapping
from typing import TYPE_CHECKING, Protocol, TypeVar, overload

from centrifuge import CentrifugeError, Client
from typing_extensions import override

if TYPE_CHECKING:
    from typing import TypeGuard

    from ._session_operations import SessionOperations
    from ._transport import Transport
    from .models import Session

_SubscriptionT = TypeVar("_SubscriptionT")
_DefaultT = TypeVar("_DefaultT")
POSTGRES_CHANNEL_SEGMENTS = 3
POSTGRES_PUBLICATION_SEGMENTS = 5
CENTRIFUGE_ERROR: type[Exception] = CentrifugeError
SUBSCRIPTION_REGISTRY_UNAVAILABLE = (
    "centrifuge client subscription registry is unavailable"
)


def consume_presence_result(task: asyncio.Task[object]) -> None:
    if not task.cancelled():
        _ = task.exception()


def postgres_route_matches(candidate: str, publication: str) -> bool:
    candidate_parts = candidate.split(":")
    publication_parts = publication.split(":")
    return (
        len(candidate_parts) == POSTGRES_CHANNEL_SEGMENTS
        and candidate_parts[0] == "postgres"
        and len(publication_parts) == POSTGRES_PUBLICATION_SEGMENTS
        and publication_parts[1:4] == candidate_parts
    )


def is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    return isinstance(value, dict)


class RealtimeContext(Protocol):
    """Client capabilities required by realtime connections."""

    def transport(self) -> Transport:
        """Return the current transport, including runtime replacements."""
        ...

    def anon_token(self) -> str:
        """Return the current anonymous credential."""
        ...

    def session_token(self) -> str:
        """Return the current session credential."""
        ...

    def capture_session_binding(
        self,
    ) -> tuple[int, SessionOperations, Session | None]:
        """Capture the session with its generation and refresh lineage."""
        ...


class CentrifugeSubscription(Protocol):
    """Centrifuge subscription operations used by the SDK."""

    async def subscribe(self) -> None:
        """Subscribe to the remote channel."""
        ...

    async def ready(self) -> None:
        """Wait for acknowledgement using the client request timeout."""
        ...

    async def publish(self, data: object) -> object:
        """Publish a payload to the remote channel."""
        ...

    async def unsubscribe(self) -> None:
        """Unsubscribe from the remote channel."""
        ...

    async def presence(self) -> object:
        """Return the clients currently present on the channel."""
        ...


async def unsubscribe_native(subscription: CentrifugeSubscription) -> None:
    # Finish the native stop before releasing the connection lock on cancellation.
    task = asyncio.create_task(subscription.unsubscribe())
    cancelled: asyncio.CancelledError | None = None
    while not task.done():
        try:
            await asyncio.shield(task)
        except asyncio.CancelledError as error:
            cancelled = error
        except CENTRIFUGE_ERROR:
            if cancelled is None:
                raise
    finish_unsubscribe(task, cancelled)


def finish_unsubscribe(
    task: asyncio.Task[None],
    cancelled: asyncio.CancelledError | None,
) -> None:
    if cancelled is not None:
        if not task.cancelled():
            _ = task.exception()
        raise cancelled
    task.result()


class CentrifugeConnection(Protocol):
    """Centrifuge connection operations used by the SDK."""

    @property
    def state(self) -> object:
        """Native connection state."""
        ...

    async def connect(self) -> None:
        """Open the remote connection."""
        ...

    async def disconnect(self) -> None:
        """Close the remote connection."""
        ...

    def new_subscription(
        self,
        name: str,
        /,
        *,
        events: object,
        join_leave: bool,
        recoverable: bool,
    ) -> CentrifugeSubscription:
        """Create a subscription for a remote channel."""
        ...

    def remove_subscription(self, subscription: CentrifugeSubscription, /) -> None:
        """Remove an unsubscribed channel from the connection registry."""
        ...


class CentrifugeFactory(Protocol):
    """Construct a typed Centrifuge connection."""

    def __call__(
        self,
        address: str,
        *,
        events: object,
        token: str,
        get_token: Callable[[], Awaitable[str]],
    ) -> CentrifugeConnection:
        """Construct a Centrifuge connection."""
        ...


class Publication(Protocol):
    """Publication payload received from Centrifuge."""

    data: object


class PublicationContext(Protocol):
    """Centrifuge callback context containing a publication."""

    pub: Publication


def native_attribute(value: object, name: str, default: object = None) -> object:
    return getattr(value, name, default)


def native_presence_clients(value: object) -> Mapping[str, object] | None:
    if not is_object_mapping(value):
        return None
    clients: dict[str, object] = {}
    for client_id, info in value.items():
        if not isinstance(client_id, str):
            return None
        clients[client_id] = info
    return clients


def centrifuge_client(
    address: str,
    *,
    events: object,
    token: str,
    get_token: Callable[[], Awaitable[str]],
) -> CentrifugeConnection:
    return Client(address, events=events, token=token, get_token=get_token)


class ProjectAwareSubscriptions(dict[str, _SubscriptionT]):
    @overload
    def get(self, key: str, default: None = None) -> _SubscriptionT | None: ...

    @overload
    def get(self, key: str, default: _SubscriptionT) -> _SubscriptionT: ...

    @overload
    def get(self, key: str, default: _DefaultT) -> _SubscriptionT | _DefaultT: ...

    @override
    def get(
        self, key: str, default: _DefaultT | None = None
    ) -> _SubscriptionT | _DefaultT | None:
        subscription = super().get(key)
        if subscription is not None:
            return subscription
        matches = [
            (channel, candidate)
            for channel, candidate in self.items()
            if key.endswith(f":{channel}") or postgres_route_matches(channel, key)
        ]
        return max(matches, key=lambda match: len(match[0]))[1] if matches else default


def project_subscriptions(value: object) -> ProjectAwareSubscriptions[object]:
    if not is_object_dict(value):
        raise TypeError(SUBSCRIPTION_REGISTRY_UNAVAILABLE)
    subscriptions = ProjectAwareSubscriptions[object]()
    for channel, subscription in value.items():
        if not isinstance(channel, str):
            raise TypeError(SUBSCRIPTION_REGISTRY_UNAVAILABLE)
        subscriptions[channel] = subscription
    return subscriptions


class VolcanoCentrifugeConnection:
    def __init__(self, connection: CentrifugeConnection) -> None:
        self._connection: CentrifugeConnection = connection
        state = vars(connection)
        state["_subs"] = project_subscriptions(state.get("_subs"))

    async def connect(self) -> None:
        await self._connection.connect()

    async def disconnect(self) -> None:
        await self._connection.disconnect()

    @property
    def is_connected(self) -> bool:
        state = self._connection.state
        return native_attribute(state, "value") == "connected"

    def new_subscription(
        self,
        name: str,
        *,
        events: object,
        join_leave: bool,
        recoverable: bool,
    ) -> CentrifugeSubscription:
        return self._connection.new_subscription(
            name,
            events=events,
            join_leave=join_leave,
            recoverable=recoverable,
        )

    def remove_subscription(self, subscription: CentrifugeSubscription) -> None:
        self._connection.remove_subscription(subscription)
