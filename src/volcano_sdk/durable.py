"""Durable execution facade."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import Protocol, cast, runtime_checkable
from uuid import UUID

from ._transport import (
    DurableExecutionListRequest,
    Transport,
    TransportResponse,
    invoke,
    response_payload,
)
from .models import (
    DurableExecution,
    DurableExecutionFailure,
    DurableExecutionPage,
    DurableExecutionStatus,
    JSONValue,
)

_INVALID_EXECUTION_PAYLOAD = "Expected a complete durable execution"
_INVALID_EXECUTION_PAGE = "Expected a complete durable execution page"
_INVALID_DURABLE_TRANSPORT = "Transport does not support durable executions"
# The spec's maxLength on X-Volcano-Execution-Name. Checked here so an
# over-long name is refused before a request is spent on it, the way the
# JavaScript SDK refuses it.
_MAX_EXECUTION_NAME_LENGTH = 255

_INVALID_IDENTIFIERS = {
    "function_name": "function_name must be a non-empty string",
    "execution_name": "execution_name must be a non-empty string",
    "project_id": "project_id must be a non-empty string",
    "execution_id": "execution_id must be a non-empty string",
}
# The two identifiers the transport converts to a UUID before sending. Checked
# here so a malformed one is a facade ValidationError rather than a
# `badly formed hexadecimal UUID string` raised from inside the transport,
# outside the error hierarchy this package documents.
_UUID_IDENTIFIERS = {
    "project_id": "project_id must be a UUID",
    "execution_id": "execution_id must be a UUID",
}
_HTTP_ACCEPTED = 202
_HTTP_OK = 200


class DurableClientContext(Protocol):
    """Client capabilities required by durable execution requests."""

    _transport: Transport

    def _function_token(self) -> str: ...

    def _session_token(self) -> str: ...


@runtime_checkable
class DurableTransport(Protocol):
    """Transport operations required by the durable facade."""

    def start_durable_execution_from_application(
        self,
        *,
        authorization: str,
        function_id: str,
        payload: JSONValue,
        execution_name: str | None = None,
    ) -> TransportResponse:
        """Start an execution of a durable function."""
        ...

    def get_durable_execution(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        execution_id: str,
    ) -> TransportResponse:
        """Read one execution of a durable function."""
        ...

    def list_durable_executions(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        request: DurableExecutionListRequest,
    ) -> TransportResponse:
        """List a durable function's executions."""
        ...

    def stop_durable_execution(
        self,
        *,
        authorization: str,
        project_id: str,
        function_id: str,
        execution_id: str,
    ) -> TransportResponse:
        """Ask a running execution to stop."""
        ...


