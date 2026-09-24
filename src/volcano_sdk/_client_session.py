"""Bootstrap credentials and session notification failure handling."""

from __future__ import annotations

from typing import TYPE_CHECKING, TypedDict

from .models import Session

if TYPE_CHECKING:
    from types import TracebackType

_BOOTSTRAP_ACCESS_REQUIRED = "refresh_token requires access_token"


class BootstrapCredentials(TypedDict, total=False):
    access_token: str | None
    refresh_token: str | None


def validate_bootstrap_credential(name: str, token: object) -> None:
    if token is not None and (not isinstance(token, str) or not token.strip()):
        message = f"{name} must be a non-empty string"
        raise ValueError(message)


def bootstrap_session(
    credentials: BootstrapCredentials,
) -> Session | None:
    unknown = credentials.keys() - {"access_token", "refresh_token"}
    if unknown:
        message = f"Unexpected keyword argument: {next(iter(unknown))}"
        raise TypeError(message)
    access_token = credentials.get("access_token")
    refresh_token = credentials.get("refresh_token")
    if access_token is None:
        if refresh_token is not None:
            raise ValueError(_BOOTSTRAP_ACCESS_REQUIRED)
        return None
    for name, token in (
        ("access_token", access_token),
        ("refresh_token", refresh_token),
    ):
        validate_bootstrap_credential(name, token)
    return Session(access_token=access_token, refresh_token=refresh_token)


class CallbackOutcome:
    """Capture a callback failure without unwinding dispatcher ownership."""

    def __init__(self) -> None:
        self.error: BaseException | None = None

    def __enter__(self) -> None:
        return None

    def __exit__(
        self,
        _error_type: type[BaseException] | None,
        error: BaseException | None,
        _traceback: TracebackType | None,
    ) -> bool:
        self.error = error
        return error is not None
