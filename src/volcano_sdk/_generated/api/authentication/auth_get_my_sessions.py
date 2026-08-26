from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_get_my_sessions_response_200 import AuthGetMySessionsResponse200
from ...models.auth_get_my_sessions_sort import AuthGetMySessionsSort
from ...models.auth_get_my_sessions_sort import check_auth_get_my_sessions_sort
from ...models.auth_get_my_sessions_status import AuthGetMySessionsStatus
from ...models.auth_get_my_sessions_status import check_auth_get_my_sessions_status
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: AuthGetMySessionsSort | Unset = 'last_activity',
    status: AuthGetMySessionsStatus | Unset = UNSET,
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
        "url": "/auth/user/sessions",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthGetMySessionsResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthGetMySessionsResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthGetMySessionsResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: AuthGetMySessionsSort | Unset = 'last_activity',
    status: AuthGetMySessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[AuthGetMySessionsResponse200 | Error]:
    """ Get current user's sessions

     Returns paginated sessions for the currently authenticated user.
    Each session includes device info, IP addresses, and activity timestamps.
    The current session is marked with `is_current: true`.

    **Ordering and pagination.** Without `sort`, results are ordered by most
    recent activity and paged with `page`/`limit`, returning the
    `sessions`/`total`/`page`/`limit`/`total_pages` body below. This is the
    legacy default and is preserved for existing clients.

    Send `sort=created_at` to opt into the standard list contract: results are
    ordered by session start (newest first) and may be paged either with
    `page`/`limit` or by cursor with `cursor`/`ending_before` plus a bounded
    `offset` past the cursor anchor. Cursor responses use the shared
    `data` envelope with `next_cursor`/`prev_cursor`.

    Unlike other list endpoints, sending `limit` without `page` does **not**
    select cursor mode here; `sort=created_at` is the only opt-in. Cursor
    pagination is rejected with 400 for the activity order, because
    `last_activity_at` changes whenever a session refreshes its token: a row
    that crosses the cursor anchor between two requests would be skipped and
    never shown. The `status=expired` filter is also offset-only because a
    session can expire above the cursor anchor during a walk. Sending that
    filter in cursor mode, `page` with `cursor` or `ending_before`, or both
    cursor directions returns 400.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (AuthGetMySessionsSort | Unset):  Default: 'last_activity'.
        status (AuthGetMySessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthGetMySessionsResponse200 | Error]
     """


    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: AuthGetMySessionsSort | Unset = 'last_activity',
    status: AuthGetMySessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> AuthGetMySessionsResponse200 | Error | None:
    """ Get current user's sessions

     Returns paginated sessions for the currently authenticated user.
    Each session includes device info, IP addresses, and activity timestamps.
    The current session is marked with `is_current: true`.

    **Ordering and pagination.** Without `sort`, results are ordered by most
    recent activity and paged with `page`/`limit`, returning the
    `sessions`/`total`/`page`/`limit`/`total_pages` body below. This is the
    legacy default and is preserved for existing clients.

    Send `sort=created_at` to opt into the standard list contract: results are
    ordered by session start (newest first) and may be paged either with
    `page`/`limit` or by cursor with `cursor`/`ending_before` plus a bounded
    `offset` past the cursor anchor. Cursor responses use the shared
    `data` envelope with `next_cursor`/`prev_cursor`.

    Unlike other list endpoints, sending `limit` without `page` does **not**
    select cursor mode here; `sort=created_at` is the only opt-in. Cursor
    pagination is rejected with 400 for the activity order, because
    `last_activity_at` changes whenever a session refreshes its token: a row
    that crosses the cursor anchor between two requests would be skipped and
    never shown. The `status=expired` filter is also offset-only because a
    session can expire above the cursor anchor during a walk. Sending that
    filter in cursor mode, `page` with `cursor` or `ending_before`, or both
    cursor directions returns 400.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (AuthGetMySessionsSort | Unset):  Default: 'last_activity'.
        status (AuthGetMySessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthGetMySessionsResponse200 | Error
     """


    return sync_detailed(
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
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: AuthGetMySessionsSort | Unset = 'last_activity',
    status: AuthGetMySessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[AuthGetMySessionsResponse200 | Error]:
    """ Get current user's sessions

     Returns paginated sessions for the currently authenticated user.
    Each session includes device info, IP addresses, and activity timestamps.
    The current session is marked with `is_current: true`.

    **Ordering and pagination.** Without `sort`, results are ordered by most
    recent activity and paged with `page`/`limit`, returning the
    `sessions`/`total`/`page`/`limit`/`total_pages` body below. This is the
    legacy default and is preserved for existing clients.

    Send `sort=created_at` to opt into the standard list contract: results are
    ordered by session start (newest first) and may be paged either with
    `page`/`limit` or by cursor with `cursor`/`ending_before` plus a bounded
    `offset` past the cursor anchor. Cursor responses use the shared
    `data` envelope with `next_cursor`/`prev_cursor`.

    Unlike other list endpoints, sending `limit` without `page` does **not**
    select cursor mode here; `sort=created_at` is the only opt-in. Cursor
    pagination is rejected with 400 for the activity order, because
    `last_activity_at` changes whenever a session refreshes its token: a row
    that crosses the cursor anchor between two requests would be skipped and
    never shown. The `status=expired` filter is also offset-only because a
    session can expire above the cursor anchor during a walk. Sending that
    filter in cursor mode, `page` with `cursor` or `ending_before`, or both
    cursor directions returns 400.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (AuthGetMySessionsSort | Unset):  Default: 'last_activity'.
        status (AuthGetMySessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthGetMySessionsResponse200 | Error]
     """


    kwargs = _get_kwargs(
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
    *,
    client: AuthenticatedClient,
    page: int | Unset = 1,
    limit: int | Unset = 20,
    sort: AuthGetMySessionsSort | Unset = 'last_activity',
    status: AuthGetMySessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> AuthGetMySessionsResponse200 | Error | None:
    """ Get current user's sessions

     Returns paginated sessions for the currently authenticated user.
    Each session includes device info, IP addresses, and activity timestamps.
    The current session is marked with `is_current: true`.

    **Ordering and pagination.** Without `sort`, results are ordered by most
    recent activity and paged with `page`/`limit`, returning the
    `sessions`/`total`/`page`/`limit`/`total_pages` body below. This is the
    legacy default and is preserved for existing clients.

    Send `sort=created_at` to opt into the standard list contract: results are
    ordered by session start (newest first) and may be paged either with
    `page`/`limit` or by cursor with `cursor`/`ending_before` plus a bounded
    `offset` past the cursor anchor. Cursor responses use the shared
    `data` envelope with `next_cursor`/`prev_cursor`.

    Unlike other list endpoints, sending `limit` without `page` does **not**
    select cursor mode here; `sort=created_at` is the only opt-in. Cursor
    pagination is rejected with 400 for the activity order, because
    `last_activity_at` changes whenever a session refreshes its token: a row
    that crosses the cursor anchor between two requests would be skipped and
    never shown. The `status=expired` filter is also offset-only because a
    session can expire above the cursor anchor during a walk. Sending that
    filter in cursor mode, `page` with `cursor` or `ending_before`, or both
    cursor directions returns 400.

    Args:
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 20.
        sort (AuthGetMySessionsSort | Unset):  Default: 'last_activity'.
        status (AuthGetMySessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthGetMySessionsResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
page=page,
limit=limit,
sort=sort,
status=status,
cursor=cursor,
ending_before=ending_before,
offset=offset,

    )).parsed
