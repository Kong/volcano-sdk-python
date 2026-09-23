"""Refresh and sign-out fail at transports that lack their operation."""

from __future__ import annotations

import pytest
from transport_fixtures import RejectingTransport

from volcano_sdk import Session, VolcanoClient


def test_refresh_requires_transport_capability() -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        client.auth._request_refreshed_session("refresh")


def test_sign_out_requires_transport_capability_and_keeps_session() -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())
    session = Session("access", "refresh", "user")
    client.auth.set_session(session)
    current = client.current_session

    with pytest.raises(TypeError, match="requested auth operation"):
        client.auth.sign_out()

    assert client.current_session is current
