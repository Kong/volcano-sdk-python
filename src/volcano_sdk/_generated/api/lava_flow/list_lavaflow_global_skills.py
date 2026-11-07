from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_global_skill_list import LavaflowGlobalSkillList
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
        "url": "/lavaflow/global-skills",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowGlobalSkillList | None:
    if response.status_code == 200:
        response_200 = LavaflowGlobalSkillList.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowGlobalSkillList]:
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

) -> Response[Error | LavaflowGlobalSkillList]:
    """ List Volcano's global skills

     Lists the skills Volcano wrote for every project. Volcano writes and
    reviews each one, and none holds customer content. They belong to no
    project, so items carry `scope` and no `project_id`; `project_id`
    authorizes the caller. While the project's `lavaflow.skills`
    capability is unavailable, the list is empty.

    Project access tokens can list them, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowGlobalSkillList]
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

) -> Error | LavaflowGlobalSkillList | None:
    """ List Volcano's global skills

     Lists the skills Volcano wrote for every project. Volcano writes and
    reviews each one, and none holds customer content. They belong to no
    project, so items carry `scope` and no `project_id`; `project_id`
    authorizes the caller. While the project's `lavaflow.skills`
    capability is unavailable, the list is empty.

    Project access tokens can list them, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowGlobalSkillList
     """


    return sync_detailed(
        client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | LavaflowGlobalSkillList]:
    """ List Volcano's global skills

     Lists the skills Volcano wrote for every project. Volcano writes and
    reviews each one, and none holds customer content. They belong to no
    project, so items carry `scope` and no `project_id`; `project_id`
    authorizes the caller. While the project's `lavaflow.skills`
    capability is unavailable, the list is empty.

    Project access tokens can list them, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowGlobalSkillList]
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

) -> Error | LavaflowGlobalSkillList | None:
    """ List Volcano's global skills

     Lists the skills Volcano wrote for every project. Volcano writes and
    reviews each one, and none holds customer content. They belong to no
    project, so items carry `scope` and no `project_id`; `project_id`
    authorizes the caller. While the project's `lavaflow.skills`
    capability is unavailable, the list is empty.

    Project access tokens can list them, including read-only ones.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowGlobalSkillList
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,

    )).parsed
