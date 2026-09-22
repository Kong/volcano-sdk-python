"""Validate runtime callbacks without erasing their static signatures."""


def require_callable(value: object, message: str) -> None:
    """Reject non-callable values supplied by unchecked callers.

    Raises:
        TypeError: The value is not callable.

    """
    if not callable(value):
        raise TypeError(message)
