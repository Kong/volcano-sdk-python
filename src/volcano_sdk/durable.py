"""Durable execution facade."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Literal, Protocol, Unpack, runtime_checkable

from ._client_context import ClientContextSource, facade_context
from ._durable_approval_response import (
    APPROVAL_STATUSES,
    durable_approval,
    durable_approval_page,
    durable_approval_stats,
)
from ._durable_arguments import identifier, known_options
from ._durable_messages import DurableMessageChannels, DurableMessages
from ._durable_response import durable_execution, durable_execution_page
from ._transport import (
    DurableApprovalListRequest,
    DurableApprovalStatsRequest,
    DurableExecutionListRequest,
    Transport,
    TransportResponse,
    invoke,
    response_payload,
)

if TYPE_CHECKING:
    from .models import (
        DurableApproval,
        DurableApprovalListOptions,
        DurableApprovalPage,
        DurableApprovalStats,
        DurableApprovalStatsOptions,
        DurableApprovalStatus,
        DurableExecution,
        DurableExecutionPage,
        DurableExecutionStatus,
        JSONValue,
    )

_INVALID_DURABLE_TRANSPORT = "Transport does not support durable executions"
_INVALID_APPROVAL_TRANSPORT = "Transport does not support durable approvals"
# The spec's limits on a function filter and a decision comment.
_MAX_FUNCTION_LENGTH = 255
_MAX_COMMENT_LENGTH = 2000
_LIST_OPTIONS = frozenset(
    {"status", "function", "execution_id", "from_", "to", "page", "limit"}
)
_STATS_OPTIONS = frozenset({"function", "from_", "to"})
# The spec's maxLength on X-Volcano-Execution-Name. Checked here so an
# over-long name is refused before a request is spent on it, the way the
# JavaScript SDK refuses it.
_MAX_EXECUTION_NAME_LENGTH = 255
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


@runtime_checkable
class DurableApprovalsTransport(Protocol):
    """Transport operations required by the durable approvals facade."""

    def list_durable_approvals(
        self,
        *,
        authorization: str,
        project_id: str,
        request: DurableApprovalListRequest,
    ) -> TransportResponse:
        """List a project's durable approvals."""
        ...

    def get_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
    ) -> TransportResponse:
        """Read one durable approval."""
        ...

    def get_durable_approval_stats(
        self,
        *,
        authorization: str,
        project_id: str,
        request: DurableApprovalStatsRequest,
    ) -> TransportResponse:
        """Count a project's durable approvals by outcome."""
        ...

    def approve_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
        comment: str | None,
    ) -> TransportResponse:
        """Approve a pending durable approval."""
        ...

    def deny_durable_approval(
        self,
        *,
        authorization: str,
        project_id: str,
        approval_id: str,
        comment: str | None,
    ) -> TransportResponse:
        """Deny a pending durable approval."""
        ...


