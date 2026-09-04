from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.call_o_auth_provider_api_body import CallOAuthProviderAPIBody
from ...models.call_o_auth_provider_api_provider import CallOAuthProviderAPIProvider
from ...models.call_o_auth_provider_api_provider import check_call_o_auth_provider_api_provider
from ...models.call_o_auth_provider_api_response_200 import CallOAuthProviderAPIResponse200
from ...models.error import Error
from typing import cast



def _get_kwargs(
    provider: CallOAuthProviderAPIProvider,
    *,
    body: CallOAuthProviderAPIBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/oauth/{provider}/call-api".format(provider=quote(str(provider), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CallOAuthProviderAPIResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = CallOAuthProviderAPIResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CallOAuthProviderAPIResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: CallOAuthProviderAPIProvider,
    *,
    client: AuthenticatedClient,
    body: CallOAuthProviderAPIBody,

) -> Response[CallOAuthProviderAPIResponse200 | Error]:
    """ Call OAuth provider API

     Make an authenticated request to an OAuth provider's API on behalf of the user.
    The user's stored access token is automatically used and refreshed if needed.

    The request is always sent to the provider's fixed API base URL joined with
    the caller-supplied `endpoint`. `endpoint` must be a relative path beginning
    with `/` (optionally with a query string); it cannot change the target host.
    Absolute URLs, protocol-relative `//host` values, or userinfo (`@host`) are
    rejected with `400` so the request can never be redirected to another host.

    Examples of `endpoint`:
    - Google userinfo: `/oauth2/v1/userinfo`
    - GitHub repositories: `/user/repos`
    - Microsoft Graph profile: `/me`

    The response is the raw JSON response from the provider's API.

    Args:
        provider (CallOAuthProviderAPIProvider):
        body (CallOAuthProviderAPIBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallOAuthProviderAPIResponse200 | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: CallOAuthProviderAPIProvider,
    *,
    client: AuthenticatedClient,
    body: CallOAuthProviderAPIBody,

) -> CallOAuthProviderAPIResponse200 | Error | None:
    """ Call OAuth provider API

     Make an authenticated request to an OAuth provider's API on behalf of the user.
    The user's stored access token is automatically used and refreshed if needed.

    The request is always sent to the provider's fixed API base URL joined with
    the caller-supplied `endpoint`. `endpoint` must be a relative path beginning
    with `/` (optionally with a query string); it cannot change the target host.
    Absolute URLs, protocol-relative `//host` values, or userinfo (`@host`) are
    rejected with `400` so the request can never be redirected to another host.

    Examples of `endpoint`:
    - Google userinfo: `/oauth2/v1/userinfo`
    - GitHub repositories: `/user/repos`
    - Microsoft Graph profile: `/me`

    The response is the raw JSON response from the provider's API.

    Args:
        provider (CallOAuthProviderAPIProvider):
        body (CallOAuthProviderAPIBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallOAuthProviderAPIResponse200 | Error
     """


    return sync_detailed(
        provider=provider,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    provider: CallOAuthProviderAPIProvider,
    *,
    client: AuthenticatedClient,
    body: CallOAuthProviderAPIBody,

) -> Response[CallOAuthProviderAPIResponse200 | Error]:
    """ Call OAuth provider API

     Make an authenticated request to an OAuth provider's API on behalf of the user.
    The user's stored access token is automatically used and refreshed if needed.

    The request is always sent to the provider's fixed API base URL joined with
    the caller-supplied `endpoint`. `endpoint` must be a relative path beginning
    with `/` (optionally with a query string); it cannot change the target host.
    Absolute URLs, protocol-relative `//host` values, or userinfo (`@host`) are
    rejected with `400` so the request can never be redirected to another host.

    Examples of `endpoint`:
    - Google userinfo: `/oauth2/v1/userinfo`
    - GitHub repositories: `/user/repos`
    - Microsoft Graph profile: `/me`

    The response is the raw JSON response from the provider's API.

    Args:
        provider (CallOAuthProviderAPIProvider):
        body (CallOAuthProviderAPIBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallOAuthProviderAPIResponse200 | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: CallOAuthProviderAPIProvider,
    *,
    client: AuthenticatedClient,
    body: CallOAuthProviderAPIBody,

) -> CallOAuthProviderAPIResponse200 | Error | None:
    """ Call OAuth provider API

     Make an authenticated request to an OAuth provider's API on behalf of the user.
    The user's stored access token is automatically used and refreshed if needed.

    The request is always sent to the provider's fixed API base URL joined with
    the caller-supplied `endpoint`. `endpoint` must be a relative path beginning
    with `/` (optionally with a query string); it cannot change the target host.
    Absolute URLs, protocol-relative `//host` values, or userinfo (`@host`) are
    rejected with `400` so the request can never be redirected to another host.

    Examples of `endpoint`:
    - Google userinfo: `/oauth2/v1/userinfo`
    - GitHub repositories: `/user/repos`
    - Microsoft Graph profile: `/me`

    The response is the raw JSON response from the provider's API.

    Args:
        provider (CallOAuthProviderAPIProvider):
        body (CallOAuthProviderAPIBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallOAuthProviderAPIResponse200 | Error
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
body=body,

    )).parsed
