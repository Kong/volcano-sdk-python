"""Validate durable execution responses before exposing immutable models."""

from __future__ import annotations

import json
import math
from collections.abc import Mapping
from datetime import datetime
from typing import TypeGuard

from .models import (
    DurableExecution,
    DurableExecutionFailure,
    DurableExecutionPage,
    DurableExecutionStatus,
    JSONValue,
)

_INVALID_EXECUTION_PAYLOAD = "Expected a complete durable execution"
_INVALID_EXECUTION_PAGE = "Expected a complete durable execution page"
_EXECUTION_STATUSES: tuple[DurableExecutionStatus, ...] = (
    "pending",
    "running",
    "succeeded",
    "failed",
    "timed_out",
    "stopped",
    "unknown",
)


def _execution_fields(payload: object) -> Mapping[str, object]:
    if not _is_object_mapping(payload):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    for required in ("id", "function_id", "name", "status", "region", "created_at"):
        if not isinstance(payload.get(required), str) or not payload[required]:
            raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    return payload


def _is_object_mapping(value: object) -> TypeGuard[Mapping[str, object]]:
    return _is_mapping(value) and all(isinstance(key, str) for key in value)


def _is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _is_sequence(value: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def _execution_status(value: object) -> DurableExecutionStatus:
    for status in _EXECUTION_STATUSES:
        if value == status:
            return status
    raise TypeError(_INVALID_EXECUTION_PAYLOAD)


def _json_result(value: object) -> JSONValue:
    try:
        if _is_json_value(value, set()):
            return value
    except RecursionError as error:
        raise TypeError(_INVALID_EXECUTION_PAYLOAD) from error
    raise TypeError(_INVALID_EXECUTION_PAYLOAD)


def _is_json_value(value: object, active: set[int]) -> TypeGuard[JSONValue]:
    if _is_json_scalar(value):
        return True
    if _is_mapping(value):
        return _is_json_mapping(value, active)
    if _is_sequence(value):
        return _is_json_sequence(value, active)
    return False


def _is_json_scalar(value: object) -> TypeGuard[str | int | float | bool | None]:
    if value is None or isinstance(value, bool):
        return True
    if isinstance(value, str):
        return _is_utf8(value)
    if isinstance(value, int):
        return _is_json_int(value)
    if isinstance(value, float):
        return math.isfinite(value)
    return False


def _is_utf8(value: str) -> bool:
    try:
        _ = value.encode()
    except UnicodeEncodeError:
        return False
    return True


def _is_json_int(value: int) -> bool:
    try:
        _ = json.dumps(value)
    except ValueError:
        return False
    return True


def _is_json_mapping(value: Mapping[object, object], active: set[int]) -> bool:
    marker = id(value)
    if marker in active:
        return False
    active.add(marker)
    try:
        return all(
            isinstance(key, str) and _is_utf8(key) and _is_json_value(item, active)
            for key, item in value.items()
        )
    finally:
        active.remove(marker)


def _is_json_sequence(
    value: list[object] | tuple[object, ...], active: set[int]
) -> bool:
    marker = id(value)
    if marker in active:
        return False
    active.add(marker)
    try:
        return all(_is_json_value(item, active) for item in value)
    finally:
        active.remove(marker)


def durable_execution(payload: object) -> DurableExecution:
    """Validate and snapshot one durable execution.

    Returns:
        The complete execution model.

    Raises:
        TypeError: The result-expired flag is not a boolean.

    """
    values = _execution_fields(payload)
    created_at = _parse_datetime(values["created_at"])
    result_expired = values.get("result_expired")
    if result_expired is not None and not isinstance(result_expired, bool):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    return DurableExecution(
        id=str(values["id"]),
        function_id=str(values["function_id"]),
        name=str(values["name"]),
        status=_execution_status(values["status"]),
        region=str(values["region"]),
        created_at=created_at,
        result=_json_result(values.get("result")),
        result_expired=result_expired,
        error=_durable_error(values.get("error")),
        completed_at=optional_datetime(values.get("completed_at")),
    )


def _durable_error(payload: object) -> DurableExecutionFailure | None:
    if payload is None:
        return None
    if not _is_object_mapping(payload):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    error_type = payload.get("type")
    message = payload.get("message")
    return DurableExecutionFailure(
        type=None if error_type is None else str(error_type),
        message=None if message is None else str(message),
    )


def durable_execution_page(payload: object) -> DurableExecutionPage:
    """Validate and snapshot a page of executions.

    Returns:
        Executions and validated pagination metadata.

    Raises:
        TypeError: The page container or pagination fields are invalid.

    """
    if not _is_object_mapping(payload):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    raw_data: object = payload.get("data")
    if raw_data is None:
        raw_data = list[object]()
    if not _is_sequence(raw_data):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    data = tuple(raw_data)
    has_more = payload.get("has_more", False)
    if not isinstance(has_more, bool):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    return DurableExecutionPage(
        executions=tuple(durable_execution(entry) for entry in data),
        page=_count(payload.get("page")),
        limit=_count(payload.get("limit")),
        total=_count(payload.get("total")),
        has_more=has_more,
    )


def _count(value: object) -> int:
    if value is None:
        return 0
    if type(value) is not int:
        raise TypeError(_INVALID_EXECUTION_PAGE)
    return value


def optional_datetime(value: object) -> datetime | None:
    """Parse an optional completion timestamp.

    Returns:
        The parsed timestamp, or None when no value is present.

    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return _parse_datetime(value)


def _parse_datetime(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        raise TypeError(_INVALID_EXECUTION_PAYLOAD) from error
