"""Public Volcano SDK value objects."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, Literal, TypeAlias, TypedDict

if TYPE_CHECKING:
    from datetime import datetime

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
OAuthProviderName: TypeAlias = Literal["google", "github", "microsoft", "apple"]
AuthMethodType: TypeAlias = Literal["password", "oauth", "anonymous"]


class SessionListOptions(TypedDict, total=False):
    """Optional filters and cursor controls for listing device sessions."""

    sort: Literal["last_activity", "created_at"]
    status: Literal["active", "expired"]
    cursor: str
    ending_before: str
    offset: int


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
    """Authenticated Volcano user."""

    id: str
    email: str
    project_id: str | None = None
    email_confirmed: bool | None = None
    user_metadata: Mapping[str, JSONValue] | None = field(
        default=None,
        repr=False,
    )
    app_metadata: Mapping[str, JSONValue] | None = field(
        default=None,
        repr=False,
    )
    avatar_url: str | None = None
    status: str | None = None
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

    access_token: str = field(repr=False)
    refresh_token: str | None = field(default=None, repr=False)
    user_id: str | None = None
    expires_in: int | None = None


@dataclass(frozen=True, slots=True)
class SignUpResult:
    """Result of an email-and-password sign-up request."""

    confirmation_required: bool
    message: str
    user: User | None = None
    session: Session | None = None


@dataclass(frozen=True, slots=True)
class MessageResult:
    """Acknowledgement returned by an authentication operation."""

    message: str


@dataclass(frozen=True, slots=True)
class EmailChangeResult:
    """Result of an email-change request."""

    message: str
    new_email: str
    email_change_token: str | None = field(default=None, repr=False)


@dataclass(frozen=True, slots=True)
class AuthorizationRequest:
    """Authorization URL and state for a hosted authentication flow."""

    authorization_url: str = field(repr=False)
    state: str = field(repr=False)


@dataclass(frozen=True, slots=True)
class OAuthProvider:
    """OAuth provider linked to the current user."""

    provider: OAuthProviderName
    linked_at: datetime | None = None
    updated_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class OAuthTokenResult:
    """Acknowledgement for an OAuth provider-token operation."""

    provider: OAuthProviderName
    expires_in: int | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class AuthIdentity:
    """Verified email identity owned by the current user."""

    id: str
    email: str
    email_verified: bool
    is_primary: bool
    created_at: datetime


@dataclass(frozen=True, slots=True)
class AuthMethod:
    """Sign-in method owned by the current user."""

    id: str
    type: AuthMethodType
    identity_id: str
    email: str
    is_primary: bool
    created_at: datetime
    updated_at: datetime
    provider: str | None = None
    last_used_at: datetime | None = None


@dataclass(frozen=True, slots=True)
class AuthSession:
    """Device session associated with the current user."""

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
    """Page of device sessions associated with the current user."""

    sessions: tuple[AuthSession, ...] = ()
    total: int | None = None
    page: int | None = None
    limit: int | None = None
    total_pages: int | None = None
    has_more: bool | None = None
    next_cursor: str | None = None
    prev_cursor: str | None = None


@dataclass(frozen=True, slots=True)
class LockLease:
    """Lease returned for an acquired distributed lock."""

    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
