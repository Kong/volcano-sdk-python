from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_reset_password_body import AuthResetPasswordBody
from ...models.auth_reset_password_response_200 import AuthResetPasswordResponse200
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    body: AuthResetPasswordBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_volcano_proxy_authorization, Unset):
        headers["X-Volcano-Proxy-Authorization"] = x_volcano_proxy_authorization

    if not isinstance(x_volcano_client_ip, Unset):
        headers["X-Volcano-Client-IP"] = x_volcano_client_ip



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/reset-password",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthResetPasswordResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthResetPasswordResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthResetPasswordResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResetPasswordBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthResetPasswordResponse200 | Error]:
    """ Reset password with recovery token

     Reset password using recovery token from forgot-password.
    Revokes all existing sessions for security.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthResetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthResetPasswordResponse200 | Error]
     """


    kwargs = request_kwargs(
        body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: AuthResetPasswordBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthResetPasswordResponse200 | Error | None:
    """ Reset password with recovery token

     Reset password using recovery token from forgot-password.
    Revokes all existing sessions for security.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthResetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthResetPasswordResponse200 | Error
     """


    return sync_detailed(
        client=client,
body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResetPasswordBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthResetPasswordResponse200 | Error]:
    """ Reset password with recovery token

     Reset password using recovery token from forgot-password.
    Revokes all existing sessions for security.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthResetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthResetPasswordResponse200 | Error]
     """


    kwargs = request_kwargs(
        body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthResetPasswordBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthResetPasswordResponse200 | Error | None:
    """ Reset password with recovery token

     Reset password using recovery token from forgot-password.
    Revokes all existing sessions for security.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthResetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthResetPasswordResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    )).parsed
