"""Serverless function invocation facade."""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol, cast

from . import _function_resolution
from ._function_resolution import FunctionResolution
from ._transport import TransportResponse, invoke, response_payload
from .errors import NotFoundError
from .models import FunctionResponse, JSONValue

if TYPE_CHECKING:
    from .client import VolcanoClient

_FUNCTION_NAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")
_INVALID_FUNCTION_NAME = (
    "Function name must be DNS-safe: lowercase letters, numbers, and hyphens; "
    "1-63 characters"
)
_INVALID_FUNCTION_RESPONSE = "Expected a complete function response"
_INVALID_FUNCTION_PAYLOAD = "Function payload must be a mapping"
_UNKNOWN_FUNCTION = "Function was not found"
_HTTP_SUCCESS_MIN = 200
_HTTP_SUCCESS_MAX = 300
_HTTP_NOT_FOUND = 404


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


class Functions:
    """Invoke deployed Volcano functions by name."""

    def __init__(self, client: VolcanoClient) -> None:
        """Bind function calls to a Volcano client."""
        self._client = client

    def invoke(
        self,
        name: str,
        payload: Mapping[str, JSONValue] | None = None,
    ) -> FunctionResponse:
        """Resolve and invoke a function with an optional JSON object payload."""
        name = _function_name(name)
        request_payload = _function_payload(payload)
        authorization = self._client._function_token()
        transport = cast("FunctionsTransport", self._client._transport)
        resolution = self._resolve(transport, authorization, name)
        response = self._invoke_resolved(
            transport, authorization, resolution, request_payload
        )
        if _stale_mapping(response):
            # The function was deleted and recreated, so the cached identity no
            # longer exists. Resolve again before giving up.
            _function_resolution.forget(
                self._client._api_base_url(), authorization, name
            )
            resolution = self._resolve(transport, authorization, name)
            response = self._invoke_resolved(
                transport, authorization, resolution, request_payload
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
        return cast("TransportResponse", response)

    def _resolve(
        self,
        transport: FunctionsTransport,
        authorization: str,
        name: str,
    ) -> FunctionResolution:
        """Return the function's identity, reusing a live cached resolution."""
        api_url = self._client._api_base_url()
        cached = _function_resolution.lookup(api_url, authorization, name)
        if cached is not None:
            if cached.resolution is None:
                raise NotFoundError(_UNKNOWN_FUNCTION, status=_HTTP_NOT_FOUND)
            return cached.resolution

        resolved = invoke(
            transport.resolve_function_for_invocation,
            authorization=authorization,
            name=name,
        )
        if int(resolved.status_code) == _HTTP_NOT_FOUND:
            _function_resolution.store_missing(api_url, authorization, name)
        payload = response_payload(resolved, _HTTP_SUCCESS_MIN)
        resolution = self._resolution(payload)
        _function_resolution.store(
            api_url, authorization, name, resolution, self._cache_ttl(payload)
        )
        return resolution

    @staticmethod
    def _resolution(payload: object) -> FunctionResolution:
        if not isinstance(payload, Mapping):
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        values = cast("Mapping[str, object]", payload)
        function_id = values.get("function_id")
        if not isinstance(function_id, str) or not function_id:
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        # Absent when the deployment serves no public invocation domain, as in
        # local development; the function is reached through the API instead.
        return FunctionResolution(
            function_id=function_id,
            invoke_url=_function_resolution.valid_invoke_url(values.get("invoke_url")),
        )

    @staticmethod
    def _cache_ttl(payload: object) -> float:
        values = cast("Mapping[str, object]", payload)
        ttl = values.get("cache_ttl_seconds")
        if not isinstance(ttl, int) or isinstance(ttl, bool) or ttl <= 0:
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        return float(ttl)

    @staticmethod
    def _response(response: TransportResponse) -> FunctionResponse:
        status = int(response.status_code)
        version = _header(response.headers, "X-Volcano-Version")
        if not _HTTP_SUCCESS_MIN <= status < _HTTP_SUCCESS_MAX and version is None:
            response_payload(response, _HTTP_SUCCESS_MIN)
        headers = {} if response.headers is None else dict(response.headers)
        return FunctionResponse(
            data=_function_data(response),
            status=status,
            headers=headers,
            version=version,
        )


def _stale_mapping(response: TransportResponse) -> bool:
    """Report a platform 404, which means the cached function identity is gone.

    A function that answers 404 itself carries the version header, and its
    response must be returned rather than retried: invoking twice would run
    the caller's side effects twice.
    """
    return (
        int(response.status_code) == _HTTP_NOT_FOUND
        and _header(response.headers, "X-Volcano-Version") is None
    )


def _function_data(response: TransportResponse) -> JSONValue:
    if not response.content:
        return cast("JSONValue", response.payload)
    text = response.content.decode("utf-8-sig", errors="replace")
    if not text:
        return None
    content_type = (_header(response.headers, "Content-Type") or "").lower()
    if "application/json" in content_type or text.startswith(("{", "[")):
        try:
            return cast(
                "JSONValue", json.loads(text, parse_constant=_reject_json_constant)
            )
        except ValueError:
            pass
    return text


def _reject_json_constant(value: str) -> None:
    raise ValueError(value)


def _header(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is None:
        return None
    for key, value in headers.items():
        if key.casefold() == name.casefold():
            return value
    return None


def _function_name(value: object) -> str:
    if not isinstance(value, str) or _FUNCTION_NAME.fullmatch(value) is None:
        raise ValueError(_INVALID_FUNCTION_NAME)
    return value


def _function_payload(value: object) -> dict[str, JSONValue]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise TypeError(_INVALID_FUNCTION_PAYLOAD)
    return dict(cast("Mapping[str, JSONValue]", value))
