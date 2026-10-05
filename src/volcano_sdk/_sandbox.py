"""Internal Sandbox validation and transport boundary."""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import replace
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, cast, runtime_checkable
from uuid import UUID, uuid4

from ._transport import TransportResponse, response_payload
from .errors import ValidationError

if TYPE_CHECKING:
    from ._transport_sandbox import SandboxRequest
    from .models import JSONValue
from .sandbox_models import SandboxCommandResult, SandboxState

_STATES = frozenset(
    {
        "starting",
        "running",
        "suspending",
        "suspended",
        "resuming",
        "terminating",
        "terminated",
        "unknown",
    }
)


def identifier(value: str) -> str:
    """Normalize a UUID before any request is sent.

    Returns:
        The validated response or request value.

    Raises:
        ValidationError: If the supplied value violates the Sandbox contract.

    """
    try:
        return str(UUID(value))
    except (ValueError, AttributeError, TypeError) as error:
        message = "Sandbox resource and request IDs must be UUIDs"
        raise ValidationError(message) from error


def record(value: object) -> Mapping[str, object]:
    """Validate a response object.

    Returns:
        The validated response or request value.

    Raises:
        TypeError: If the supplied value violates the Sandbox contract.

    """
    if not isinstance(value, Mapping):
        message = "Invalid Sandbox response"
        raise TypeError(message)
    return cast("Mapping[str, object]", value)


def text(value: object) -> str:
    """Validate a response text field.

    Returns:
        The validated response or request value.

    Raises:
        TypeError: If the supplied value violates the Sandbox contract.

    """
    if not isinstance(value, str):
        message = "Invalid Sandbox text field"
        raise TypeError(message)
    return value


def integer(value: object) -> int:
    """Validate a response integer without accepting booleans.

    Returns:
        The validated response or request value.

    Raises:
        TypeError: If the supplied value violates the Sandbox contract.

    """
    if type(value) is not int:
        message = "Invalid Sandbox integer field"
        raise TypeError(message)
    return value


def flag(value: object) -> bool:
    """Validate a response boolean.

    Returns:
        The validated response or request value.

    Raises:
        TypeError: If the supplied value violates the Sandbox contract.

    """
    if not isinstance(value, bool):
        message = "Invalid Sandbox flag"
        raise TypeError(message)
    return value


def state(value: object) -> SandboxState:
    """Validate a lifecycle state.

    Returns:
        The validated response or request value.

    Raises:
        TypeError: If the supplied value violates the Sandbox contract.

    """
    result = text(value)
    if result not in _STATES:
        message = "Invalid Sandbox state"
        raise TypeError(message)
    return cast("SandboxState", result)


def timestamp(value: object) -> datetime:
    """Parse an aware timestamp from the Sandbox API.

    Returns:
        The aware response timestamp.

    Raises:
        TypeError: If the response timestamp is invalid or lacks an offset.

    """
    try:
        result = datetime.fromisoformat(text(value))
    except ValueError as error:
        message = "Invalid Sandbox timestamp"
        raise TypeError(message) from error
    if result.utcoffset() is None:
        message = "Sandbox timestamps must include an offset"
        raise TypeError(message)
    return result


def grant_expiry(value: object) -> str:
    """Serialize an aware grant expiry.

    Returns:
        The expiry with its timezone offset.

    Raises:
        ValidationError: If the expiry is not an aware datetime.

    """
    if not isinstance(value, datetime) or value.utcoffset() is None:
        message = "Sandbox grant expiry must be an aware datetime"
        raise ValidationError(message)
    return value.isoformat()


def command_result(value: object) -> SandboxCommandResult:
    """Decode command output without interpreting the exit code as an API error.

    Returns:
        The validated response or request value.

    """
    data = record(value)
    return SandboxCommandResult(
        text(data.get("stdout")),
        text(data.get("stderr")),
        integer(data.get("exit_code")),
        flag(data.get("timed_out")),
        flag(data.get("stdout_truncated")),
        flag(data.get("stderr_truncated")),
    )


def selector(options: Mapping[str, object]) -> dict[str, JSONValue]:
    """Preserve omitted memory so named Sandboxes retain their configuration.

    Returns:
        The validated response or request value.

    Raises:
        ValidationError: If the supplied value violates the Sandbox contract.

    """
    if (options.get("preset") is None) == (options.get("sandbox_id") is None):
        message = "Choose exactly one preset or sandbox_id"
        raise ValidationError(message)
    data: dict[str, JSONValue] = {"region": text(options.get("region"))}
    for key in ("preset", "sandbox_id", "memory_mb"):
        if key in options:
            value = options[key]
            data[key] = integer(value) if key == "memory_mb" else text(value)
    if "sandbox_id" in data:
        data["sandbox_id"] = identifier(text(data["sandbox_id"]))
    return data


def command_body(command: str, options: Mapping[str, object]) -> dict[str, JSONValue]:
    """Copy command options for a single dispatch.

    Returns:
        The validated response or request value.

    """
    body: dict[str, JSONValue] = {"command": command}
    if "timeout_seconds" in options:
        body["timeout_seconds"] = integer(options["timeout_seconds"])
    if "environment" in options:
        body["environment"] = {
            key: text(value) for key, value in record(options["environment"]).items()
        }
    return body


@runtime_checkable
class SandboxTransport(Protocol):
    """Internal transport implemented using generated operations."""

    def sandbox_request(
        self, *, authorization: str | None, request: SandboxRequest
    ) -> TransportResponse:
        """Dispatch once without replaying uncertain side effects."""
        ...


class SandboxRequests:
    """Bind current credentials without falling back to an anonymous key."""

    def __init__(
        self,
        dispatch: Callable[[SandboxRequest], TransportResponse],
        *,
        service_only: bool = False,
    ) -> None:
        """Bind credential-aware dispatch."""
        self._dispatch: Callable[[SandboxRequest], TransportResponse] = dispatch
        self._service_only: bool = service_only

    def management(self) -> SandboxRequests:
        """Bind an owned handle to management credentials.

        Returns:
            A request context that never substitutes a project user.

        """
        return SandboxRequests(self._dispatch, service_only=True)

    def send(self, request: SandboxRequest, status: int = 200) -> object:
        """Dispatch through normal typed error handling.

        Returns:
            The validated response or request value.

        """
        response = self._dispatch(replace(request, service_only=self._service_only))
        return response_payload(response, status)


def request_id(options: Mapping[str, object]) -> str:
    """Keep explicit retry identities stable; allocate once otherwise.

    Returns:
        The validated response or request value.

    """
    value = options.get("request_id")
    return identifier(text(value)) if value is not None else str(uuid4())
