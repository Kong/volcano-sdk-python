from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_projects import PaginatedProjects
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
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
        "url": "/projects",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedProjects | None:
    if response.status_code == 200:
        response_200 = PaginatedProjects.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedProjects]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[Error | PaginatedProjects]:
    """ List all projects for authenticated user

     Returns projects that are not deleting or deleted, newest first.
    Supports two mutually exclusive pagination modes. Offset mode uses
    `page` and `limit`. Cursor mode uses `cursor` or `ending_before` with
    `limit`, returns `next_cursor`/`prev_cursor`, and supports a bounded
    `offset` past the cursor anchor. Supplying `limit` without `page`
    selects cursor mode. `search` applies a case-insensitive project-name
    filter in either mode. Sending `page` with `cursor` or `ending_before`,
    or sending both cursor directions, returns 400.

    Args:
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
        Response[Error | PaginatedProjects]
     """


    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Error | PaginatedProjects | None:
    """ List all projects for authenticated user

     Returns projects that are not deleting or deleted, newest first.
    Supports two mutually exclusive pagination modes. Offset mode uses
    `page` and `limit`. Cursor mode uses `cursor` or `ending_before` with
    `limit`, returns `next_cursor`/`prev_cursor`, and supports a bounded
    `offset` past the cursor anchor. Supplying `limit` without `page`
    selects cursor mode. `search` applies a case-insensitive project-name
    filter in either mode. Sending `page` with `cursor` or `ending_before`,
    or sending both cursor directions, returns 400.

    Args:
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
        Error | PaginatedProjects
     """


    return sync_detailed(
        client=client,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[Error | PaginatedProjects]:
    """ List all projects for authenticated user

     Returns projects that are not deleting or deleted, newest first.
    Supports two mutually exclusive pagination modes. Offset mode uses
    `page` and `limit`. Cursor mode uses `cursor` or `ending_before` with
    `limit`, returns `next_cursor`/`prev_cursor`, and supports a bounded
    `offset` past the cursor anchor. Supplying `limit` without `page`
    selects cursor mode. `search` applies a case-insensitive project-name
    filter in either mode. Sending `page` with `cursor` or `ending_before`,
    or sending both cursor directions, returns 400.

    Args:
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
        Response[Error | PaginatedProjects]
     """


    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Error | PaginatedProjects | None:
    """ List all projects for authenticated user

     Returns projects that are not deleting or deleted, newest first.
    Supports two mutually exclusive pagination modes. Offset mode uses
    `page` and `limit`. Cursor mode uses `cursor` or `ending_before` with
    `limit`, returns `next_cursor`/`prev_cursor`, and supports a bounded
    `offset` past the cursor anchor. Supplying `limit` without `page`
    selects cursor mode. `search` applies a case-insensitive project-name
    filter in either mode. Sending `page` with `cursor` or `ending_before`,
    or sending both cursor directions, returns 400.

    Args:
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
        Error | PaginatedProjects
     """


    return (await asyncio_detailed(
        client=client,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    )).parsed
