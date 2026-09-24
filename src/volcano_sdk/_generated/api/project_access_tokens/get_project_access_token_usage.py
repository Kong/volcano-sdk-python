from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_access_token_usage import ProjectAccessTokenUsage
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    token_id: UUID | str,
    *,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/access-tokens/{token_id}/usage".format(id=quote(str(id), safe=""),token_id=quote(str(token_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectAccessTokenUsage | None:
    if response.status_code == 200:
        response_200 = ProjectAccessTokenUsage.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectAccessTokenUsage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    token_id: UUID | str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Error | ProjectAccessTokenUsage]:
    """ Per-day request counts for one access token

     Returns a zero-filled daily series of request counts for a single token,
    oldest first, so the response always has exactly `days` entries.

    `days` defaults to 30 and is capped at 60, matching how long per-day
    counts are retained.

    A project access token may read only its own usage; asking for another
    token's returns `403`. A platform token may read any token in the
    project.

    Args:
        id (UUID):
        token_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectAccessTokenUsage]
     """


    kwargs = request_kwargs(
        id=id,
token_id=token_id,
days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    token_id: UUID | str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | ProjectAccessTokenUsage | None:
    """ Per-day request counts for one access token

     Returns a zero-filled daily series of request counts for a single token,
    oldest first, so the response always has exactly `days` entries.

    `days` defaults to 30 and is capped at 60, matching how long per-day
    counts are retained.

    A project access token may read only its own usage; asking for another
    token's returns `403`. A platform token may read any token in the
    project.

    Args:
        id (UUID):
        token_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectAccessTokenUsage
     """


    return sync_detailed(
        id=id,
token_id=token_id,
client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    token_id: UUID | str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Error | ProjectAccessTokenUsage]:
    """ Per-day request counts for one access token

     Returns a zero-filled daily series of request counts for a single token,
    oldest first, so the response always has exactly `days` entries.

    `days` defaults to 30 and is capped at 60, matching how long per-day
    counts are retained.

    A project access token may read only its own usage; asking for another
    token's returns `403`. A platform token may read any token in the
    project.

    Args:
        id (UUID):
        token_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectAccessTokenUsage]
     """


    kwargs = request_kwargs(
        id=id,
token_id=token_id,
days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    token_id: UUID | str,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | ProjectAccessTokenUsage | None:
    """ Per-day request counts for one access token

     Returns a zero-filled daily series of request counts for a single token,
    oldest first, so the response always has exactly `days` entries.

    `days` defaults to 30 and is capped at 60, matching how long per-day
    counts are retained.

    A project access token may read only its own usage; asking for another
    token's returns `403`. A platform token may read any token in the
    project.

    Args:
        id (UUID):
        token_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectAccessTokenUsage
     """


    return (await asyncio_detailed(
        id=id,
token_id=token_id,
client=client,
days=days,

    )).parsed
