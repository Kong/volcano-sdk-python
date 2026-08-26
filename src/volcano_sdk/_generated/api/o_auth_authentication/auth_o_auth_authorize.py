from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_o_auth_authorize_provider import AuthOAuthAuthorizeProvider
from ...models.auth_o_auth_authorize_provider import check_auth_o_auth_authorize_provider
from ...models.auth_o_auth_authorize_response_mode import AuthOAuthAuthorizeResponseMode
from ...models.auth_o_auth_authorize_response_mode import check_auth_o_auth_authorize_response_mode
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    provider: AuthOAuthAuthorizeProvider,
    *,
    anon_key: str,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthOAuthAuthorizeResponseMode | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["anon_key"] = anon_key

    params["redirect_url"] = redirect_url

    params["client_state"] = client_state

    json_response_mode: str | Unset = UNSET
    if not isinstance(response_mode, Unset):
        json_response_mode = response_mode

    params["response_mode"] = json_response_mode


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/oauth/{provider}/authorize".format(provider=quote(str(provider), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | None:
    if response.status_code == 307:
        return None

    if response.status_code == 400:
        return None

    if response.status_code == 404:
        return None

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: AuthOAuthAuthorizeProvider,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthOAuthAuthorizeResponseMode | Unset = UNSET,

) -> Response[Any]:
    """ Start OAuth authorization

     Redirects user to OAuth provider for authorization.
    Handles CSRF protection with state parameter.
    Project is identified via the anon_key query parameter.

    Args:
        provider (AuthOAuthAuthorizeProvider):
        anon_key (str):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthOAuthAuthorizeResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        provider=provider,
anon_key=anon_key,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    provider: AuthOAuthAuthorizeProvider,
    *,
    client: AuthenticatedClient | Client,
    anon_key: str,
    redirect_url: str | Unset = UNSET,
    client_state: str | Unset = UNSET,
    response_mode: AuthOAuthAuthorizeResponseMode | Unset = UNSET,

) -> Response[Any]:
    """ Start OAuth authorization

     Redirects user to OAuth provider for authorization.
    Handles CSRF protection with state parameter.
    Project is identified via the anon_key query parameter.

    Args:
        provider (AuthOAuthAuthorizeProvider):
        anon_key (str):
        redirect_url (str | Unset):
        client_state (str | Unset):
        response_mode (AuthOAuthAuthorizeResponseMode | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
     """


    kwargs = _get_kwargs(
        provider=provider,
anon_key=anon_key,
redirect_url=redirect_url,
client_state=client_state,
response_mode=response_mode,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

