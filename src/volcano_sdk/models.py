"""Public Volcano SDK value objects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


@dataclass(frozen=True, slots=True)
class Session:
    """Authenticated user session."""

    access_token: str
    refresh_token: str
    user_id: str


@dataclass(frozen=True, slots=True)
class LockLease:
    """Lease returned for an acquired distributed lock."""

    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
