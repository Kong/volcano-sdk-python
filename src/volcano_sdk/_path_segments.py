"""Keep caller values inside the route they are written into.

httpx removes ``.`` and ``..`` segments when it joins a request path to the
API URL, and Volcano routes on the decoded path, so an encoded ``/`` still
separates segments there. A value that becomes a dot or empty segment would
send the request to a different route than the operation intended; an empty
segment can also turn an item route into its collection route.
"""

from __future__ import annotations

import re
from typing import Final

SEGMENT_RULE: Final = 'cannot contain empty, ".", or ".." segments'
REQUEST_PATH_SEGMENTS: Final = f"Request path {SEGMENT_RULE}"
STORAGE_PATH_SEGMENTS: Final = f"Storage path {SEGMENT_RULE}"
INVALID_BUCKET_NAME: Final = 'Bucket name must be 1-64 letters, numbers, "_", or "-"'
INVALID_DATABASE_NAME: Final = (
    'Database name must be 1-64 lowercase letters, numbers, or "_"'
)
INVALID_LOCK_KEY: Final = (
    "Lock key must start with a letter or number and contain at most 128 "
    'letters, numbers, ".", "_", ":", or "-"'
)
INVALID_IDENTIFIER: Final = '{field} cannot contain "/" or be "." or ".."'

_DOT_SEGMENTS: Final = frozenset({".", ".."})
_BUCKET_NAME: Final = re.compile(r"[A-Za-z0-9_-]{1,64}")
_DATABASE_NAME: Final = re.compile(r"[a-z0-9_]{1,64}")
_LOCK_KEY: Final = re.compile(r"[A-Za-z0-9][A-Za-z0-9._:-]{0,127}")
_ENCODED_DOT: Final = re.compile(r"%2e", re.IGNORECASE)
_ENCODED_SLASH: Final = re.compile(r"%2f", re.IGNORECASE)


def bucket_relative_path(path: str) -> str:
    """Drop one leading separator; Volcano treats "/a.txt" and "a.txt" alike.

    Returns:
        The path relative to its bucket.

    """
    return path.removeprefix("/")


def invalid_storage_path(path: str) -> bool:
    """Report whether an object path has an empty, "." or ".." segment.

    Returns:
        Whether the path would leave its object route.

    """
    relative = bucket_relative_path(path)
    return not relative or any(
        not segment or segment in _DOT_SEGMENTS for segment in relative.split("/")
    )


def bucket_name(value: str) -> str:
    """Require the API's bucket name pattern across the whole value.

    Returns:
        The unchanged bucket name.

    Raises:
        ValueError: The name does not match the bucket name pattern.

    """
    if not _BUCKET_NAME.fullmatch(value):
        raise ValueError(INVALID_BUCKET_NAME)
    return value


def database_name(value: str) -> str:
    """Require the API's database name pattern across the whole value.

    Returns:
        The unchanged database name.

    Raises:
        ValueError: The name does not match the database name pattern.

    """
    if not _DATABASE_NAME.fullmatch(value):
        raise ValueError(INVALID_DATABASE_NAME)
    return value


def lock_key(value: str) -> str:
    """Require the API's lock key pattern across the whole value.

    Returns:
        The unchanged lock key.

    Raises:
        ValueError: The key does not match the lock key pattern.

    """
    if not _LOCK_KEY.fullmatch(value):
        raise ValueError(INVALID_LOCK_KEY)
    return value


def path_identifier(value: str, field: str) -> str:
    """Refuse an identifier that would not stay one path segment.

    Returns:
        The unchanged identifier.

    Raises:
        ValueError: The identifier is ".", "..", or contains "/".

    """
    if value in _DOT_SEGMENTS or "/" in value:
        raise ValueError(INVALID_IDENTIFIER.format(field=field))
    return value


def invalid_request_segment(segment: str) -> bool:
    """Report whether an encoded path segment resolves to an empty or dot segment.

    Returns:
        Whether the segment, decoded the way Volcano routes it, is empty,
        "." or "..".

    """
    decoded = _ENCODED_DOT.sub(".", segment)
    return any(
        not part or part in _DOT_SEGMENTS for part in _ENCODED_SLASH.split(decoded)
    )


def check_request_path(path: str) -> str:
    """Refuse a relative request path before httpx resolves it.

    Returns:
        The unchanged path.

    Raises:
        ValueError: A segment is empty, "." or "..", directly or once decoded.

    """
    route = path.removeprefix("/")
    if any(invalid_request_segment(segment) for segment in route.split("/")):
        raise ValueError(REQUEST_PATH_SEGMENTS)
    return path


def object_path(path: str) -> str:
    """Check an object path and return it relative to its bucket.

    Returns:
        The path without its leading separator.

    Raises:
        ValueError: A segment is empty, "." or "..".

    """
    if invalid_storage_path(path):
        raise ValueError(STORAGE_PATH_SEGMENTS)
    return bucket_relative_path(path)
