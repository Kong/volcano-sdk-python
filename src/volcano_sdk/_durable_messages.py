"""Send, list, and follow the messages of durable executions."""

from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Protocol, Unpack, runtime_checkable

from ._callbacks import require_callable
from ._durable_arguments import identifier, known_options
from ._durable_callback import operation_name
from ._durable_message_response import durable_message, durable_message_page
from ._durable_message_stream import DurableMessageStream
from ._transport import HTTP_CREATED, HTTP_OK, invoke, invoke_async, response_payload
from ._transport_types import (
    DurableMessageListRequest,
    DurableMessageSendRequest,
    DurableMessageTarget,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from ._transport import Transport, TransportResponse
    from .models import (
        DurableMessage,
        DurableMessageDirection,
        DurableMessageListOptions,
        DurableMessagePage,
        DurableMessageSendOptions,
        DurableMessageTargetOptions,
        JSONValue,
    )

_INVALID_TRANSPORT = "Transport does not support durable messages"
_NO_REALTIME = "subscribe() needs a VolcanoClient, which owns the realtime connection"
_NO_SESSION = (
    "subscribe() needs a signed-in session to open the realtime connection; "
    "a client token or service key alone cannot"
)
_ALREADY_SUBSCRIBED = (
    "This client already subscribes to the execution's messages; unsubscribe first"
)
# The spec's bounds on Idempotency-Key, X-Volcano-Client-Token, and a page.
_MAX_IDEMPOTENCY_KEY_LENGTH = 255
_MAX_CLIENT_TOKEN_LENGTH = 128
_MAX_LIST_LIMIT = 500
_TARGET_OPTIONS = frozenset({"client_token", "project_id"})
_SEND_OPTIONS = _TARGET_OPTIONS | {"idempotency_key"}
_LIST_OPTIONS = _TARGET_OPTIONS | {"direction", "name", "after", "limit"}


class DurableMessagesContext(Protocol):
    """Client capabilities required by durable message requests."""

    def transport(self) -> Transport:
        """Return the active typed transport."""
        ...

    def function_token(self) -> str:
        """Return the current function-invocation credential."""
        ...

    def session_token(self) -> str:
        """Return the active session credential."""
        ...


@runtime_checkable
class DurableMessagesTransport(Protocol):
    """Transport operations required by the durable messages facade."""

    def send_durable_message(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageSendRequest,
    ) -> TransportResponse:
        """Send a message to a durable execution."""
        ...

    def list_durable_messages(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageListRequest,
    ) -> TransportResponse:
        """List a durable execution's messages."""
        ...

    async def list_durable_messages_async(
        self,
        *,
        authorization: str,
        target: DurableMessageTarget,
        request: DurableMessageListRequest,
    ) -> TransportResponse:
        """List a durable execution's messages without blocking the event loop."""
        ...


class DurableChannel(Protocol):
    """An execution's realtime channel, as a subscription uses it."""

    # Called each time the channel is subscribed again after a drop.
    resubscribed: Callable[[], None] | None
    # Called when the client's realtime facade removes or disconnects it.
    ended: Callable[[], None] | None
    # Called each time a full callback queue drops a publication.
    dropped: Callable[[], None] | None

    @property
    def name(self) -> str:
        """The channel's name on the realtime connection."""
        ...

    def on(self, event: str, callback: Callable[[object], object]) -> object:
        """Register a callback for the channel's publications."""
        ...

    async def subscribe(self) -> None:
        """Wait until the channel is subscribed."""
        ...


class DurableMessageChannels(Protocol):
    """The realtime connection a subscription follows an execution on."""

    def durable_channel(
        self, execution_id: str, client_token: str | None
    ) -> DurableChannel | None:
        """Open the execution's channel, or None when it is already open."""
        ...

    async def remove_durable_channel(self, channel: DurableChannel) -> None:
        """Unsubscribe and forget the execution's channel."""
        ...

    def session_check(self) -> Callable[[], bool]:
        """Return whether the client still has the session signed in now."""
        ...


class DurableMessageSubscription:
    """Messages an execution publishes, delivered until `unsubscribe`."""

    def __init__(
        self,
        stream: DurableMessageStream,
        channel: DurableChannel,
        realtime: DurableMessageChannels,
    ) -> None:
        """Own a subscription's stream and channel."""
        self._stream: DurableMessageStream = stream
        self._channel: DurableChannel = channel
        self._realtime: DurableMessageChannels = realtime

    async def unsubscribe(self) -> None:
        """Stop delivering messages and leave the execution's channel.

        Safe to repeat, and to call from the handler.
        """
        self._stream.close()
        await self._realtime.remove_durable_channel(self._channel)


class DurableMessages:
    """Send to, list, and follow the messages of durable executions.

    Each method addresses an execution by its function's name and its id. By
    default they use the application route with the client's credential, as a
    start does; pass `client_token` where that credential needs it. Pass
    `project_id` to use the owner's project route with the session's platform
    token instead.
    """

    def __init__(
        self,
        client: DurableMessagesContext,
        realtime: DurableMessageChannels | None,
    ) -> None:
        """Bind message operations to a Volcano client."""
        self._client: DurableMessagesContext = client
        self._realtime: DurableMessageChannels | None = realtime

    def _transport(self) -> DurableMessagesTransport:
        transport = self._client.transport()
        if not isinstance(transport, DurableMessagesTransport):
            raise TypeError(_INVALID_TRANSPORT)
        return transport

    def _authorization(self, target: DurableMessageTarget) -> str:
        if target.project_id is None:
            return self._client.function_token()
        return self._client.session_token()

    def send(
        self,
        function_name: str,
        execution_id: str,
        name: str,
        data: JSONValue = None,
        **options: Unpack[DurableMessageSendOptions],
    ) -> DurableMessage:
        """Send a message to a running execution.

        It is queued until a `ctx.wait_for_message(name)` takes it. A send with
        an `idempotency_key` the same sender has used on the execution returns
        the message the first one stored, and sends nothing. A send to an
        execution that has ended, or that already holds 100 untaken messages,
        raises `ConflictError`.

        Returns
        -------
        DurableMessage
            The stored message: `queued`, `delivered`, or `delivering` while
            its handover to a wait is still being confirmed.

        """
        known_options(options, _SEND_OPTIONS)
        target = _target(function_name, execution_id, options)
        request = DurableMessageSendRequest(
            name=operation_name(name),
            data=data,
            idempotency_key=_bounded_text(
                options.get("idempotency_key"),
                "idempotency_key",
                _MAX_IDEMPOTENCY_KEY_LENGTH,
            ),
        )
        response = invoke(
            self._transport().send_durable_message,
            authorization=self._authorization(target),
            target=target,
            request=request,
        )
        created = int(response.status_code) == HTTP_CREATED
        response_body: object = response_payload(
            response, HTTP_CREATED if created else HTTP_OK
        )
        return durable_message(response_body)

    def list(
        self,
        function_name: str,
        execution_id: str,
        **options: Unpack[DurableMessageListOptions],
    ) -> DurableMessagePage:
        """List an execution's messages in both directions, oldest first.

        Read the next page with `after` set to the last message's `seq`.

        Returns
        -------
        DurableMessagePage
            The messages and whether more follow.

        """
        known_options(options, _LIST_OPTIONS)
        target = _target(function_name, execution_id, options)
        direction = options.get("direction")
        name = options.get("name")
        request = DurableMessageListRequest(
            direction=None if direction is None else _direction(direction),
            name=None if name is None else operation_name(name),
            after=_after(options.get("after")),
            limit=_limit(options.get("limit")),
        )
        response = invoke(
            self._transport().list_durable_messages,
            authorization=self._authorization(target),
            target=target,
            request=request,
        )
        response_body: object = response_payload(response, HTTP_OK)
        return durable_message_page(response_body)

    async def subscribe(
        self,
        function_name: str,
        execution_id: str,
        handler: Callable[[DurableMessage], object],
        **options: Unpack[DurableMessageTargetOptions],
    ) -> DurableMessageSubscription:
        """Deliver every message the execution publishes, in order, once each.

        Messages it published before the call are delivered first. After a
        reconnect, the ones published meanwhile are read back before live
        delivery resumes. The handler may be a coroutine function; one that is
        not callable raises `TypeError`.

        Follows the execution on the client's realtime connection, which needs
        a signed-in session; a client token or service key alone cannot open
        it. Signing out, signing in again, or setting another session ends the
        subscription and leaves the channel; a token refresh does not.

        Returns
        -------
        DurableMessageSubscription
            The subscription, once the messages published so far are delivered.

        Raises
        ------
        RuntimeError
            If the client has no signed-in session, or already subscribes to
            the execution.

        """
        known_options(options, _TARGET_OPTIONS)
        target = _target(function_name, execution_id, options)
        deliver = _deliverer(handler)
        realtime = self._realtime
        if realtime is None:
            raise RuntimeError(_NO_REALTIME)
        try:
            _ = self._client.session_token()
        except RuntimeError as error:
            raise RuntimeError(_NO_SESSION) from error
        stream = DurableMessageStream(
            deliver, self._reader(target), realtime.session_check()
        )
        channel = realtime.durable_channel(target.execution_id, target.client_token)
        if channel is None:
            raise RuntimeError(_ALREADY_SUBSCRIBED)
        return await _follow(stream, channel, realtime)

    def _reader(
        self, target: DurableMessageTarget
    ) -> Callable[[int], Awaitable[DurableMessagePage]]:
        transport = self._transport()

        async def list_after(after: int) -> DurableMessagePage:
            response = await invoke_async(
                transport.list_durable_messages_async,
                authorization=self._authorization(target),
                target=target,
                request=DurableMessageListRequest(direction="out", after=after),
            )
            response_body: object = response_payload(response, HTTP_OK)
            return durable_message_page(response_body)

        return list_after


async def _follow(
    stream: DurableMessageStream,
    channel: DurableChannel,
    realtime: DurableMessageChannels,
) -> DurableMessageSubscription:
    subscription = DurableMessageSubscription(stream, channel, realtime)
    _ = channel.on("message", stream.live)
    channel.ended = stream.close
    try:
        await channel.subscribe()
        channel.resubscribed = stream.resubscribed
        channel.dropped = stream.dropped
        await stream.catch_up()
    except BaseException:
        await subscription.unsubscribe()
        raise
    stream.end_with(subscription.unsubscribe)
    return subscription


def _deliverer(
    handler: Callable[[DurableMessage], object],
) -> Callable[[DurableMessage], Awaitable[None]]:
    require_callable(handler, "subscribe() requires a handler function")

    async def deliver(message: DurableMessage) -> None:
        result = handler(message)
        if inspect.isawaitable(result):
            await result

    return deliver


def _target(
    function_name: object,
    execution_id: object,
    options: DurableMessageTargetOptions,
) -> DurableMessageTarget:
    project_id = options.get("project_id")
    return DurableMessageTarget(
        function_id=identifier(function_name, "function_name"),
        execution_id=identifier(execution_id, "execution_id"),
        project_id=None if project_id is None else identifier(project_id, "project_id"),
        client_token=_bounded_text(
            options.get("client_token"), "client_token", _MAX_CLIENT_TOKEN_LENGTH
        ),
    )


def _bounded_text(value: object, field: str, limit: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value:
        message = f"{field} must be a non-empty string"
        raise ValueError(message)
    # Sent as a header, which carries printable ASCII only.
    if not (value.isascii() and value.isprintable()):
        message = f"{field} must be printable ASCII"
        raise ValueError(message)
    if len(value) > limit:
        message = f"{field} must be at most {limit} characters"
        raise ValueError(message)
    return value


def _after(value: object) -> int | None:
    if value is None:
        return None
    if type(value) is not int or value < 0:
        message = "after must be a non-negative integer"
        raise ValueError(message)
    return value


def _limit(value: object) -> int | None:
    if value is None:
        return None
    if type(value) is not int or not 1 <= value <= _MAX_LIST_LIMIT:
        message = f"limit must be an integer between 1 and {_MAX_LIST_LIMIT}"
        raise ValueError(message)
    return value


def _direction(value: object) -> DurableMessageDirection:
    if value == "in":
        return "in"
    if value == "out":
        return "out"
    message = "direction must be 'in' or 'out'"
    raise ValueError(message)
