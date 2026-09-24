"""Function request validation and immutable response conversion."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Callable, Mapping
from types import MappingProxyType
from typing import TYPE_CHECKING, Protocol, TypeGuard

if TYPE_CHECKING:
    from ._transport import TransportResponse
    from .models import JSONValue

FUNCTION_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")

INVALID_FUNCTION_NAME = (
    "Function name must be DNS-safe: lowercase letters, numbers, and hyphens; "
    "1-63 characters"
)

INVALID_FUNCTION_RESPONSE = "Expected a complete function response"

INVALID_FUNCTION_PAYLOAD = "Function payload must be a mapping"

INVALID_FUNCTION_JSON_KEY = "Function JSON object keys must be strings"

INVALID_FUNCTION_DATA = "Function data must be JSON-compatible"

INVALID_FUNCTION_TRANSPORT = "Transport does not support function invocation"

HTTP_SUCCESS_MIN = 200

HTTP_SUCCESS_MAX = 300

HTTP_SUCCESS_STATUSES = range(HTTP_SUCCESS_MIN, HTTP_SUCCESS_MAX)

HTTP_NOT_FOUND = 404

HTTP_UNAUTHORIZED = 401

FUNCTION_INVOKED_HEADER = "X-Volcano-Function-Invoked"

FUNCTION_VERSION_HEADER = "X-Volcano-Version"

CONTENT_TYPE_HEADER = "Content-Type"

FUNCTION_TEXT_ENCODING = "utf-8-sig"


def stale_mapping(response: TransportResponse) -> bool:
    """Report a platform 404, which means the cached function identity is gone.

    A function that answers 404 itself must be returned rather than retried:
    invoking twice would run the caller's side effects twice. The platform sets
    X-Volcano-Function-Invoked only after dispatch, so its absence is what
    separates the two. X-Volcano-Version cannot: the server stamps it on every
    response, including errors raised before the function is reached.

    Returns
    -------
    bool
        True only for a 404 without the function-dispatch header.

    """
    return (
        int(response.status_code) == HTTP_NOT_FOUND
        and header(response.headers, FUNCTION_INVOKED_HEADER) is None
    )


class JSONLoader(Protocol):
    def loads(self, s: str, /, *, parse_constant: Callable[[str], None]) -> object: ...


JSON_LOADER: JSONLoader = json


def function_data(response: TransportResponse) -> JSONValue:
    if not response.content:
        return json_value(response.payload)
    text = response.content.decode(FUNCTION_TEXT_ENCODING, errors="replace")
    if not text:
        return None
    content_type = header(response.headers, CONTENT_TYPE_HEADER)
    is_json = content_type is not None and "application/json" in content_type.lower()
    if is_json or text.startswith(("{", "[")):
        try:
            decoded = JSON_LOADER.loads(text, parse_constant=reject_json_constant)
            return json_value(decoded)
        except ValueError:
            pass
    return text


def reject_json_constant(_value: str) -> None:
    raise ValueError


def json_mapping(
    value: Mapping[object, object], active: set[int]
) -> Mapping[str, JSONValue]:
    marker = enter_json_container(value, active)
    try:
        frozen: dict[str, JSONValue] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise TypeError(INVALID_FUNCTION_JSON_KEY)
            validate_json_string(key, INVALID_FUNCTION_JSON_KEY)
            frozen[key] = json_value_checked(item, active)
        return MappingProxyType(frozen)
    finally:
        active.remove(marker)


def json_sequence(
    value: list[object] | tuple[object, ...], active: set[int]
) -> tuple[JSONValue, ...]:
    marker = enter_json_container(value, active)
    try:
        return tuple(json_value_checked(item, active) for item in value)
    finally:
        active.remove(marker)


def enter_json_container(value: object, active: set[int]) -> int:
    marker = id(value)
    if marker in active:
        raise TypeError(INVALID_FUNCTION_DATA)
    active.add(marker)
    return marker


def validate_json_string(value: str, message: str) -> None:
    try:
        _ = str.encode(value)
    except UnicodeEncodeError as error:
        raise TypeError(message) from error


def is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def is_sequence(value: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def json_value(value: object) -> JSONValue:
    try:
        return json_value_checked(value, set())
    except RecursionError as error:
        raise TypeError(INVALID_FUNCTION_DATA) from error


def json_value_checked(value: object, active: set[int]) -> JSONValue:
    if is_mapping(value):
        return json_mapping(value, active)
    if is_sequence(value):
        return json_sequence(value, active)
    return json_scalar(value)


def json_scalar(value: object) -> JSONValue:
    if isinstance(value, str):
        validate_json_string(value, INVALID_FUNCTION_DATA)
        return value
    if isinstance(value, float) and not math.isfinite(value):
        raise TypeError(INVALID_FUNCTION_DATA)
    if isinstance(value, int) and not isinstance(value, bool):
        return json_int(value)
    if value is None or isinstance(value, (float, bool)):
        return value
    raise TypeError(INVALID_FUNCTION_DATA)


def json_int(value: int) -> int:
    try:
        _ = json.dumps(value)
    except ValueError as error:
        raise TypeError(INVALID_FUNCTION_DATA) from error
    return value


def header(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is None:
        return None
    for key, value in headers.items():
        if key.casefold() == name.casefold():
            return value
    return None


def function_name(value: object) -> str:
    if not isinstance(value, str) or FUNCTION_NAME.fullmatch(value) is None:
        raise ValueError(INVALID_FUNCTION_NAME)
    return value


def function_payload(value: object) -> Mapping[str, JSONValue]:
    if value is None:
        return {}
    if not is_mapping(value):
        raise TypeError(INVALID_FUNCTION_PAYLOAD)
    try:
        return json_mapping(value, set())
    except RecursionError as error:
        raise TypeError(INVALID_FUNCTION_DATA) from error
