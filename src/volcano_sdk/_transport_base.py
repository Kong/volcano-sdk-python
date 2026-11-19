"""HTTP configuration for the generated transport."""

from __future__ import annotations

from typing import final

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
        client = _CheckedAuthenticatedClient(
            base_url=self._api_url,
            token=authorization,
            headers=user_agent_headers(),
            timeout=self._limits(timeout),
        )
        client.route_transport = self._httpx_transport
        return client

    def _public_client(self, *, timeout: float | None = None) -> Client:
        client = _CheckedClient(
            base_url=self._api_url,
            headers=user_agent_headers(),
            timeout=self._limits(timeout),
        )
        client.route_transport = self._httpx_transport
        return client

    def _limits(self, timeout: float | None) -> httpx.Timeout:
        return httpx.Timeout(self._timeout if timeout is None else timeout)


# The generated clients build a plain httpx client for whichever side a call
# enters. These build the route-checking client instead, still only for the
# side that is used.
@final
class _CheckedClient(Client):
    route_transport: httpx.BaseTransport | None = None

    @override
    def get_httpx_client(self) -> httpx.Client:
        if self._client is None:
            self._client = _RouteCheckingClient(
                base_url=self._base_url,
                headers=self._headers,
                timeout=self._timeout,
                transport=self.route_transport,
            )
        return self._client

    @override
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = _RouteCheckingAsyncClient(
                base_url=self._base_url,
                headers=self._headers,
                timeout=self._timeout,
                transport=_async_side(self.route_transport),
            )
        return self._async_client


@final
class _CheckedAuthenticatedClient(AuthenticatedClient):
    route_transport: httpx.BaseTransport | None = None

    @override
    def get_httpx_client(self) -> httpx.Client:
        if self._client is None:
            self._client = _RouteCheckingClient(
                base_url=self._base_url,
                headers=self._credentialed_headers(),
                timeout=self._timeout,
                transport=self.route_transport,
            )
        return self._client

    @override
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = _RouteCheckingAsyncClient(
                base_url=self._base_url,
                headers=self._credentialed_headers(),
                timeout=self._timeout,
                transport=_async_side(self.route_transport),
            )
        return self._async_client

    def _credentialed_headers(self) -> dict[str, str]:
        return {**self._headers, self.auth_header_name: f"{self.prefix} {self.token}"}


def _async_side(
    transport: httpx.BaseTransport | None,
) -> httpx.AsyncBaseTransport | None:
    # A mock can serve both directions; a plain synchronous transport has no
    # asynchronous side to reuse.
    side: object = transport
    return side if isinstance(side, httpx.AsyncBaseTransport) else None
