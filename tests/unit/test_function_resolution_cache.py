from __future__ import annotations

import pytest

from volcano_sdk import _function_resolution as cache

API_URL = "https://api.volcano.test"
AUTHORIZATION = "service-key"
RESOLUTION = cache.FunctionResolution("function-id", None)


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


def test_capacity_reclaims_expired_entries_before_live_entries(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clock = [100.0]
    monkeypatch.setattr(cache, "_now", lambda: clock[0])
    populate_cache(ttl=10.0)
    cache.store(API_URL, AUTHORIZATION, "0", RESOLUTION, 60.0)
    clock[0] += 10.0

    cache.store(API_URL, AUTHORIZATION, "new", RESOLUTION, 30.0)

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


def test_replacing_an_entry_at_capacity_preserves_other_entries(
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
