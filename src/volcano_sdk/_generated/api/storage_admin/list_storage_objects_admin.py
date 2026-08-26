from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_storage_objects_admin_response_200 import ListStorageObjectsAdminResponse200
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    owner_id: UUID | Unset = UNSET,
    page: int | Unset = 1,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_owner_id: str | Unset = UNSET
    if not isinstance(owner_id, Unset):
        json_owner_id = str(owner_id)
    params["owner_id"] = json_owner_id

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/storage/objects".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ListStorageObjectsAdminResponse200 | None:
    if response.status_code == 200:
        response_200 = ListStorageObjectsAdminResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ListStorageObjectsAdminResponse200]:
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
    owner_id: UUID | Unset = UNSET,
    page: int | Unset = 1,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[ListStorageObjectsAdminResponse200]:
    """ List all storage objects in a project

     Returns a paginated list of all storage objects across all buckets in the project.
    Supports filtering by owner and pagination.

    Args:
        id (UUID):
        owner_id (UUID | Unset):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListStorageObjectsAdminResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
owner_id=owner_id,
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
    owner_id: UUID | Unset = UNSET,
    page: int | Unset = 1,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> ListStorageObjectsAdminResponse200 | None:
    """ List all storage objects in a project

     Returns a paginated list of all storage objects across all buckets in the project.
    Supports filtering by owner and pagination.

    Args:
        id (UUID):
        owner_id (UUID | Unset):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListStorageObjectsAdminResponse200
     """


    return sync_detailed(
        id=id,
client=client,
owner_id=owner_id,
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
    owner_id: UUID | Unset = UNSET,
    page: int | Unset = 1,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> Response[ListStorageObjectsAdminResponse200]:
    """ List all storage objects in a project

     Returns a paginated list of all storage objects across all buckets in the project.
    Supports filtering by owner and pagination.

    Args:
        id (UUID):
        owner_id (UUID | Unset):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ListStorageObjectsAdminResponse200]
     """


    kwargs = _get_kwargs(
        id=id,
owner_id=owner_id,
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
    owner_id: UUID | Unset = UNSET,
    page: int | Unset = 1,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,

) -> ListStorageObjectsAdminResponse200 | None:
    """ List all storage objects in a project

     Returns a paginated list of all storage objects across all buckets in the project.
    Supports filtering by owner and pagination.

    Args:
        id (UUID):
        owner_id (UUID | Unset):
        page (int | Unset):  Default: 1.
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ListStorageObjectsAdminResponse200
     """


    return (await asyncio_detailed(
        id=id,
client=client,
owner_id=owner_id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,

    )).parsed
