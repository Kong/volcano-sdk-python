from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.function_runtimes_response import FunctionRuntimesResponse
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/functions/runtimes",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FunctionRuntimesResponse | None:
    if response.status_code == 200:
        response_200 = FunctionRuntimesResponse.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FunctionRuntimesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[FunctionRuntimesResponse]:
    """ List supported function runtimes

     Returns the public function runtime catalog used by CLI clients to select supported runtimes,
    language defaults, and local source packaging metadata for deployments.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FunctionRuntimesResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> FunctionRuntimesResponse | None:
    """ List supported function runtimes

     Returns the public function runtime catalog used by CLI clients to select supported runtimes,
    language defaults, and local source packaging metadata for deployments.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FunctionRuntimesResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[FunctionRuntimesResponse]:
    """ List supported function runtimes

     Returns the public function runtime catalog used by CLI clients to select supported runtimes,
    language defaults, and local source packaging metadata for deployments.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FunctionRuntimesResponse]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> FunctionRuntimesResponse | None:
    """ List supported function runtimes

     Returns the public function runtime catalog used by CLI clients to select supported runtimes,
    language defaults, and local source packaging metadata for deployments.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FunctionRuntimesResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
