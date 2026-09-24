"""Distributed lock request validation and response values."""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from uuid import UUID, uuid4

from typing_extensions import TypeIs

_MIN_LOCK_TTL_SECONDS = 5
_MAX_LOCK_TTL_SECONDS = 7_776_000
_INVALID_LOCK_TTL = "ttl must be an integer between 5 seconds and 90 days"
INVALID_LOCK_RESPONSE = "Expected a complete lock response"


def parse_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


def is_lock_mapping(payload: object) -> TypeIs[Mapping[object, object]]:
    return isinstance(payload, Mapping)


def lock_values(payload: object) -> Mapping[object, object]:
    if not is_lock_mapping(payload):
        raise TypeError(INVALID_LOCK_RESPONSE)
    return payload


def fencing_token(value: object) -> int | None:
    if value is None or type(value) is int:
        return value
    raise TypeError(INVALID_LOCK_RESPONSE)


def lease_fields(payload: Mapping[object, object]) -> tuple[datetime, int]:
    expires_at = payload.get("expires_at")
    fencing_token = payload.get("fencing_token")
    if not isinstance(expires_at, str) or type(fencing_token) is not int:
        raise TypeError(INVALID_LOCK_RESPONSE)
    return datetime.fromisoformat(expires_at), fencing_token


def validate_ttl(ttl: object) -> None:
    if (
        isinstance(ttl, bool)
        or not isinstance(ttl, int)
        or not _MIN_LOCK_TTL_SECONDS <= ttl <= _MAX_LOCK_TTL_SECONDS
    ):
        raise ValueError(_INVALID_LOCK_TTL)


def request_uuid(value: str | None, name: str) -> str:
    if value is None:
        return str(uuid4())
    try:
        _ = UUID(value)
    except (AttributeError, ValueError) as error:
        message = f"{name} must be a UUID string"
        raise ValueError(message) from error
    return value
