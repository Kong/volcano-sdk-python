"""Public Volcano SDK value objects."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal, TypeAlias

if TYPE_CHECKING:
    from datetime import datetime

JSONValue: TypeAlias = (
    str | int | float | bool | list["JSONValue"] | dict[str, "JSONValue"] | None
)
OAuthProviderName: TypeAlias = Literal["google", "github", "microsoft", "apple"]


@dataclass(frozen=True, slots=True)
class User:
    """Authenticated Volcano user."""

    id: str
    email: str
    project_id: str | None = None
    email_confirmed: bool | None = None
    user_metadata: dict[str, JSONValue] | None = field(default=None, repr=False)
    app_metadata: dict[str, JSONValue] | None = field(default=None, repr=False)
    avatar_url: str | None = None
    status: str | None = None
    banned_until: datetime | None = None
    last_sign_in_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


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


@dataclass(frozen=True, slots=True)
class LockLease:
    """Lease returned for an acquired distributed lock."""

    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
