from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_signup_anonymous_body import AuthSignupAnonymousBody
from ...models.auth_token_response import AuthTokenResponse
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    body: AuthSignupAnonymousBody | Unset = UNSET,
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
        "url": "/auth/signup-anonymous",
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthTokenResponse | Error | None:
    if response.status_code == 201:
        response_201 = AuthTokenResponse.from_dict(response.json())



        return response_201

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthTokenResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSignupAnonymousBody | Unset = UNSET,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse | Error]:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse | Error]
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
    body: AuthSignupAnonymousBody | Unset = UNSET,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthTokenResponse | Error | None:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse | Error
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
    body: AuthSignupAnonymousBody | Unset = UNSET,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse | Error]:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse | Error]
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
    body: AuthSignupAnonymousBody | Unset = UNSET,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthTokenResponse | Error | None:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    )).parsed
