"""Internal session continuity checks shared by refresh and revocation."""

from __future__ import annotations

import base64
import json
from collections.abc import Mapping
from typing import TYPE_CHECKING, cast
from uuid import UUID

from .errors import AuthenticationError

if TYPE_CHECKING:
    from .models import Session

_JWT_PARTS = 3
_REFRESH_USER_MISMATCH = "Refreshed session belongs to a different user"
_REFRESH_SESSION_MISMATCH = "Refreshed credentials belong to a different server session"
_MISSING_SESSION_ID = "Cannot refresh supplied credentials without a session identifier"


def session_id_from_access_token(access_token: str) -> str | None:
    """Read an untrusted continuity constraint; this never authenticates a user."""
    parts = access_token.split(".")
    if len(parts) != _JWT_PARTS:
        return None
    padding = "=" * (-len(parts[1]) % 4)
    try:
        payload: object = json.loads(
            base64.urlsafe_b64decode(parts[1] + padding).decode()
        )
    except (ValueError, UnicodeDecodeError, RecursionError):
        return None
    if not isinstance(payload, Mapping):
        return None
    values = cast("Mapping[object, object]", payload)
    session_id = values.get("session_id")
    if not isinstance(session_id, str) or not session_id.strip():
        return None
    try:
        return str(UUID(session_id.strip()))
    except ValueError:
        return None


def validate_refresh_source(current: Session, *, verified: bool = False) -> None:
    """Require a session constraint for supplied credentials."""
    if not verified and session_id_from_access_token(current.access_token) is None:
        raise AuthenticationError(_MISSING_SESSION_ID)


def validate_refresh_identity(current: Session | None, refreshed: Session) -> None:
    """Reject a refresh outside the captured server session or validated user."""
    if current is None:
        return
    session_id = session_id_from_access_token(current.access_token)
    if session_id is not None and session_id != session_id_from_access_token(
        refreshed.access_token
    ):
        raise AuthenticationError(_REFRESH_SESSION_MISMATCH)
    if current.user_id is None:
        return
    if current.user_id == refreshed.user_id:
        return
    try:
        matches = UUID(current.user_id) == UUID(str(refreshed.user_id))
    except ValueError:
        matches = False
    if not matches:
        raise AuthenticationError(_REFRESH_USER_MISMATCH)
