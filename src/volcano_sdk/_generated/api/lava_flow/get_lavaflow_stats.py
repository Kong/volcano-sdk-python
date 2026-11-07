from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_lavaflow_stats_category import check_get_lavaflow_stats_category
from ...models.get_lavaflow_stats_category import GetLavaflowStatsCategory
from ...models.lavaflow_stats import LavaflowStats
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    days: int | Unset = 30,
    category: GetLavaflowStatsCategory | Unset = UNSET,

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
        "url": "/lavaflow/stats",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowStats | None:
    if response.status_code == 200:
        response_200 = LavaflowStats.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowStats]:
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
    category: GetLavaflowStatsCategory | Unset = UNSET,

) -> Response[Error | LavaflowStats]:
    """ Get LavaFlow stats

     Counts the issues LavaFlow took on and the pull requests it opened per
    UTC day, oldest first, with every day in the window present. Merges
    never count. The window ends today, which is partial. The totals equal
    the sum of `days` and of the per-resource counts from
    `GET /lavaflow/resources` for the same project, `days` and `category`.

    `category` counts only runs in that category. These counts are issues
    taken on and pull requests opened, while `GET /lavaflow/runs` counts
    runs, so the two need not match.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (GetLavaflowStatsCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowStats]
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
    category: GetLavaflowStatsCategory | Unset = UNSET,

) -> Error | LavaflowStats | None:
    """ Get LavaFlow stats

     Counts the issues LavaFlow took on and the pull requests it opened per
    UTC day, oldest first, with every day in the window present. Merges
    never count. The window ends today, which is partial. The totals equal
    the sum of `days` and of the per-resource counts from
    `GET /lavaflow/resources` for the same project, `days` and `category`.

    `category` counts only runs in that category. These counts are issues
    taken on and pull requests opened, while `GET /lavaflow/runs` counts
    runs, so the two need not match.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (GetLavaflowStatsCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowStats
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
    category: GetLavaflowStatsCategory | Unset = UNSET,

) -> Response[Error | LavaflowStats]:
    """ Get LavaFlow stats

     Counts the issues LavaFlow took on and the pull requests it opened per
    UTC day, oldest first, with every day in the window present. Merges
    never count. The window ends today, which is partial. The totals equal
    the sum of `days` and of the per-resource counts from
    `GET /lavaflow/resources` for the same project, `days` and `category`.

    `category` counts only runs in that category. These counts are issues
    taken on and pull requests opened, while `GET /lavaflow/runs` counts
    runs, so the two need not match.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (GetLavaflowStatsCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowStats]
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
    category: GetLavaflowStatsCategory | Unset = UNSET,

) -> Error | LavaflowStats | None:
    """ Get LavaFlow stats

     Counts the issues LavaFlow took on and the pull requests it opened per
    UTC day, oldest first, with every day in the window present. Merges
    never count. The window ends today, which is partial. The totals equal
    the sum of `days` and of the per-resource counts from
    `GET /lavaflow/resources` for the same project, `days` and `category`.

    `category` counts only runs in that category. These counts are issues
    taken on and pull requests opened, while `GET /lavaflow/runs` counts
    runs, so the two need not match.

    Args:
        project_id (UUID):
        days (int | Unset):  Default: 30.
        category (GetLavaflowStatsCategory | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowStats
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
days=days,
category=category,

    )).parsed