class Durable:
    """Start and follow executions of deployed durable functions."""

    def __init__(self, client: DurableClientContext) -> None:
        """Bind durable operations to a Volcano client."""
        self._client: DurableClientContext = client

    def _durable_transport(self) -> DurableTransport:
        transport = self._client._transport
        if not isinstance(transport, DurableTransport):
            raise TypeError(_INVALID_DURABLE_TRANSPORT)
        return transport

    def start(
        self,
        function_name: str,
        payload: JSONValue = None,
        *,
        execution_name: str | None = None,
    ) -> DurableExecution:
        """Start a durable execution and return a handle to it.

        A durable function is never invoked synchronously: it can run for up to
        366 days, so the platform accepts the start and answers with an execution
        to follow. Starting is the only durable operation an application
        credential may perform -- reading a result or stopping an execution is
        owner-scoped.

        Passing `execution_name` makes the start idempotent: starting again
        under the same name returns the execution that already exists rather
        than beginning a second one, and is charged once.

        Returns
        -------
        DurableExecution
            The accepted execution, or the existing execution for an idempotent start.

        """
        identifier = _identifier(function_name, "function_name")
        name = None if execution_name is None else _execution_name(execution_name)
        transport = self._durable_transport()
        response = invoke(
            transport.start_durable_execution_from_application,
            authorization=self._client._function_token(),
            function_id=identifier,
            payload={} if payload is None else payload,
            execution_name=name,
        )
        response_body: object = response_payload(response, _HTTP_ACCEPTED)
        return _durable_execution(response_body)

    def get(
        self,
        project_id: str,
        function_name: str,
        execution_id: str,
    ) -> DurableExecution:
        """Read an execution, including its result once it has succeeded.

        Owner-scoped: it takes the project id and the project owner's platform
        user token, because an execution is addressed by its id alone. Poll it
        from a backend, not a browser. Auth-user sessions, anonymous keys,
        service keys, and project access tokens are not accepted.

        Returns
        -------
        DurableExecution
            The execution snapshot, including any available result or failure.

        """
        project = _identifier(project_id, "project_id")
        identifier = _identifier(function_name, "function_name")
        execution = _identifier(execution_id, "execution_id")
        transport = self._durable_transport()
        response = invoke(
            transport.get_durable_execution,
            authorization=self._client._session_token(),
            project_id=project,
            function_id=identifier,
            execution_id=execution,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return _durable_execution(response_body)

    def list(
        self,
        project_id: str,
        function_name: str,
        *,
        status: DurableExecutionStatus | None = None,
        page: int | None = None,
        limit: int | None = None,
    ) -> DurableExecutionPage:
        """List a durable function's executions, most recent first.

        Each entry carries the status the platform last observed rather than a
        live one; read a single execution for that. Owner-scoped, like `get`.

        Returns
        -------
        DurableExecutionPage
            Execution summaries and pagination metadata.

        """
        project = _identifier(project_id, "project_id")
        identifier = _identifier(function_name, "function_name")
        transport = self._durable_transport()
        request = DurableExecutionListRequest(status=status, page=page, limit=limit)
        response = invoke(
            transport.list_durable_executions,
            authorization=self._client._session_token(),
            project_id=project,
            function_id=identifier,
            request=request,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return _durable_execution_page(response_body)

    def stop(
        self,
        project_id: str,
        function_name: str,
        execution_id: str,
    ) -> DurableExecution:
        """Ask a running execution to stop.

        Accepted rather than awaited: what comes back is the execution read
        after asking, and it often still says `running`, so poll `get` to see
        it reach `stopped`. Completed steps are not undone. Repeating a stop is
        safe -- an execution that has already finished reports the state it is
        in. Owner-scoped, like `get`.

        Returns
        -------
        DurableExecution
            The execution snapshot after the stop request; it may still be running.

        """
        project = _identifier(project_id, "project_id")
        identifier = _identifier(function_name, "function_name")
        execution = _identifier(execution_id, "execution_id")
        transport = self._durable_transport()
        response = invoke(
            transport.stop_durable_execution,
            authorization=self._client._session_token(),
            project_id=project,
            function_id=identifier,
            execution_id=execution,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return _durable_execution(response_body)


def _execution_name(value: object) -> str:
    """Require a name the platform will accept, including its length.

    The header carries a documented maximum, and a name over it is refused
    server-side with a 400 -- a request, an allowance check and a round trip
    spent on something that could be answered here.

    Returns
    -------
    str
        The trimmed execution name.

    Raises
    ------
    ValueError
        If the name is empty, is not a string, or exceeds the length limit.

    """
    name = _identifier(value, "execution_name")
    if len(name) > _MAX_EXECUTION_NAME_LENGTH:
        message = (
            f"execution_name must be at most {_MAX_EXECUTION_NAME_LENGTH} characters"
        )
        raise ValueError(message)
    return name


def _identifier(value: object, field: str) -> str:
    """Require a non-empty path segment, and a UUID where one is sent as one.

    An empty segment would address the collection instead of the execution,
    which is a different request rather than a failed one.

    Returns
    -------
    str
        The trimmed identifier, preserving its UUID spelling.

    Raises
    ------
    ValueError
        If the value is empty, is not a string, or requires a valid UUID.

    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(_INVALID_IDENTIFIERS[field])
    trimmed = value.strip()
    if field in _UUID_IDENTIFIERS:
        try:
            _ = UUID(trimmed)
        except ValueError as exc:
            raise ValueError(_UUID_IDENTIFIERS[field]) from exc
    return trimmed


def _execution_fields(payload: object) -> Mapping[str, object]:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    values = cast("Mapping[str, object]", payload)
    for required in ("id", "function_id", "name", "status", "region", "created_at"):
        if not isinstance(values.get(required), str) or not values[required]:
            raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    return values


def _durable_execution(payload: object) -> DurableExecution:
    values = _execution_fields(payload)
    created_at = _parse_datetime(values["created_at"])
    result_expired = values.get("result_expired")
    if result_expired is not None and not isinstance(result_expired, bool):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    return DurableExecution(
        id=str(values["id"]),
        function_id=str(values["function_id"]),
        name=str(values["name"]),
        status=cast("DurableExecutionStatus", str(values["status"])),
        region=str(values["region"]),
        created_at=created_at,
        result=cast("JSONValue", values.get("result")),
        result_expired=result_expired,
        error=_durable_error(values.get("error")),
        completed_at=_datetime(values.get("completed_at")),
    )


def _durable_error(payload: object) -> DurableExecutionFailure | None:
    if payload is None:
        return None
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    values = cast("Mapping[str, object]", payload)
    error_type = values.get("type")
    message = values.get("message")
    return DurableExecutionFailure(
        type=None if error_type is None else str(error_type),
        message=None if message is None else str(message),
    )


def _durable_execution_page(payload: object) -> DurableExecutionPage:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    values = cast("Mapping[str, object]", payload)
    raw_data = values.get("data")
    if raw_data is None:
        raw_data = []
    if not isinstance(raw_data, (list, tuple)):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    data = tuple(cast("Sequence[object]", raw_data))
    has_more = values.get("has_more", False)
    if not isinstance(has_more, bool):
        raise TypeError(_INVALID_EXECUTION_PAGE)
    return DurableExecutionPage(
        executions=tuple(_durable_execution(entry) for entry in data),
        page=_count(values.get("page")),
        limit=_count(values.get("limit")),
        total=_count(values.get("total")),
        has_more=has_more,
    )


def _count(value: object) -> int:
    if value is None:
        return 0
    if type(value) is not int:
        raise TypeError(_INVALID_EXECUTION_PAGE)
    return value


def _datetime(value: object) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    return _parse_datetime(value)


def _parse_datetime(value: object) -> datetime:
    if not isinstance(value, str) or not value:
        raise TypeError(_INVALID_EXECUTION_PAYLOAD)
    text = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(text)
    except ValueError as error:
        raise TypeError(_INVALID_EXECUTION_PAYLOAD) from error
