"""Internal session continuity checks shared by refresh and revocation."""

from __future__ import annotations

import base64
import json
from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, TypeGuard
from uuid import UUID

from .errors import AuthenticationError

if TYPE_CHECKING:
    from .models import Session

_JWT_PARTS = 3
_REFRESH_USER_MISMATCH = "Refreshed session belongs to a different user"
_REFRESH_SESSION_MISMATCH = "Refreshed credentials belong to a different server session"
_MISSING_SESSION_ID = "Cannot refresh supplied credentials without a session identifier"
_decode_json: Callable[[str], object] = json.loads


def _is_claim_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def session_id_from_access_token(access_token: str) -> str | None:
    """Read an untrusted continuity constraint; this never authenticates a user.

    Returns
    -------
    str or None
        The normalized session UUID, or None for an absent or malformed claim.

    """
    parts = access_token.split(".")
    if len(parts) != _JWT_PARTS:
        return None
    padding = "=" * (-len(parts[1]) % 4)
    try:
        payload = _decode_json(base64.urlsafe_b64decode(parts[1] + padding).decode())
    except (ValueError, UnicodeDecodeError, RecursionError):
        return None
    if not _is_claim_mapping(payload):
        return None
    return _normalized_session_id(payload.get("session_id"))


def _normalized_session_id(session_id: object) -> str | None:
    if not isinstance(session_id, str) or not session_id.strip():
        return None
    try:
        return str(UUID(session_id.strip()))
    except ValueError:
        return None


def validate_refresh_source(current: Session, *, verified: bool = False) -> None:
    """Require a session constraint for supplied credentials.

    Raises
    ------
    AuthenticationError
        The credentials are unverified and contain no usable session identifier.

    """
    if not verified and session_id_from_access_token(current.access_token) is None:
        raise AuthenticationError(_MISSING_SESSION_ID)


def validate_refresh_identity(current: Session | None, refreshed: Session) -> None:
    """Reject a refresh outside the captured server session or validated user.

    Raises
    ------
    AuthenticationError
        Refreshed credentials change a known session identifier or user identity.

    """
    if current is None:
        return
    session_id = session_id_from_access_token(current.access_token)
    if session_id is not None and session_id != session_id_from_access_token(
        refreshed.access_token
    ):
        raise AuthenticationError(_REFRESH_SESSION_MISMATCH)
    if current.user_id is not None and not _same_user_id(
        current.user_id, refreshed.user_id
    ):
        raise AuthenticationError(_REFRESH_USER_MISMATCH)


def _same_user_id(current: str, refreshed: str | None) -> bool:
    if current == refreshed:
        return True
    try:
        return UUID(current) == UUID(str(refreshed))
    except ValueError:
        return False
