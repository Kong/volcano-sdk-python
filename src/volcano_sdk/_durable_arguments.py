"""Arguments the durable facades check before spending a request."""

from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from collections.abc import Mapping

_INVALID_IDENTIFIERS = {
    "function_name": "function_name must be a non-empty string",
    "execution_name": "execution_name must be a non-empty string",
    "project_id": "project_id must be a non-empty string",
    "execution_id": "execution_id must be a non-empty string",
    "approval_id": "approval_id must be a non-empty string",
}
# The identifiers the transport converts to a UUID before sending. Checked
# here so a malformed one is a facade ValidationError rather than a
# `badly formed hexadecimal UUID string` raised from inside the transport,
# outside the error hierarchy this package documents.
_UUID_IDENTIFIERS = {
    "project_id": "project_id must be a UUID",
    "execution_id": "execution_id must be a UUID",
    "approval_id": "approval_id must be a UUID",
}


def identifier(value: object, field: str) -> str:
    """Require a non-empty path segment, and a UUID where one is sent as one.

    An empty segment would address the collection instead of the execution,
    which is a different request rather than a failed one.

    Returns
    -------
    str
        The trimmed identifier, with a UUID in its canonical form.

    Raises
    ------
    ValueError
        If the value is empty, is not a string, or requires a valid UUID.

    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(_INVALID_IDENTIFIERS[field])
    trimmed = value.strip()
    if field not in _UUID_IDENTIFIERS:
        return trimmed
    try:
        return str(UUID(trimmed))
    except ValueError as exc:
        raise ValueError(_UUID_IDENTIFIERS[field]) from exc


def known_options(options: Mapping[str, object], known: frozenset[str]) -> None:
    """Refuse keyword options a method does not take.

    Raises
    ------
    TypeError
        If any option is not in `known`.

    """
    unknown = sorted(options.keys() - known)
    if unknown:
        message = f"unexpected option: {', '.join(unknown)}"
        raise TypeError(message)
