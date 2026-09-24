"""Durable execution facade."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable
from uuid import UUID

from ._client_context import ClientContextSource, facade_context
from ._durable_response import durable_execution, durable_execution_page
from ._transport import (
    DurableExecutionListRequest,
    Transport,
    TransportResponse,
    invoke,
    response_payload,
)

if TYPE_CHECKING:
    from .models import (
        DurableExecution,
        DurableExecutionPage,
        DurableExecutionStatus,
        JSONValue,
    )

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

    def transport(self) -> Transport:
        """Return the active typed transport."""
        ...

    def function_token(self) -> str:
        """Return the current function-invocation credential."""
        ...

    def session_token(self) -> str:
        """Return the active session credential."""
        ...


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

    def __init__(self, client: DurableClientContext | ClientContextSource) -> None:
        """Bind durable operations to a Volcano client."""
        self._client: DurableClientContext = facade_context(client)

    def _durable_transport(self) -> DurableTransport:
        transport = self._client.transport()
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

        A durable function is never invoked synchronously: it can run for
        hours, so the platform accepts the start and answers with an execution
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
            authorization=self._client.function_token(),
            function_id=identifier,
            payload={} if payload is None else payload,
            execution_name=name,
        )
        response_body: object = response_payload(response, _HTTP_ACCEPTED)
        return durable_execution(response_body)

    def get(
        self,
        project_id: str,
        function_name: str,
        execution_id: str,
    ) -> DurableExecution:
        """Read an execution, including its result once it has succeeded.

        Owner-scoped: it takes the project id and the project's own platform
        token, because an execution is addressed by its id alone and an
        anonymous key is held by everyone who loads the page. Poll it from a
        backend, not a browser. Neither an auth-user session from sign-in nor a
        service key is accepted here -- the route takes a user token, and
        anything else is answered 401.

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
            authorization=self._client.session_token(),
            project_id=project,
            function_id=identifier,
            execution_id=execution,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_execution(response_body)

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
            authorization=self._client.session_token(),
            project_id=project,
            function_id=identifier,
            request=request,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_execution_page(response_body)

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
            authorization=self._client.session_token(),
            project_id=project,
            function_id=identifier,
            execution_id=execution,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_execution(response_body)


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
