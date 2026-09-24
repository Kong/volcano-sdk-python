"""Public Sandbox options and response values."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NotRequired, TypedDict


class SandboxCreateOptions(TypedDict):
    """Choose one preset or named Sandbox for a session."""

    region: str
    preset: NotRequired[str]
    sandbox_id: NotRequired[str]
    memory_mb: NotRequired[int]
    max_duration_seconds: NotRequired[int]
    idle_timeout_seconds: NotRequired[int]
    request_id: NotRequired[str]


class SandboxCommandOptions(TypedDict, total=False):
    """Command timeout, environment, and stable retry identity."""

    timeout_seconds: int
    environment: dict[str, str]
    request_id: str


class SandboxExecOptions(SandboxCreateOptions, SandboxCommandOptions):
    """One-shot execution selector and command options."""


@dataclass(frozen=True)
class SandboxCommandResult:
    """Command output, including nonzero exit codes as data."""

    stdout: str
    stderr: str
    exit_code: int
    timed_out: bool
    stdout_truncated: bool
    stderr_truncated: bool


@dataclass(frozen=True)
class SandboxExecutionResult(SandboxCommandResult):
    """One-shot output returned after session reclamation."""

    session_id: str
    region: str
    duration_ms: int


@dataclass(frozen=True)
class SandboxAccess:
    """Expiring HTTP access; the credential is omitted from representations."""

    url: str
    token: str = field(repr=False)
    expires_at: str


@dataclass(frozen=True)
class SandboxPreset:
    """Published preset and its available memory and regions."""

    id: str
    memory_mb: int
    regions: tuple[str, ...]
