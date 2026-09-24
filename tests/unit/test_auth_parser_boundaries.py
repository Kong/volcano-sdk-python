from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

import httpx
import pytest
from test_auth_facade_recovery import client_for

from volcano_sdk import AuthenticationError, VolcanoError
from volcano_sdk._generated.models import (
    AuthGetUserResponse200,
    AuthListOAuthProvidersResponse200,
    AuthListOAuthProvidersResponse200ProvidersItem,
    CallOAuthProviderAPIResponse200,
)
from volcano_sdk._generated.types import UNSET, Unset
from volcano_sdk.auth import (
    _email_change_result_from_payload,
    _linked_oauth_providers_from_payload,
    _oauth_api_data_from_payload,
    _oauth_link_from_payload,
    _oauth_provider_token_status_from_payload,
    _oauth_state,
    _optional_session_string,
    _session_from_payload,
    _session_page_from_payload,
    _sign_up_result_from_payload,
    _user_from_payload,
)

if TYPE_CHECKING:
    from collections.abc import Callable


@pytest.mark.parametrize("parameter", ["redirect", "state"])
@pytest.mark.parametrize("value", ["", " \t\n"])
def test_oauth_rejects_blank_parameters_without_sending_credentials(
    parameter: str, value: str
) -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    client = client_for(handle)
    original = client.current_session
    with pytest.raises(ValueError, match="OAuth parameters must be non-empty strings"):
        _ = client.auth.sign_in_with_oauth(
            provider="github",
            redirect_to=value if parameter == "redirect" else "https://app.test/auth",
            state=value if parameter == "state" else "state",
        )
    assert client.current_session is original
    assert requests == []


def test_oauth_rejects_oversized_state_before_exchanging_a_code() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200)

    client = client_for(handle)
    original = client.current_session
    with pytest.raises(ValueError, match="OAuth state must not exceed 255 characters"):
        _ = client.auth.exchange_oauth_code(
            code="code",
            redirect_to="https://app.test/auth",
            state="s" * 256,
            expected_state="s" * 256,
        )
    assert client.current_session is original
    assert requests == []


def test_oauth_accepts_the_maximum_state_length() -> None:
    state = "s" * 255
    assert _oauth_state(state) == state


@pytest.mark.parametrize(
    "payload",
    [
        42,
        {
            "access_token": "access",
            "refresh_token": "refresh",
            "user": [],
        },
    ],
)
def test_session_parser_rejects_nonmapping_payloads(payload: object) -> None:
    with pytest.raises(ValueError, match="Expected a complete Session"):
        _ = _session_from_payload(payload)


def test_session_parser_rejects_non_json_user_data() -> None:
    payload = {
        "access_token": "access",
        "refresh_token": "refresh",
        "user": {"id": "user", "metadata": {"invalid": object()}},
    }
    with pytest.raises(TypeError, match="Expected a complete Session"):
        _ = _session_from_payload(payload)


@pytest.mark.parametrize("field", ["user_metadata", "app_metadata"])
def test_profile_parser_rejects_non_json_metadata(field: str) -> None:
    payload = AuthGetUserResponse200.from_dict(
        {
            "user": {
                "id": "00000000-0000-4000-8000-000000000001",
                "email": "user@example.com",
                "status": "active",
                field: {"invalid": object()},
            }
        }
    )
    with pytest.raises(AuthenticationError, match="complete user profile"):
        _ = _user_from_payload(payload)


def test_profile_parser_rejects_non_json_extra_user_data() -> None:
    payload = AuthGetUserResponse200.from_dict(
        {
            "user": {
                "id": "00000000-0000-4000-8000-000000000001",
                "email": "user@example.com",
                "status": "active",
                "invalid": object(),
            }
        }
    )
    with pytest.raises(AuthenticationError, match="complete user profile"):
        _ = _user_from_payload(payload)


@pytest.mark.parametrize("data", [object(), [object()], {"invalid": object()}])
def test_oauth_api_parser_rejects_non_json_provider_data(data: object) -> None:
    payload = CallOAuthProviderAPIResponse200.from_dict(
        {
            "provider": "github",
            "endpoint": "/user",
            "status_code": 200,
            "data": data,
        }
    )
    with pytest.raises(VolcanoError, match="OAuth provider API response data"):
        _ = _oauth_api_data_from_payload(payload)


def test_oauth_api_parser_preserves_nested_json() -> None:
    payload = CallOAuthProviderAPIResponse200.from_dict(
        {
            "provider": "github",
            "endpoint": "/user",
            "status_code": 200,
            "data": {"values": [1, {"enabled": True}]},
        }
    )
    assert _oauth_api_data_from_payload(payload) == {"values": (1, {"enabled": True})}


def test_profile_parser_preserves_a_ban_without_a_project_id() -> None:
    banned_until = datetime.fromisoformat("2026-10-01T12:00:00+00:00")
    payload = AuthGetUserResponse200.from_dict(
        {
            "user": {
                "id": "00000000-0000-4000-8000-000000000001",
                "email": "user@example.com",
                "status": "active",
                "banned_until": banned_until.isoformat(),
            }
        }
    )

    profile, _ = _user_from_payload(payload)

    assert profile.project_id is None
    assert profile.banned_until == banned_until


@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        {},
        {"confirmation_required": True},
        {"message": "Check your email"},
        {"confirmation_required": 1, "message": "Check your email"},
        {"confirmation_required": True, "message": 42},
    ],
)
def test_sign_up_acknowledgement_requires_boolean_and_message(payload: object) -> None:
    with pytest.raises(TypeError, match="Expected a complete sign-up acknowledgement"):
        _ = _sign_up_result_from_payload(payload)


@pytest.mark.parametrize("field", ["message", "new_email"])
@pytest.mark.parametrize("value", [False, 42, [], {}])
def test_email_change_acknowledgement_rejects_invalid_fields(
    field: str, value: object
) -> None:
    with pytest.raises(
        TypeError, match="Expected a valid email-change acknowledgement"
    ):
        _ = _email_change_result_from_payload({field: value})


@pytest.mark.parametrize("value", [UNSET, None])
def test_optional_session_strings_preserve_absence(value: Unset | None) -> None:
    assert _optional_session_string(value) is None


@pytest.mark.parametrize("payload", [None, {}, [], True, "response"])
@pytest.mark.parametrize(
    ("parse", "message"),
    [
        (_session_page_from_payload, "Expected a complete session page"),
        (
            _linked_oauth_providers_from_payload,
            "Expected complete linked OAuth providers",
        ),
        (_oauth_link_from_payload, "Expected an OAuth authorization URL"),
        (
            _oauth_provider_token_status_from_payload,
            "Expected complete OAuth provider token status",
        ),
        (_oauth_api_data_from_payload, "Expected OAuth provider API response data"),
    ],
)
def test_auth_parsers_reject_values_without_the_expected_model(
    parse: Callable[[object], object], message: str, payload: object
) -> None:
    with pytest.raises(VolcanoError, match=message):
        _ = parse(payload)


def test_linked_providers_require_the_collection_to_be_present() -> None:
    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        _ = _linked_oauth_providers_from_payload(AuthListOAuthProvidersResponse200())


@pytest.mark.parametrize("provider", [UNSET, "", " \t"])
def test_linked_providers_require_a_nonempty_provider(provider: str | Unset) -> None:
    payload = AuthListOAuthProvidersResponse200(
        providers=[AuthListOAuthProvidersResponse200ProvidersItem(provider=provider)]
    )
    with pytest.raises(VolcanoError, match="Expected complete linked OAuth providers"):
        _ = _linked_oauth_providers_from_payload(payload)
