from __future__ import annotations

from typing import TYPE_CHECKING, cast

import httpx
import pytest

from volcano_sdk import Session, VolcanoClient
from volcano_sdk._transport import GeneratedTransport

if TYPE_CHECKING:
    from collections.abc import Mapping

    from volcano_sdk.models import JSONValue


@pytest.mark.parametrize("operation", ["signin", "anonymous", "refresh"])
def test_authentication_retains_the_local_user_snapshot(operation: str) -> None:
    user = {
        "id": "00000000-0000-4000-8000-000000000001",
        "email": "user@example.com",
        "status": "active",
        "user_metadata": {"roles": ["reader"]},
    }

    def handle(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            201 if request.url.path == "/auth/signup-anonymous" else 200,
            json={
                "access_token": "access",
                "refresh_token": "refresh",
                "user": user,
                "token_type": "bearer",
                "expires_in": 3600,
            },
        )

    client = VolcanoClient(
        anon_key="anon",
        _transport=GeneratedTransport(
            api_url="https://api.test.volcano.dev",
            httpx_transport=httpx.MockTransport(handle),
        ),
    )
    client.auth.set_session(Session("old", "old-refresh", str(user["id"])))
    operations = {
        "signin": lambda: client.auth.sign_in(
            email="user@example.com", password="secret"
        ),
        "anonymous": client.auth.sign_in_anonymously,
        "refresh": client.auth.refresh_session,
    }
    session = operations[operation]()

    assert session.user is not None
    assert session.user["email"] == "user@example.com"
    assert session.user["user_metadata"] == {"roles": ("reader",)}
    assert client.auth.get_session() is session


def test_session_adoption_copies_nested_user_data() -> None:
    roles: list[JSONValue] = ["reader"]
    source: Mapping[str, JSONValue] = {"id": "user", "user_metadata": {"roles": roles}}
    session = Session("access", "refresh", "user", user=source)
    roles.append("admin")
    client = VolcanoClient(anon_key="anon")

    adopted = client.auth.set_session(session)

    assert adopted.user == {"id": "user", "user_metadata": {"roles": ("reader",)}}
    assert adopted is not session
    with pytest.raises(TypeError):
        cast("dict[str, JSONValue]", adopted.user)["id"] = "other"


def test_session_adoption_rejects_a_mismatched_user_snapshot() -> None:
    client = VolcanoClient(anon_key="anon")
    session = Session("access", "refresh", "user", user={"id": "other"})

    with pytest.raises(ValueError, match="complete Session"):
        client.auth.set_session(session)
    assert client.auth.get_session() is None


def test_legacy_session_construction_remains_supported() -> None:
    session = Session("access", "refresh", "user")
    assert session.user is None
