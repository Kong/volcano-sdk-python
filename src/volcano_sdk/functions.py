"""Serverless function invocation facade."""

from __future__ import annotations

import re
from collections.abc import Mapping
from http import HTTPStatus
from typing import TYPE_CHECKING, Protocol, cast

from ._transport import TransportResponse, invoke, response_payload
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
_HTTP_SUCCESS_MIN = 200
_HTTP_SUCCESS_MAX = 300


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
        resolved = invoke(
            transport.resolve_function_for_invocation,
            authorization=authorization,
            name=name,
        )
        function_id = self._function_id(response_payload(resolved, _HTTP_SUCCESS_MIN))
        response = invoke(
            transport.invoke_function,
            authorization=authorization,
            function_id=function_id,
            payload=request_payload,
        )
        return self._response(response)

    @staticmethod
    def _function_id(payload: object) -> str:
        if not isinstance(payload, Mapping):
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        values = cast("Mapping[str, object]", payload)
        function_id = values.get("function_id")
        if not isinstance(function_id, str) or not function_id:
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        return function_id

    @staticmethod
    def _response(response: TransportResponse) -> FunctionResponse:
        status = int(response.status_code)
        version = _header(response.headers, "X-Volcano-Version")
        if not _HTTP_SUCCESS_MIN <= status < _HTTP_SUCCESS_MAX and version is None:
            response_payload(response, _HTTP_SUCCESS_MIN)
        data = response.payload
        no_content = (
            status == HTTPStatus.NO_CONTENT and not response.content and data is None
        )
        if not isinstance(data, Mapping) and not no_content:
            raise TypeError(_INVALID_FUNCTION_RESPONSE)
        headers = {} if response.headers is None else dict(response.headers)
        return FunctionResponse(
            data=cast("Mapping[str, JSONValue] | None", data),
            status=status,
            headers=headers,
            version=version,
        )


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
