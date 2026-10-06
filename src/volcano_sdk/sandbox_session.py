"""Stateful Sandbox handle and byte-preserving guest files."""

from __future__ import annotations

import base64
from contextlib import suppress
from typing import TYPE_CHECKING, Self, Unpack

if TYPE_CHECKING:
    from datetime import datetime
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
    timestamp,
)
from ._transport_sandbox import SandboxRequest
from .errors import NotFoundError, ValidationError
from .sandbox_models import (
    SandboxAccess,
    SandboxCommandOptions,
    SandboxCommandResult,
    SandboxState,
)

_FILE_LIMIT = 8 * 1024 * 1024


class SandboxFiles:
    """Read and write bytes inside a session."""

    def __init__(self, requests: SandboxRequests, session_id: str) -> None:
        """Bind files to a validated session identity."""
        self._requests: SandboxRequests = requests
        self._session_id: str = session_id

    def read(self, path: str) -> bytes:
        """Read a guest file without text conversion.

        Returns:
            The validated response or request value.

        """
        response = self._requests.send(
            SandboxRequest(
                "read_sandbox_session_file", self._session_id, body={"path": path}
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
        _ = self._requests.send(
            SandboxRequest(
                "write_sandbox_session_file",
                self._session_id,
                body={"path": path, "data": base64.b64encode(data).decode()},
            ),
            204,
        )


class SandboxSession:
    """A session handle; context exit requests durable termination."""

    def __init__(self, requests: SandboxRequests, value: object) -> None:
        """Construct from a validated API response."""
        data = record(value)
        self._requests: SandboxRequests = requests
        self._id: str = identifier(text(data.get("id")))
        self._project_id: str = identifier(text(data.get("project_id")))
        self._region: str = text(data.get("region"))
        self._state: SandboxState = state(data.get("state"))
        self._expires_at: datetime = timestamp(data.get("expires_at"))
        self._files: SandboxFiles = SandboxFiles(requests, self._id)

    @property
    def id(self) -> str:
        """The immutable session identity."""
        return self._id

    @property
    def project_id(self) -> str:
        """The project that owns this session."""
        return self._project_id

    @property
    def region(self) -> str:
        """The session's region."""
        return self._region

    @property
    def state(self) -> SandboxState:
        """The most recently observed lifecycle state."""
        return self._state

    @property
    def expires_at(self) -> datetime:
        """The aware expiration timestamp observed from the API."""
        return self._expires_at

    @property
    def files(self) -> SandboxFiles:
        """The file operations bound to this session."""
        return self._files

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
            self._requests.send(SandboxRequest(operation, self.id), status)
        )
        if response.get("id") != self.id:
            message = "Sandbox session identity changed"
            raise TypeError(message)
        next_state = state(response.get("state"))
        expiry = timestamp(response.get("expires_at"))
        self._state, self._expires_at = next_state, expiry
        return self

    def exec(
        self, command: str, **options: Unpack[SandboxCommandOptions]
    ) -> SandboxCommandResult:
        """Execute with a stable retry identity and return nonzero exits as data.

        Returns:
            The validated response or request value.

        """
        response = self._requests.send(
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
            self._requests.send(
                SandboxRequest(
                    "create_sandbox_session_access", self.id, body={"port": port}
                )
            )
        )
        return SandboxAccess(
            text(response.get("url")),
            text(response.get("token")),
            timestamp(response.get("expires_at")),
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
        if self.state not in {"terminating", "terminated"}:
            try:
                self._cleanup()
            except Exception as cleanup_error:
                if _error is None:
                    raise
                _error.add_note(f"Sandbox cleanup failed: {cleanup_error}")

    def _cleanup(self) -> None:
        with suppress(NotFoundError):
            _ = self.terminate()
