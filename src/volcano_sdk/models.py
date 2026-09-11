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
UploadSessionState: TypeAlias = Literal[
    "pending",
    "uploading",
    "completing",
    "completed",
    "aborted",
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
    """Sign-up acknowledgement with an optional follow-up sign-in session."""

    confirmation_required: bool
    message: str
    session: Session | None = field(default=None, repr=False)


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


@dataclass(frozen=True, slots=True)
class LockState:
    """Current state of a distributed lock."""

    held: bool
    expires_at: datetime | None
    fencing_token: int | None


@dataclass(frozen=True, slots=True)
class FunctionResponse:
    """Response returned by an invoked function."""

    data: Mapping[str, JSONValue] | None = field(hash=False)
    status: int
    headers: Mapping[str, str] = field(hash=False)
    version: str | None

    def __post_init__(self) -> None:
        """Defensively freeze response data and headers."""
        object.__setattr__(self, "data", _freeze_json(self.data))
        object.__setattr__(
            self,
            "headers",
            MappingProxyType(dict(self.headers)),
        )


@dataclass(frozen=True, slots=True)
class LogSearchResponse:
    """Immutable page returned by a project log search."""

    data: tuple[Mapping[str, JSONValue], ...] = field(hash=False)
    limit: int
    has_more: bool
    next_cursor: str | None = None

    def __post_init__(self) -> None:
        """Defensively freeze log events owned by this value."""
        object.__setattr__(
            self,
            "data",
            tuple(_freeze_json(event) for event in self.data),
        )


@dataclass(frozen=True, slots=True)
class LogActivityResponse:
    """Immutable bucketed project log activity."""

    data: tuple[Mapping[str, JSONValue], ...] = field(hash=False)
    total: int

    def __post_init__(self) -> None:
        """Defensively freeze activity buckets owned by this value."""
        object.__setattr__(
            self,
            "data",
            tuple(_freeze_json(bucket) for bucket in self.data),
        )


@dataclass(frozen=True, slots=True)
class UploadSession:
    """Server-created state for a resumable storage upload."""

    session_id: str
    part_size: int
    total_parts: int
    expires_at: datetime


@dataclass(frozen=True, slots=True)
class UploadPart:
    """Metadata returned after uploading one resumable part."""

    part_number: int
    etag: str
    size: int


@dataclass(frozen=True, slots=True)
class UploadSessionStatus:
    """Server-reported progress for one resumable storage upload."""

    session_id: str
    status: UploadSessionState
    path: str
    content_type: str
    total_size: int
    part_size: int
    total_parts: int
    parts_uploaded: int
    bytes_uploaded: int
    parts: tuple[UploadPart, ...]
    expires_at: datetime
    created_at: datetime

    def __post_init__(self) -> None:
        """Defensively snapshot uploaded part metadata."""
        object.__setattr__(self, "parts", tuple(self.parts))


@dataclass(frozen=True, slots=True)
class StorageObject:
    """Object metadata returned by a storage bucket."""

    id: str
    bucket_id: str
    name: str
    size: int
    mime_type: str
    is_public: bool
    owner_id: str | None = None
    etag: str | None = None
    metadata: Mapping[str, JSONValue] | None = field(
        default=None,
        repr=False,
        hash=False,
    )
    created_at: datetime | None = None
    updated_at: datetime | None = None
    public_url: str | None = None

    def __post_init__(self) -> None:
        """Defensively freeze nested metadata owned by this value."""
        object.__setattr__(self, "metadata", _freeze_metadata(self.metadata))


@dataclass(frozen=True, slots=True)
class StoragePage:
    """Cursor-paginated objects from a storage bucket."""

    objects: tuple[StorageObject, ...]
    next_cursor: str | None = None

    def __post_init__(self) -> None:
        """Defensively snapshot the objects in this page."""
        object.__setattr__(self, "objects", tuple(self.objects))
