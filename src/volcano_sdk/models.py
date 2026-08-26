from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Session:
    access_token: str
    refresh_token: str
    user_id: str


@dataclass(frozen=True, slots=True)
class LockLease:
    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
