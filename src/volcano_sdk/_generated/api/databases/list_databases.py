from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.paginated_databases import PaginatedDatabases
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> PaginatedDatabases | None:
    if response.status_code == 200:
        response_200 = PaginatedDatabases.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[PaginatedDatabases]:
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
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[PaginatedDatabases]:
    """ List all databases for a project

     Supports two mutually exclusive pagination modes. Offset mode uses `page`
    and `limit`. Cursor mode uses `cursor` and `limit`, supports `search`
    (case-insensitive name match), and returns `next_cursor`/`prev_cursor`.
    The optional `status` filter applies in both modes and is bound to the
    cursor. Sending both `page` and `cursor` (or `page` and `search`) returns 400.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedDatabases]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> PaginatedDatabases | None:
    """ List all databases for a project

     Supports two mutually exclusive pagination modes. Offset mode uses `page`
    and `limit`. Cursor mode uses `cursor` and `limit`, supports `search`
    (case-insensitive name match), and returns `next_cursor`/`prev_cursor`.
    The optional `status` filter applies in both modes and is bound to the
    cursor. Sending both `page` and `cursor` (or `page` and `search`) returns 400.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedDatabases
     """


    return sync_detailed(
        id=id,
client=client,
page=page,
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[PaginatedDatabases]:
    """ List all databases for a project

     Supports two mutually exclusive pagination modes. Offset mode uses `page`
    and `limit`. Cursor mode uses `cursor` and `limit`, supports `search`
    (case-insensitive name match), and returns `next_cursor`/`prev_cursor`.
    The optional `status` filter applies in both modes and is bound to the
    cursor. Sending both `page` and `cursor` (or `page` and `search`) returns 400.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PaginatedDatabases]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> PaginatedDatabases | None:
    """ List all databases for a project

     Supports two mutually exclusive pagination modes. Offset mode uses `page`
    and `limit`. Cursor mode uses `cursor` and `limit`, supports `search`
    (case-insensitive name match), and returns `next_cursor`/`prev_cursor`.
    The optional `status` filter applies in both modes and is bound to the
    cursor. Sending both `page` and `cursor` (or `page` and `search`) returns 400.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PaginatedDatabases
     """


    return (await asyncio_detailed(
        id=id,
client=client,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    )).parsed
