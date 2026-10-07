"""Public custom Sandbox deployment options and response values."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, NotRequired, TypedDict


class SandboxDeployOptions(TypedDict):
    """A build configuration and stable replay identity."""

    name: str
    memory_mb: NotRequired[Literal[1024, 2048]]
    ports: NotRequired[list[int]]
    request_id: NotRequired[str]


class SandboxBuildLogOptions(TypedDict):
    """Regional build log selection and pagination."""

    region: str
    cursor: NotRequired[str]
    limit: NotRequired[int]


@dataclass(frozen=True)
class SandboxDeployment:
    """The current status of one custom image deployment."""

    id: str
    status: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class SandboxDeploymentPage:
    """One page of deployment history."""

    data: tuple[SandboxDeployment, ...]
    limit: int
    has_more: bool
    next_cursor: str | None


@dataclass(frozen=True)
class SandboxBuildLog:
    """A timestamped build message."""

    timestamp: str
    message: str


@dataclass(frozen=True)
class SandboxBuildLogPage:
    """A bounded page of regional build output."""

    data: tuple[SandboxBuildLog, ...]
    next_cursor: str | None
