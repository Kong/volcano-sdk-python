from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.refresh_o_auth_provider_token_provider import check_refresh_o_auth_provider_token_provider
from ...models.refresh_o_auth_provider_token_provider import RefreshOAuthProviderTokenProvider
from ...models.refresh_o_auth_provider_token_response_200 import RefreshOAuthProviderTokenResponse200
from typing import cast



def _get_kwargs(
    provider: RefreshOAuthProviderTokenProvider,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/oauth/{provider}/refresh-token".format(provider=quote(str(provider), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | RefreshOAuthProviderTokenResponse200 | None:
    if response.status_code == 200:
        response_200 = RefreshOAuthProviderTokenResponse200.from_dict(response.json())



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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | RefreshOAuthProviderTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: RefreshOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Error | RefreshOAuthProviderTokenResponse200]:
    """ Refresh OAuth provider token

     Refresh the access token for an OAuth provider using its refresh token.
    Allows calling provider APIs on user's behalf (e.g., Google Drive, GitHub repos).

    Args:
        provider (RefreshOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RefreshOAuthProviderTokenResponse200]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: RefreshOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Error | RefreshOAuthProviderTokenResponse200 | None:
    """ Refresh OAuth provider token

     Refresh the access token for an OAuth provider using its refresh token.
    Allows calling provider APIs on user's behalf (e.g., Google Drive, GitHub repos).

    Args:
        provider (RefreshOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RefreshOAuthProviderTokenResponse200
     """


    return sync_detailed(
        provider=provider,
client=client,

    ).parsed

async def asyncio_detailed(
    provider: RefreshOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Error | RefreshOAuthProviderTokenResponse200]:
    """ Refresh OAuth provider token

     Refresh the access token for an OAuth provider using its refresh token.
    Allows calling provider APIs on user's behalf (e.g., Google Drive, GitHub repos).

    Args:
        provider (RefreshOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RefreshOAuthProviderTokenResponse200]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: RefreshOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Error | RefreshOAuthProviderTokenResponse200 | None:
    """ Refresh OAuth provider token

     Refresh the access token for an OAuth provider using its refresh token.
    Allows calling provider APIs on user's behalf (e.g., Google Drive, GitHub repos).

    Args:
        provider (RefreshOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RefreshOAuthProviderTokenResponse200
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,

    )).parsed
