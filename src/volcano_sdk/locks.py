from __future__ import annotations

from datetime import datetime
from typing import Any, Protocol
from uuid import uuid4

from ._transport import Transport, invoke, response_payload
from .models import LockLease


class LocksContext(Protocol):
    _transport: Transport

    def _service_token(self) -> str: ...


def _parse_datetime(value: Any) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(str(value))


class Locks:
    def __init__(self, client: LocksContext) -> None:
        self._client = client

    def acquire(self, key: str, *, ttl: int) -> LockLease:
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
        response = invoke(
            self._client._transport.release_project_lock,
            authorization=self._client._service_token(),
            key=key,
            token=lease.token,
        )
        response_payload(response, 204)
