"""Optional auth operations reject transports without the requested capability."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from transport_fixtures import RejectingTransport

from volcano_sdk import VolcanoClient

if TYPE_CHECKING:
    from collections.abc import Callable

    from volcano_sdk.auth import Auth


_AUTH_OPERATIONS: tuple[Callable[[Auth], object], ...] = (
    lambda auth: auth.sign_up(email="user@example.com", password="password"),
    lambda auth: auth.sign_in_anonymously(),
    lambda auth: auth.reset_password_for_email(email="user@example.com"),
)


@pytest.mark.parametrize(
    "operation",
    _AUTH_OPERATIONS,
    ids=("sign-up", "anonymous-sign-up", "forgot-password"),
)
def test_optional_auth_operation_requires_transport_capability(
    operation: Callable[[Auth], object],
) -> None:
    client = VolcanoClient(anon_key="anon", _transport=RejectingTransport())

    with pytest.raises(TypeError, match="requested auth operation"):
        operation(client.auth)
