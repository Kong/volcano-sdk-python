from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_durable_functions import PaginatedDurableFunctions
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["search"] = search


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/durable-functions".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedDurableFunctions | None:
    if response.status_code == 200:
        response_200 = PaginatedDurableFunctions.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedDurableFunctions]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,

) -> Response[Error | PaginatedDurableFunctions]:
    """ List all durable functions in a project

     Standard functions never appear here, and durable functions never appear
    under `/projects/{id}/functions`. The two are separate collections.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableFunctions]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
search=search,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,

) -> Error | PaginatedDurableFunctions | None:
    """ List all durable functions in a project

     Standard functions never appear here, and durable functions never appear
    under `/projects/{id}/functions`. The two are separate collections.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableFunctions
     """


    return sync_detailed(
        id=id,
client=client,
page=page,
limit=limit,
search=search,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,

) -> Response[Error | PaginatedDurableFunctions]:
    """ List all durable functions in a project

     Standard functions never appear here, and durable functions never appear
    under `/projects/{id}/functions`. The two are separate collections.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableFunctions]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
search=search,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,

) -> Error | PaginatedDurableFunctions | None:
    """ List all durable functions in a project

     Standard functions never appear here, and durable functions never appear
    under `/projects/{id}/functions`. The two are separate collections.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableFunctions
     """


    return (await asyncio_detailed(
        id=id,
client=client,
page=page,
limit=limit,
search=search,

    )).parsed
