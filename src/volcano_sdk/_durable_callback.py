"""Rules shared by the callbacks Volcano completes for a workflow."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, TypeGuard

from ._transport_types import decode_json

if TYPE_CHECKING:
    from .models import JSONValue

# A name is also the runtime's operation name, which allows 256 printable ASCII
# characters, and the runtimes add suffixes of up to 19 characters to it; every
# SDK holds names to the same limit.
MAX_NAME_LENGTH = 237
_NOT_PRINTABLE_ASCII = "name must be printable ASCII"
_NUL = "\0"


def operation_name(value: object) -> str:
    """Require a name the runtime and Volcano both accept.

    Returns:
        The name, unchanged.

    Raises:
        ValueError: The name is empty, too long, or not printable ASCII.

    """
    name = text(value, "name", limit=MAX_NAME_LENGTH, required=True)
    if not (name.isascii() and name.isprintable()):
        raise ValueError(_NOT_PRINTABLE_ASCII)
    return name


def text(value: object, field: str, *, limit: int, required: bool) -> str:
    """Require a string Volcano can record.

    Returns:
        The string, unchanged.

    Raises:
        TypeError: The value is not a string, or holds a lone surrogate.
        ValueError: The string is required but blank.

    """
    if not isinstance(value, str):
        message = f"{field} must be a string"
        raise TypeError(message)
    try:
        _ = value.encode()
    except UnicodeEncodeError as error:
        message = f"{field} must be JSON-serializable: it contains a surrogate"
        raise TypeError(message) from error
    if required and not value.strip():
        message = f"{field} must not be empty"
        raise ValueError(message)
    return _recordable(value, field, limit)


def _recordable(value: str, field: str, limit: int) -> str:
    if len(value) > limit:
        message = f"{field} must be at most {limit} characters"
        raise ValueError(message)
    if _NUL in value:
        message = f"{field} must not contain NUL characters"
        raise ValueError(message)
    return value


def has_nul(value: JSONValue) -> bool:
    """Whether any string in a JSON value, key or value, holds a NUL.

    Returns:
        True when Volcano would refuse to store the value.

    """
    if isinstance(value, str):
        return _NUL in value
    if isinstance(value, dict):
        return any(_NUL in key or has_nul(item) for key, item in value.items())
    if isinstance(value, list):
        return any(has_nul(item) for item in value)
    return False


def callback_fields(result: object, invalid: str) -> Mapping[str, object]:
    """Read the object Volcano completed a callback with.

    The runtime hands the result back as Volcano sent it, a JSON document, or
    already decoded.

    Returns:
        The result's fields.

    Raises:
        TypeError: The result is not a JSON object.

    """
    if isinstance(result, (str, bytes)):
        document = result.encode() if isinstance(result, str) else result
        try:
            result = decode_json(document)
        except ValueError as error:
            raise TypeError(invalid) from error
    if not _is_fields(result):
        raise TypeError(invalid)
    return result


def _is_fields(value: object) -> TypeGuard[Mapping[str, object]]:
    return is_mapping(value) and all(isinstance(key, str) for key in value)


def is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    """Narrow a decoded value to a mapping.

    Returns:
        True when the value is a mapping.

    """
    return isinstance(value, Mapping)
