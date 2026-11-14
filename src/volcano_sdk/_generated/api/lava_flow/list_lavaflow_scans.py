from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_lavaflow_scans import PaginatedLavaflowScans
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/scans",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedLavaflowScans | None:
    if response.status_code == 200:
        response_200 = PaginatedLavaflowScans.from_dict(response.json())



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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedLavaflowScans]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,

) -> Response[Error | PaginatedLavaflowScans]:
    """ List LavaFlow Code Quality scans

     Pages the project's Code Quality scans, newest first. The first page
    starts with the project's waiting scan, if it has one: the deploys
    that went live since the last scan, with `status: waiting` and the
    bound it waits at in `waiting_reason`. A bound never drops a deploy:
    the waiting scan covers every commit since the last one when it
    starts. A platform publication pause is reported as `feature_paused`
    and does not spend the scan's retry allowance. With publication enabled,
    a separate pause on starting runs is reported as `feature_unavailable`.

    Each scan shows the commits it compared, the resources whose deploys
    it covers, what it did with what it found, and the findings whose
    runs were billed. Scans stay readable while LavaFlow or Code Quality
    is off. Project access tokens can read them, including read-only
    ones.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedLavaflowScans]
     """


    kwargs = request_kwargs(
        project_id=project_id,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,

) -> Error | PaginatedLavaflowScans | None:
    """ List LavaFlow Code Quality scans

     Pages the project's Code Quality scans, newest first. The first page
    starts with the project's waiting scan, if it has one: the deploys
    that went live since the last scan, with `status: waiting` and the
    bound it waits at in `waiting_reason`. A bound never drops a deploy:
    the waiting scan covers every commit since the last one when it
    starts. A platform publication pause is reported as `feature_paused`
    and does not spend the scan's retry allowance. With publication enabled,
    a separate pause on starting runs is reported as `feature_unavailable`.

    Each scan shows the commits it compared, the resources whose deploys
    it covers, what it did with what it found, and the findings whose
    runs were billed. Scans stay readable while LavaFlow or Code Quality
    is off. Project access tokens can read them, including read-only
    ones.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedLavaflowScans
     """


    return sync_detailed(
        client=client,
project_id=project_id,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,

) -> Response[Error | PaginatedLavaflowScans]:
    """ List LavaFlow Code Quality scans

     Pages the project's Code Quality scans, newest first. The first page
    starts with the project's waiting scan, if it has one: the deploys
    that went live since the last scan, with `status: waiting` and the
    bound it waits at in `waiting_reason`. A bound never drops a deploy:
    the waiting scan covers every commit since the last one when it
    starts. A platform publication pause is reported as `feature_paused`
    and does not spend the scan's retry allowance. With publication enabled,
    a separate pause on starting runs is reported as `feature_unavailable`.

    Each scan shows the commits it compared, the resources whose deploys
    it covers, what it did with what it found, and the findings whose
    runs were billed. Scans stay readable while LavaFlow or Code Quality
    is off. Project access tokens can read them, including read-only
    ones.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedLavaflowScans]
     """


    kwargs = request_kwargs(
        project_id=project_id,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,

) -> Error | PaginatedLavaflowScans | None:
    """ List LavaFlow Code Quality scans

     Pages the project's Code Quality scans, newest first. The first page
    starts with the project's waiting scan, if it has one: the deploys
    that went live since the last scan, with `status: waiting` and the
    bound it waits at in `waiting_reason`. A bound never drops a deploy:
    the waiting scan covers every commit since the last one when it
    starts. A platform publication pause is reported as `feature_paused`
    and does not spend the scan's retry allowance. With publication enabled,
    a separate pause on starting runs is reported as `feature_unavailable`.

    Each scan shows the commits it compared, the resources whose deploys
    it covers, what it did with what it found, and the findings whose
    runs were billed. Scans stay readable while LavaFlow or Code Quality
    is off. Project access tokens can read them, including read-only
    ones.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedLavaflowScans
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
limit=limit,
cursor=cursor,

    )).parsed
