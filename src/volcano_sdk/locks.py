"""Distributed lock facade."""

from __future__ import annotations

from datetime import datetime
from typing import Protocol, cast
from uuid import uuid4

from ._transport import Transport, invoke, response_payload
from .models import LockLease, LockState

_MIN_LOCK_TTL_SECONDS = 5
_MAX_LOCK_TTL_SECONDS = 7_776_000
_INVALID_LOCK_TTL = "ttl must be an integer between 5 seconds and 90 days"


class LocksContext(Protocol):
    """Client capabilities required by distributed locks."""

    _transport: Transport

    def _service_token(self) -> str: ...


class LockGetTransport(Protocol):
    """Transport capability required to inspect a lock."""

    def get_project_lock(
        self,
        *,
        authorization: str,
        key: str,
    ) -> object:
        """Get one project-scoped lock."""
        ...


class LockRenewTransport(Protocol):
    """Transport capability required to renew a lock."""

    def renew_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
    ) -> object:
        """Renew one project-scoped lock."""
        ...


class LockForceReleaseTransport(Protocol):
    """Transport capability required to force release a lock."""

    def force_release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
    ) -> object:
        """Force release one project-scoped lock."""
        ...


def _parse_datetime(value: object) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


def _validate_ttl(ttl: object) -> None:
    if (
        isinstance(ttl, bool)
        or not isinstance(ttl, int)
        or not _MIN_LOCK_TTL_SECONDS <= ttl <= _MAX_LOCK_TTL_SECONDS
    ):
        raise ValueError(_INVALID_LOCK_TTL)


class Locks:
    """Acquire and release project-scoped distributed locks."""

    def __init__(self, client: LocksContext) -> None:
        """Create a lock facade backed by a client."""
        self._client = client

    def get(self, key: str) -> LockState:
        """Return the current state of a project-scoped lock."""
        transport = cast("LockGetTransport", self._client._transport)
        response = invoke(
            transport.get_project_lock,
            authorization=self._client._service_token(),
            key=key,
        )
        payload = response_payload(response, 200)
        return LockState(
            held=payload["held"],
            expires_at=_parse_datetime(payload.get("expires_at")),
            fencing_token=payload.get("fencing_token"),
        )

    def acquire(self, key: str, *, ttl: int) -> LockLease:
        """Acquire a lock lease for the requested number of seconds."""
        _validate_ttl(ttl)
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

    def renew(self, key: str, lease: LockLease, *, ttl: int) -> LockLease:
        """Renew a lock lease and return its immutable replacement."""
        _validate_ttl(ttl)
        transport = cast("LockRenewTransport", self._client._transport)
        response = invoke(
            transport.renew_project_lock,
            authorization=self._client._service_token(),
            key=key,
            ttl=ttl,
            token=lease.token,
        )
        payload = response_payload(response, 200)
        return LockLease(
            key=key,
            token=lease.token,
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

    def force_release(self, key: str) -> None:
        """Release a lock regardless of which token owns it."""
        transport = cast("LockForceReleaseTransport", self._client._transport)
        response = invoke(
            transport.force_release_project_lock,
            authorization=self._client._service_token(),
            key=key,
        )
        response_payload(response, 204)
