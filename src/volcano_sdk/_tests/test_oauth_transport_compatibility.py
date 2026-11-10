from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import LinkedOAuthProvider, VolcanoError

from .test_auth_facade_recovery import client_for

if TYPE_CHECKING:
    from volcano_sdk.models import JSONValue


def provider_payload() -> dict[str, JSONValue]:
    return {
        "provider": "future-provider",
        "linked_at": "2026-08-30T12:00:00Z",
        "updated_at": "2026-09-01T12:00:00Z",
    }


@pytest.mark.parametrize(
    "identity",
    [{}, {"provider_user_id": "583231", "provider_login": "octocat"}],
    ids=["legacy-three-fields", "current-five-fields"],
)
def test_linked_providers_preserve_legacy_and_current_wire_responses(
    identity: dict[str, JSONValue],
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(
            200, json={"providers": [{**provider_payload(), **identity}]}
        )

    client = client_for(handle)
    original = client.current_session

    result = client.auth.list_linked_oauth_providers()

    assert result == (
        LinkedOAuthProvider(
            provider="future-provider",
            linked_at=datetime.fromisoformat("2026-08-30T12:00:00+00:00"),
            updated_at=datetime.fromisoformat("2026-09-01T12:00:00+00:00"),
        ),
    )
    assert [(request.method, request.url.path) for request in requests] == [
        ("GET", "/auth/oauth/providers")
    ]
    assert original is not None
    assert requests[0].headers["authorization"] == f"Bearer {original.access_token}"
    assert client.current_session is original


@pytest.mark.parametrize("field", ["provider", "linked_at", "updated_at"])
@pytest.mark.parametrize("value", [None, False, 42, [], {}, "", " \t"])
def test_linked_provider_wire_values_keep_native_validation(
    field: str, value: JSONValue
) -> None:
    provider = {**provider_payload(), field: value}
    client = client_for(
        lambda _request: httpx.Response(200, json={"providers": [provider]})
    )
    original = client.current_session

    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        _ = client.auth.list_linked_oauth_providers()

    assert client.current_session is original


@pytest.mark.parametrize("field", ["linked_at", "updated_at"])
@pytest.mark.parametrize(
    "value", ["2026-02-30T12:00:00Z", "2026-08-30T12:00:00", "2026-08-30"]
)
def test_linked_provider_wire_dates_reject_invalid_calendar_values(
    field: str, value: str
) -> None:
    provider = {**provider_payload(), field: value}
    client = client_for(
        lambda _request: httpx.Response(200, json={"providers": [provider]})
    )

    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        _ = client.auth.list_linked_oauth_providers()


def test_linked_provider_wire_dates_preserve_fractional_offsets() -> None:
    provider = {
        **provider_payload(),
        "linked_at": "2026-08-30T12:00:00.123456+05:30",
        "updated_at": "2026-08-30T12:00:00.123456+05:30",
    }
    client = client_for(
        lambda _request: httpx.Response(200, json={"providers": [provider]})
    )

    result = client.auth.list_linked_oauth_providers()

    expected = datetime(
        2026, 8, 30, 12, 0, 0, 123456, tzinfo=timezone(timedelta(hours=5, minutes=30))
    )
    assert (result[0].linked_at, result[0].updated_at) == (expected, expected)


def test_linked_providers_accept_an_empty_wire_collection() -> None:
    client = client_for(lambda _request: httpx.Response(200, json={"providers": []}))

    assert client.auth.list_linked_oauth_providers() == ()


@pytest.mark.parametrize(
    "payload",
    [None, [], {}, {"providers": None}, {"providers": {}}, {"providers": [None]}],
)
def test_linked_provider_wire_collection_must_be_complete(payload: JSONValue) -> None:
    client = client_for(lambda _request: httpx.Response(200, json=payload))

    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        _ = client.auth.list_linked_oauth_providers()
