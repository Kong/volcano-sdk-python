"""Postgres connection helpers for Volcano functions."""

import re
from urllib.parse import quote, unquote, urlencode

_FULL_ACCESS_APP_NAME = "volcano_full_access"
_USER_ACCESS_APP_NAME = "volcano_user_access"
_CONNECTION_URI_PREFIX = re.compile(r"^postgres(?:ql)?://")
_INVALID_PERCENT_ENCODING = re.compile(r"%(?![0-9A-Fa-f]{2})")
_REQUIRED_ERROR = (
    "database_connection_string: base_connection_string (DATABASE_URL) is required"
)
_INVALID_ERROR = (
    "database_connection_string: base_connection_string is not a valid connection URL"
)


def database_connection_string(
    base_connection_string: str,
    *,
    user_id: str | None = None,
) -> str:
    """Select full or user-scoped database access for a Volcano function.

    Returns
    -------
    str
        The connection URL with application_name replaced by the selected
        access mode. Other query parameters and credentials are preserved.

    Raises
    ------
    ValueError
        The URL is empty, lacks a postgres/postgresql scheme, or contains
        invalid percent escapes.

    """
    if not base_connection_string:
        raise ValueError(_REQUIRED_ERROR)

    target, query = _connection_parts(base_connection_string)
    parameters = _query_parameters(query)
    parameters.append(
        urlencode(
            {"application_name": _database_application_name(user_id)}, quote_via=quote
        )
    )
    return f"{target}?{'&'.join(parameters)}"


def _connection_parts(value: str) -> tuple[str, str]:
    prefix = _CONNECTION_URI_PREFIX.match(value)
    if prefix is None or _INVALID_PERCENT_ENCODING.search(value):
        raise ValueError(_INVALID_ERROR)

    before_at, at_separator, _ = value[prefix.end() :].partition("@")
    query_search_start = prefix.end()
    if at_separator and "/" not in before_at:
        query_search_start += len(before_at) + 1
    query_start = value.find("?", query_search_start)
    if query_start == -1:
        return value, ""
    return value[:query_start], value[query_start + 1 :]


def _query_parameters(query: str) -> list[str]:
    parameters = [
        parameter
        for parameter in query.split("&")
        if unquote(parameter.partition("=")[0]) != "application_name"
    ]
    serialized = "&".join(parameters).rstrip("&")
    return serialized.split("&") if serialized else []


def _database_application_name(user_id: str | None) -> str:
    value = "" if user_id is None else str(user_id)
    if not value:
        return _FULL_ACCESS_APP_NAME
    return f"{_USER_ACCESS_APP_NAME}:{value}"
