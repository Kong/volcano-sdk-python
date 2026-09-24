"""Serverless function invocation facade."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, cast, runtime_checkable

from ._client_context import ClientContextSource, facade_context
from ._function_requests import FunctionAuth, FunctionsContext
from ._function_resolution import (
    FunctionResolution,
    forget,
    lookup,
    resolve_lock,
    store,
    store_missing,
    valid_invoke_url,
)
from ._function_values import (
    FUNCTION_INVOKED_HEADER,
    FUNCTION_VERSION_HEADER,
    HTTP_NOT_FOUND,
    HTTP_SUCCESS_MIN,
    HTTP_SUCCESS_STATUSES,
    HTTP_UNAUTHORIZED,
    INVALID_FUNCTION_RESPONSE,
    INVALID_FUNCTION_TRANSPORT,
    function_data,
    function_name,
    function_payload,
    header,
    stale_mapping,
)
from ._transport import TransportResponse, invoke, response_payload
from .errors import (
    NotFoundError,
)
from .models import FunctionResponse, JSONValue

# Present only once the platform has dispatched to the function.


@runtime_checkable
class FunctionsTransport(Protocol):
    """Transport operations required by the functions facade."""

    def resolve_function_for_invocation(
        self,
        *,
        authorization: str,
        name: str,
    ) -> TransportResponse:
        """Resolve a function name to its canonical identifier."""
        ...

    def invoke_function(
        self,
        *,
        authorization: str,
        function_id: str,
        payload: Mapping[str, JSONValue],
    ) -> TransportResponse:
        """Invoke a resolved function identifier."""
        ...

    def invoke_function_url(
        self,
        *,
        authorization: str,
        invoke_url: str,
        payload: Mapping[str, JSONValue],
    ) -> TransportResponse:
        """Invoke a function at its resolved endpoint."""
        ...


__all__ = ["Functions", "FunctionsContext", "FunctionsTransport"]


class Functions:
    """Invoke deployed Volcano functions by name."""

    def __init__(self, client: FunctionsContext | ClientContextSource) -> None:
        """Bind function calls to a Volcano client."""
        self._client: FunctionsContext = facade_context(client)

    def _function_transport(self) -> FunctionsTransport:
        transport = self._client.transport()
        if not isinstance(transport, FunctionsTransport):
            raise TypeError(INVALID_FUNCTION_TRANSPORT)
        return transport

    def invoke(
        self,
        name: str,
        payload: Mapping[str, JSONValue] | None = None,
    ) -> FunctionResponse:
        """Resolve and invoke a function with an optional JSON object payload.

        Returns
        -------
        FunctionResponse
            The function's data, status, headers, and deployed version. Errors
            returned by the function are preserved; platform failures raise.

        """
        auth = FunctionAuth(self._client)
        name = function_name(name)
        request_payload = function_payload(payload)
        transport = self._function_transport()
        authorization, resolution = auth.run(
            lambda token: (token, self._resolve(transport, token, name))
        )
        response = auth.run(
            lambda token: self._invoke_resolved(
                transport, token, resolution, request_payload
            )
        )
        if stale_mapping(response):
            # The function was deleted and recreated, so the cached identity no
            # longer exists. Resolve again before giving up.
            forget(self._client.api_base_url(), authorization, name)
            _, resolution = auth.run(
                lambda token: (token, self._resolve(transport, token, name))
            )
            response = auth.run(
                lambda token: self._invoke_resolved(
                    transport, token, resolution, request_payload
                )
            )
        return self._response(response)

    @staticmethod
    def _invoke_resolved(
        transport: FunctionsTransport,
        authorization: str,
        resolution: FunctionResolution,
        payload: Mapping[str, JSONValue],
    ) -> TransportResponse:
        if resolution.invoke_url is None:
            response = invoke(
                transport.invoke_function,
                authorization=authorization,
                function_id=resolution.function_id,
                payload=payload,
            )
        else:
            response = invoke(
                transport.invoke_function_url,
                authorization=authorization,
                invoke_url=resolution.invoke_url,
                payload=payload,
            )
        if (
            response.status_code == HTTP_UNAUTHORIZED
            and header(response.headers, FUNCTION_INVOKED_HEADER) is None
        ):
            _ = response_payload(response, HTTP_SUCCESS_MIN)
        return response

    def _resolve(
        self,
        transport: FunctionsTransport,
        authorization: str,
        name: str,
    ) -> FunctionResolution:
        """Resolve a function, reusing a live cached result.

        Returns
        -------
        FunctionResolution
            The function's identifier and optional direct invocation URL.

        """
        api_url = self._client.api_base_url()
        cached = self._cached(api_url, authorization, name)
        if cached is not None:
            return cached

        # Hold the name's lock across the round trip so concurrent callers wait
        # for one resolve instead of each opening their own.
        with resolve_lock(api_url, authorization, name):
            cached = self._cached(api_url, authorization, name)
            if cached is not None:
                return cached
            return self._resolve_uncached(transport, api_url, authorization, name)

    @staticmethod
    def _cached(
        api_url: str, authorization: str, name: str
    ) -> FunctionResolution | None:
        cached = lookup(api_url, authorization, name)
        if cached is None:
            return None
        if cached.resolution is None:
            raise NotFoundError(
                cached.message,
                status=HTTP_NOT_FOUND,
                code=cached.code,
                retry_after=cached.retry_after,
            )
        return cached.resolution

    def _resolve_uncached(
        self,
        transport: FunctionsTransport,
        api_url: str,
        authorization: str,
        name: str,
    ) -> FunctionResolution:
        resolved = invoke(
            transport.resolve_function_for_invocation,
            authorization=authorization,
            name=name,
        )
        try:
            payload: object = response_payload(resolved, HTTP_SUCCESS_MIN)
        except NotFoundError as error:
            store_missing(api_url, authorization, name, error)
            raise
        resolution = self._resolution(payload, api_url)
        store(api_url, authorization, name, resolution, self._cache_ttl(payload))
        return resolution

    @staticmethod
    def _resolution(payload: object, api_url: str) -> FunctionResolution:
        if not isinstance(payload, Mapping):
            raise TypeError(INVALID_FUNCTION_RESPONSE)
        values = cast("Mapping[str, object]", payload)
        function_id = values.get("function_id")
        if not isinstance(function_id, str) or not function_id:
            raise TypeError(INVALID_FUNCTION_RESPONSE)
        # Absent when the deployment serves no public invocation domain, as in
        # local development; the function is reached through the API instead.
        return FunctionResolution(
            function_id=function_id,
            invoke_url=valid_invoke_url(values.get("invoke_url"), api_url),
        )

    @staticmethod
    def _cache_ttl(payload: object) -> float:
        values = cast("Mapping[str, object]", payload)
        ttl = values.get("cache_ttl_seconds")
        if not isinstance(ttl, int) or isinstance(ttl, bool) or ttl <= 0:
            raise TypeError(INVALID_FUNCTION_RESPONSE)
        return float(ttl)

    @staticmethod
    def _response(response: TransportResponse) -> FunctionResponse:
        status = int(response.status_code)
        version = header(response.headers, FUNCTION_VERSION_HEADER)
        # A non-2xx the platform produced never reached the function, so it is
        # an SDK error rather than the function's answer. That turns on the
        # dispatch marker, not on the version stamp, which every response
        # carries — keying on the stamp would classify every platform failure
        # as though the function had returned it.
        dispatched = header(response.headers, FUNCTION_INVOKED_HEADER) is not None
        if status not in HTTP_SUCCESS_STATUSES and not dispatched:
            _ = response_payload(response, HTTP_SUCCESS_MIN)
        headers = {} if response.headers is None else dict(response.headers)
        return FunctionResponse(
            data=function_data(response),
            status=status,
            headers=headers,
            version=version,
        )
