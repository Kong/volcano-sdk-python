from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_signin_body import AuthSigninBody
from ...models.auth_token_response import AuthTokenResponse
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    body: AuthSigninBody,
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
        "url": "/auth/signin",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthTokenResponse | None:
    if response.status_code == 200:
        response_200 = AuthTokenResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthTokenResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSigninBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ Sign in an auth user

     Authenticate with email and password. Requires an anon key.

    Set `session_mode` to `cookie` to request HttpOnly refresh-token
    storage. Cookie mode is honored only for an exact, credentialed CORS
    origin on the same schemeful site as this API. Otherwise the response
    retains the refresh token in its body. A frontend on its default
    Volcano URL is cross-site with this API and so always gets the body
    token.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSigninBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
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
    body: AuthSigninBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ Sign in an auth user

     Authenticate with email and password. Requires an anon key.

    Set `session_mode` to `cookie` to request HttpOnly refresh-token
    storage. Cookie mode is honored only for an exact, credentialed CORS
    origin on the same schemeful site as this API. Otherwise the response
    retains the refresh token in its body. A frontend on its default
    Volcano URL is cross-site with this API and so always gets the body
    token.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSigninBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
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
    body: AuthSigninBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ Sign in an auth user

     Authenticate with email and password. Requires an anon key.

    Set `session_mode` to `cookie` to request HttpOnly refresh-token
    storage. Cookie mode is honored only for an exact, credentialed CORS
    origin on the same schemeful site as this API. Otherwise the response
    retains the refresh token in its body. A frontend on its default
    Volcano URL is cross-site with this API and so always gets the body
    token.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSigninBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
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
    body: AuthSigninBody,
    x_volcano_proxy_authorization: str | Unset = UNSET,
    x_volcano_client_ip: str | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ Sign in an auth user

     Authenticate with email and password. Requires an anon key.

    Set `session_mode` to `cookie` to request HttpOnly refresh-token
    storage. Cookie mode is honored only for an exact, credentialed CORS
    origin on the same schemeful site as this API. Otherwise the response
    retains the refresh token in its body. A frontend on its default
    Volcano URL is cross-site with this API and so always gets the body
    token.

    Args:
        x_volcano_proxy_authorization (str | Unset):
        x_volcano_client_ip (str | Unset):
        body (AuthSigninBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,
x_volcano_proxy_authorization=x_volcano_proxy_authorization,
x_volcano_client_ip=x_volcano_client_ip,

    )).parsed
