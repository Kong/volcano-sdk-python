"""Postgres connection helpers for Volcano functions."""

import re
from urllib.parse import SplitResult, parse_qsl, quote, urlencode, urlsplit, urlunsplit

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
    parameters = [
        (name, value)
        for name, value in parse_qsl(connection.query, keep_blank_values=True)
        if name != "application_name"
    ]
    parameters.append(("application_name", _database_application_name(user_id)))
    query = urlencode(parameters, doseq=True, quote_via=quote)
    return urlunsplit(connection._replace(query=query))


def _connection_url(value: str) -> SplitResult:
    try:
        connection = urlsplit(value)
    except ValueError:
        raise ValueError(_INVALID_ERROR) from None
    if not connection.scheme or _INVALID_PERCENT_ENCODING.search(value):
        raise ValueError(_INVALID_ERROR)
    return connection


def _database_application_name(user_id: str | None) -> str:
    value = "" if user_id is None else str(user_id)
    if not value:
        return _FULL_ACCESS_APP_NAME
    return f"{_USER_ACCESS_APP_NAME}:{value}"
