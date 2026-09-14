from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_database_regions_response_200_item import ListDatabaseRegionsResponse200Item
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/databases/regions",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[ListDatabaseRegionsResponse200Item] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = ListDatabaseRegionsResponse200Item.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[ListDatabaseRegionsResponse200Item]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[list[ListDatabaseRegionsResponse200Item]]:
    """ List platform-supported regions for database provisioning

     Returns the regions enabled for database provisioning in this platform environment.
    These are the same regions offered for function deployment, and the only values
    the `region` field of a database accepts.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ListDatabaseRegionsResponse200Item]]
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

) -> list[ListDatabaseRegionsResponse200Item] | None:
    """ List platform-supported regions for database provisioning

     Returns the regions enabled for database provisioning in this platform environment.
    These are the same regions offered for function deployment, and the only values
    the `region` field of a database accepts.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ListDatabaseRegionsResponse200Item]
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[list[ListDatabaseRegionsResponse200Item]]:
    """ List platform-supported regions for database provisioning

     Returns the regions enabled for database provisioning in this platform environment.
    These are the same regions offered for function deployment, and the only values
    the `region` field of a database accepts.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[ListDatabaseRegionsResponse200Item]]
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

) -> list[ListDatabaseRegionsResponse200Item] | None:
    """ List platform-supported regions for database provisioning

     Returns the regions enabled for database provisioning in this platform environment.
    These are the same regions offered for function deployment, and the only values
    the `region` field of a database accepts.
    This is a public endpoint that doesn't require authentication.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[ListDatabaseRegionsResponse200Item]
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
