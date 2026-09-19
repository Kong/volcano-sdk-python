from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    if_none_match: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(if_none_match, Unset):
        headers["If-None-Match"] = if_none_match



    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/openapi.yaml",
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 304:
        response_304 = cast(Any, None)
        return response_304

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    if_none_match: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ Fetch the OpenAPI specification as YAML

     The same document as `/openapi.json`, serialized as YAML for tools that
    prefer it. See that operation for caching and authentication notes.

    Args:
        if_none_match (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        if_none_match=if_none_match,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    if_none_match: str | Unset = UNSET,

) -> Any | Error | None:
    """ Fetch the OpenAPI specification as YAML

     The same document as `/openapi.json`, serialized as YAML for tools that
    prefer it. See that operation for caching and authentication notes.

    Args:
        if_none_match (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,
if_none_match=if_none_match,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    if_none_match: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ Fetch the OpenAPI specification as YAML

     The same document as `/openapi.json`, serialized as YAML for tools that
    prefer it. See that operation for caching and authentication notes.

    Args:
        if_none_match (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        if_none_match=if_none_match,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    if_none_match: str | Unset = UNSET,

) -> Any | Error | None:
    """ Fetch the OpenAPI specification as YAML

     The same document as `/openapi.json`, serialized as YAML for tools that
    prefer it. See that operation for caching and authentication notes.

    Args:
        if_none_match (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,
if_none_match=if_none_match,

    )).parsed
