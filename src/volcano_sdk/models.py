"""Public Volcano SDK value objects."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import datetime
from types import MappingProxyType
from typing import Literal, TypeAlias

JSONValue: TypeAlias = (
    str
    | int
    | float
    | bool
    | list["JSONValue"]
    | tuple["JSONValue", ...]
    | dict[str, "JSONValue"]
    | Mapping[str, "JSONValue"]
    | None
)
OAuthProviderName: TypeAlias = Literal["apple", "github", "google", "microsoft"]
AuthChangeEvent: TypeAlias = Literal[
    "INITIAL_SESSION",
    "SIGNED_IN",
    "SIGNED_OUT",
    "TOKEN_REFRESHED",
]


def _freeze_json(value: JSONValue) -> JSONValue:
    if isinstance(value, Mapping):
        return MappingProxyType(
            {key: _freeze_json(item) for key, item in value.items()}
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    return value


def _freeze_metadata(
    value: Mapping[str, JSONValue] | None,
) -> Mapping[str, JSONValue] | None:
    if value is None:
        return None
    return MappingProxyType({key: _freeze_json(item) for key, item in value.items()})


@dataclass(frozen=True, slots=True)
class User:
    """Server-validated Volcano user profile."""

    id: str
    email: str
    status: str
    email_confirmed: bool | None = None
    user_metadata: Mapping[str, JSONValue] | None = field(
        default=None,
        repr=False,
        hash=False,
    )
    project_id: str | None = None
    app_metadata: Mapping[str, JSONValue] | None = field(
        default=None,
        repr=False,
        hash=False,
    )
    avatar_url: str | None = None
    banned_until: datetime | None = None
    last_sign_in_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def __post_init__(self) -> None:
        """Defensively freeze nested metadata owned by this value."""
        object.__setattr__(self, "user_metadata", _freeze_metadata(self.user_metadata))
        object.__setattr__(self, "app_metadata", _freeze_metadata(self.app_metadata))


@dataclass(frozen=True, slots=True)
class Session:
    """Authenticated user session."""

    access_token: str
    refresh_token: str
    user_id: str


AuthStateCallback: TypeAlias = Callable[[AuthChangeEvent, Session | None], None]


@dataclass(frozen=True, slots=True, eq=False)
class AuthSubscription:
    """Handle for an authentication-state subscription."""

    _unsubscribe: Callable[[], None] = field(repr=False, compare=False)

    def unsubscribe(self) -> None:
        """Stop queued and future authentication-state notifications.

        A callback already selected for delivery may finish after this method
        returns.
        """
        self._unsubscribe()


@dataclass(frozen=True, slots=True)
class AuthSession:
    """Server-reported authentication session for one device."""

    id: str
    user_id: str
    provider: str
    expires_at: datetime
    is_active: bool
    is_current: bool
    user_agent: str | None = None
    ip_address: str | None = None
    last_ip_address: str | None = None
    last_activity_at: datetime | None = None
    session_started_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class SessionPage:
    """Offset-paginated authentication sessions."""

    sessions: tuple[AuthSession, ...]
    total: int
    page: int
    limit: int
    total_pages: int


@dataclass(frozen=True, slots=True)
class LinkedOAuthProvider:
    """OAuth provider linked to the current account."""

    provider: str
    linked_at: datetime
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class OAuthProviderTokenStatus:
    """Validity metadata for a server-held OAuth provider token."""

    message: str
    provider: str
    expires_in: int


@dataclass(frozen=True, slots=True)
class SignUpResult:
    """Session-less acknowledgement returned after sign-up."""

    confirmation_required: bool
    message: str


@dataclass(frozen=True, slots=True)
class EmailChangeResult:
    """Acknowledgement returned after requesting an email change."""

    message: str | None
    new_email: str | None


@dataclass(frozen=True, slots=True)
class LockLease:
    """Lease returned for an acquired distributed lock."""

    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
