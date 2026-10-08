from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.verified_domains_response import VerifiedDomainsResponse
from typing import cast



def request_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/domains",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | VerifiedDomainsResponse | None:
    if response.status_code == 200:
        response_200 = VerifiedDomainsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | VerifiedDomainsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | VerifiedDomainsResponse]:
    """ List verified domains

     Lists the domains the account has verified. The account can attach any
    custom domain at or below one of them, in either TLS mode, without
    publishing another ownership record.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | VerifiedDomainsResponse]
     """


    kwargs = request_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> Error | VerifiedDomainsResponse | None:
    """ List verified domains

     Lists the domains the account has verified. The account can attach any
    custom domain at or below one of them, in either TLS mode, without
    publishing another ownership record.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | VerifiedDomainsResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | VerifiedDomainsResponse]:
    """ List verified domains

     Lists the domains the account has verified. The account can attach any
    custom domain at or below one of them, in either TLS mode, without
    publishing another ownership record.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | VerifiedDomainsResponse]
     """


    kwargs = request_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> Error | VerifiedDomainsResponse | None:
    """ List verified domains

     Lists the domains the account has verified. The account can attach any
    custom domain at or below one of them, in either TLS mode, without
    publishing another ownership record.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | VerifiedDomainsResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
