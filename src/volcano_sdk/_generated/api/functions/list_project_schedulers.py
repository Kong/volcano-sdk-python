from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_kind_filter import check_function_kind_filter
from ...models.function_kind_filter import FunctionKindFilter
from ...models.function_scheduler_list_response import FunctionSchedulerListResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    function_kind: FunctionKindFilter | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search

    json_function_kind: str | Unset = UNSET
    if not isinstance(function_kind, Unset):
        json_function_kind = function_kind

    params["function_kind"] = json_function_kind


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/schedulers".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionSchedulerListResponse | None:
    if response.status_code == 200:
        response_200 = FunctionSchedulerListResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionSchedulerListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    function_kind: FunctionKindFilter | Unset = UNSET,

) -> Response[Error | FunctionSchedulerListResponse]:
    """ List every function scheduler in a project

     Project-scoped counterpart to `/projects/{id}/functions/{functionId}/schedulers`.
    Returns schedulers across all functions in the project, ordered by
    creation time descending, with standard page/limit pagination so
    clients don't have to fan out one request per function.

    Schedulers of standard and durable functions are listed together, and
    each carries `function_kind`. Pass `function_kind` to list one kind
    only.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        function_kind (FunctionKindFilter | Unset): A function kind to filter a list by. Unlike
            `FunctionKind` it has no
            default: omitting the filter includes both kinds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionSchedulerListResponse]
     """


    kwargs = request_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
function_kind=function_kind,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    function_kind: FunctionKindFilter | Unset = UNSET,

) -> Error | FunctionSchedulerListResponse | None:
    """ List every function scheduler in a project

     Project-scoped counterpart to `/projects/{id}/functions/{functionId}/schedulers`.
    Returns schedulers across all functions in the project, ordered by
    creation time descending, with standard page/limit pagination so
    clients don't have to fan out one request per function.

    Schedulers of standard and durable functions are listed together, and
    each carries `function_kind`. Pass `function_kind` to list one kind
    only.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        function_kind (FunctionKindFilter | Unset): A function kind to filter a list by. Unlike
            `FunctionKind` it has no
            default: omitting the filter includes both kinds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionSchedulerListResponse
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
function_kind=function_kind,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    function_kind: FunctionKindFilter | Unset = UNSET,

) -> Response[Error | FunctionSchedulerListResponse]:
    """ List every function scheduler in a project

     Project-scoped counterpart to `/projects/{id}/functions/{functionId}/schedulers`.
    Returns schedulers across all functions in the project, ordered by
    creation time descending, with standard page/limit pagination so
    clients don't have to fan out one request per function.

    Schedulers of standard and durable functions are listed together, and
    each carries `function_kind`. Pass `function_kind` to list one kind
    only.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        function_kind (FunctionKindFilter | Unset): A function kind to filter a list by. Unlike
            `FunctionKind` it has no
            default: omitting the filter includes both kinds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionSchedulerListResponse]
     """


    kwargs = request_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
function_kind=function_kind,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    function_kind: FunctionKindFilter | Unset = UNSET,

) -> Error | FunctionSchedulerListResponse | None:
    """ List every function scheduler in a project

     Project-scoped counterpart to `/projects/{id}/functions/{functionId}/schedulers`.
    Returns schedulers across all functions in the project, ordered by
    creation time descending, with standard page/limit pagination so
    clients don't have to fan out one request per function.

    Schedulers of standard and durable functions are listed together, and
    each carries `function_kind`. Pass `function_kind` to list one kind
    only.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        function_kind (FunctionKindFilter | Unset): A function kind to filter a list by. Unlike
            `FunctionKind` it has no
            default: omitting the filter includes both kinds.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionSchedulerListResponse
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
function_kind=function_kind,

    )).parsed
