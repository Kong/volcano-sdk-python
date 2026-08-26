from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.paginated_storage_buckets import PaginatedStorageBuckets
from ...models.storage_bucket import StorageBucket
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/storage/buckets".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[StorageBucket] | PaginatedStorageBuckets | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> list[StorageBucket] | PaginatedStorageBuckets:
            try:
                if not isinstance(data, list):
                    raise TypeError()
                response_200_type_0 = []
                _response_200_type_0 = data
                for response_200_type_0_item_data in (_response_200_type_0):
                    response_200_type_0_item = StorageBucket.from_dict(response_200_type_0_item_data)



                    response_200_type_0.append(response_200_type_0_item)

                return response_200_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = PaginatedStorageBuckets.from_dict(data)



            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[StorageBucket] | PaginatedStorageBuckets]:
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[list[StorageBucket] | PaginatedStorageBuckets]:
    """ List all storage buckets in a project

     With no pagination params, returns the full bucket list as a bare array
    (legacy). Supplying `cursor`, `ending_before`, `search`, or `limit`
    switches to keyset (cursor) pagination and returns a paginated envelope
    with `next_cursor`/`prev_cursor` and a filtered `total`.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StorageBucket] | PaginatedStorageBuckets]
     """


    kwargs = _get_kwargs(
        id=id,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> list[StorageBucket] | PaginatedStorageBuckets | None:
    """ List all storage buckets in a project

     With no pagination params, returns the full bucket list as a bare array
    (legacy). Supplying `cursor`, `ending_before`, `search`, or `limit`
    switches to keyset (cursor) pagination and returns a paginated envelope
    with `next_cursor`/`prev_cursor` and a filtered `total`.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StorageBucket] | PaginatedStorageBuckets
     """


    return sync_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[list[StorageBucket] | PaginatedStorageBuckets]:
    """ List all storage buckets in a project

     With no pagination params, returns the full bucket list as a bare array
    (legacy). Supplying `cursor`, `ending_before`, `search`, or `limit`
    switches to keyset (cursor) pagination and returns a paginated envelope
    with `next_cursor`/`prev_cursor` and a filtered `total`.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StorageBucket] | PaginatedStorageBuckets]
     """


    kwargs = _get_kwargs(
        id=id,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> list[StorageBucket] | PaginatedStorageBuckets | None:
    """ List all storage buckets in a project

     With no pagination params, returns the full bucket list as a bare array
    (legacy). Supplying `cursor`, `ending_before`, `search`, or `limit`
    switches to keyset (cursor) pagination and returns a paginated envelope
    with `next_cursor`/`prev_cursor` and a filtered `total`.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StorageBucket] | PaginatedStorageBuckets
     """


    return (await asyncio_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    )).parsed
