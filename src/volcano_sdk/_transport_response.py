"""Validate generated requests and normalize HTTP responses."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import (
    TYPE_CHECKING,
    TypeGuard,
    overload,
)

import httpx

from ._transport_types import (
    ERROR_TYPES_BY_STATUS,
    HTTP_RATE_LIMITED,
    HTTP_SERVER_ERROR_MAX,
    HTTP_SERVER_ERROR_MIN,
    RETRY_AFTER_HEADER,
    GeneratedTransportResponse,
    JSONResponse,
    ModelPayload,
    P,
    ParsedHTTPResponse,
    RawHTTPResponse,
    T,
    TransportResponse,
    decode_json,
)
from .errors import (
    ServerError,
    TransportError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from ._generated.client import AuthenticatedClient
    from .models import JSONValue


@overload
def plain_json(value: Mapping[str, JSONValue]) -> dict[str, JSONValue]: ...


@overload
def plain_json(value: JSONValue) -> JSONValue: ...


def plain_json(value: JSONValue) -> JSONValue:
    if isinstance(value, Mapping):
        return {key: plain_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain_json(item) for item in value]
    return value


def invoke(operation: Callable[P, T], /, *args: P.args, **kwargs: P.kwargs) -> T:
    try:
        return operation(*args, **kwargs)
    except httpx.HTTPError as error:
        raise TransportError(str(error) or "Volcano transport failed") from error


async def invoke_async(
    operation: Callable[P, Awaitable[T]],
    /,
    *args: P.args,
    **kwargs: P.kwargs,
) -> T:
    try:
        return await operation(*args, **kwargs)
    except httpx.HTTPError as error:
        raise TransportError(str(error) or "Volcano transport failed") from error


def header(headers: Mapping[str, str] | None, name: str) -> str | None:
    if headers is None:
        return None
    for key, value in headers.items():
        if key.lower() == name.lower():
            return value
    return None


def error_type(status: int) -> type[VolcanoError]:
    error_type = ERROR_TYPES_BY_STATUS.get(status)
    if error_type is not None:
        return error_type
    if HTTP_SERVER_ERROR_MIN <= status <= HTTP_SERVER_ERROR_MAX:
        return ServerError
    return VolcanoError


class InvalidGeneratedRequestError(TypeError):
    def __init__(self, field: str) -> None:
        super().__init__(f"Invalid generated request field: {field}")


def required_request_string(kwargs: Mapping[str, object], key: str) -> str:
    value = kwargs.get(key)
    if not isinstance(value, str):
        raise InvalidGeneratedRequestError(key)
    return value


def is_object_mapping(value: object) -> TypeGuard[Mapping[object, object]]:
    return isinstance(value, Mapping)


def is_object_dict(value: object) -> TypeGuard[dict[object, object]]:
    return isinstance(value, dict)


def request_headers(kwargs: Mapping[str, object]) -> dict[str, str]:
    raw_headers = kwargs.get("headers", {})
    if not is_object_mapping(raw_headers):
        field = "headers"
        raise InvalidGeneratedRequestError(field)
    headers: dict[str, str] = {}
    for key, value in raw_headers.items():
        if not isinstance(key, str) or not isinstance(value, str):
            field = "headers"
            raise InvalidGeneratedRequestError(field)
        headers[key] = value
    return headers


def request_params(
    kwargs: Mapping[str, object],
) -> dict[str, str | int | float | bool | None] | None:
    raw_params = kwargs.get("params")
    if raw_params is None:
        return None
    if not is_object_mapping(raw_params):
        field = "params"
        raise InvalidGeneratedRequestError(field)
    params: dict[str, str | int | float | bool | None] = {}
    for key, value in raw_params.items():
        if not isinstance(key, str) or (
            value is not None and not isinstance(value, (str, int, float, bool))
        ):
            field = "params"
            raise InvalidGeneratedRequestError(field)
        params[key] = value
    return params


def generated_request(
    client: AuthenticatedClient, kwargs: Mapping[str, object]
) -> httpx.Response:
    if kwargs.keys() - {"method", "url", "headers", "json", "params"}:
        field = "unsupported field"
        raise InvalidGeneratedRequestError(field)
    return client.get_httpx_client().request(
        method=required_request_string(kwargs, "method"),
        url=required_request_string(kwargs, "url"),
        headers=request_headers(kwargs),
        params=request_params(kwargs),
        json=kwargs.get("json"),
    )


def json_object(response: JSONResponse) -> dict[str, object]:
    raw = response.json()
    if not is_object_dict(raw):
        field = "response body"
        raise InvalidGeneratedRequestError(field)
    payload: dict[str, object] = {}
    for key, value in raw.items():
        if not isinstance(key, str):
            field = "response body key"
            raise InvalidGeneratedRequestError(field)
        payload[key] = value
    return payload


def response_payload(response: TransportResponse, expected_status: int) -> object:
    status = int(response.status_code)
    if status != expected_status:
        payload: Mapping[object, object]
        raw_payload = response.payload
        payload = raw_payload if is_object_dict(raw_payload) else {}
        message = str(
            payload.get("error") or payload.get("message") or "Volcano request failed"
        )
        code_value = payload.get("code")
        code = str(code_value) if code_value is not None else None
        retry_after = None
        if status == HTTP_RATE_LIMITED:
            retry_after_value = header(response.headers, RETRY_AFTER_HEADER)
            try:
                retry_after = (
                    int(retry_after_value) if retry_after_value is not None else None
                )
            except ValueError:
                retry_after = None
        raise error_type(status)(
            message,
            status=status,
            code=code,
            retry_after=retry_after,
        )
    return response.payload


def parsed_response(response: ParsedHTTPResponse) -> TransportResponse:
    parsed = response.parsed
    if isinstance(parsed, ModelPayload):
        payload: object = parsed.to_dict()
    elif parsed is not None:
        payload = parsed
    else:
        try:
            raw = decode_json(response.content)
            payload = raw
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = None
    return GeneratedTransportResponse(
        status_code=int(response.status_code),
        payload=payload,
        content=response.content,
        headers=dict(response.headers),
    )


def unparsed_response(response: RawHTTPResponse) -> TransportResponse:
    try:
        payload = decode_json(response.content)
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = None
    return GeneratedTransportResponse(
        status_code=response.status_code,
        payload=payload,
        content=response.content,
        headers=dict(response.headers),
    )
