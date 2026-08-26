from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_platform_exchange_body import AuthPlatformExchangeBody
from ...models.error import Error
from ...models.platform_exchange_response import PlatformExchangeResponse
from typing import cast



def _get_kwargs(
    *,
    body: AuthPlatformExchangeBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/platform/exchange",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PlatformExchangeResponse | None:
    if response.status_code == 200:
        response_200 = PlatformExchangeResponse.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PlatformExchangeResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthPlatformExchangeBody,

) -> Response[Error | PlatformExchangeResponse]:
    """ Exchange auth-user device session for platform token

     Exchanges a verified auth-user device-flow session into a platform token for CLI usage.
    The target platform user is derived from authenticated auth-user mapping; client cannot select
    another user.

    Args:
        body (AuthPlatformExchangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PlatformExchangeResponse]
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
    body: AuthPlatformExchangeBody,

) -> Error | PlatformExchangeResponse | None:
    """ Exchange auth-user device session for platform token

     Exchanges a verified auth-user device-flow session into a platform token for CLI usage.
    The target platform user is derived from authenticated auth-user mapping; client cannot select
    another user.

    Args:
        body (AuthPlatformExchangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PlatformExchangeResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthPlatformExchangeBody,

) -> Response[Error | PlatformExchangeResponse]:
    """ Exchange auth-user device session for platform token

     Exchanges a verified auth-user device-flow session into a platform token for CLI usage.
    The target platform user is derived from authenticated auth-user mapping; client cannot select
    another user.

    Args:
        body (AuthPlatformExchangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PlatformExchangeResponse]
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
    body: AuthPlatformExchangeBody,

) -> Error | PlatformExchangeResponse | None:
    """ Exchange auth-user device session for platform token

     Exchanges a verified auth-user device-flow session into a platform token for CLI usage.
    The target platform user is derived from authenticated auth-user mapping; client cannot select
    another user.

    Args:
        body (AuthPlatformExchangeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PlatformExchangeResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
