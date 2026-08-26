from __future__ import annotations


class VolcanoError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: int | None = None,
        code: str | None = None,
        retry_after: int | None = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.retry_after = retry_after


class AuthenticationError(VolcanoError):
    pass


class ValidationError(VolcanoError):
    pass


class NotFoundError(VolcanoError):
    pass


class ConflictError(VolcanoError):
    pass


class RateLimitedError(VolcanoError):
    pass


class ServerError(VolcanoError):
    pass


class TransportError(VolcanoError):
    pass
