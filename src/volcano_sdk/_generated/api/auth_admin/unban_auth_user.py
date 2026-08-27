from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.unban_user_response import UnbanUserResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    user_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/auth/users/{user_id}/unban".format(id=quote(str(id), safe=""),user_id=quote(str(user_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | UnbanUserResponse | None:
    if response.status_code == 200:
        response_200 = UnbanUserResponse.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | UnbanUserResponse]:
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

) -> Response[Error | UnbanUserResponse]:
    """ Unban a user

     Removes a ban from a user, restoring their ability to sign in.
    The user's status is set back to 'active'.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UnbanUserResponse]
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

) -> Error | UnbanUserResponse | None:
    """ Unban a user

     Removes a ban from a user, restoring their ability to sign in.
    The user's status is set back to 'active'.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UnbanUserResponse
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

) -> Response[Error | UnbanUserResponse]:
    """ Unban a user

     Removes a ban from a user, restoring their ability to sign in.
    The user's status is set back to 'active'.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UnbanUserResponse]
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

) -> Error | UnbanUserResponse | None:
    """ Unban a user

     Removes a ban from a user, restoring their ability to sign in.
    The user's status is set back to 'active'.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UnbanUserResponse
     """


    return (await asyncio_detailed(
        id=id,
user_id=user_id,
client=client,

    )).parsed
