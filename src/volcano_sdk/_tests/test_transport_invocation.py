from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

import httpx
import pytest

from volcano_sdk import TransportError
from volcano_sdk._transport import invoke, invoke_async

if TYPE_CHECKING:
    from collections.abc import Callable


def echo_url(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, text=str(request.url))


def fail_with(error: Exception) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        del request
        raise error

    return handler


def test_invocation_preserves_http_response_type_and_arguments() -> None:
    with httpx.Client(transport=httpx.MockTransport(echo_url)) as client:
        response = assert_type(
            invoke(client.get, "https://api.volcano.test/items", params={"page": 2}),
            httpx.Response,
        )

    assert response.text == "https://api.volcano.test/items?page=2"


async def test_async_invocation_preserves_response_type_and_arguments() -> None:
    async with httpx.AsyncClient(transport=httpx.MockTransport(echo_url)) as client:
        response = assert_type(
            await invoke_async(
                client.get, "https://api.volcano.test/items", params={"page": 2}
            ),
            httpx.Response,
        )

    assert response.text == "https://api.volcano.test/items?page=2"


@pytest.mark.parametrize("message", ["connection failed", ""])
def test_invocation_retains_the_original_http_failure(message: str) -> None:
    original = httpx.ConnectError(message)
    with (
        httpx.Client(transport=httpx.MockTransport(fail_with(original))) as client,
        pytest.raises(TransportError) as caught,
    ):
        _ = invoke(client.get, "https://api.volcano.test/items")

    assert str(caught.value) == (message or "Volcano transport failed")
    assert caught.value.__cause__ is original


@pytest.mark.parametrize("message", ["connection failed", ""])
async def test_async_invocation_retains_the_original_http_failure(message: str) -> None:
    original = httpx.ConnectError(message)
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(fail_with(original))
    ) as client:
        with pytest.raises(TransportError) as caught:
            _ = await invoke_async(client.get, "https://api.volcano.test/items")

    assert str(caught.value) == (message or "Volcano transport failed")
    assert caught.value.__cause__ is original


def test_invocation_preserves_non_http_failures() -> None:
    original = ValueError("invalid transport configuration")
    with (
        httpx.Client(transport=httpx.MockTransport(fail_with(original))) as client,
        pytest.raises(ValueError, match="invalid transport configuration") as caught,
    ):
        _ = invoke(client.get, "https://api.volcano.test/items")

    assert caught.value is original


async def test_async_invocation_preserves_non_http_failures() -> None:
    original = ValueError("invalid transport configuration")
    async with httpx.AsyncClient(
        transport=httpx.MockTransport(fail_with(original))
    ) as client:
        with pytest.raises(
            ValueError, match="invalid transport configuration"
        ) as caught:
            _ = await invoke_async(client.get, "https://api.volcano.test/items")

    assert caught.value is original
