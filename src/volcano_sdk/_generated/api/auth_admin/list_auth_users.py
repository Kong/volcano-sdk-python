from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.list_auth_users_status import check_list_auth_users_status
from ...models.list_auth_users_status import ListAuthUsersStatus
from ...models.paginated_auth_users import PaginatedAuthUsers
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
    status: ListAuthUsersStatus | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/users".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedAuthUsers | None:
    if response.status_code == 200:
        response_200 = PaginatedAuthUsers.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedAuthUsers]:
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
    status: ListAuthUsersStatus | Unset = UNSET,

) -> Response[Error | PaginatedAuthUsers]:
    """ List all auth users (admin)

     List auth users in project. Requires platform token.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        status (ListAuthUsersStatus | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedAuthUsers]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
status=status,

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
    status: ListAuthUsersStatus | Unset = UNSET,

) -> Error | PaginatedAuthUsers | None:
    """ List all auth users (admin)

     List auth users in project. Requires platform token.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        status (ListAuthUsersStatus | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedAuthUsers
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
status=status,

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
    status: ListAuthUsersStatus | Unset = UNSET,

) -> Response[Error | PaginatedAuthUsers]:
    """ List all auth users (admin)

     List auth users in project. Requires platform token.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        status (ListAuthUsersStatus | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedAuthUsers]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
status=status,

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
    status: ListAuthUsersStatus | Unset = UNSET,

) -> Error | PaginatedAuthUsers | None:
    """ List all auth users (admin)

     List auth users in project. Requires platform token.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        status (ListAuthUsersStatus | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedAuthUsers
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
status=status,

    )).parsed
