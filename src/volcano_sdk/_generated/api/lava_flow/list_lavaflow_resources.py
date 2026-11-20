from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_resource_list import LavaflowResourceList
from ...models.list_lavaflow_resources_category import check_list_lavaflow_resources_category
from ...models.list_lavaflow_resources_category import ListLavaflowResourcesCategory
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    days: int | Unset = 30,
    category: ListLavaflowResourcesCategory | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params["days"] = days

    json_category: str | Unset = UNSET
    if not isinstance(category, Unset):
        json_category = category

    params["category"] = json_category


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/resources",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowResourceList | None:
    if response.status_code == 200:
        response_200 = LavaflowResourceList.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowResourceList]:
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
    days: int | Unset = 30,
    category: ListLavaflowResourcesCategory | Unset = UNSET,

) -> Response[Error | LavaflowResourceList]:
    """ List LavaFlow's resources

     Lists every function, durable function and frontend in the project with
    LavaFlow's activity in the window, zeros included, sorted by name. A
    removed resource is listed when it has activity in the window (in that
    category, with `category` set), so the counts add up to
    `GET /lavaflow/stats`.

    `anomaly.flagged` is true when the last 24 hours have at least 3
    issues opened for the resource and at least 3 times its daily average
    over the 29 days before, counting that average as at least 1.

    `category` counts, and flags anomalies from, only runs in that
    category; every current resource is still listed, and
    `last_analyzed_at` counts every run.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (ListLavaflowResourcesCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowResourceList]
     """


    kwargs = request_kwargs(
        project_id=project_id,
days=days,
category=category,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    days: int | Unset = 30,
    category: ListLavaflowResourcesCategory | Unset = UNSET,

) -> Error | LavaflowResourceList | None:
    """ List LavaFlow's resources

     Lists every function, durable function and frontend in the project with
    LavaFlow's activity in the window, zeros included, sorted by name. A
    removed resource is listed when it has activity in the window (in that
    category, with `category` set), so the counts add up to
    `GET /lavaflow/stats`.

    `anomaly.flagged` is true when the last 24 hours have at least 3
    issues opened for the resource and at least 3 times its daily average
    over the 29 days before, counting that average as at least 1.

    `category` counts, and flags anomalies from, only runs in that
    category; every current resource is still listed, and
    `last_analyzed_at` counts every run.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (ListLavaflowResourcesCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowResourceList
     """


    return sync_detailed(
        client=client,
project_id=project_id,
days=days,
category=category,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    days: int | Unset = 30,
    category: ListLavaflowResourcesCategory | Unset = UNSET,

) -> Response[Error | LavaflowResourceList]:
    """ List LavaFlow's resources

     Lists every function, durable function and frontend in the project with
    LavaFlow's activity in the window, zeros included, sorted by name. A
    removed resource is listed when it has activity in the window (in that
    category, with `category` set), so the counts add up to
    `GET /lavaflow/stats`.

    `anomaly.flagged` is true when the last 24 hours have at least 3
    issues opened for the resource and at least 3 times its daily average
    over the 29 days before, counting that average as at least 1.

    `category` counts, and flags anomalies from, only runs in that
    category; every current resource is still listed, and
    `last_analyzed_at` counts every run.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (ListLavaflowResourcesCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowResourceList]
     """


    kwargs = request_kwargs(
        project_id=project_id,
days=days,
category=category,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    days: int | Unset = 30,
    category: ListLavaflowResourcesCategory | Unset = UNSET,

) -> Error | LavaflowResourceList | None:
    """ List LavaFlow's resources

     Lists every function, durable function and frontend in the project with
    LavaFlow's activity in the window, zeros included, sorted by name. A
    removed resource is listed when it has activity in the window (in that
    category, with `category` set), so the counts add up to
    `GET /lavaflow/stats`.

    `anomaly.flagged` is true when the last 24 hours have at least 3
    issues opened for the resource and at least 3 times its daily average
    over the 29 days before, counting that average as at least 1.

    `category` counts, and flags anomalies from, only runs in that
    category; every current resource is still listed, and
    `last_analyzed_at` counts every run.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (ListLavaflowResourcesCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowResourceList
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
days=days,
category=category,

    )).parsed
