from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_user import AuthUser
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    user_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/users/{user_id}".format(id=quote(str(id), safe=""),user_id=quote(str(user_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthUser | None:
    if response.status_code == 200:
        response_200 = AuthUser.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthUser]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AuthUser]:
    """ Get specific auth user (admin)

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthUser]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AuthUser | None:
    """ Get specific auth user (admin)

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthUser
     """


    return sync_detailed(
        id=id,
user_id=user_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AuthUser]:
    """ Get specific auth user (admin)

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthUser]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AuthUser | None:
    """ Get specific auth user (admin)

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthUser
     """


    return (await asyncio_detailed(
        id=id,
user_id=user_id,
client=client,

    )).parsed
