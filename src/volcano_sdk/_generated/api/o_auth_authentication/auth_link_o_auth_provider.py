from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_link_o_auth_provider_provider import AuthLinkOAuthProviderProvider
from ...models.auth_link_o_auth_provider_provider import check_auth_link_o_auth_provider_provider
from ...models.auth_link_o_auth_provider_response_200 import AuthLinkOAuthProviderResponse200
from ...models.auth_link_o_auth_provider_response_mode import AuthLinkOAuthProviderResponseMode
from ...models.auth_link_o_auth_provider_response_mode import check_auth_link_o_auth_provider_response_mode
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    provider: AuthLinkOAuthProviderProvider,
    *,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthLinkOAuthProviderResponseMode | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["redirect_url"] = redirect_url

    params["client_state"] = client_state

    json_response_mode: str | Unset = UNSET
    if not isinstance(response_mode, Unset):
        json_response_mode = response_mode

    params["response_mode"] = json_response_mode


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/oauth/{provider}/link".format(provider=quote(str(provider), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthLinkOAuthProviderResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthLinkOAuthProviderResponse200.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthLinkOAuthProviderResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: AuthLinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthLinkOAuthProviderResponseMode | Unset = UNSET,

) -> Response[AuthLinkOAuthProviderResponse200 | Error]:
    """ Link OAuth provider to current user

     Generates authorization URL to link OAuth provider to existing account.
    User must be authenticated.

    Args:
        provider (AuthLinkOAuthProviderProvider):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthLinkOAuthProviderResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthLinkOAuthProviderResponse200 | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: AuthLinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthLinkOAuthProviderResponseMode | Unset = UNSET,

) -> AuthLinkOAuthProviderResponse200 | Error | None:
    """ Link OAuth provider to current user

     Generates authorization URL to link OAuth provider to existing account.
    User must be authenticated.

    Args:
        provider (AuthLinkOAuthProviderProvider):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthLinkOAuthProviderResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthLinkOAuthProviderResponse200 | Error
     """


    return sync_detailed(
        provider=provider,
client=client,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    ).parsed

async def asyncio_detailed(
    provider: AuthLinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthLinkOAuthProviderResponseMode | Unset = UNSET,

) -> Response[AuthLinkOAuthProviderResponse200 | Error]:
    """ Link OAuth provider to current user

     Generates authorization URL to link OAuth provider to existing account.
    User must be authenticated.

    Args:
        provider (AuthLinkOAuthProviderProvider):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthLinkOAuthProviderResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthLinkOAuthProviderResponse200 | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: AuthLinkOAuthProviderProvider,
    *,
    client: AuthenticatedClient,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthLinkOAuthProviderResponseMode | Unset = UNSET,

) -> AuthLinkOAuthProviderResponse200 | Error | None:
    """ Link OAuth provider to current user

     Generates authorization URL to link OAuth provider to existing account.
    User must be authenticated.

    Args:
        provider (AuthLinkOAuthProviderProvider):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthLinkOAuthProviderResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthLinkOAuthProviderResponse200 | Error
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    )).parsed
