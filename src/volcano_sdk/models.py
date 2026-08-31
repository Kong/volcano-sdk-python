"""Public Volcano SDK value objects."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import TYPE_CHECKING, TypeAlias

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

    def __post_init__(self) -> None:
        """Defensively freeze nested metadata owned by this value."""
        object.__setattr__(self, "user_metadata", _freeze_metadata(self.user_metadata))


@dataclass(frozen=True, slots=True)
class Session:
    """Authenticated user session."""

    access_token: str
    refresh_token: str
    user_id: str


@dataclass(frozen=True, slots=True)
class SignUpResult:
    """Session-less acknowledgement returned after sign-up."""

    confirmation_required: bool
    message: str


@dataclass(frozen=True, slots=True)
class LockLease:
    """Lease returned for an acquired distributed lock."""

    key: str
    token: str
    expires_at: datetime | None
    fencing_token: int | None
