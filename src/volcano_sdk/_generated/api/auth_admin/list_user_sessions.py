from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.list_user_sessions_response_200 import ListUserSessionsResponse200
from ...models.list_user_sessions_sort import check_list_user_sessions_sort
from ...models.list_user_sessions_sort import ListUserSessionsSort
from ...models.list_user_sessions_status import check_list_user_sessions_status
from ...models.list_user_sessions_status import ListUserSessionsStatus
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    user_id: UUID,
    *,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: ListUserSessionsSort | Unset = 'last_activity',
    status: ListUserSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort

    params["sort"] = json_sort

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/users/{user_id}/sessions".format(id=quote(str(id), safe=""),user_id=quote(str(user_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | ListUserSessionsResponse200 | None:
    if response.status_code == 200:
        response_200 = ListUserSessionsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error | ListUserSessionsResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: ListUserSessionsSort | Unset = 'last_activity',
    status: ListUserSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[Any | Error | ListUserSessionsResponse200]:
    """ List user sessions

     List paginated sessions for a specific auth user.
    Returns session details including device info, IP address, and activity timestamps.

    Ordering and pagination match `GET /auth/user/sessions`: the default is
    activity order with `page`/`limit` and the legacy `sessions` body, and
    `sort=created_at` opts into the standard cursor/offset hybrid with the
    shared `data` envelope. Cursor pagination is only available for
    `sort=created_at`, because the activity timestamp changes under paging.
    The `status=expired` filter is offset-only because sessions can expire
    above a cursor anchor during a walk.

    Args:
        id (UUID):
        user_id (UUID):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (ListUserSessionsSort | Unset):  Default: 'last_activity'.
        status (ListUserSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | ListUserSessionsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
page=page,
limit=limit,
sort=sort,
status=status,
cursor=cursor,
ending_before=ending_before,
offset=offset,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: ListUserSessionsSort | Unset = 'last_activity',
    status: ListUserSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Any | Error | ListUserSessionsResponse200 | None:
    """ List user sessions

     List paginated sessions for a specific auth user.
    Returns session details including device info, IP address, and activity timestamps.

    Ordering and pagination match `GET /auth/user/sessions`: the default is
    activity order with `page`/`limit` and the legacy `sessions` body, and
    `sort=created_at` opts into the standard cursor/offset hybrid with the
    shared `data` envelope. Cursor pagination is only available for
    `sort=created_at`, because the activity timestamp changes under paging.
    The `status=expired` filter is offset-only because sessions can expire
    above a cursor anchor during a walk.

    Args:
        id (UUID):
        user_id (UUID):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (ListUserSessionsSort | Unset):  Default: 'last_activity'.
        status (ListUserSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | ListUserSessionsResponse200
     """


    return sync_detailed(
        id=id,
user_id=user_id,
client=client,
page=page,
limit=limit,
sort=sort,
status=status,
cursor=cursor,
ending_before=ending_before,
offset=offset,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: ListUserSessionsSort | Unset = 'last_activity',
    status: ListUserSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[Any | Error | ListUserSessionsResponse200]:
    """ List user sessions

     List paginated sessions for a specific auth user.
    Returns session details including device info, IP address, and activity timestamps.

    Ordering and pagination match `GET /auth/user/sessions`: the default is
    activity order with `page`/`limit` and the legacy `sessions` body, and
    `sort=created_at` opts into the standard cursor/offset hybrid with the
    shared `data` envelope. Cursor pagination is only available for
    `sort=created_at`, because the activity timestamp changes under paging.
    The `status=expired` filter is offset-only because sessions can expire
    above a cursor anchor during a walk.

    Args:
        id (UUID):
        user_id (UUID):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (ListUserSessionsSort | Unset):  Default: 'last_activity'.
        status (ListUserSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | ListUserSessionsResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
user_id=user_id,
page=page,
limit=limit,
sort=sort,
status=status,
cursor=cursor,
ending_before=ending_before,
offset=offset,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    user_id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: ListUserSessionsSort | Unset = 'last_activity',
    status: ListUserSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Any | Error | ListUserSessionsResponse200 | None:
    """ List user sessions

     List paginated sessions for a specific auth user.
    Returns session details including device info, IP address, and activity timestamps.

    Ordering and pagination match `GET /auth/user/sessions`: the default is
    activity order with `page`/`limit` and the legacy `sessions` body, and
    `sort=created_at` opts into the standard cursor/offset hybrid with the
    shared `data` envelope. Cursor pagination is only available for
    `sort=created_at`, because the activity timestamp changes under paging.
    The `status=expired` filter is offset-only because sessions can expire
    above a cursor anchor during a walk.

    Args:
        id (UUID):
        user_id (UUID):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (ListUserSessionsSort | Unset):  Default: 'last_activity'.
        status (ListUserSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | ListUserSessionsResponse200
     """


    return (await asyncio_detailed(
        id=id,
user_id=user_id,
client=client,
page=page,
limit=limit,
sort=sort,
status=status,
cursor=cursor,
ending_before=ending_before,
offset=offset,

    )).parsed
