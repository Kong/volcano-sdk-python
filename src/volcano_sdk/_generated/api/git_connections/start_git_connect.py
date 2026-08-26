from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.git_connect_start_response import GitConnectStartResponse
from ...models.start_git_connect_provider import check_start_git_connect_provider
from ...models.start_git_connect_provider import StartGitConnectProvider
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    provider: StartGitConnectProvider | Unset = 'github',
    redirect: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_provider: str | Unset = UNSET
    if not isinstance(provider, Unset):
        json_provider = provider

    params["provider"] = json_provider

    params["redirect"] = redirect


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user/git/connect",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | GitConnectStartResponse | None:
    if response.status_code == 200:
        response_200 = GitConnectStartResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | GitConnectStartResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    provider: StartGitConnectProvider | Unset = 'github',
    redirect: str | Unset = UNSET,

) -> Response[Error | GitConnectStartResponse]:
    """ Start a git provider connection

     Starts a first-party dashboard user's git provider connection flow and
    returns the provider authorization URL. The response also sets a
    short-lived HttpOnly callback binding cookie tied to the authenticated
    user through the signed provider state.

    Args:
        provider (StartGitConnectProvider | Unset):  Default: 'github'.
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitConnectStartResponse]
     """


    kwargs = _get_kwargs(
        provider=provider,
redirect=redirect,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    provider: StartGitConnectProvider | Unset = 'github',
    redirect: str | Unset = UNSET,

) -> Error | GitConnectStartResponse | None:
    """ Start a git provider connection

     Starts a first-party dashboard user's git provider connection flow and
    returns the provider authorization URL. The response also sets a
    short-lived HttpOnly callback binding cookie tied to the authenticated
    user through the signed provider state.

    Args:
        provider (StartGitConnectProvider | Unset):  Default: 'github'.
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitConnectStartResponse
     """


    return sync_detailed(
        client=client,
provider=provider,
redirect=redirect,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    provider: StartGitConnectProvider | Unset = 'github',
    redirect: str | Unset = UNSET,

) -> Response[Error | GitConnectStartResponse]:
    """ Start a git provider connection

     Starts a first-party dashboard user's git provider connection flow and
    returns the provider authorization URL. The response also sets a
    short-lived HttpOnly callback binding cookie tied to the authenticated
    user through the signed provider state.

    Args:
        provider (StartGitConnectProvider | Unset):  Default: 'github'.
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | GitConnectStartResponse]
     """


    kwargs = _get_kwargs(
        provider=provider,
redirect=redirect,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    provider: StartGitConnectProvider | Unset = 'github',
    redirect: str | Unset = UNSET,

) -> Error | GitConnectStartResponse | None:
    """ Start a git provider connection

     Starts a first-party dashboard user's git provider connection flow and
    returns the provider authorization URL. The response also sets a
    short-lived HttpOnly callback binding cookie tied to the authenticated
    user through the signed provider state.

    Args:
        provider (StartGitConnectProvider | Unset):  Default: 'github'.
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | GitConnectStartResponse
     """


    return (await asyncio_detailed(
        client=client,
provider=provider,
redirect=redirect,

    )).parsed
