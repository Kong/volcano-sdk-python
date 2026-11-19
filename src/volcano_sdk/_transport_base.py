"""HTTP configuration for the generated transport."""

from __future__ import annotations

import httpx
from typing_extensions import override

from ._generated.client import AuthenticatedClient, Client
from ._path_segments import check_request_path
from ._transport_types import URL_TRAILING_SLASHES
from ._user_agent import user_agent_headers


def _checked_route(url: httpx.URL | str) -> httpx.URL | str:
    """Check a relative route before httpx joins it to the API URL.

    httpx resolves dot segments while joining, after which a route that left
    its operation looks like any other, so the check has to see the route
    exactly as the generated operation built it. An absolute URL, such as a
    resolved function endpoint, is not joined.

    Returns:
        The unchanged URL.

    """
    if isinstance(url, str) and url.startswith("/"):
        _ = check_request_path(url)
    return url


class _RouteCheckingClient(httpx.Client):
    @override
    def _merge_url(self, url: httpx.URL | str) -> httpx.URL:
        return super()._merge_url(_checked_route(url))


class _RouteCheckingAsyncClient(httpx.AsyncClient):
    @override
    def _merge_url(self, url: httpx.URL | str) -> httpx.URL:
        return super()._merge_url(_checked_route(url))


class TransportBase:
    """Share HTTP configuration across generated operation adapters."""

    def __init__(
        self,
        *,
        api_url: str,
        timeout: float = 60.0,
        httpx_transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._api_url: str = api_url.rstrip(URL_TRAILING_SLASHES)
        self._timeout: float = timeout
        self._httpx_transport: httpx.BaseTransport | None = httpx_transport

    def _client(
        self, authorization: str, *, timeout: float | None = None
    ) -> AuthenticatedClient:
        client = AuthenticatedClient(base_url=self._api_url, token=authorization)
        limits = httpx.Timeout(self._timeout if timeout is None else timeout)
        # Both sides are set, so neither entry builds an unchecked httpx client.
        _ = client.set_async_httpx_client(
            _RouteCheckingAsyncClient(
                base_url=self._api_url,
                headers={**user_agent_headers(), **_credential_header(client)},
                timeout=limits,
                transport=_async_side(self._httpx_transport),
            )
        )
        return client.set_httpx_client(
            _RouteCheckingClient(
                base_url=self._api_url,
                headers={**user_agent_headers(), **_credential_header(client)},
                timeout=limits,
                transport=self._httpx_transport,
            )
        )

    def _public_client(self, *, timeout: float | None = None) -> Client:
        return Client(base_url=self._api_url).set_httpx_client(
            _RouteCheckingClient(
                base_url=self._api_url,
                headers=user_agent_headers(),
                timeout=httpx.Timeout(timeout),
                transport=self._httpx_transport,
            )
        )


def _credential_header(client: AuthenticatedClient) -> dict[str, str]:
    return {client.auth_header_name: f"{client.prefix} {client.token}"}


def _async_side(
    transport: httpx.BaseTransport | None,
) -> httpx.AsyncBaseTransport | None:
    # A mock can serve both directions; a plain synchronous transport has no
    # asynchronous side to reuse.
    side: object = transport
    return side if isinstance(side, httpx.AsyncBaseTransport) else None
