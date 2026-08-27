from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_refresh_body import AuthRefreshBody
from ...models.auth_token_response import AuthTokenResponse
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: AuthRefreshBody | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/refresh",
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthTokenResponse | Error | None:
    if response.status_code == 200:
        response_200 = AuthTokenResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthTokenResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthRefreshBody | Unset = UNSET,

) -> Response[AuthTokenResponse | Error]:
    """ Refresh access token

     Get a new access token using a refresh token. Requires an anon key.

    Send `refresh_token` in the body for the default flow. An eligible
    cookie-mode browser request may instead send `session_mode: cookie`
    with an empty token or omit the request body; the API reads and resets
    the project's HttpOnly cookie and omits `refresh_token` from the
    response.

    Args:
        body (AuthRefreshBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokenResponse | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: AuthRefreshBody | Unset = UNSET,

) -> AuthTokenResponse | Error | None:
    """ Refresh access token

     Get a new access token using a refresh token. Requires an anon key.

    Send `refresh_token` in the body for the default flow. An eligible
    cookie-mode browser request may instead send `session_mode: cookie`
    with an empty token or omit the request body; the API reads and resets
    the project's HttpOnly cookie and omits `refresh_token` from the
    response.

    Args:
        body (AuthRefreshBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokenResponse | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthRefreshBody | Unset = UNSET,

) -> Response[AuthTokenResponse | Error]:
    """ Refresh access token

     Get a new access token using a refresh token. Requires an anon key.

    Send `refresh_token` in the body for the default flow. An eligible
    cookie-mode browser request may instead send `session_mode: cookie`
    with an empty token or omit the request body; the API reads and resets
    the project's HttpOnly cookie and omits `refresh_token` from the
    response.

    Args:
        body (AuthRefreshBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokenResponse | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthRefreshBody | Unset = UNSET,

) -> AuthTokenResponse | Error | None:
    """ Refresh access token

     Get a new access token using a refresh token. Requires an anon key.

    Send `refresh_token` in the body for the default flow. An eligible
    cookie-mode browser request may instead send `session_mode: cookie`
    with an empty token or omit the request body; the API reads and resets
    the project's HttpOnly cookie and omits `refresh_token` from the
    response.

    Args:
        body (AuthRefreshBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokenResponse | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
