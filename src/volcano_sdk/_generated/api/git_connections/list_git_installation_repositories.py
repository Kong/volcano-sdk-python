from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.git_repositories_response import GitRepositoriesResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    connection_id: UUID,
    installation_id: int,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/git/connections/{connection_id}/installations/{installation_id}/repositories".format(connection_id=quote(str(connection_id), safe=""),installation_id=quote(str(installation_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | GitRepositoriesResponse | None:
    if response.status_code == 200:
        response_200 = GitRepositoriesResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | GitRepositoriesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connection_id: UUID,
    installation_id: int,
    *,
    client: AuthenticatedClient,

) -> Response[Error | GitRepositoriesResponse]:
    """ List repos accessible to a connection through an installation

     Live proxy to GitHub: lists the repos the connection's stored user
    token can access through installationId. Nothing is persisted by this
    call.

    Args:
        connection_id (UUID):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitRepositoriesResponse]
     """


    kwargs = _get_kwargs(
        connection_id=connection_id,
installation_id=installation_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    connection_id: UUID,
    installation_id: int,
    *,
    client: AuthenticatedClient,

) -> Error | GitRepositoriesResponse | None:
    """ List repos accessible to a connection through an installation

     Live proxy to GitHub: lists the repos the connection's stored user
    token can access through installationId. Nothing is persisted by this
    call.

    Args:
        connection_id (UUID):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitRepositoriesResponse
     """


    return sync_detailed(
        connection_id=connection_id,
installation_id=installation_id,
client=client,

    ).parsed

async def asyncio_detailed(
    connection_id: UUID,
    installation_id: int,
    *,
    client: AuthenticatedClient,

) -> Response[Error | GitRepositoriesResponse]:
    """ List repos accessible to a connection through an installation

     Live proxy to GitHub: lists the repos the connection's stored user
    token can access through installationId. Nothing is persisted by this
    call.

    Args:
        connection_id (UUID):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitRepositoriesResponse]
     """


    kwargs = _get_kwargs(
        connection_id=connection_id,
installation_id=installation_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    connection_id: UUID,
    installation_id: int,
    *,
    client: AuthenticatedClient,

) -> Error | GitRepositoriesResponse | None:
    """ List repos accessible to a connection through an installation

     Live proxy to GitHub: lists the repos the connection's stored user
    token can access through installationId. Nothing is persisted by this
    call.

    Args:
        connection_id (UUID):
        installation_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitRepositoriesResponse
     """


    return (await asyncio_detailed(
        connection_id=connection_id,
installation_id=installation_id,
client=client,

    )).parsed
