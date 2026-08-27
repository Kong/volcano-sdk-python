from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function import Function
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    function_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/functions/{function_id}".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Function | None:
    if response.status_code == 200:
        response_200 = Function.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Function]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | Function]:
    """ Get function by ID

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Function]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | Function | None:
    """ Get function by ID

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Function
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | Function]:
    """ Get function by ID

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Function]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | Function | None:
    """ Get function by ID

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Function
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,

    )).parsed
