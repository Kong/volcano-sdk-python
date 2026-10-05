"""Realtime values, payload validation, and fetch configuration."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field, replace
from types import MappingProxyType
from typing import (
    TYPE_CHECKING,
    Literal,
    TypeAlias,
    TypeVar,
)

from centrifuge import CentrifugeError

import volcano_sdk._realtime_transport as _native

from ._json_values import freeze_json

if TYPE_CHECKING:
    from typing import TypeGuard

    from ._session_operations import SessionOperations
    from .models import JSONValue

CentrifugeConnection: TypeAlias = _native.CentrifugeConnection


CentrifugeFactory: TypeAlias = _native.CentrifugeFactory


CentrifugeSubscription: TypeAlias = _native.CentrifugeSubscription


Publication: TypeAlias = _native.Publication


PublicationContext: TypeAlias = _native.PublicationContext


RealtimeContext: TypeAlias = _native.RealtimeContext


_MessageT = TypeVar("_MessageT")


MessageCallback: TypeAlias = Callable[[_MessageT], object]


RealtimeCallback: TypeAlias = Callable[[_MessageT], object]


UnsubscribeCallback = Callable[[], None]


ChannelType: TypeAlias = Literal["broadcast", "presence", "postgres"]


PostgresEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE"]


PostgresListenerEvent: TypeAlias = Literal["INSERT", "UPDATE", "DELETE", "*"]


PostgresChangeCallback = Callable[["PostgresChange"], object]


POSTGRES_EVENTS = frozenset({"INSERT", "UPDATE", "DELETE"})


POSTGRES_CHANNEL_SEGMENTS = 3


POSTGRES_PUBLICATION_SEGMENTS = 5


CENTRIFUGE_ERROR: type[Exception] = CentrifugeError


CALLBACK_QUEUE_LIMIT = 128


POSTGRES_QUEUE_LIMIT = 128


POSTGRES_BATCH_WINDOW_MS = 20


POSTGRES_MAX_BATCH_SIZE = 50


NO_PENDING_CALLBACK = object()


CALLBACK_QUEUE_FULL_MESSAGE = (
    "Volcano realtime callback queue is full; publication dropped"
)


CHANNEL_NOT_SUBSCRIBED = "Channel must be subscribed before sending"


CHANNEL_REMOVAL_IN_PROGRESS = "realtime channel removal is in progress"


CHANNEL_NOT_MANAGED = "realtime channel is no longer managed"


PRESENCE_ONLY = "operation is only available for presence channels"


BROADCAST_ONLY = "send is only available for broadcast channels"


POSTGRES_ONLY = "operation is only available for postgres channels"


CALLBACK_NOT_CALLABLE = "callback must be callable"


SUBSCRIPTION_REGISTRY_UNAVAILABLE = (
    "centrifuge client subscription registry is unavailable"
)


NO_ACTIVE_SESSION = "No active session"


CONNECTION_SESSION_UNAVAILABLE = "Realtime connection has no session binding"


CONNECTION_SESSION_CHANGED = "Realtime connection session changed"


POSTGRES_FETCH_FAILED_MESSAGE = "Volcano realtime Postgres row fetch failed"


POSTGRES_QUERY_UNAVAILABLE = "Transport does not support realtime Postgres row fetch"


INVALID_POSTGRES_ROW_VALUE = "Realtime Postgres row contains a non-JSON value"


def empty_presence_data() -> Mapping[str, JSONValue]:
    return MappingProxyType({})


def freeze_mapping(value: Mapping[str, JSONValue]) -> Mapping[str, JSONValue]:
    return MappingProxyType({key: freeze_json(item) for key, item in value.items()})


def validate_channel_type(channel_type: str) -> ChannelType:
    if channel_type == "broadcast":
        return "broadcast"
    if channel_type == "presence":
        return "presence"
    if channel_type == "postgres":
        return "postgres"
    message = f"unsupported realtime channel type: {channel_type}"
    raise ValueError(message)


@dataclass(frozen=True, slots=True)
class RealtimeConnectContext:
    """Details reported after a realtime transport connects."""

    client: str | None = None


@dataclass(frozen=True, slots=True)
class RealtimeDisconnectContext:
    """Details reported after a realtime transport disconnects."""

    code: int | None = None
    reason: str | None = None


@dataclass(frozen=True, slots=True)
class RealtimeErrorContext:
    """Details reported when the realtime transport emits an error."""

    code: int | None = None
    message: str | None = None
    error: Exception | None = None


@dataclass(frozen=True, slots=True)
class RealtimePresenceInfo:
    """Immutable identity and metadata for one present realtime client."""

    client: str
    user: str | None = None
    data: Mapping[str, JSONValue] = field(
        default_factory=empty_presence_data,
        hash=False,
    )

    def __post_init__(self) -> None:
        """Defensively freeze nested connection metadata."""
        object.__setattr__(self, "data", freeze_mapping(self.data))


@dataclass(frozen=True, slots=True)
class PostgresChange:
    """Immutable RLS-scoped Postgres row-change notification."""

    type: PostgresEvent
    schema: str
    table: str
    record: Mapping[str, JSONValue] | None = field(default=None, hash=False)
    old_record: Mapping[str, JSONValue] | None = field(default=None, hash=False)
    columns: tuple[str, ...] | None = None
    timestamp: str = ""
    id: JSONValue = field(default=None, hash=False)
    mode: Literal["lightweight"] | None = None

    def __post_init__(self) -> None:
        """Defensively freeze nested row and identifier values."""
        if self.record is not None:
            object.__setattr__(self, "record", freeze_mapping(self.record))
        if self.old_record is not None:
            object.__setattr__(self, "old_record", freeze_mapping(self.old_record))
        object.__setattr__(self, "id", freeze_json(self.id))


def normalize_postgres_delete(change: PostgresChange) -> PostgresChange:
    if change.mode != "lightweight" or change.type != "DELETE":
        return change
    old_record = change.old_record
    if old_record is None and change.id is not None:
        old_record = {"id": change.id}
    return replace(change, old_record=old_record, id=None, mode=None)


def filter_postgres_changes(
    event: PostgresListenerEvent,
    schema: str,
    table: str,
    callback: PostgresChangeCallback,
) -> PostgresChangeCallback:
    def filtered(change: PostgresChange) -> object:
        if change.schema != schema or change.table != table:
            return None
        if event not in {"*", change.type}:
            return None
        return callback(change)

    return filtered


@dataclass(frozen=True, slots=True)
class PostgresFetchConfig:
    enabled: bool
    batch_window_ms: int
    max_batch_size: int

    @property
    def batch_window_seconds(self) -> float:
        return self.batch_window_ms / 1_000


def postgres_fetch_config(
    *,
    auto_fetch: bool,
    fetch_batch_window_ms: object,
    fetch_max_batch_size: object,
) -> PostgresFetchConfig:
    if type(fetch_batch_window_ms) is not int or fetch_batch_window_ms <= 0:
        message = "fetch_batch_window_ms must be a positive integer"
        raise ValueError(message)
    if (
        type(fetch_max_batch_size) is not int
        or not 1 <= fetch_max_batch_size <= POSTGRES_QUEUE_LIMIT
    ):
        message = (
            f"fetch_max_batch_size must be an integer between 1 and "
            f"{POSTGRES_QUEUE_LIMIT}"
        )
        raise ValueError(message)
    return PostgresFetchConfig(
        enabled=auto_fetch,
        batch_window_ms=fetch_batch_window_ms,
        max_batch_size=fetch_max_batch_size,
    )


@dataclass(frozen=True, slots=True)
class PostgresDeliveryIdentity:
    session_lineage: SessionOperations | None
    subscription_epoch: object


@dataclass(frozen=True, slots=True)
class PostgresDelivery:
    change: PostgresChange
    identity: PostgresDeliveryIdentity


@dataclass(frozen=True, slots=True)
class CallbackDelivery:
    event: str
    data: object
    postgres_identity: PostgresDeliveryIdentity | None = None
    delivery_epoch: object | None = None


def is_postgres_event(value: object) -> TypeGuard[PostgresEvent]:
    return isinstance(value, str) and value in POSTGRES_EVENTS


def is_object_sequence(value: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(value, (list, tuple))


def postgres_change(data: object) -> PostgresChange | None:
    if not _native.is_object_mapping(data):
        return None
    event = data.get("type")
    schema = data.get("schema")
    table = data.get("table")
    timestamp = data.get("timestamp")
    mode = data.get("mode")
    record = data.get("record")
    old_record = data.get("old_record")
    raw_columns = data.get("columns")
    identifier = data.get("id")
    if (
        not is_json_record_or_none(record)
        or not is_json_record_or_none(old_record)
        or not is_json_value(identifier)
    ):
        return None
    if (
        not is_postgres_event(event)
        or not isinstance(schema, str)
        or not isinstance(table, str)
        or not isinstance(timestamp, str)
        or not postgres_mode(mode)
    ):
        return None
    valid_columns, columns = postgres_columns(raw_columns)
    if not valid_columns:
        return None
    return PostgresChange(
        type=event,
        schema=schema,
        table=table,
        record=record,
        old_record=old_record,
        columns=columns,
        timestamp=timestamp,
        id=identifier,
        mode=mode,
    )


def is_json_record_or_none(value: object) -> TypeGuard[Mapping[str, JSONValue] | None]:
    return value is None or is_json_record(value)


def postgres_mode(value: object) -> TypeGuard[Literal["lightweight"] | None]:
    return value is None or value == "lightweight"


def postgres_columns(value: object) -> tuple[bool, tuple[str, ...] | None]:
    if value is None:
        return True, None
    if not is_object_sequence(value):
        return False, None
    columns: list[str] = []
    for column in value:
        if not isinstance(column, str):
            return False, None
        columns.append(column)
    return True, tuple(columns)


def is_json_value(value: object) -> TypeGuard[JSONValue]:
    if value is None or isinstance(value, (str, int, float, bool)):
        return True
    if is_object_sequence(value):
        return all(is_json_value(item) for item in value)
    if _native.is_object_mapping(value):
        return all(
            isinstance(key, str) and is_json_value(item) for key, item in value.items()
        )
    return False


def is_json_record(value: object) -> TypeGuard[Mapping[str, JSONValue]]:
    return _native.is_object_mapping(value) and all(
        isinstance(key, str) and is_json_value(item) for key, item in value.items()
    )


def checked_postgres_row(row: dict[str, object]) -> Mapping[str, JSONValue]:
    if not is_json_record(row):
        raise TypeError(INVALID_POSTGRES_ROW_VALUE)
    return row


def presence_info(info: object) -> RealtimePresenceInfo:
    data = _native.native_attribute(info, "conn_info")
    user = _native.native_attribute(info, "user")
    typed_data = data if is_json_record(data) else empty_presence_data()
    return RealtimePresenceInfo(
        client=str(_native.native_attribute(info, "client", "")),
        user=user if isinstance(user, str) else None,
        data=typed_data,
    )
