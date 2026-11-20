from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share_stats import ShareStats
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["share_id"] = share_id

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/share-stats",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ShareStats | None:
    if response.status_code == 200:
        response_200 = ShareStats.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ShareStats]:
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
    days: int | Unset = 30,

) -> Response[Error | ShareStats]:
    """ Get a deploy link's click and deploy counts

     Counts what happened at the link: clicks, previews, confirmations, projects
    created, and how many became ready or failed. Informational only. Visitors
    are counted from a salted hash and no address is stored. Events are kept
    for 90 days, so a `days` above 90 is rejected with `400`.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareStats]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,
days=days,

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
    days: int | Unset = 30,

) -> Error | ShareStats | None:
    """ Get a deploy link's click and deploy counts

     Counts what happened at the link: clicks, previews, confirmations, projects
    created, and how many became ready or failed. Informational only. Visitors
    are counted from a salted hash and no address is stored. Events are kept
    for 90 days, so a `days` above 90 is rejected with `400`.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareStats
     """


    return sync_detailed(
        client=client,
share_id=share_id,
project_id=project_id,
days=days,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,
    days: int | Unset = 30,

) -> Response[Error | ShareStats]:
    """ Get a deploy link's click and deploy counts

     Counts what happened at the link: clicks, previews, confirmations, projects
    created, and how many became ready or failed. Informational only. Visitors
    are counted from a salted hash and no address is stored. Events are kept
    for 90 days, so a `days` above 90 is rejected with `400`.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareStats]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,
days=days,

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
    days: int | Unset = 30,

) -> Error | ShareStats | None:
    """ Get a deploy link's click and deploy counts

     Counts what happened at the link: clicks, previews, confirmations, projects
    created, and how many became ready or failed. Informational only. Visitors
    are counted from a salted hash and no address is stored. Events are kept
    for 90 days, so a `days` above 90 is rejected with `400`.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareStats
     """


    return (await asyncio_detailed(
        client=client,
share_id=share_id,
project_id=project_id,
days=days,

    )).parsed
