from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_device_authorize_body import AuthDeviceAuthorizeBody
from ...models.device_authorization_response import DeviceAuthorizationResponse
from ...models.o_auth_error_response import OAuthErrorResponse
from typing import cast



def _get_kwargs(
    *,
    body: AuthDeviceAuthorizeBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/device/authorize",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeviceAuthorizationResponse | OAuthErrorResponse | None:
    if response.status_code == 200:
        response_200 = DeviceAuthorizationResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = OAuthErrorResponse.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeviceAuthorizationResponse | OAuthErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthDeviceAuthorizeBody,

) -> Response[DeviceAuthorizationResponse | OAuthErrorResponse]:
    """ Start RFC8628 device authorization

     Starts OAuth 2.0 Device Authorization Grant (RFC 8628).
    Returns `device_code` for the CLI and `user_code` for browser verification.

    By default the returned `verification_uri` / `verification_uri_complete`
    point at the project's managed device-approval page served by this API
    (`/projects/{projectId}/auth/hosted?action=device&user_code=...&anon_key=...`),
    which requires managed auth enabled and a default anon key for the
    project.

    Projects can override this by setting `device_verification_url` on the
    auth config (`PATCH /auth/config`). When set, that URL is returned as-is
    with the `user_code` appended (no `action=device` hint and no embedded
    anon key — the page brings its own), so a CLI's `login` command surfaces
    the project's own RFC 8628 approval page. With a custom URL, device login
    does **not** require managed auth to be enabled; the custom page's origin
    must be in the project's auth CORS allowlist to call
    `POST /auth/device/verify`. Either way the verification page must
    authenticate the end user and call `POST /auth/device/verify` with the
    `user_code`. See the device-auth guide for both approaches.

    Args:
        body (AuthDeviceAuthorizeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeviceAuthorizationResponse | OAuthErrorResponse]
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
    body: AuthDeviceAuthorizeBody,

) -> DeviceAuthorizationResponse | OAuthErrorResponse | None:
    """ Start RFC8628 device authorization

     Starts OAuth 2.0 Device Authorization Grant (RFC 8628).
    Returns `device_code` for the CLI and `user_code` for browser verification.

    By default the returned `verification_uri` / `verification_uri_complete`
    point at the project's managed device-approval page served by this API
    (`/projects/{projectId}/auth/hosted?action=device&user_code=...&anon_key=...`),
    which requires managed auth enabled and a default anon key for the
    project.

    Projects can override this by setting `device_verification_url` on the
    auth config (`PATCH /auth/config`). When set, that URL is returned as-is
    with the `user_code` appended (no `action=device` hint and no embedded
    anon key — the page brings its own), so a CLI's `login` command surfaces
    the project's own RFC 8628 approval page. With a custom URL, device login
    does **not** require managed auth to be enabled; the custom page's origin
    must be in the project's auth CORS allowlist to call
    `POST /auth/device/verify`. Either way the verification page must
    authenticate the end user and call `POST /auth/device/verify` with the
    `user_code`. See the device-auth guide for both approaches.

    Args:
        body (AuthDeviceAuthorizeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeviceAuthorizationResponse | OAuthErrorResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: AuthDeviceAuthorizeBody,

) -> Response[DeviceAuthorizationResponse | OAuthErrorResponse]:
    """ Start RFC8628 device authorization

     Starts OAuth 2.0 Device Authorization Grant (RFC 8628).
    Returns `device_code` for the CLI and `user_code` for browser verification.

    By default the returned `verification_uri` / `verification_uri_complete`
    point at the project's managed device-approval page served by this API
    (`/projects/{projectId}/auth/hosted?action=device&user_code=...&anon_key=...`),
    which requires managed auth enabled and a default anon key for the
    project.

    Projects can override this by setting `device_verification_url` on the
    auth config (`PATCH /auth/config`). When set, that URL is returned as-is
    with the `user_code` appended (no `action=device` hint and no embedded
    anon key — the page brings its own), so a CLI's `login` command surfaces
    the project's own RFC 8628 approval page. With a custom URL, device login
    does **not** require managed auth to be enabled; the custom page's origin
    must be in the project's auth CORS allowlist to call
    `POST /auth/device/verify`. Either way the verification page must
    authenticate the end user and call `POST /auth/device/verify` with the
    `user_code`. See the device-auth guide for both approaches.

    Args:
        body (AuthDeviceAuthorizeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeviceAuthorizationResponse | OAuthErrorResponse]
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
    body: AuthDeviceAuthorizeBody,

) -> DeviceAuthorizationResponse | OAuthErrorResponse | None:
    """ Start RFC8628 device authorization

     Starts OAuth 2.0 Device Authorization Grant (RFC 8628).
    Returns `device_code` for the CLI and `user_code` for browser verification.

    By default the returned `verification_uri` / `verification_uri_complete`
    point at the project's managed device-approval page served by this API
    (`/projects/{projectId}/auth/hosted?action=device&user_code=...&anon_key=...`),
    which requires managed auth enabled and a default anon key for the
    project.

    Projects can override this by setting `device_verification_url` on the
    auth config (`PATCH /auth/config`). When set, that URL is returned as-is
    with the `user_code` appended (no `action=device` hint and no embedded
    anon key — the page brings its own), so a CLI's `login` command surfaces
    the project's own RFC 8628 approval page. With a custom URL, device login
    does **not** require managed auth to be enabled; the custom page's origin
    must be in the project's auth CORS allowlist to call
    `POST /auth/device/verify`. Either way the verification page must
    authenticate the end user and call `POST /auth/device/verify` with the
    `user_code`. See the device-auth guide for both approaches.

    Args:
        body (AuthDeviceAuthorizeBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeviceAuthorizationResponse | OAuthErrorResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
