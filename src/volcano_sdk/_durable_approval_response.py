"""Validate durable approval responses before exposing immutable models."""

from __future__ import annotations

import math
from collections.abc import Mapping
from datetime import date, datetime
from typing import TypeGuard

from ._durable_response import json_value
from .models import (
    DurableApproval,
    DurableApprovalCounts,
    DurableApprovalDailyCounts,
    DurableApprovalDecider,
    DurableApprovalDecision,
    DurableApprovalExecution,
    DurableApprovalFunction,
    DurableApprovalFunctionCounts,
    DurableApprovalPage,
    DurableApprovalStats,
    DurableApprovalStatus,
    DurableExecutionStatus,
)

_INVALID_APPROVAL = "Expected a complete durable approval"
_INVALID_PAGE = "Expected a complete durable approval page"
_INVALID_STATS = "Expected complete durable approval stats"
APPROVAL_STATUSES: tuple[DurableApprovalStatus, ...] = (
    "pending",
    "approved",
    "denied",
    "expired",
    "cancelled",
)
_EXECUTION_STATUSES: tuple[DurableExecutionStatus, ...] = (
    "pending",
    "running",
    "succeeded",
    "failed",
    "timed_out",
    "stopped",
    "unknown",
)
_COUNT_FIELDS = ("requested", "pending", "approved", "denied", "expired", "cancelled")


def _is_fields(value: object) -> TypeGuard[Mapping[str, object]]:
    return _is_mapping(value) and all(isinstance(key, str) for key in value)


