from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_skill_list import LavaflowSkillList
from ...models.lavaflow_skill_status import check_lavaflow_skill_status
from ...models.lavaflow_skill_status import LavaflowSkillStatus
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    status: LavaflowSkillStatus | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/skills",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSkillList | None:
    if response.status_code == 200:
        response_200 = LavaflowSkillList.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSkillList]:
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
    status: LavaflowSkillStatus | Unset = UNSET,

) -> Response[Error | LavaflowSkillList]:
    """ List LavaFlow skills

     Lists the project's skills, newest first: short, cited notes on how
    the project wants something done, with each one's active version,
    counts and source. A project skill belongs to its project and never
    leaves it. Filter by `status`. The list holds at most 350 skills, so
    it has no pages.

    LavaFlow doesn't yet learn skills from corrections to its fixes or
    load them into runs; both come in a later release.

    Project access tokens can list skills, including read-only ones.
    Skills stay readable while the project's `lavaflow.skills` capability
    is unavailable.

    Args:
        project_id (UUID):
        status (LavaflowSkillStatus | Unset): `proposed` waits for the owner to activate it.
            `active` is in force. `retired` is set aside and can be restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkillList]
     """


    kwargs = request_kwargs(
        project_id=project_id,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    status: LavaflowSkillStatus | Unset = UNSET,

) -> Error | LavaflowSkillList | None:
    """ List LavaFlow skills

     Lists the project's skills, newest first: short, cited notes on how
    the project wants something done, with each one's active version,
    counts and source. A project skill belongs to its project and never
    leaves it. Filter by `status`. The list holds at most 350 skills, so
    it has no pages.

    LavaFlow doesn't yet learn skills from corrections to its fixes or
    load them into runs; both come in a later release.

    Project access tokens can list skills, including read-only ones.
    Skills stay readable while the project's `lavaflow.skills` capability
    is unavailable.

    Args:
        project_id (UUID):
        status (LavaflowSkillStatus | Unset): `proposed` waits for the owner to activate it.
            `active` is in force. `retired` is set aside and can be restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkillList
     """


    return sync_detailed(
        client=client,
project_id=project_id,
status=status,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    status: LavaflowSkillStatus | Unset = UNSET,

) -> Response[Error | LavaflowSkillList]:
    """ List LavaFlow skills

     Lists the project's skills, newest first: short, cited notes on how
    the project wants something done, with each one's active version,
    counts and source. A project skill belongs to its project and never
    leaves it. Filter by `status`. The list holds at most 350 skills, so
    it has no pages.

    LavaFlow doesn't yet learn skills from corrections to its fixes or
    load them into runs; both come in a later release.

    Project access tokens can list skills, including read-only ones.
    Skills stay readable while the project's `lavaflow.skills` capability
    is unavailable.

    Args:
        project_id (UUID):
        status (LavaflowSkillStatus | Unset): `proposed` waits for the owner to activate it.
            `active` is in force. `retired` is set aside and can be restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkillList]
     """


    kwargs = request_kwargs(
        project_id=project_id,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    status: LavaflowSkillStatus | Unset = UNSET,

) -> Error | LavaflowSkillList | None:
    """ List LavaFlow skills

     Lists the project's skills, newest first: short, cited notes on how
    the project wants something done, with each one's active version,
    counts and source. A project skill belongs to its project and never
    leaves it. Filter by `status`. The list holds at most 350 skills, so
    it has no pages.

    LavaFlow doesn't yet learn skills from corrections to its fixes or
    load them into runs; both come in a later release.

    Project access tokens can list skills, including read-only ones.
    Skills stay readable while the project's `lavaflow.skills` capability
    is unavailable.

    Args:
        project_id (UUID):
        status (LavaflowSkillStatus | Unset): `proposed` waits for the owner to activate it.
            `active` is in force. `retired` is set aside and can be restored.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkillList
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
status=status,

    )).parsed
