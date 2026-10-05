"""Shared cache for function name resolution.

`GET /functions/resolve` maps a function name to the identity and endpoint used
to invoke it, and tells us how long that mapping stays valid. Without a cache
every invocation pays that round trip. Entries are shared process-wide so
separate clients against the same API reuse one resolution, and keyed by
credential so a mapping never crosses an identity.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlsplit

import httpx

if TYPE_CHECKING:
    from .errors import NotFoundError

MAX_ENTRIES = 1024
NEGATIVE_TTL_SECONDS = 30.0

# Concurrent misses for one name serialize on a shared lock rather than each
# opening its own resolve. Striping keeps that bounded: a per-key lock table
# would grow with every name ever invoked.
_LOCK_STRIPES = 64


def _now() -> float:
    """Read the clock used for cache lifetimes.

    Returns
    -------
    float
        Monotonic seconds, unaffected by wall-clock adjustments.

    """
    return time.monotonic()


@dataclass(frozen=True, slots=True)
class FunctionResolution:
    """A resolved function identity and the endpoint that invokes it."""

    function_id: str
    invoke_url: str | None


@dataclass(frozen=True, slots=True)
class CachedOutcome:
    """A cached resolve result: a resolution, or a remembered miss when None."""

    resolution: FunctionResolution | None
    message: str = "Function was not found"
    code: str | None = None
    retry_after: int | None = None


@dataclass(frozen=True, slots=True)
class _Entry:
    outcome: CachedOutcome
    expires_at: float


_lock = threading.Lock()
entries: dict[tuple[str, str, str], _Entry] = {}
_stripes = [threading.Lock() for _ in range(_LOCK_STRIPES)]


def resolve_lock(api_url: str, authorization: str, name: str) -> threading.Lock:
    """Select the lock for resolving one name.

    Returns
    -------
    threading.Lock
        A shared stripe keyed by API URL, credential, and function name.

    """
    return _stripes[hash((api_url, authorization, name)) % _LOCK_STRIPES]


def valid_invoke_url(value: object, api_url: str) -> str | None:
    """Return an absolute invocation URL, or None when unusable.

    The URL carries the caller's bearer token. Plaintext is accepted only when
    the API itself is plaintext, so a resolve response cannot downgrade a
    credential that is otherwise protected in transit.

    Anything unusable yields None so the caller falls back to the API path. A
    malformed server response must not raise out of invoke().

    Returns
    -------
    str or None
        The accepted URL unchanged, or None to use the API endpoint.

    """
    if not isinstance(value, str):
        return None
    scheme = _absolute_url_scheme(value)
    if scheme == "https":
        return value
    if scheme == "http" and _absolute_url_scheme(api_url) == "http":
        return value
    return None


def _absolute_url_scheme(value: str) -> str | None:
    """Return the lowercase scheme of an absolute URL, or None when unusable.

    Unparseable input yields None rather than raising, so a malformed URL reads
    as unusable to every caller.

    Returns
    -------
    str or None
        The lowercase scheme, or None for an invalid authority or URL.

    """
    if not value or any(character.isspace() for character in value):
        return None
    try:
        parsed = urlsplit(value)
        # Reading the authority is the validation: an unclosed IPv6 literal or
        # a port out of range raises here rather than at request time.
        host, _port = parsed.hostname, parsed.port
        # urlsplit accepts controls that HTTPX rejects when invoking the URL.
        _ = httpx.URL(value)
    except (ValueError, httpx.InvalidURL):
        return None
    return parsed.scheme.lower() if host else None


def lookup(api_url: str, authorization: str, name: str) -> CachedOutcome | None:
    """Look up a function within its API and credential scope.

    Returns
    -------
    CachedOutcome or None
        An unexpired resolution or remembered miss; None requires a new resolve.

    """
    key = (api_url, authorization, name)
    now = _now()
    with _lock:
        entry = entries.get(key)
        if entry is None:
            return None
        if entry.expires_at <= now:
            del entries[key]
            return None
        return entry.outcome


def store(
    api_url: str,
    authorization: str,
    name: str,
    resolution: FunctionResolution,
    ttl_seconds: float,
) -> None:
    """Cache a resolution for the server-advertised lifetime."""
    _store((api_url, authorization, name), CachedOutcome(resolution), ttl_seconds)


def store_missing(
    api_url: str, authorization: str, name: str, error: NotFoundError
) -> None:
    """Remember briefly that a name does not resolve.

    A caller retrying an unknown name in a loop would otherwise re-ask the
    server on every attempt.
    """
    _store(
        (api_url, authorization, name),
        CachedOutcome(None, str(error), error.code, error.retry_after),
        NEGATIVE_TTL_SECONDS,
    )


def _store(
    key: tuple[str, str, str],
    outcome: CachedOutcome,
    ttl_seconds: float,
) -> None:
    now = _now()
    with _lock:
        entries[key] = _Entry(outcome=outcome, expires_at=now + ttl_seconds)
        if len(entries) <= MAX_ENTRIES:
            return
        for expired in [k for k, v in entries.items() if v.expires_at <= now]:
            del entries[expired]
        while len(entries) > MAX_ENTRIES:
            del entries[min(entries, key=lambda k: entries[k].expires_at)]


def forget(api_url: str, authorization: str, name: str) -> None:
    """Drop one cached resolution that turned out to be stale."""
    with _lock:
        _ = entries.pop((api_url, authorization, name), None)


def clear() -> None:
    """Drop every cached resolution. Used by tests for isolation."""
    with _lock:
        entries.clear()
