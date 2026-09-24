from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_access_token import ProjectAccessToken
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    token_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/access-tokens/{token_id}".format(id=quote(str(id), safe=""),token_id=quote(str(token_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectAccessToken | None:
    if response.status_code == 200:
        response_200 = ProjectAccessToken.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectAccessToken]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectAccessToken]:
    """ Get a project access token

     Returns one token's metadata. Never its secret, which is not stored in a
    recoverable form.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectAccessToken]
     """


    kwargs = _get_kwargs(
        id=id,
token_id=token_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectAccessToken | None:
    """ Get a project access token

     Returns one token's metadata. Never its secret, which is not stored in a
    recoverable form.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectAccessToken
     """


    return sync_detailed(
        id=id,
token_id=token_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectAccessToken]:
    """ Get a project access token

     Returns one token's metadata. Never its secret, which is not stored in a
    recoverable form.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectAccessToken]
     """


    kwargs = _get_kwargs(
        id=id,
token_id=token_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectAccessToken | None:
    """ Get a project access token

     Returns one token's metadata. Never its secret, which is not stored in a
    recoverable form.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectAccessToken
     """


    return (await asyncio_detailed(
        id=id,
token_id=token_id,
client=client,

    )).parsed
