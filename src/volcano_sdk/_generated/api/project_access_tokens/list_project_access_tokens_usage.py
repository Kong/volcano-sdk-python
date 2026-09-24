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



def _get_kwargs(
    id: UUID,
    *,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/access-tokens/usage".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | list[ProjectAccessTokenUsage] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = ProjectAccessTokenUsage.from_dict(response_200_item_data)



            response_200.append(response_200_item)

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | list[ProjectAccessTokenUsage]]:
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
    days: int | Unset = 30,

) -> Response[Error | list[ProjectAccessTokenUsage]]:
    """ Per-day request counts for every access token in a project

     Returns a zero-filled daily series of request counts for each of the
    project's access tokens, oldest first. Every day in the window is
    present, so a gap reads as zero rather than missing.

    Revoked tokens are included, because the traffic they made before
    revocation is usually the reason you are looking.

    `days` defaults to 30 and is capped at 60, which is also how long per-day
    counts are retained — a longer window cannot be answered.

    A platform token sees every token in the project. A project access token
    sees only its own row, so it can watch its own traffic without being
    able to enumerate the project's other credentials by name.

    Args:
        id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[ProjectAccessTokenUsage]]
     """


    kwargs = _get_kwargs(
        id=id,
days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | list[ProjectAccessTokenUsage] | None:
    """ Per-day request counts for every access token in a project

     Returns a zero-filled daily series of request counts for each of the
    project's access tokens, oldest first. Every day in the window is
    present, so a gap reads as zero rather than missing.

    Revoked tokens are included, because the traffic they made before
    revocation is usually the reason you are looking.

    `days` defaults to 30 and is capped at 60, which is also how long per-day
    counts are retained — a longer window cannot be answered.

    A platform token sees every token in the project. A project access token
    sees only its own row, so it can watch its own traffic without being
    able to enumerate the project's other credentials by name.

    Args:
        id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[ProjectAccessTokenUsage]
     """


    return sync_detailed(
        id=id,
client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Error | list[ProjectAccessTokenUsage]]:
    """ Per-day request counts for every access token in a project

     Returns a zero-filled daily series of request counts for each of the
    project's access tokens, oldest first. Every day in the window is
    present, so a gap reads as zero rather than missing.

    Revoked tokens are included, because the traffic they made before
    revocation is usually the reason you are looking.

    `days` defaults to 30 and is capped at 60, which is also how long per-day
    counts are retained — a longer window cannot be answered.

    A platform token sees every token in the project. A project access token
    sees only its own row, so it can watch its own traffic without being
    able to enumerate the project's other credentials by name.

    Args:
        id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | list[ProjectAccessTokenUsage]]
     """


    kwargs = _get_kwargs(
        id=id,
days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | list[ProjectAccessTokenUsage] | None:
    """ Per-day request counts for every access token in a project

     Returns a zero-filled daily series of request counts for each of the
    project's access tokens, oldest first. Every day in the window is
    present, so a gap reads as zero rather than missing.

    Revoked tokens are included, because the traffic they made before
    revocation is usually the reason you are looking.

    `days` defaults to 30 and is capped at 60, which is also how long per-day
    counts are retained — a longer window cannot be answered.

    A platform token sees every token in the project. A project access token
    sees only its own row, so it can watch its own traffic without being
    able to enumerate the project's other credentials by name.

    Args:
        id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | list[ProjectAccessTokenUsage]
     """


    return (await asyncio_detailed(
        id=id,
client=client,
days=days,

    )).parsed
