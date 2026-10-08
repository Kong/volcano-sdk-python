"""Public Volcano SDK value objects."""

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from datetime import date, datetime
from types import MappingProxyType
from typing import Literal, TypeAlias, TypedDict

from ._json_values import JSONValue as _JSONValue
from ._json_values import freeze_json

JSONValue: TypeAlias = _JSONValue
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
# "unknown" is terminal and the platform writes it itself, for an execution
# whose outcome it could not find out. Code that switches on status has to
# handle it, or it treats a finished execution as one still running.
DurableExecutionStatus: TypeAlias = Literal[
    "pending",
    "running",
    "succeeded",
    "failed",
    "timed_out",
    "stopped",
    "unknown",
]
DURABLE_TERMINAL_STATUSES: frozenset[DurableExecutionStatus] = frozenset(
    {"succeeded", "failed", "timed_out", "stopped", "unknown"}
)
# Every status but "pending" is final. "expired" means the approval's timeout
# passed first; "cancelled" means its execution ended while it was pending.
DurableApprovalStatus: TypeAlias = Literal[
    "pending",
    "approved",
    "denied",
    "expired",
    "cancelled",
]


def _freeze_metadata(
    value: Mapping[str, JSONValue] | None,
) -> Mapping[str, JSONValue] | None:
    if value is None:
        return None
    return MappingProxyType({key: freeze_json(item) for key, item in value.items()})


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
    """Local credentials with optional refresh credentials and user identity."""

    access_token: str
    refresh_token: str | None = None
    user_id: str | None = None
    user: Mapping[str, JSONValue] | None = field(default=None, repr=False, hash=False)

    def __post_init__(self) -> None:
        """Own a local user snapshot without treating it as server validation."""
        object.__setattr__(self, "user", _freeze_metadata(self.user))


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

    data: JSONValue = field(hash=False)
    status: int
    headers: Mapping[str, str] = field(hash=False)
    version: str | None

    def __post_init__(self) -> None:
        """Defensively freeze response data and headers."""
        object.__setattr__(self, "data", freeze_json(self.data))
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
            tuple(freeze_json(event) for event in self.data),
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
            tuple(freeze_json(bucket) for bucket in self.data),
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


@dataclass(frozen=True, slots=True)
class DurableExecutionFailure:
    """Why a failed or timed-out execution ended.

    A value read off an execution, not an exception. Named for that: every
    `*Error` this package exports subclasses `VolcanoError`, so a reader who
    wrote `except DurableExecutionError:` on the wire schema's name would get a
    `TypeError` about catching a class that is not an exception.
    """

    type: str | None = None
    message: str | None = None


@dataclass(frozen=True, slots=True)
class DurableExecution:
    """A durable execution, as the platform last observed it."""

    id: str
    function_id: str
    name: str
    status: DurableExecutionStatus
    region: str
    created_at: datetime
    # Whatever the function returned. Absent while the execution is still
    # running, and absent once the result stops being retained -- which is not
    # the same as a function that returned nothing, so read result_expired
    # before concluding anything from a missing result.
    result: JSONValue = field(default=None, repr=False, hash=False)
    result_expired: bool | None = None
    error: DurableExecutionFailure | None = None
    completed_at: datetime | None = None

    def __post_init__(self) -> None:
        """Defensively freeze the function's own result."""
        object.__setattr__(self, "result", freeze_json(self.result))

    @property
    def is_terminal(self) -> bool:
        """Report whether the execution has stopped changing."""
        return self.status in DURABLE_TERMINAL_STATUSES


@dataclass(frozen=True, slots=True)
class DurableExecutionPage:
    """One page of a durable function's executions, most recent first."""

    executions: tuple[DurableExecution, ...]
    page: int
    limit: int
    total: int
    has_more: bool

    def __post_init__(self) -> None:
        """Defensively snapshot the executions in this page."""
        object.__setattr__(self, "executions", tuple(self.executions))


class DurableApprovalStatsOptions(TypedDict, total=False):
    """Narrow approval stats to one function and a window.

    The window defaults to the last 30 days and may span at most 366.
    """

    # A durable function's id or name.
    function: str
    from_: datetime
    to: datetime


