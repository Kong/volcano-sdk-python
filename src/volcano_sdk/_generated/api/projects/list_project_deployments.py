from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.list_project_deployments_resource_type import check_list_project_deployments_resource_type
from ...models.list_project_deployments_resource_type import ListProjectDeploymentsResourceType
from ...models.paginated_project_deployments import PaginatedProjectDeployments
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    id: UUID,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    search: str | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListProjectDeploymentsResourceType | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["search"] = search

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after

    json_resource_type: str | Unset = UNSET
    if not isinstance(resource_type, Unset):
        json_resource_type = resource_type

    params["resource_type"] = json_resource_type


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/deployments".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedProjectDeployments | None:
    if response.status_code == 200:
        response_200 = PaginatedProjectDeployments.from_dict(response.json())



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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedProjectDeployments]:
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
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListProjectDeploymentsResourceType | Unset = UNSET,

) -> Response[Error | PaginatedProjectDeployments]:
    """ List deployments in a project

     Lists Function and Frontend deployment attempts across the project,
    ordered most-recent first. Each item includes a normalized resource
    reference so clients can render both resource types without extra
    fetches.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListProjectDeploymentsResourceType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectDeployments]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
created_after=created_after,
resource_type=resource_type,

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
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListProjectDeploymentsResourceType | Unset = UNSET,

) -> Error | PaginatedProjectDeployments | None:
    """ List deployments in a project

     Lists Function and Frontend deployment attempts across the project,
    ordered most-recent first. Each item includes a normalized resource
    reference so clients can render both resource types without extra
    fetches.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListProjectDeploymentsResourceType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectDeployments
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
created_after=created_after,
resource_type=resource_type,

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
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListProjectDeploymentsResourceType | Unset = UNSET,

) -> Response[Error | PaginatedProjectDeployments]:
    """ List deployments in a project

     Lists Function and Frontend deployment attempts across the project,
    ordered most-recent first. Each item includes a normalized resource
    reference so clients can render both resource types without extra
    fetches.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListProjectDeploymentsResourceType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectDeployments]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
search=search,
created_after=created_after,
resource_type=resource_type,

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
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListProjectDeploymentsResourceType | Unset = UNSET,

) -> Error | PaginatedProjectDeployments | None:
    """ List deployments in a project

     Lists Function and Frontend deployment attempts across the project,
    ordered most-recent first. Each item includes a normalized resource
    reference so clients can render both resource types without extra
    fetches.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        search (str | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListProjectDeploymentsResourceType | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectDeployments
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
created_after=created_after,
resource_type=resource_type,

    )).parsed
