"""Postgres connection helpers for Volcano functions."""

import re
from urllib.parse import quote, unquote

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
    application_name = quote(_database_application_name(user_id), safe="")
    parameters.append(f"application_name={application_name}")
    return f"{target}?{'&'.join(parameters)}"


def _connection_parts(value: str) -> tuple[str, str]:
    prefix = _CONNECTION_URI_PREFIX.match(value)
    if prefix is None or _INVALID_PERCENT_ENCODING.search(value):
        raise ValueError(_INVALID_ERROR)

    authority_end = value.find("/", prefix.end())
    possible_userinfo_end = value.find("@", prefix.end())
    userinfo_end = (
        possible_userinfo_end
        if possible_userinfo_end != -1
        and (authority_end == -1 or possible_userinfo_end < authority_end)
        else -1
    )
    query_start = value.find("?", max(prefix.end(), userinfo_end + 1))
    if query_start == -1:
        return value, ""
    return value[:query_start], value[query_start + 1 :]


def _query_parameters(query: str) -> list[str]:
    if not query:
        return []
    parameters = [
        parameter
        for parameter in query.split("&")
        if unquote(parameter.partition("=")[0]) != "application_name"
    ]
    for index in range(len(parameters) - 1, -1, -1):
        if parameters[index]:
            return parameters[: index + 1]
    return []


def _database_application_name(user_id: str | None) -> str:
    value = "" if user_id is None else str(user_id)
    if not value:
        return _FULL_ACCESS_APP_NAME
    return f"{_USER_ACCESS_APP_NAME}:{value}"
