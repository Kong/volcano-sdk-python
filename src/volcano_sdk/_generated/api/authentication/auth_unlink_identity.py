from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    identity_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/auth/user/identities/{identity_id}".format(identity_id=quote(str(identity_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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
    identity_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Unlink an identity from the current user

     Removes a non-primary identity and its attached sign-in methods. Refused
    when the identity is the account's primary, its only identity, or when
    removing it would leave the account with no way to sign in.

    Args:
        identity_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        identity_id=identity_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    identity_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Unlink an identity from the current user

     Removes a non-primary identity and its attached sign-in methods. Refused
    when the identity is the account's primary, its only identity, or when
    removing it would leave the account with no way to sign in.

    Args:
        identity_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        identity_id=identity_id,
client=client,

    ).parsed

async def asyncio_detailed(
    identity_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Unlink an identity from the current user

     Removes a non-primary identity and its attached sign-in methods. Refused
    when the identity is the account's primary, its only identity, or when
    removing it would leave the account with no way to sign in.

    Args:
        identity_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        identity_id=identity_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    identity_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Unlink an identity from the current user

     Removes a non-primary identity and its attached sign-in methods. Refused
    when the identity is the account's primary, its only identity, or when
    removing it would leave the account with no way to sign in.

    Args:
        identity_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        identity_id=identity_id,
client=client,

    )).parsed
