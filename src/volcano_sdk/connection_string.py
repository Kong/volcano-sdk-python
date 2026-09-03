"""Postgres connection helpers for Volcano functions."""

import re
from urllib.parse import SplitResult, quote, unquote, urlsplit, urlunsplit

_FULL_ACCESS_APP_NAME = "volcano_full_access"
_USER_ACCESS_APP_NAME = "volcano_user_access"
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
    """Select full or user-scoped database access for a Volcano function."""
    if not base_connection_string:
        raise ValueError(_REQUIRED_ERROR)

    connection = _connection_url(base_connection_string)
    parameters = _query_parameters(connection.query)
    application_name = quote(_database_application_name(user_id), safe="")
    parameters.append(f"application_name={application_name}")
    query = "&".join(parameters)
    return urlunsplit(connection._replace(query=query))


def _connection_url(value: str) -> SplitResult:
    try:
        connection = urlsplit(value)
    except ValueError:
        raise ValueError(_INVALID_ERROR) from None
    if (
        not connection.scheme
        or connection.fragment
        or _INVALID_PERCENT_ENCODING.search(value)
    ):
        raise ValueError(_INVALID_ERROR)
    return connection


def _query_parameters(query: str) -> list[str]:
    if not query:
        return []
    return [
        parameter
        for parameter in query.split("&")
        if unquote(parameter.partition("=")[0]) != "application_name"
    ]


def _database_application_name(user_id: str | None) -> str:
    value = "" if user_id is None else str(user_id)
    if not value:
        return _FULL_ACCESS_APP_NAME
    return f"{_USER_ACCESS_APP_NAME}:{value}"
