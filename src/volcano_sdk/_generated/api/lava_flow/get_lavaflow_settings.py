from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_settings import LavaflowSettings
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/settings",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSettings | None:
    if response.status_code == 200:
        response_200 = LavaflowSettings.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSettings]:
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

) -> Response[Error | LavaflowSettings]:
    """ Get LavaFlow settings

     Returns whether LavaFlow works on the project's issues and how far it
    goes on its own. LavaFlow takes project guidance from the repository's
    AGENTS.md and CLAUDE.md, not from a setting. A project
    that never saved settings returns the defaults, with LavaFlow off.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    `can_update` says whether the caller can save the settings: only the
    project's owner can, with a platform token. Project access tokens can
    read the settings, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSettings]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | LavaflowSettings | None:
    """ Get LavaFlow settings

     Returns whether LavaFlow works on the project's issues and how far it
    goes on its own. LavaFlow takes project guidance from the repository's
    AGENTS.md and CLAUDE.md, not from a setting. A project
    that never saved settings returns the defaults, with LavaFlow off.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    `can_update` says whether the caller can save the settings: only the
    project's owner can, with a platform token. Project access tokens can
    read the settings, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSettings
     """


    return sync_detailed(
        client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | LavaflowSettings]:
    """ Get LavaFlow settings

     Returns whether LavaFlow works on the project's issues and how far it
    goes on its own. LavaFlow takes project guidance from the repository's
    AGENTS.md and CLAUDE.md, not from a setting. A project
    that never saved settings returns the defaults, with LavaFlow off.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    `can_update` says whether the caller can save the settings: only the
    project's owner can, with a platform token. Project access tokens can
    read the settings, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSettings]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | LavaflowSettings | None:
    """ Get LavaFlow settings

     Returns whether LavaFlow works on the project's issues and how far it
    goes on its own. LavaFlow takes project guidance from the repository's
    AGENTS.md and CLAUDE.md, not from a setting. A project
    that never saved settings returns the defaults, with LavaFlow off.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    `can_update` says whether the caller can save the settings: only the
    project's owner can, with a platform token. Project access tokens can
    read the settings, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSettings
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,

    )).parsed
