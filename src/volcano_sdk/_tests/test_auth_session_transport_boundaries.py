"""Refresh and sign-out fail at transports that lack their operation."""

from __future__ import annotations

import pytest

from volcano_sdk import Session

from .client_inspection import InspectedClient
from .transport_fixtures import RejectingTransport


def test_refresh_requires_transport_capability() -> None:
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = client.requests.request_refreshed_session("refresh")


def test_sign_out_requires_transport_capability_and_keeps_session() -> None:
    client = InspectedClient(anon_key="anon", _transport=RejectingTransport())
    session = Session("access", "refresh", "user")
    _ = client.auth.set_session(session)
    current = client.current_session

    with pytest.raises(TypeError, match="requested auth operation"):
        client.auth.sign_out()

    assert client.current_session is current
