"""Sandbox creation, execution, and backend-granted session access."""

from __future__ import annotations

from dataclasses import asdict
from typing import Unpack, cast

from ._sandbox import (
    SandboxRequests,
    command_body,
    command_result,
    identifier,
    integer,
    record,
    request_id,
    selector,
    text,
)
from ._transport import SandboxRequest
from .sandbox_models import (
    SandboxCreateOptions,
    SandboxExecOptions,
    SandboxExecutionResult,
    SandboxPreset,
)
from .sandbox_session import SandboxSession


class Sandboxes:
    """Create isolated sessions or run a command to completion."""

    def __init__(self, requests: SandboxRequests) -> None:
        """Bind the client's Sandbox request scope."""
        self.requests = requests

    def presets(self) -> tuple[SandboxPreset, ...]:
        """List the published preset catalog.

        Returns:
            The validated response or request value.

        Raises:
            TypeError: If the supplied value violates the Sandbox contract.

        """
        payload = record(self.requests.send(SandboxRequest("list_sandbox_presets")))
        rows = payload.get("data")
        if not isinstance(rows, list):
            message = "Invalid Sandbox preset catalog"
            raise TypeError(message)
        return tuple(_preset(row) for row in cast("list[object]", rows))

    def create(
        self, project_id: str, **options: Unpack[SandboxCreateOptions]
    ) -> SandboxSession:
        """Create a session; preserve request_id when retrying an uncertain result.

        Returns:
            The validated response or request value.

        """
        body = selector(options)
        for key in ("max_duration_seconds", "idle_timeout_seconds"):
            if key in options:
                body[key] = integer(options.get(key))
        response = self.requests.send(
            SandboxRequest(
                "create_sandbox_session",
                identifier(project_id),
                body=body,
                request_id=request_id(options),
            ),
            201,
        )
        return SandboxSession(self.requests, response)

    def get(self, session_id: str) -> SandboxSession:
        """Fetch a session visible to the current credential.

        Returns:
            The validated response or request value.

        """
        response = self.requests.send(
            SandboxRequest("get_sandbox_session", identifier(session_id))
        )
        return SandboxSession(self.requests, response)

    def exec(
        self, project_id: str, command: str, **options: Unpack[SandboxExecOptions]
    ) -> SandboxExecutionResult:
        """Execute once and return output after confirmed reclamation.

        Returns:
            The validated response or request value.

        """
        body = selector(options) | command_body(command, options)
        result = record(
            self.requests.send(
                SandboxRequest(
                    "execute_sandbox",
                    identifier(project_id),
                    body=body,
                    request_id=request_id(options),
                )
            )
        )
        return SandboxExecutionResult(
            **asdict(command_result(result)),
            session_id=text(result.get("session_id")),
            region=text(result.get("region")),
            duration_ms=integer(result.get("duration_ms")),
        )

    def grant(self, session_id: str, auth_user_id: str, expires_at: str) -> None:
        """Grant one project auth user access until the specified expiry."""
        _ = self.requests.send(
            SandboxRequest(
                "grant_sandbox_session",
                identifier(session_id),
                identifier(auth_user_id),
                {"expires_at": expires_at},
            ),
            204,
        )

    def revoke(self, session_id: str, auth_user_id: str) -> None:
        """Revoke one user's session access."""
        _ = self.requests.send(
            SandboxRequest(
                "revoke_sandbox_session",
                identifier(session_id),
                identifier(auth_user_id),
            ),
            204,
        )


def _preset(value: object) -> SandboxPreset:
    data = record(value)
    regions = data.get("regions")
    if not isinstance(regions, list):
        message = "Invalid Sandbox regions"
        raise TypeError(message)
    return SandboxPreset(
        text(data.get("id")),
        integer(data.get("memory_mb")),
        tuple(text(region) for region in cast("list[object]", regions)),
    )
