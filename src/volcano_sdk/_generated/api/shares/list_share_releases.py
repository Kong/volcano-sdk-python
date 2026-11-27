from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_share_releases import PaginatedShareReleases
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["share_id"] = share_id

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/share-releases",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedShareReleases | None:
    if response.status_code == 200:
        response_200 = PaginatedShareReleases.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedShareReleases]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Response[Error | PaginatedShareReleases]:
    """ List a deploy link's releases

     Pages the link's releases, newest first. Follow `next_cursor` while
    `has_more` is true.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedShareReleases]
     """


    kwargs = request_kwargs(
        share_id=share_id,
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
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Error | PaginatedShareReleases | None:
    """ List a deploy link's releases

     Pages the link's releases, newest first. Follow `next_cursor` while
    `has_more` is true.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedShareReleases
     """


    return sync_detailed(
        client=client,
share_id=share_id,
project_id=project_id,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Response[Error | PaginatedShareReleases]:
    """ List a deploy link's releases

     Pages the link's releases, newest first. Follow `next_cursor` while
    `has_more` is true.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedShareReleases]
     """


    kwargs = request_kwargs(
        share_id=share_id,
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
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Error | PaginatedShareReleases | None:
    """ List a deploy link's releases

     Pages the link's releases, newest first. Follow `next_cursor` while
    `has_more` is true.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedShareReleases
     """


    return (await asyncio_detailed(
        client=client,
share_id=share_id,
project_id=project_id,
limit=limit,
cursor=cursor,

    )).parsed
