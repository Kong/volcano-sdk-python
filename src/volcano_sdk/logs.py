"""Project runtime log facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, cast

from ._transport import TransportResponse, invoke, response_payload
from .models import JSONValue, LogActivityResponse, LogSearchResponse, _freeze_json

if TYPE_CHECKING:
    from .client import VolcanoClient

_INVALID_PROJECT_ID = "project_id must be a non-empty string"
_INVALID_LOG_REQUEST = "Log request must be a mapping"
_INVALID_LOG_RESPONSE = "Expected a complete log response"


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

    def __init__(self, client: VolcanoClient) -> None:
        """Bind log reads to a Volcano client."""
        self._client = client

    def search(
        self,
        project_id: str,
        request: Mapping[str, JSONValue],
    ) -> LogSearchResponse:
        """Search retained logs for one project resource type."""
        project_id, request = _log_request(project_id, request)
        transport = cast("LogsTransport", self._client._transport)
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
        """Get bucketed activity for one project resource type."""
        project_id, request = _log_request(project_id, request)
        transport = cast("LogsTransport", self._client._transport)
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


def _response_values(payload: object) -> Mapping[str, object]:
    if not isinstance(payload, Mapping):
        raise TypeError(_INVALID_LOG_RESPONSE)
    return cast("Mapping[str, object]", payload)


def _response_data(values: Mapping[str, object]) -> tuple[Mapping[str, JSONValue], ...]:
    raw_data = values.get("data")
    if not isinstance(raw_data, list):
        raise TypeError(_INVALID_LOG_RESPONSE)
    data = cast("list[object]", raw_data)
    if any(not isinstance(item, Mapping) for item in data):
        raise TypeError(_INVALID_LOG_RESPONSE)
    return tuple(cast("Mapping[str, JSONValue]", item) for item in data)


def _search_response(payload: object) -> LogSearchResponse:
    values = _response_values(payload)
    limit = values.get("limit")
    has_more = values.get("has_more")
    next_cursor = values.get("next_cursor")
    if (
        not isinstance(limit, int)
        or isinstance(limit, bool)
        or not isinstance(has_more, bool)
        or (next_cursor is not None and not isinstance(next_cursor, str))
    ):
        raise TypeError(_INVALID_LOG_RESPONSE)
    return LogSearchResponse(
        data=_response_data(values),
        limit=limit,
        has_more=has_more,
        next_cursor=next_cursor,
    )


def _activity_response(payload: object) -> LogActivityResponse:
    values = _response_values(payload)
    total = values.get("total")
    if not isinstance(total, int) or isinstance(total, bool):
        raise TypeError(_INVALID_LOG_RESPONSE)
    return LogActivityResponse(data=_response_data(values), total=total)
