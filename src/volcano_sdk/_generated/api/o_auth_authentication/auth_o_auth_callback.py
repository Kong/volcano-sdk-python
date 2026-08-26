from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_o_auth_callback_provider import AuthOAuthCallbackProvider
from ...models.auth_o_auth_callback_provider import check_auth_o_auth_callback_provider
from ...models.auth_token_response import AuthTokenResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    provider: AuthOAuthCallbackProvider,
    *,
    code: str,
    state: str,
    error: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["code"] = code

    params["state"] = state

    params["error"] = error


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/oauth/{provider}/callback".format(provider=quote(str(provider), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthTokenResponse | None:
    if response.status_code == 200:
        response_200 = AuthTokenResponse.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = AuthTokenResponse.from_dict(response.json())



        return response_201

    if response.status_code == 303:
        response_303 = cast(Any, None)
        return response_303

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthTokenResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: AuthOAuthCallbackProvider,
    *,
    client: AuthenticatedClient | Client,
    code: str,
    state: str,
    error: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ OAuth callback handler

     Handles OAuth provider callback with authorization code.
    Exchanges code for tokens and creates/signs in user.

    Args:
        provider (AuthOAuthCallbackProvider):
        code (str):
        state (str):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
     """


    kwargs = _get_kwargs(
        provider=provider,
code=code,
state=state,
error=error,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: AuthOAuthCallbackProvider,
    *,
    client: AuthenticatedClient | Client,
    code: str,
    state: str,
    error: str | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ OAuth callback handler

     Handles OAuth provider callback with authorization code.
    Exchanges code for tokens and creates/signs in user.

    Args:
        provider (AuthOAuthCallbackProvider):
        code (str):
        state (str):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
     """


    return sync_detailed(
        provider=provider,
client=client,
code=code,
state=state,
error=error,

    ).parsed

async def asyncio_detailed(
    provider: AuthOAuthCallbackProvider,
    *,
    client: AuthenticatedClient | Client,
    code: str,
    state: str,
    error: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ OAuth callback handler

     Handles OAuth provider callback with authorization code.
    Exchanges code for tokens and creates/signs in user.

    Args:
        provider (AuthOAuthCallbackProvider):
        code (str):
        state (str):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
     """


    kwargs = _get_kwargs(
        provider=provider,
code=code,
state=state,
error=error,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: AuthOAuthCallbackProvider,
    *,
    client: AuthenticatedClient | Client,
    code: str,
    state: str,
    error: str | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ OAuth callback handler

     Handles OAuth provider callback with authorization code.
    Exchanges code for tokens and creates/signs in user.

    Args:
        provider (AuthOAuthCallbackProvider):
        code (str):
        state (str):
        error (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
code=code,
state=state,
error=error,

    )).parsed
