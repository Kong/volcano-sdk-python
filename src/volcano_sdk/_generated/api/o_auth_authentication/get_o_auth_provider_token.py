from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_o_auth_provider_token_provider import check_get_o_auth_provider_token_provider
from ...models.get_o_auth_provider_token_provider import GetOAuthProviderTokenProvider
from ...models.get_o_auth_provider_token_response_200 import GetOAuthProviderTokenResponse200
from typing import cast



def _get_kwargs(
    provider: GetOAuthProviderTokenProvider,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/oauth/{provider}/token".format(provider=quote(str(provider), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | GetOAuthProviderTokenResponse200 | None:
    if response.status_code == 200:
        response_200 = GetOAuthProviderTokenResponse200.from_dict(response.json())



        return response_200

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | GetOAuthProviderTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: GetOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Error | GetOAuthProviderTokenResponse200]:
    """ Get current provider access token

     Get valid access token for OAuth provider.
    Automatically refreshes if expired.

    Args:
        provider (GetOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetOAuthProviderTokenResponse200]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: GetOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Error | GetOAuthProviderTokenResponse200 | None:
    """ Get current provider access token

     Get valid access token for OAuth provider.
    Automatically refreshes if expired.

    Args:
        provider (GetOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetOAuthProviderTokenResponse200
     """


    return sync_detailed(
        provider=provider,
client=client,

    ).parsed

async def asyncio_detailed(
    provider: GetOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Response[Error | GetOAuthProviderTokenResponse200]:
    """ Get current provider access token

     Get valid access token for OAuth provider.
    Automatically refreshes if expired.

    Args:
        provider (GetOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GetOAuthProviderTokenResponse200]
     """


    kwargs = _get_kwargs(
        provider=provider,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: GetOAuthProviderTokenProvider,
    *,
    client: AuthenticatedClient,

) -> Error | GetOAuthProviderTokenResponse200 | None:
    """ Get current provider access token

     Get valid access token for OAuth provider.
    Automatically refreshes if expired.

    Args:
        provider (GetOAuthProviderTokenProvider):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GetOAuthProviderTokenResponse200
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,

    )).parsed
