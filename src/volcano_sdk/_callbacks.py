"""Validate runtime callbacks without erasing their static signatures."""

from collections.abc import Callable
from typing import ParamSpec, TypeVar

_P = ParamSpec("_P")
T = TypeVar("T")


def require_callable(value: object, message: str) -> None:
    """Reject non-callable values supplied by unchecked callers.

    Raises:
        TypeError: The value is not callable.

    """
    if not callable(value):
        raise TypeError(message)


def named_operation(
    name: str | Callable[_P, T] | None,
    func: Callable[_P, T] | None,
    operation: str,
) -> tuple[str | None, Callable[_P, T]]:
    """Accept both the named and unnamed form of an operation.

    The name is what the operation is recorded under, so it is worth
    encouraging, but a single obvious operation reads better without one.

    Returns:
        The optional recording name and the operation's callable.

    """
    if isinstance(name, str) or name is None:
        return name, operation_callable(func, operation)
    return None, operation_callable(name, operation)


def operation_callable(func: Callable[_P, T] | None, operation: str) -> Callable[_P, T]:
    """Validate an operation without erasing its callback signature.

    Returns:
        The supplied callable with its parameter and return types.

    Raises:
        TypeError: The operation is not callable.

    """
    if not callable(func):
        message = f"{operation}() requires a function to run"
        raise TypeError(message)
    return func