def _is_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def _is_sequence(value: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def _fields(value: object, message: str) -> Mapping[str, object]:
    if not _is_fields(value):
        raise TypeError(message)
    return value


def _text(values: Mapping[str, object], key: str, message: str) -> str:
    value = values.get(key)
    if not isinstance(value, str):
        raise TypeError(message)
    return value


def _identifier(values: Mapping[str, object], key: str, message: str) -> str:
    value = _text(values, key, message)
    if not value:
        raise TypeError(message)
    return value


def _optional_identifier(values: Mapping[str, object], key: str) -> str | None:
    if values.get(key) is None:
        return None
    return _text(values, key, _INVALID_APPROVAL)


def _timestamp(value: object, message: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise TypeError(message)
    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        raise TypeError(message) from error


def _status(value: object) -> DurableApprovalStatus:
    for status in APPROVAL_STATUSES:
        if value == status:
            return status
    raise TypeError(_INVALID_APPROVAL)


def _execution_status(value: object) -> DurableExecutionStatus | None:
    if value is None:
        return None
    for status in _EXECUTION_STATUSES:
        if value == status:
            return status
    raise TypeError(_INVALID_APPROVAL)


def _function(payload: object, message: str) -> DurableApprovalFunction:
    values = _fields(payload, message)
    function_id = values.get("id")
    if function_id is not None and not isinstance(function_id, str):
        raise TypeError(message)
    return DurableApprovalFunction(
        id=function_id, name=_identifier(values, "name", message)
    )


def _execution(payload: object) -> DurableApprovalExecution:
    values = _fields(payload, _INVALID_APPROVAL)
    return DurableApprovalExecution(
        id=_optional_identifier(values, "id"),
        name=_identifier(values, "name", _INVALID_APPROVAL),
        status=_execution_status(values.get("status")),
    )


def _decider(payload: object) -> DurableApprovalDecider | None:
    if payload is None:
        return None
    values = _fields(payload, _INVALID_APPROVAL)
    return DurableApprovalDecider(
        id=_text(values, "id", _INVALID_APPROVAL),
        email=_text(values, "email", _INVALID_APPROVAL),
    )


def _decision(payload: object) -> DurableApprovalDecision | None:
    if payload is None:
        return None
    values = _fields(payload, _INVALID_APPROVAL)
    return DurableApprovalDecision(
        comment=_text(values, "comment", _INVALID_APPROVAL),
        decided_by=_decider(values.get("decided_by")),
        decided_at=_timestamp(values.get("decided_at"), _INVALID_APPROVAL),
    )


def _expires_at(value: object) -> datetime | None:
    if value is None:
        return None
    return _timestamp(value, _INVALID_APPROVAL)


def durable_approval(payload: object) -> DurableApproval:
    """Validate and snapshot one durable approval.

    Returns:
        The complete approval model.

    """
    values = _fields(payload, _INVALID_APPROVAL)
    return DurableApproval(
        id=_identifier(values, "id", _INVALID_APPROVAL),
        status=_status(values.get("status")),
        name=_text(values, "name", _INVALID_APPROVAL),
        title=_text(values, "title", _INVALID_APPROVAL),
        description=_text(values, "description", _INVALID_APPROVAL),
        function=_function(values.get("function"), _INVALID_APPROVAL),
        execution=_execution(values.get("execution")),
        requested_at=_timestamp(values.get("requested_at"), _INVALID_APPROVAL),
        expires_at=_expires_at(values.get("expires_at")),
        decision=_decision(values.get("decision")),
        details=json_value(values.get("details"), _INVALID_APPROVAL),
    )


def durable_approval_page(payload: object) -> DurableApprovalPage:
    """Validate and snapshot a page of approvals.

    Returns:
        Approvals and validated pagination metadata.

    Raises:
        TypeError: The page container or pagination fields are invalid.

    """
    values = _fields(payload, _INVALID_PAGE)
    data: object = values.get("data")
    if data is None:
        data = list[object]()
    if not _is_sequence(data):
        raise TypeError(_INVALID_PAGE)
    has_more = values.get("has_more", False)
    if not isinstance(has_more, bool):
        raise TypeError(_INVALID_PAGE)
    return DurableApprovalPage(
        approvals=tuple(durable_approval(entry) for entry in data),
        page=_page_count(values.get("page")),
        limit=_page_count(values.get("limit")),
        total=_page_count(values.get("total")),
        has_more=has_more,
    )


def _page_count(value: object) -> int:
    if value is None:
        return 0
    if type(value) is not int:
        raise TypeError(_INVALID_PAGE)
    return value


def _count(values: Mapping[str, object], key: str) -> int:
    value = values.get(key)
    if type(value) is not int:
        raise TypeError(_INVALID_STATS)
    return value


def _counts(payload: object) -> DurableApprovalCounts:
    values = _fields(payload, _INVALID_STATS)
    requested, pending, approved, denied, expired, cancelled = (
        _count(values, key) for key in _COUNT_FIELDS
    )
    return DurableApprovalCounts(
        requested=requested,
        pending=pending,
        approved=approved,
        denied=denied,
        expired=expired,
        cancelled=cancelled,
    )


def _rate(value: object) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(_INVALID_STATS)
    if not math.isfinite(value):
        raise TypeError(_INVALID_STATS)
    return float(value)


def _entries(value: object) -> tuple[Mapping[str, object], ...]:
    if not _is_sequence(value):
        raise TypeError(_INVALID_STATS)
    return tuple(_fields(entry, _INVALID_STATS) for entry in value)


def _function_counts(values: Mapping[str, object]) -> DurableApprovalFunctionCounts:
    return DurableApprovalFunctionCounts(
        function=_function(values.get("function"), _INVALID_STATS),
        counts=_counts(values.get("counts")),
    )


def _day(value: object) -> date:
    if not isinstance(value, str):
        raise TypeError(_INVALID_STATS)
    try:
        return date.fromisoformat(value)
    except ValueError as error:
        raise TypeError(_INVALID_STATS) from error


def _daily_counts(values: Mapping[str, object]) -> DurableApprovalDailyCounts:
    return DurableApprovalDailyCounts(
        day=_day(values.get("date")), counts=_counts(values.get("counts"))
    )


def durable_approval_stats(payload: object) -> DurableApprovalStats:
    """Validate and snapshot approval stats.

    Returns:
        The complete stats model.

    """
    values = _fields(payload, _INVALID_STATS)
    return DurableApprovalStats(
        from_=_timestamp(values.get("from"), _INVALID_STATS),
        to=_timestamp(values.get("to"), _INVALID_STATS),
        counts=_counts(values.get("counts")),
        approval_rate=_rate(values.get("approval_rate")),
        median_seconds_to_decision=_rate(values.get("median_seconds_to_decision")),
        p90_seconds_to_decision=_rate(values.get("p90_seconds_to_decision")),
        functions=tuple(
            _function_counts(entry) for entry in _entries(values.get("functions"))
        ),
        other_functions=_counts(values.get("other_functions")),
        daily=tuple(_daily_counts(entry) for entry in _entries(values.get("daily"))),
    )
