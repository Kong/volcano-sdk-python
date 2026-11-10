from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.account_session_list import AccountSessionList
from ...models.error import Error
from ...models.list_account_sessions_sort import check_list_account_sessions_sort
from ...models.list_account_sessions_sort import ListAccountSessionsSort
from ...models.list_account_sessions_status import check_list_account_sessions_status
from ...models.list_account_sessions_status import ListAccountSessionsStatus
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    sort: ListAccountSessionsSort | Unset = 'last_activity',
    status: ListAccountSessionsStatus | Unset = UNSET,
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
        "url": "/user/sessions",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AccountSessionList | Error | None:
    if response.status_code == 200:
        response_200 = AccountSessionList.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AccountSessionList | Error]:
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
    limit: int | Unset = UNSET,
    sort: ListAccountSessionsSort | Unset = 'last_activity',
    status: ListAccountSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[AccountSessionList | Error]:
    """ List your account's sign-in sessions

     Lists the sign-in sessions of the account that owns the calling
    platform token: dashboard sign-ins (`kind: browser`) and CLI logins
    (`kind: cli`). The session the calling token was exchanged from is
    marked `is_current: true`. A token created in the dashboard or through
    the management API, rather than by signing in, has no session, so no
    session is current.

    Ordering and pagination match `GET /auth/user/sessions`.

    Only a platform token (`pk-`) can call it. A project access token is
    refused with `403`.

    Args:
        page (int | Unset):
        limit (int | Unset):
        sort (ListAccountSessionsSort | Unset):  Default: 'last_activity'.
        status (ListAccountSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountSessionList | Error]
     """


    kwargs = request_kwargs(
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

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    sort: ListAccountSessionsSort | Unset = 'last_activity',
    status: ListAccountSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> AccountSessionList | Error | None:
    """ List your account's sign-in sessions

     Lists the sign-in sessions of the account that owns the calling
    platform token: dashboard sign-ins (`kind: browser`) and CLI logins
    (`kind: cli`). The session the calling token was exchanged from is
    marked `is_current: true`. A token created in the dashboard or through
    the management API, rather than by signing in, has no session, so no
    session is current.

    Ordering and pagination match `GET /auth/user/sessions`.

    Only a platform token (`pk-`) can call it. A project access token is
    refused with `403`.

    Args:
        page (int | Unset):
        limit (int | Unset):
        sort (ListAccountSessionsSort | Unset):  Default: 'last_activity'.
        status (ListAccountSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountSessionList | Error
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
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    sort: ListAccountSessionsSort | Unset = 'last_activity',
    status: ListAccountSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> Response[AccountSessionList | Error]:
    """ List your account's sign-in sessions

     Lists the sign-in sessions of the account that owns the calling
    platform token: dashboard sign-ins (`kind: browser`) and CLI logins
    (`kind: cli`). The session the calling token was exchanged from is
    marked `is_current: true`. A token created in the dashboard or through
    the management API, rather than by signing in, has no session, so no
    session is current.

    Ordering and pagination match `GET /auth/user/sessions`.

    Only a platform token (`pk-`) can call it. A project access token is
    refused with `403`.

    Args:
        page (int | Unset):
        limit (int | Unset):
        sort (ListAccountSessionsSort | Unset):  Default: 'last_activity'.
        status (ListAccountSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AccountSessionList | Error]
     """


    kwargs = request_kwargs(
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

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = UNSET,
    sort: ListAccountSessionsSort | Unset = 'last_activity',
    status: ListAccountSessionsStatus | Unset = UNSET,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = UNSET,

) -> AccountSessionList | Error | None:
    """ List your account's sign-in sessions

     Lists the sign-in sessions of the account that owns the calling
    platform token: dashboard sign-ins (`kind: browser`) and CLI logins
    (`kind: cli`). The session the calling token was exchanged from is
    marked `is_current: true`. A token created in the dashboard or through
    the management API, rather than by signing in, has no session, so no
    session is current.

    Ordering and pagination match `GET /auth/user/sessions`.

    Only a platform token (`pk-`) can call it. A project access token is
    refused with `403`.

    Args:
        page (int | Unset):
        limit (int | Unset):
        sort (ListAccountSessionsSort | Unset):  Default: 'last_activity'.
        status (ListAccountSessionsStatus | Unset):
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AccountSessionList | Error
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
