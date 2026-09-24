from __future__ import annotations

import json

import httpx
import pytest
from hypothesis import given, seed
from hypothesis import strategies as st

from volcano_sdk import NotFoundError, VolcanoClient
from volcano_sdk import _function_resolution as cache
from volcano_sdk._transport import GeneratedTransport

from .property_support import PROPERTY_SEED
from .typing import Annotated, TypeAlias

API_URL = "https://api.volcano.test"
AUTHORIZATION = "service-key"
RESOLUTION = cache.FunctionResolution("function-id", None)
URLControl: TypeAlias = Annotated[
    str, st.sampled_from([*(chr(value) for value in range(32)), "\x7f"])
]


def test_resolution_lifetime_expires_at_the_advertised_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(cache, "_now", lambda: clock[0])

    cache.store(API_URL, AUTHORIZATION, "first", RESOLUTION, 10.0)
    clock[0] = 109.999
    assert cache.lookup(API_URL, AUTHORIZATION, "first") == cache.CachedOutcome(
        RESOLUTION
    )
    clock[0] = 110.0
    assert cache.lookup(API_URL, AUTHORIZATION, "first") is None


def test_negative_resolution_keeps_error_details_until_its_exact_expiry(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(cache, "_now", lambda: clock[0])
    error = NotFoundError(
        "unknown function", status=404, code="function_missing", retry_after=7
    )

    cache.store_missing(API_URL, AUTHORIZATION, "missing", error)
    expected = cache.CachedOutcome(None, "unknown function", "function_missing", 7)
    assert cache.lookup(API_URL, AUTHORIZATION, "missing") == expected
    clock[0] = 100.0 + cache.NEGATIVE_TTL_SECONDS - 0.001
    assert cache.lookup(API_URL, AUTHORIZATION, "missing") == expected
    clock[0] = 100.0 + cache.NEGATIVE_TTL_SECONDS
    assert cache.lookup(API_URL, AUTHORIZATION, "missing") is None


def test_forget_only_drops_the_requested_credential_scope() -> None:
    other = cache.FunctionResolution("other-id", "https://functions.volcano.test/")
    cache.store(API_URL, AUTHORIZATION, "same-name", RESOLUTION, 60.0)
    cache.store(API_URL, "another-key", "same-name", other, 60.0)
    cache.store(
        "https://another-api.volcano.test", AUTHORIZATION, "same-name", other, 60.0
    )
    cache.store(API_URL, AUTHORIZATION, "another-name", other, 60.0)

    cache.forget(API_URL, AUTHORIZATION, "same-name")

    assert cache.lookup(API_URL, AUTHORIZATION, "same-name") is None
    assert cache.lookup(API_URL, "another-key", "same-name") == cache.CachedOutcome(
        other
    )
    assert cache.lookup(
        "https://another-api.volcano.test", AUTHORIZATION, "same-name"
    ) == cache.CachedOutcome(other)
    assert cache.lookup(API_URL, AUTHORIZATION, "another-name") == cache.CachedOutcome(
        other
    )


def test_forget_is_idempotent_when_concurrent_stale_calls_invalidate_one_key() -> None:
    cache.store(API_URL, AUTHORIZATION, "same-name", RESOLUTION, 60.0)

    cache.forget(API_URL, AUTHORIZATION, "same-name")
    cache.forget(API_URL, AUTHORIZATION, "same-name")

    assert cache.lookup(API_URL, AUTHORIZATION, "same-name") is None


def test_miss_locks_are_shared_for_one_key_but_striped_across_keys() -> None:
    first = cache.resolve_lock(API_URL, AUTHORIZATION, "first")
    assert cache.resolve_lock(API_URL, AUTHORIZATION, "first") is first
    stripes = {
        cache.resolve_lock(API_URL, AUTHORIZATION, str(index))
        for index in range(cache.MAX_ENTRIES)
    }
    assert len(stripes) > 1


@seed(PROPERTY_SEED)
@given(...)
def test_resolved_url_rejects_ascii_controls(control: URLControl) -> None:
    assert (
        cache.valid_invoke_url(f"https://functions.volcano.test/{control}path", API_URL)
        is None
    )


@pytest.mark.parametrize(
    "invoke_url",
    [
        "\x00https://functions.volcano.test/",
        "https://functions.volcano.test/\x00path",
        "https://functions.volcano.test/\x1bpath",
        "https://functions.volcano.test/\x7fpath",
        "https://functions.volcano.test/\ud800path",
    ],
)
def test_invalid_character_in_resolved_url_uses_api_path(invoke_url: str) -> None:
    paths: list[str] = []

    def handle(request: httpx.Request) -> httpx.Response:
        paths.append(request.url.path)
        if request.url.path == "/functions/resolve":
            return httpx.Response(
                200,
                content=json.dumps(
                    {
                        "name": "send-welcome",
                        "function_id": "00000000-0000-4000-8000-000000000040",
                        "invoke_url": invoke_url,
                        "cache_ttl_seconds": 60,
                    }
                ).encode(),
                headers={"content-type": "application/json"},
            )
        return httpx.Response(200, json={"ok": True})

    client = VolcanoClient(
        anon_key="anon-key",
        _transport=GeneratedTransport(
            api_url=API_URL, httpx_transport=httpx.MockTransport(handle)
        ),
    )

    assert client.functions.invoke("send-welcome").data == {"ok": True}
    assert paths == [
        "/functions/resolve",
        "/functions/00000000-0000-4000-8000-000000000040/invoke",
    ]


def populate_cache(*, ttl: float) -> None:
    for index in range(cache.MAX_ENTRIES):
        cache.store(API_URL, AUTHORIZATION, str(index), RESOLUTION, ttl)


def test_capacity_evicts_the_earliest_expiry_not_the_oldest_insert(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cache, "_now", lambda: 100.0)
    populate_cache(ttl=60.0)
    cache.store(API_URL, AUTHORIZATION, "1", RESOLUTION, 10.0)

    cache.store(API_URL, AUTHORIZATION, "new", RESOLUTION, 30.0)

    assert cache.lookup(API_URL, AUTHORIZATION, "1") is None
    assert cache.lookup(API_URL, AUTHORIZATION, "new") == cache.CachedOutcome(
        RESOLUTION
    )
    assert all(
        cache.lookup(API_URL, AUTHORIZATION, str(index))
        == cache.CachedOutcome(RESOLUTION)
        for index in range(cache.MAX_ENTRIES)
        if index != 1
    )


def test_capacity_reclaims_expiredentries_before_liveentries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(cache, "_now", lambda: clock[0])
    populate_cache(ttl=10.0)
    cache.store(API_URL, AUTHORIZATION, "0", RESOLUTION, 60.0)
    clock[0] += 10.0

    cache.store(API_URL, AUTHORIZATION, "new", RESOLUTION, 30.0)

    assert len(cache.entries) == 2
    assert cache.lookup(API_URL, AUTHORIZATION, "0") == cache.CachedOutcome(RESOLUTION)
    assert cache.lookup(API_URL, AUTHORIZATION, "new") == cache.CachedOutcome(
        RESOLUTION
    )
    assert all(
        cache.lookup(API_URL, AUTHORIZATION, str(index)) is None
        for index in range(1, cache.MAX_ENTRIES)
    )


@pytest.mark.parametrize(
    ("api_url", "authorization", "name"),
    [
        (API_URL, "other-key", "0"),
        ("https://other-api.volcano.test", AUTHORIZATION, "0"),
        (API_URL, AUTHORIZATION, "other-function"),
    ],
)
def test_eviction_preserves_resolution_scope(
    monkeypatch: pytest.MonkeyPatch,
    api_url: str,
    authorization: str,
    name: str,
) -> None:
    monkeypatch.setattr(cache, "_now", lambda: 100.0)
    populate_cache(ttl=60.0)
    cache.store(API_URL, AUTHORIZATION, "0", RESOLUTION, 10.0)
    other = cache.FunctionResolution(
        "other-function-id", "https://functions.volcano.test"
    )

    cache.store(api_url, authorization, name, other, 30.0)

    assert cache.lookup(API_URL, AUTHORIZATION, "0") is None
    assert cache.lookup(api_url, authorization, name) == cache.CachedOutcome(other)
    assert cache.lookup(API_URL, AUTHORIZATION, "1") == cache.CachedOutcome(RESOLUTION)


def test_replacing_an_entry_at_capacity_preserves_otherentries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cache, "_now", lambda: 100.0)
    populate_cache(ttl=60.0)
    updated = cache.FunctionResolution("replacement-id", None)

    cache.store(API_URL, AUTHORIZATION, "0", updated, 30.0)

    assert cache.lookup(API_URL, AUTHORIZATION, "0") == cache.CachedOutcome(updated)
    assert all(
        cache.lookup(API_URL, AUTHORIZATION, str(index))
        == cache.CachedOutcome(RESOLUTION)
        for index in range(1, cache.MAX_ENTRIES)
    )
    assert len(cache.entries) == cache.MAX_ENTRIES


def test_replacing_at_capacity_defers_the_expired_entry_sweep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(cache, "_now", lambda: clock[0])
    populate_cache(ttl=10.0)
    clock[0] = 110.0

    cache.store(API_URL, AUTHORIZATION, "0", RESOLUTION, 30.0)

    # A replacement cannot exceed capacity; scanning every entry here would
    # turn a common write into an O(capacity) operation.
    assert len(cache.entries) == cache.MAX_ENTRIES
    assert cache.lookup(API_URL, AUTHORIZATION, "0") == cache.CachedOutcome(RESOLUTION)
