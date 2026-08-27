from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_device_verify_body import AuthDeviceVerifyBody
from ...models.auth_device_verify_response_200 import AuthDeviceVerifyResponse200
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: AuthDeviceVerifyBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/device/verify",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthDeviceVerifyResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthDeviceVerifyResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthDeviceVerifyResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthDeviceVerifyBody,

) -> Response[AuthDeviceVerifyResponse200 | Error]:
    """ Approve or deny a device code

     Browser-side endpoint for authenticated auth-users to approve (`approve`) or deny (`deny`) a
    `user_code`.

    Called by the verification page after the end user signs in. The grant is
    scoped to the project the auth-user token belongs to: approving a
    `user_code` issued for a different project returns `403`. This endpoint
    does not require managed auth to be enabled, so a custom verification page
    (hosted anywhere) can drive approval — it just needs an authenticated
    project auth-user access token and, for cross-origin browser calls, the
    page origin allowed in the project's auth CORS settings.

    Args:
        body (AuthDeviceVerifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthDeviceVerifyResponse200 | Error]
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
    body: AuthDeviceVerifyBody,

) -> AuthDeviceVerifyResponse200 | Error | None:
    """ Approve or deny a device code

     Browser-side endpoint for authenticated auth-users to approve (`approve`) or deny (`deny`) a
    `user_code`.

    Called by the verification page after the end user signs in. The grant is
    scoped to the project the auth-user token belongs to: approving a
    `user_code` issued for a different project returns `403`. This endpoint
    does not require managed auth to be enabled, so a custom verification page
    (hosted anywhere) can drive approval — it just needs an authenticated
    project auth-user access token and, for cross-origin browser calls, the
    page origin allowed in the project's auth CORS settings.

    Args:
        body (AuthDeviceVerifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthDeviceVerifyResponse200 | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthDeviceVerifyBody,

) -> Response[AuthDeviceVerifyResponse200 | Error]:
    """ Approve or deny a device code

     Browser-side endpoint for authenticated auth-users to approve (`approve`) or deny (`deny`) a
    `user_code`.

    Called by the verification page after the end user signs in. The grant is
    scoped to the project the auth-user token belongs to: approving a
    `user_code` issued for a different project returns `403`. This endpoint
    does not require managed auth to be enabled, so a custom verification page
    (hosted anywhere) can drive approval — it just needs an authenticated
    project auth-user access token and, for cross-origin browser calls, the
    page origin allowed in the project's auth CORS settings.

    Args:
        body (AuthDeviceVerifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthDeviceVerifyResponse200 | Error]
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
    body: AuthDeviceVerifyBody,

) -> AuthDeviceVerifyResponse200 | Error | None:
    """ Approve or deny a device code

     Browser-side endpoint for authenticated auth-users to approve (`approve`) or deny (`deny`) a
    `user_code`.

    Called by the verification page after the end user signs in. The grant is
    scoped to the project the auth-user token belongs to: approving a
    `user_code` issued for a different project returns `403`. This endpoint
    does not require managed auth to be enabled, so a custom verification page
    (hosted anywhere) can drive approval — it just needs an authenticated
    project auth-user access token and, for cross-origin browser calls, the
    page origin allowed in the project's auth CORS settings.

    Args:
        body (AuthDeviceVerifyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthDeviceVerifyResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
