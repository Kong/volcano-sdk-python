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
from urllib.parse import urlsplit

MAX_ENTRIES = 1024
NEGATIVE_TTL_SECONDS = 30.0

# Concurrent misses for one name serialize on a shared lock rather than each
# opening its own resolve. Striping keeps that bounded: a per-key lock table
# would grow with every name ever invoked.
_LOCK_STRIPES = 64


def _now() -> float:
    """Read the clock lifetimes are measured against, immune to wall-clock jumps."""
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


@dataclass(frozen=True, slots=True)
class _Entry:
    outcome: CachedOutcome
    expires_at: float


_lock = threading.Lock()
_entries: dict[tuple[str, str, str], _Entry] = {}
_stripes = [threading.Lock() for _ in range(_LOCK_STRIPES)]


def resolve_lock(api_url: str, authorization: str, name: str) -> threading.Lock:
    """Return the lock that serializes resolving one name."""
    return _stripes[hash((api_url, authorization, name)) % _LOCK_STRIPES]


def valid_invoke_url(value: object, api_url: str) -> str | None:
    """Return an absolute invocation URL, or None when unusable.

    The URL carries the caller's bearer token. Plaintext is accepted only when
    the API itself is plaintext, so a resolve response cannot downgrade a
    credential that is otherwise protected in transit.
    """
    if not isinstance(value, str) or not value:
        return None
    parsed = urlsplit(value)
    scheme = parsed.scheme.lower()
    if not parsed.netloc:
        return None
    if scheme == "https":
        return value
    if scheme == "http" and urlsplit(api_url).scheme.lower() == "http":
        return value
    return None


def lookup(api_url: str, authorization: str, name: str) -> CachedOutcome | None:
    """Return the cached outcome for a name, or None when it must be resolved."""
    key = (api_url, authorization, name)
    now = _now()
    with _lock:
        entry = _entries.get(key)
        if entry is None:
            return None
        if entry.expires_at <= now:
            del _entries[key]
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


def store_missing(api_url: str, authorization: str, name: str) -> None:
    """Remember briefly that a name does not resolve.

    A caller retrying an unknown name in a loop would otherwise re-ask the
    server on every attempt.
    """
    _store((api_url, authorization, name), CachedOutcome(None), NEGATIVE_TTL_SECONDS)


def _store(
    key: tuple[str, str, str],
    outcome: CachedOutcome,
    ttl_seconds: float,
) -> None:
    now = _now()
    with _lock:
        _entries[key] = _Entry(outcome=outcome, expires_at=now + ttl_seconds)
        if len(_entries) <= MAX_ENTRIES:
            return
        for expired in [k for k, v in _entries.items() if v.expires_at <= now]:
            del _entries[expired]
        while len(_entries) > MAX_ENTRIES:
            del _entries[min(_entries, key=lambda k: _entries[k].expires_at)]


def forget(api_url: str, authorization: str, name: str) -> None:
    """Drop one cached resolution that turned out to be stale."""
    with _lock:
        _entries.pop((api_url, authorization, name), None)


def clear() -> None:
    """Drop every cached resolution. Used by tests for isolation."""
    with _lock:
        _entries.clear()
