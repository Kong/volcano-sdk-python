"""Project runtime log facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, cast, runtime_checkable

from ._log_response import (
    activity_total,
    response_data,
    response_values,
    search_metadata,
)
from ._transport import Transport, TransportResponse, invoke, response_payload
from .models import JSONValue, LogActivityResponse, LogSearchResponse, _freeze_json

if TYPE_CHECKING:
    from .auth import Auth

_INVALID_PROJECT_ID = "project_id must be a non-empty string"
_INVALID_LOG_REQUEST = "Log request must be a mapping"
_INVALID_LOG_TRANSPORT = "Transport does not support project logs"


class LogsContext(Protocol):
    """Client capabilities required by project log reads."""

    _transport: Transport
    auth: Auth


@runtime_checkable
class LogsTransport(Protocol):
    """Transport operations required by the logs facade."""

    def search_project_logs(
        self,
        *,
        authorization: str,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> TransportResponse:
        """Search a project's retained logs."""
        ...

    def get_project_log_activity(
        self,
        *,
        authorization: str,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> TransportResponse:
        """Get bucketed log activity for a project."""
        ...


class Logs:
    """Search retained project logs and activity."""

    def __init__(self, client: LogsContext) -> None:
        """Bind log reads to a Volcano client."""
        self._client: LogsContext = client

    def _logs_transport(self) -> LogsTransport:
        transport = self._client._transport
        if not isinstance(transport, LogsTransport):
            raise TypeError(_INVALID_LOG_TRANSPORT)
        return transport

    def search(
        self,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> LogSearchResponse:
        """Search retained logs for one project resource type.

        Returns
        -------
        LogSearchResponse
            Matching log entries with the page limit and continuation cursor.

        """
        project_id, request = _log_request(project_id, request)
        transport = self._logs_transport()
        response = self._client.auth._session_request(
            lambda token: invoke(
                transport.search_project_logs,
                authorization=token,
                project_id=project_id,
                request=request,
            )
        )
        return _search_response(response_payload(response, 200))

    def activity(
        self,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> LogActivityResponse:
        """Get bucketed activity for one project resource type.

        Returns
        -------
        LogActivityResponse
            Activity buckets and the total count reported by the server.

        """
        project_id, request = _log_request(project_id, request)
        transport = self._logs_transport()
        response = self._client.auth._session_request(
            lambda token: invoke(
                transport.get_project_log_activity,
                authorization=token,
                project_id=project_id,
                request=request,
            )
        )
        return _activity_response(response_payload(response, 200))


def _log_request(
    project_id: object,
    request: object,
) -> tuple[str, Mapping[str, JSONValue]]:
    if not isinstance(project_id, str) or not project_id.strip():
        raise ValueError(_INVALID_PROJECT_ID)
    if not isinstance(request, Mapping):
        raise TypeError(_INVALID_LOG_REQUEST)
    snapshot = _freeze_json(cast("Mapping[str, JSONValue]", request))
    return project_id, cast("Mapping[str, JSONValue]", snapshot)


def _search_response(payload: object) -> LogSearchResponse:
    values = response_values(payload)
    limit, has_more, next_cursor = search_metadata(values)
    return LogSearchResponse(
        data=response_data(values),
        limit=limit,
        has_more=has_more,
        next_cursor=next_cursor,
    )


def _activity_response(payload: object) -> LogActivityResponse:
    values = response_values(payload)
    return LogActivityResponse(data=response_data(values), total=activity_total(values))
