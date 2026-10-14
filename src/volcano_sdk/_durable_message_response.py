"""Validate durable message responses before exposing immutable models."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import TypeGuard

from ._durable_response import json_value
from .models import (
    DurableMessage,
    DurableMessageDirection,
    DurableMessagePage,
    DurableMessageSender,
    DurableMessageStatus,
)

_INVALID_MESSAGE = "Expected a complete durable message"
_INVALID_PAGE = "Expected a complete durable message page"
_DIRECTIONS: tuple[DurableMessageDirection, ...] = ("in", "out")
_STATUSES: tuple[DurableMessageStatus, ...] = (
    "queued",
    "delivering",
    "delivered",
    "dropped",
    "published",
)


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


def _text(values: Mapping[str, object], key: str) -> str:
    value = values.get(key)
    if not isinstance(value, str) or not value:
        raise TypeError(_INVALID_MESSAGE)
    return value


def _timestamp(value: object) -> datetime:
    if not isinstance(value, str):
        raise TypeError(_INVALID_MESSAGE)
    try:
        return datetime.fromisoformat(value)
    except ValueError as error:
        raise TypeError(_INVALID_MESSAGE) from error


def _direction(value: object) -> DurableMessageDirection:
    for direction in _DIRECTIONS:
        if value == direction:
            return direction
    raise TypeError(_INVALID_MESSAGE)


def _status(value: object) -> DurableMessageStatus:
    for status in _STATUSES:
        if value == status:
            return status
    raise TypeError(_INVALID_MESSAGE)


def _seq(value: object) -> int:
    if type(value) is not int or value < 1:
        raise TypeError(_INVALID_MESSAGE)
    return value


def _sender(payload: object) -> DurableMessageSender:
    values = _fields(payload, _INVALID_MESSAGE)
    user_id = values.get("user_id")
    if user_id is not None and not isinstance(user_id, str):
        raise TypeError(_INVALID_MESSAGE)
    return DurableMessageSender(type=_text(values, "type"), user_id=user_id)


def _delivered_at(value: object) -> datetime | None:
    if value is None:
        return None
    return _timestamp(value)


def durable_message(payload: object) -> DurableMessage:
    """Validate and snapshot one durable message.

    Returns:
        The complete message model.

    """
    values = _fields(payload, _INVALID_MESSAGE)
    return DurableMessage(
        id=_text(values, "id"),
        execution_id=_text(values, "execution_id"),
        direction=_direction(values.get("direction")),
        seq=_seq(values.get("seq")),
        name=_text(values, "name"),
        data=json_value(values.get("data"), _INVALID_MESSAGE),
        sender=_sender(values.get("sender")),
        status=_status(values.get("status")),
        sent_at=_timestamp(values.get("sent_at")),
        delivered_at=_delivered_at(values.get("delivered_at")),
    )


def broadcast_prev_seq(payload: object) -> int:
    """Read the `seq` a broadcast says the execution published before it.

    Returns:
        That `seq`, or 0, naming no gap, when the broadcast has none.

    """
    prev_seq = payload.get("prev_seq") if _is_mapping(payload) else None
    return prev_seq if type(prev_seq) is int else 0


def durable_message_page(payload: object) -> DurableMessagePage:
    """Validate and snapshot a page of messages.

    Returns:
        The messages and whether more follow.

    Raises:
        TypeError: The page container or `has_more` is invalid.

    """
    values = _fields(payload, _INVALID_PAGE)
    data = values.get("data")
    has_more = values.get("has_more")
    if not _is_sequence(data) or not isinstance(has_more, bool):
        raise TypeError(_INVALID_PAGE)
    return DurableMessagePage(
        messages=tuple(durable_message(entry) for entry in data),
        has_more=has_more,
    )
