"""Typed errors raised by the Volcano SDK."""

from __future__ import annotations


class VolcanoError(Exception):
    """Base error containing structured Volcano response details."""

    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: str | None = None,
        retry_after: int | None = None,
    ) -> None:
        """Create an error from an API or transport failure."""
        super().__init__(message)
        self.status = status
        self.code = code
        self.retry_after = retry_after


class AuthenticationError(VolcanoError):
    """The supplied credentials are missing or invalid."""


class ValidationError(VolcanoError):
    """The request failed API validation."""


class NotFoundError(VolcanoError):
    """The requested resource does not exist."""


class ConflictError(VolcanoError):
    """The request conflicts with the current resource state."""


class SessionChangedError(ConflictError):
    """An auth operation completed after the client session changed."""

    def __init__(self) -> None:
        """Create a deterministic stale-auth-operation error."""
        super().__init__(
            "Session changed during authentication operation",
            status=409,
            code="auth_session_changed",
        )


class RateLimitedError(VolcanoError):
    """The API rejected the request because of a rate limit."""


class ServerError(VolcanoError):
    """The Volcano API failed to process the request."""


class TransportError(VolcanoError):
    """The request failed before receiving an API response."""