class DurableApprovalListOptions(TypedDict, total=False):
    """Filter and page a project's durable approvals."""

    status: DurableApprovalStatus
    # A durable function's id or name.
    function: str
    execution_id: str
    # Requested at or after `from_`, and before `to`.
    from_: datetime
    to: datetime
    page: int
    limit: int


@dataclass(frozen=True, slots=True)
class DurableApprovalDecider:
    """The person who approved or denied an approval."""

    id: str
    email: str


@dataclass(frozen=True, slots=True)
class DurableApprovalDecision:
    """Who decided an approval, when, and what they said."""

    comment: str
    # None once the deciding account no longer exists.
    decided_by: DurableApprovalDecider | None
    decided_at: datetime


@dataclass(frozen=True, slots=True)
class DurableApprovalFunction:
    """The durable function that requested an approval."""

    # None once the function has been deleted; the name is kept.
    id: str | None
    name: str


@dataclass(frozen=True, slots=True)
class DurableApprovalExecution:
    """The durable execution that requested an approval."""

    # Both None once the execution is no longer retained; the name is kept.
    id: str | None
    name: str
    status: DurableExecutionStatus | None


@dataclass(frozen=True, slots=True)
class DurableApproval:
    """An approval a durable workflow requested with `ctx.wait_for_approval`."""

    id: str
    status: DurableApprovalStatus
    name: str
    title: str
    description: str
    function: DurableApprovalFunction
    execution: DurableApprovalExecution
    requested_at: datetime
    # None when the workflow set no timeout: the approval then lasts as long as
    # its execution.
    expires_at: datetime | None
    # Set only once the approval is approved or denied.
    decision: DurableApprovalDecision | None
    details: JSONValue = field(default=None, repr=False, hash=False)

    def __post_init__(self) -> None:
        """Defensively freeze the details the workflow attached."""
        object.__setattr__(self, "details", freeze_json(self.details))

    @property
    def is_pending(self) -> bool:
        """Report whether the approval is still waiting for a decision."""
        return self.status == "pending"


@dataclass(frozen=True, slots=True)
class DurableApprovalPage:
    """One page of a project's durable approvals, most recent first."""

    approvals: tuple[DurableApproval, ...]
    page: int
    limit: int
    total: int
    has_more: bool

    def __post_init__(self) -> None:
        """Defensively snapshot the approvals in this page."""
        object.__setattr__(self, "approvals", tuple(self.approvals))


@dataclass(frozen=True, slots=True)
class DurableApprovalCounts:
    """Approvals counted by outcome; `requested` is all of them."""

    requested: int
    pending: int
    approved: int
    denied: int
    expired: int
    cancelled: int


@dataclass(frozen=True, slots=True)
class DurableApprovalFunctionCounts:
    """Approval counts for one durable function."""

    function: DurableApprovalFunction
    counts: DurableApprovalCounts


@dataclass(frozen=True, slots=True)
class DurableApprovalDailyCounts:
    """Approval counts for one UTC day, by the day they were requested."""

    day: date
    counts: DurableApprovalCounts


@dataclass(frozen=True, slots=True)
class DurableApprovalStats:
    """Approval outcomes and decision times over a window."""

    from_: datetime
    to: datetime
    counts: DurableApprovalCounts
    # Each None while there is nothing to compute it from.
    approval_rate: float | None
    median_seconds_to_decision: float | None
    p90_seconds_to_decision: float | None
    # The ten functions with the most requests; the rest are summed in
    # other_functions.
    functions: tuple[DurableApprovalFunctionCounts, ...]
    other_functions: DurableApprovalCounts
    # Days with no requests are left out.
    daily: tuple[DurableApprovalDailyCounts, ...]

    def __post_init__(self) -> None:
        """Defensively snapshot the per-function and per-day breakdowns."""
        object.__setattr__(self, "functions", tuple(self.functions))
        object.__setattr__(self, "daily", tuple(self.daily))
