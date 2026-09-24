from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from uuid import UUID



def request_kwargs(
    id: UUID | str,
    user_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/auth/users/{user_id}/sessions".format(id=quote(str(id), safe=""),user_id=quote(str(user_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 204:
        return None

    if response.status_code == 404:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    user_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any]:
    """ Delete all user sessions

     Revokes all sessions for a user, forcing them to re-authenticate on all devices.
    Use this to log out a user from everywhere.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = request_kwargs(
        id=id,
user_id=user_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)


async def asyncio_detailed(
    id: UUID | str,
    user_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any]:
    """ Delete all user sessions

     Revokes all sessions for a user, forcing them to re-authenticate on all devices.
    Use this to log out a user from everywhere.

    Args:
        id (UUID):
        user_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = request_kwargs(
        id=id,
user_id=user_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

