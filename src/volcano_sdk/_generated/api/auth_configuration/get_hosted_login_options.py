from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hosted_login_options_response import HostedLoginOptionsResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    anon_key: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["anon_key"] = anon_key


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/hosted/login/options".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | HostedLoginOptionsResponse | None:
    if response.status_code == 200:
        response_200 = HostedLoginOptionsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | HostedLoginOptionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,

) -> Response[Any | HostedLoginOptionsResponse]:
    """ Get hosted login runtime options

     Returns runtime options for the built-in managed login flow.
    Requires `anon_key` query parameter.
    Rate limited per project and client IP. Excess requests return `429` and `Retry-After`.

    Args:
        id (UUID):
        anon_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HostedLoginOptionsResponse]
     """


    kwargs = _get_kwargs(
        id=id,
anon_key=anon_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,

) -> Any | HostedLoginOptionsResponse | None:
    """ Get hosted login runtime options

     Returns runtime options for the built-in managed login flow.
    Requires `anon_key` query parameter.
    Rate limited per project and client IP. Excess requests return `429` and `Retry-After`.

    Args:
        id (UUID):
        anon_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HostedLoginOptionsResponse
     """


    return sync_detailed(
        id=id,
client=client,
anon_key=anon_key,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,

) -> Response[Any | HostedLoginOptionsResponse]:
    """ Get hosted login runtime options

     Returns runtime options for the built-in managed login flow.
    Requires `anon_key` query parameter.
    Rate limited per project and client IP. Excess requests return `429` and `Retry-After`.

    Args:
        id (UUID):
        anon_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HostedLoginOptionsResponse]
     """


    kwargs = _get_kwargs(
        id=id,
anon_key=anon_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,

) -> Any | HostedLoginOptionsResponse | None:
    """ Get hosted login runtime options

     Returns runtime options for the built-in managed login flow.
    Requires `anon_key` query parameter.
    Rate limited per project and client IP. Excess requests return `429` and `Retry-After`.

    Args:
        id (UUID):
        anon_key (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HostedLoginOptionsResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
anon_key=anon_key,

    )).parsed
