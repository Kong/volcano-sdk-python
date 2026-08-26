from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.ban_auth_user_body import BanAuthUserBody
from ...models.ban_user_response import BanUserResponse
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    user_id: UUID,
    *,
    body: BanAuthUserBody | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/auth/users/{user_id}/ban".format(id=quote(str(id), safe=""),user_id=quote(str(user_id), safe=""),),
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BanUserResponse | Error | None:
    if response.status_code == 200:
        response_200 = BanUserResponse.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BanUserResponse | Error]:
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
    body: BanAuthUserBody | Unset = UNSET,

) -> Response[BanUserResponse | Error]:
    """ Ban a user

     Bans a user temporarily or permanently. Banned users cannot sign in
    and all their active sessions are immediately revoked.

    - Omit `banned_until` for a permanent ban
    - Provide `banned_until` ISO timestamp for a temporary ban

    Args:
        id (UUID):
        user_id (UUID):
        body (BanAuthUserBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BanUserResponse | Error]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
body=body,

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
    body: BanAuthUserBody | Unset = UNSET,

) -> BanUserResponse | Error | None:
    """ Ban a user

     Bans a user temporarily or permanently. Banned users cannot sign in
    and all their active sessions are immediately revoked.

    - Omit `banned_until` for a permanent ban
    - Provide `banned_until` ISO timestamp for a temporary ban

    Args:
        id (UUID):
        user_id (UUID):
        body (BanAuthUserBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BanUserResponse | Error
     """


    return sync_detailed(
        id=id,
user_id=user_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    body: BanAuthUserBody | Unset = UNSET,

) -> Response[BanUserResponse | Error]:
    """ Ban a user

     Bans a user temporarily or permanently. Banned users cannot sign in
    and all their active sessions are immediately revoked.

    - Omit `banned_until` for a permanent ban
    - Provide `banned_until` ISO timestamp for a temporary ban

    Args:
        id (UUID):
        user_id (UUID):
        body (BanAuthUserBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BanUserResponse | Error]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
body=body,

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
    body: BanAuthUserBody | Unset = UNSET,

) -> BanUserResponse | Error | None:
    """ Ban a user

     Bans a user temporarily or permanently. Banned users cannot sign in
    and all their active sessions are immediately revoked.

    - Omit `banned_until` for a permanent ban
    - Provide `banned_until` ISO timestamp for a temporary ban

    Args:
        id (UUID):
        user_id (UUID):
        body (BanAuthUserBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BanUserResponse | Error
     """


    return (await asyncio_detailed(
        id=id,
user_id=user_id,
client=client,
body=body,

    )).parsed
