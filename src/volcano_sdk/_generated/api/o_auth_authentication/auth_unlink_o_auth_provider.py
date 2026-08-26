from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_unlink_o_auth_provider_provider import AuthUnlinkOAuthProviderProvider
from ...models.auth_unlink_o_auth_provider_provider import check_auth_unlink_o_auth_provider_provider
from ...models.error import Error
from typing import cast



def _get_kwargs(
    provider: AuthUnlinkOAuthProviderProvider,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/auth/oauth/{provider}/unlink".format(provider=quote(str(provider), safe=""),),
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
    provider: AuthUnlinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Unlink OAuth provider

     Remove OAuth provider from user's account.
    Cannot unlink if it's the only authentication method.

    Args:
        provider (AuthUnlinkOAuthProviderProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: AuthUnlinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Unlink OAuth provider

     Remove OAuth provider from user's account.
    Cannot unlink if it's the only authentication method.

    Args:
        provider (AuthUnlinkOAuthProviderProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        provider=provider,
client=client,

    ).parsed

async def asyncio_detailed(
    provider: AuthUnlinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Unlink OAuth provider

     Remove OAuth provider from user's account.
    Cannot unlink if it's the only authentication method.

    Args:
        provider (AuthUnlinkOAuthProviderProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: AuthUnlinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Unlink OAuth provider

     Remove OAuth provider from user's account.
    Cannot unlink if it's the only authentication method.

    Args:
        provider (AuthUnlinkOAuthProviderProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,

    )).parsed
