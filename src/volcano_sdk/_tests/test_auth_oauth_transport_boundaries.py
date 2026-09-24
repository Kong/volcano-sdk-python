"""OAuth operations reject transports without the requested capability."""

from __future__ import annotations

import pytest

from volcano_sdk import Session, VolcanoClient

from .transport_fixtures import RejectingTransport
from .typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.auth import Auth


_LINKED_PROVIDER_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.list_linked_oauth_providers(),
    lambda auth: auth.link_oauth_provider(provider="github"),
    lambda auth: auth.call_oauth_api(provider="github", endpoint="/user"),
)


@pytest.mark.parametrize(
    "operation",
    _LINKED_PROVIDER_OPERATIONS,
    ids=("list-linked", "link", "call-api"),
)
def test_linked_provider_operation_requires_transport_capability(
    operation: Callable[[Auth], object],
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())
    _ = client.auth.set_session(Session("access", "refresh", "user"))

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = operation(client.auth)


def test_oauth_exchange_requires_transport_capability() -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        _ = client.auth.exchange_oauth_code(
            code="code",
            redirect_to="https://example.com/callback",
            state="state",
            expected_state="state",
        )
