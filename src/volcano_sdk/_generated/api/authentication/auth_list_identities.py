from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_identities_response import AuthIdentitiesResponse
from ...models.error import Error
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/user/identities",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthIdentitiesResponse | Error | None:
    if response.status_code == 200:
        response_200 = AuthIdentitiesResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthIdentitiesResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AuthIdentitiesResponse | Error]:
    """ List the current user's identities

     Returns every real email identity the account owns. An account can own
    multiple identities (for example a password identity plus one or more
    OAuth identities on different emails). Anonymous accounts have no real
    identity and return an empty list.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthIdentitiesResponse | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> AuthIdentitiesResponse | Error | None:
    """ List the current user's identities

     Returns every real email identity the account owns. An account can own
    multiple identities (for example a password identity plus one or more
    OAuth identities on different emails). Anonymous accounts have no real
    identity and return an empty list.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthIdentitiesResponse | Error
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AuthIdentitiesResponse | Error]:
    """ List the current user's identities

     Returns every real email identity the account owns. An account can own
    multiple identities (for example a password identity plus one or more
    OAuth identities on different emails). Anonymous accounts have no real
    identity and return an empty list.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthIdentitiesResponse | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> AuthIdentitiesResponse | Error | None:
    """ List the current user's identities

     Returns every real email identity the account owns. An account can own
    multiple identities (for example a password identity plus one or more
    OAuth identities on different emails). Anonymous accounts have no real
    identity and return an empty list.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthIdentitiesResponse | Error
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
