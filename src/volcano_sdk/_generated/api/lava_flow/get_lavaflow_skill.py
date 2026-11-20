from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_skill import LavaflowSkill
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    skill_id: UUID | str,
    *,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/skills/{skill_id}".format(skill_id=quote(str(skill_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSkill | None:
    if response.status_code == 200:
        response_200 = LavaflowSkill.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSkill]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    skill_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowSkill]:
    """ Get a LavaFlow skill

     Returns one of a project's skills with its active version. The skill's
    project authorizes the read, so `project_id` is optional. Project
    access tokens can read skills, including read-only ones.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkill]
     """


    kwargs = request_kwargs(
        skill_id=skill_id,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    skill_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowSkill | None:
    """ Get a LavaFlow skill

     Returns one of a project's skills with its active version. The skill's
    project authorizes the read, so `project_id` is optional. Project
    access tokens can read skills, including read-only ones.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkill
     """


    return sync_detailed(
        skill_id=skill_id,
client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    skill_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowSkill]:
    """ Get a LavaFlow skill

     Returns one of a project's skills with its active version. The skill's
    project authorizes the read, so `project_id` is optional. Project
    access tokens can read skills, including read-only ones.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkill]
     """


    kwargs = request_kwargs(
        skill_id=skill_id,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    skill_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowSkill | None:
    """ Get a LavaFlow skill

     Returns one of a project's skills with its active version. The skill's
    project authorizes the read, so `project_id` is optional. Project
    access tokens can read skills, including read-only ones.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkill
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
client=client,
project_id=project_id,

    )).parsed
