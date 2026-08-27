"""Distributed lock facade."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import uuid4

from ._transport import Transport, invoke, response_payload
from .models import LockLease


class LocksContext(Protocol):
    """Client capabilities required by distributed locks."""

    _transport: Transport

    def _service_token(self) -> str: ...


def _parse_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


class Locks:
    """Acquire and release project-scoped distributed locks."""

    def __init__(self, client: LocksContext) -> None:
        """Create a lock facade backed by a client."""
        self._client = client

    def acquire(self, key: str, *, ttl: int) -> LockLease:
        """Acquire a lock lease for the requested number of seconds."""
        token = str(uuid4())
        response = invoke(
            self._client._transport.acquire_project_lock,
            authorization=self._client._service_token(),
            key=key,
            ttl=ttl,
            token=token,
        )
        payload = response_payload(response, 201)
        return LockLease(
            key=key,
            token=token,
            expires_at=_parse_datetime(payload.get("expires_at")),
            fencing_token=payload.get("fencing_token"),
        )

    def release(self, key: str, lease: LockLease) -> None:
        """Release a lock lease."""
        response = invoke(
            self._client._transport.release_project_lock,
            authorization=self._client._service_token(),
            key=key,
            token=lease.token,
        )
        response_payload(response, 204)
