"""HTTP configuration for the generated transport."""

from __future__ import annotations

import httpx

from ._generated.client import AuthenticatedClient
from ._transport_types import URL_TRAILING_SLASHES


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

    def _client(self, authorization: str) -> AuthenticatedClient:
        httpx_args: dict[str, object] = {}
        if self._httpx_transport is not None:
            httpx_args["transport"] = self._httpx_transport
        return AuthenticatedClient(
            base_url=self._api_url,
            token=authorization,
            timeout=httpx.Timeout(self._timeout),
            httpx_args=httpx_args,
        )
