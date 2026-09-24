"""Stateful Sandbox handle and byte-preserving guest files."""

from __future__ import annotations

import base64
from typing import TYPE_CHECKING, Self, Unpack

if TYPE_CHECKING:
    from types import TracebackType

from ._sandbox import (
    SandboxRequests,
    command_body,
    command_result,
    identifier,
    record,
    request_id,
    state,
    text,
)
from ._transport_sandbox import SandboxRequest
from .errors import ValidationError
from .sandbox_models import SandboxAccess, SandboxCommandOptions, SandboxCommandResult

_FILE_LIMIT = 8 * 1024 * 1024


class SandboxFiles:
    """Read and write bytes inside a session."""

    def __init__(self, requests: SandboxRequests, session_id: str) -> None:
        """Bind files to a validated session identity."""
        self.requests: SandboxRequests = requests
        self.session_id: str = session_id

    def read(self, path: str) -> bytes:
        """Read a guest file without text conversion.

        Returns:
            The validated response or request value.

        """
        response = self.requests.send(
            SandboxRequest(
                "read_sandbox_session_file", self.session_id, body={"path": path}
            )
        )
        return base64.b64decode(text(record(response).get("data")), validate=True)

    def write(self, path: str, data: bytes) -> None:
        """Write up to 8 MiB of binary content.

        Raises:
            ValidationError: If the supplied value violates the Sandbox contract.

        """
        if len(data) > _FILE_LIMIT:
            message = "Sandbox files are limited to 8 MiB"
            raise ValidationError(message)
        _ = self.requests.send(
            SandboxRequest(
                "write_sandbox_session_file",
                self.session_id,
                body={"path": path, "data": base64.b64encode(data).decode()},
            ),
            204,
        )


class SandboxSession:
    """A session handle; context exit requests durable termination."""

    def __init__(self, requests: SandboxRequests, value: object) -> None:
        """Construct from a validated API response."""
        data = record(value)
        self.requests: SandboxRequests = requests
        self.id: str = identifier(text(data.get("id")))
        self.project_id: str = identifier(text(data.get("project_id")))
        self.region: str = text(data.get("region"))
        self.state: str = state(data.get("state"))
        self.expires_at: str = text(data.get("expires_at"))
        self.files: SandboxFiles = SandboxFiles(requests, self.id)

    def refresh(self) -> SandboxSession:
        """Refresh observed lifecycle state.

        Returns:
            The validated response or request value.

        """
        return self._update("get_sandbox_session")

    def suspend(self) -> SandboxSession:
        """Request suspension while retaining guest files.

        Returns:
            The validated response or request value.

        """
        return self._update("suspend_sandbox_session", 202)

    def resume(self) -> SandboxSession:
        """Request resumption under current admission policy.

        Returns:
            The validated response or request value.

        """
        return self._update("resume_sandbox_session", 202)

    def terminate(self) -> SandboxSession:
        """Request durable termination; completion is asynchronous.

        Returns:
            The validated response or request value.

        """
        return self._update("terminate_sandbox_session", 202)

    def _update(self, operation: str, status: int = 200) -> SandboxSession:
        response = record(
            self.requests.send(SandboxRequest(operation, self.id), status)
        )
        if response.get("id") != self.id:
            message = "Sandbox session identity changed"
            raise TypeError(message)
        next_state = state(response.get("state"))
        expiry = text(response.get("expires_at"))
        self.state, self.expires_at = next_state, expiry
        return self

    def exec(
        self, command: str, **options: Unpack[SandboxCommandOptions]
    ) -> SandboxCommandResult:
        """Execute with a stable retry identity and return nonzero exits as data.

        Returns:
            The validated response or request value.

        """
        response = self.requests.send(
            SandboxRequest(
                "execute_sandbox_session",
                self.id,
                body=command_body(command, options),
                request_id=request_id(options),
                timeout=float(options.get("timeout_seconds", 60)) + 120,
            )
        )
        return command_result(response)

    def access(self, port: int) -> SandboxAccess:
        """Create expiring authenticated HTTP access to a guest port.

        Returns:
            The validated response or request value.

        """
        response = record(
            self.requests.send(
                SandboxRequest(
                    "create_sandbox_session_access", self.id, body={"port": port}
                )
            )
        )
        return SandboxAccess(
            text(response.get("url")),
            text(response.get("token")),
            text(response.get("expires_at")),
        )

    def __enter__(self) -> Self:
        """Return the owned session.

        Returns:
            The validated response or request value.

        """
        return self

    def __exit__(
        self,
        _kind: type[BaseException] | None,
        _error: BaseException | None,
        _traceback: TracebackType | None,
    ) -> None:
        """Request cleanup even if the context body raises."""
        if self.state != "terminated":
            _ = self.terminate()
