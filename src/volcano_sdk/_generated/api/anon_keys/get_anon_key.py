from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.anon_key import AnonKey
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    key_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/anon-keys/{key_id}".format(id=quote(str(id), safe=""),key_id=quote(str(key_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AnonKey | Any | None:
    if response.status_code == 200:
        response_200 = AnonKey.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AnonKey | Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    key_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AnonKey | Any]:
    """ Get anon key

     Get details of a specific anon key

    Args:
        id (UUID):
        key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonKey | Any]
     """


    kwargs = _get_kwargs(
        id=id,
key_id=key_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    key_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AnonKey | Any | None:
    """ Get anon key

     Get details of a specific anon key

    Args:
        id (UUID):
        key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonKey | Any
     """


    return sync_detailed(
        id=id,
key_id=key_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    key_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AnonKey | Any]:
    """ Get anon key

     Get details of a specific anon key

    Args:
        id (UUID):
        key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AnonKey | Any]
     """


    kwargs = _get_kwargs(
        id=id,
key_id=key_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    key_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AnonKey | Any | None:
    """ Get anon key

     Get details of a specific anon key

    Args:
        id (UUID):
        key_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AnonKey | Any
     """


    return (await asyncio_detailed(
        id=id,
key_id=key_id,
client=client,

    )).parsed
