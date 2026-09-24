"""Typed callback registration and deferred connection-event delivery."""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Generic, Protocol, TypeAlias, TypeVar

from ._callbacks import require_callable

ContextT = TypeVar("ContextT")
Invocation: TypeAlias = Callable[[], object]
DynamicCallback: TypeAlias = Callable[..., object]


def bind_callback(
    callback: Callable[[ContextT], object], value: ContextT
) -> Invocation:
    """Bind a callback to its validated event type.

    Returns:
        A deferred invocation with no remaining untyped arguments.

    """

    def invoke() -> object:
        return callback(value)

    return invoke


class ConnectionDelivery(Protocol):
    """A queued connection event whose callback arguments remain paired."""

    @property
    def event(self) -> str:
        """Connection event name for error reporting."""
        ...

    @property
    def empty(self) -> bool:
        """Whether this event had no registered listeners when queued."""
        ...

    def invocations(self) -> Iterator[Invocation]:
        """Iterate the listeners that are still registered."""
        ...


@dataclass(frozen=True, slots=True)
class CallbackBatch(Generic[ContextT]):
    """Capture event identity while honoring later listener removals."""

    event: str
    callbacks: dict[int, Callable[[ContextT], object]]
    identifiers: tuple[int, ...]
    context: ContextT

    @property
    def empty(self) -> bool:
        """Whether the captured listener set is empty."""
        return not self.identifiers

    def invocations(self) -> Iterator[Invocation]:
        """Yield typed invocations for each remaining captured listener.

        Yields:
            A callback with its context already bound.

        """
        for identifier in self.identifiers:
            callback = self.callbacks.get(identifier)
            if callback is not None:
                yield bind_callback(callback, self.context)


def register_callback(
    callbacks: dict[int, Callable[[ContextT], object]],
    identifiers: Iterator[int],
    callback: Callable[[ContextT], object],
    invalid_message: str,
) -> Callable[[], None]:
    """Register one typed callback without widening its argument type.

    Returns:
        An idempotent listener removal function.

    """
    require_callable(callback, invalid_message)
    identifier = next(identifiers)
    callbacks[identifier] = callback

    def unsubscribe() -> None:
        _ = callbacks.pop(identifier, None)

    return unsubscribe