class DurableApprovals:
    """Review and decide the approvals durable workflows wait on.

    Owner-scoped, like reading an execution: every method takes the project id
    and the session's platform token. Only a person decides: a project access
    token can read approvals but is refused with `PermissionDeniedError` when it
    approves or denies one.
    """

    def __init__(self, client: DurableClientContext) -> None:
        """Bind approval operations to a Volcano client."""
        self._client: DurableClientContext = client

    def _transport(self) -> DurableApprovalsTransport:
        transport = self._client.transport()
        if not isinstance(transport, DurableApprovalsTransport):
            raise TypeError(_INVALID_APPROVAL_TRANSPORT)
        return transport

    def list(
        self, project_id: str, **options: Unpack[DurableApprovalListOptions]
    ) -> DurableApprovalPage:
        """List a project's approvals, newest first.

        Decided, expired, and cancelled approvals are kept for a year.

        Returns
        -------
        DurableApprovalPage
            Approvals and pagination metadata.

        """
        project = identifier(project_id, "project_id")
        request = _list_request(options)
        transport = self._transport()
        response = invoke(
            transport.list_durable_approvals,
            authorization=self._client.session_token(),
            project_id=project,
            request=request,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_approval_page(response_body)

    def get(self, project_id: str, approval_id: str) -> DurableApproval:
        """Read one approval, including its decision once it has one.

        Returns
        -------
        DurableApproval
            The approval.

        """
        project = identifier(project_id, "project_id")
        approval = identifier(approval_id, "approval_id")
        transport = self._transport()
        response = invoke(
            transport.get_durable_approval,
            authorization=self._client.session_token(),
            project_id=project,
            approval_id=approval,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_approval(response_body)

    def stats(
        self, project_id: str, **options: Unpack[DurableApprovalStatsOptions]
    ) -> DurableApprovalStats:
        """Count approvals by outcome, overall, per function, and per day.

        The window defaults to the last 30 days and may span at most 366.

        Returns
        -------
        DurableApprovalStats
            Counts, approval rate, and decision times over the window.

        """
        project = identifier(project_id, "project_id")
        request = _stats_request(options)
        transport = self._transport()
        response = invoke(
            transport.get_durable_approval_stats,
            authorization=self._client.session_token(),
            project_id=project,
            request=request,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_approval_stats(response_body)

    def approve(
        self, project_id: str, approval_id: str, *, comment: str | None = None
    ) -> DurableApproval:
        """Approve a pending approval, resuming the workflow waiting on it.

        Repeating the same decision returns the approval unchanged. Deciding
        the other way, or deciding one that expired or was cancelled, raises
        `ConflictError`.

        Returns
        -------
        DurableApproval
            The approval with its decision.

        """
        return self._decide("approve", project_id, approval_id, comment)

    def deny(
        self, project_id: str, approval_id: str, *, comment: str | None = None
    ) -> DurableApproval:
        """Deny a pending approval; the workflow resumes with a denied decision.

        Repeats and conflicts behave as they do for `approve`.

        Returns
        -------
        DurableApproval
            The approval with its decision.

        """
        return self._decide("deny", project_id, approval_id, comment)

    def _decide(
        self,
        decision: Literal["approve", "deny"],
        project_id: str,
        approval_id: str,
        comment: object,
    ) -> DurableApproval:
        project = identifier(project_id, "project_id")
        approval = identifier(approval_id, "approval_id")
        note = _comment(comment)
        transport = self._transport()
        operation = (
            transport.approve_durable_approval
            if decision == "approve"
            else transport.deny_durable_approval
        )
        response = invoke(
            operation,
            authorization=self._client.session_token(),
            project_id=project,
            approval_id=approval,
            comment=note,
        )
        response_body: object = response_payload(response, _HTTP_OK)
        return durable_approval(response_body)


class Durable:
    """Start and follow executions of deployed durable functions."""

    def __init__(
        self,
        client: DurableClientContext | ClientContextSource,
        *,
        _realtime: DurableMessageChannels | None = None,
    ) -> None:
        """Bind durable operations to a Volcano client."""
        self._client: DurableClientContext = facade_context(client)
        # Approvals that workflows wait on with `ctx.wait_for_approval`.
        self.approvals: DurableApprovals = DurableApprovals(self._client)
        # Messages workflows wait on with `ctx.wait_for_message`, and the ones
        # they publish with `ctx.publish`.
        self.messages: DurableMessages = DurableMessages(self._client, _realtime)

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
        function = identifier(function_name, "function_name")
        name = None if execution_name is None else _execution_name(execution_name)
        transport = self._durable_transport()
        response = invoke(
            transport.start_durable_execution_from_application,
            authorization=self._client.function_token(),
            function_id=function,
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
        project = identifier(project_id, "project_id")
        function = identifier(function_name, "function_name")
        execution = identifier(execution_id, "execution_id")
        transport = self._durable_transport()
        response = invoke(
            transport.get_durable_execution,
            authorization=self._client.session_token(),
            project_id=project,
            function_id=function,
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
        project = identifier(project_id, "project_id")
        function = identifier(function_name, "function_name")
        transport = self._durable_transport()
        request = DurableExecutionListRequest(status=status, page=page, limit=limit)
        response = invoke(
            transport.list_durable_executions,
            authorization=self._client.session_token(),
            project_id=project,
            function_id=function,
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
        project = identifier(project_id, "project_id")
        function = identifier(function_name, "function_name")
        execution = identifier(execution_id, "execution_id")
        transport = self._durable_transport()
        response = invoke(
            transport.stop_durable_execution,
            authorization=self._client.session_token(),
            project_id=project,
            function_id=function,
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
    name = identifier(value, "execution_name")
    if len(name) > _MAX_EXECUTION_NAME_LENGTH:
        message = (
            f"execution_name must be at most {_MAX_EXECUTION_NAME_LENGTH} characters"
        )
        raise ValueError(message)
    return name


def _list_request(options: DurableApprovalListOptions) -> DurableApprovalListRequest:
    known_options(options, _LIST_OPTIONS)
    status = options.get("status")
    execution_id = options.get("execution_id")
    return DurableApprovalListRequest(
        status=None if status is None else _approval_status(status),
        function=_function_filter(options.get("function")),
        execution_id=(
            None if execution_id is None else identifier(execution_id, "execution_id")
        ),
        from_=_moment(options.get("from_"), "from_"),
        to=_moment(options.get("to"), "to"),
        page=options.get("page"),
        limit=options.get("limit"),
    )


def _stats_request(
    options: DurableApprovalStatsOptions,
) -> DurableApprovalStatsRequest:
    known_options(options, _STATS_OPTIONS)
    return DurableApprovalStatsRequest(
        function=_function_filter(options.get("function")),
        from_=_moment(options.get("from_"), "from_"),
        to=_moment(options.get("to"), "to"),
    )


def _approval_status(value: object) -> DurableApprovalStatus:
    for status in APPROVAL_STATUSES:
        if value == status:
            return status
    message = f"status must be one of {', '.join(APPROVAL_STATUSES)}"
    raise ValueError(message)


def _function_filter(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        message = "function must be a non-empty string"
        raise ValueError(message)
    function = value.strip()
    if len(function) > _MAX_FUNCTION_LENGTH:
        message = f"function must be at most {_MAX_FUNCTION_LENGTH} characters"
        raise ValueError(message)
    return function


def _moment(value: object, field: str) -> datetime | None:
    """Require an aware datetime, so the window does not shift with the host's zone.

    Returns:
        The datetime, or None when the filter is unset.

    Raises:
        ValueError: The value is not a timezone-aware datetime.

    """
    if value is None:
        return None
    if not isinstance(value, datetime) or value.utcoffset() is None:
        message = f"{field} must be a timezone-aware datetime"
        raise ValueError(message)
    return value


def _comment(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        message = "comment must be a string"
        raise TypeError(message)
    if len(value) > _MAX_COMMENT_LENGTH:
        message = f"comment must be at most {_MAX_COMMENT_LENGTH} characters"
        raise ValueError(message)
    return value
