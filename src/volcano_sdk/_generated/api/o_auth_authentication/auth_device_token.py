from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_device_token_body import AuthDeviceTokenBody
from ...models.auth_token_response import AuthTokenResponse
from ...models.o_auth_error_response import OAuthErrorResponse
from typing import cast



def _get_kwargs(
    *,
    body: AuthDeviceTokenBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/device/token",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthTokenResponse | OAuthErrorResponse | None:
    if response.status_code == 200:
        response_200 = AuthTokenResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = OAuthErrorResponse.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = OAuthErrorResponse.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthTokenResponse | OAuthErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthDeviceTokenBody,

) -> Response[AuthTokenResponse | OAuthErrorResponse]:
    """ Poll device token endpoint

     RFC8628 token polling endpoint.
    Returns OAuth errors such as `authorization_pending`, `slow_down`, `access_denied`, and
    `expired_token`.

    Args:
        body (AuthDeviceTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokenResponse | OAuthErrorResponse]
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
    client: AuthenticatedClient | Client,
    body: AuthDeviceTokenBody,

) -> AuthTokenResponse | OAuthErrorResponse | None:
    """ Poll device token endpoint

     RFC8628 token polling endpoint.
    Returns OAuth errors such as `authorization_pending`, `slow_down`, `access_denied`, and
    `expired_token`.

    Args:
        body (AuthDeviceTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokenResponse | OAuthErrorResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthDeviceTokenBody,

) -> Response[AuthTokenResponse | OAuthErrorResponse]:
    """ Poll device token endpoint

     RFC8628 token polling endpoint.
    Returns OAuth errors such as `authorization_pending`, `slow_down`, `access_denied`, and
    `expired_token`.

    Args:
        body (AuthDeviceTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthTokenResponse | OAuthErrorResponse]
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
    client: AuthenticatedClient | Client,
    body: AuthDeviceTokenBody,

) -> AuthTokenResponse | OAuthErrorResponse | None:
    """ Poll device token endpoint

     RFC8628 token polling endpoint.
    Returns OAuth errors such as `authorization_pending`, `slow_down`, `access_denied`, and
    `expired_token`.

    Args:
        body (AuthDeviceTokenBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthTokenResponse | OAuthErrorResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
