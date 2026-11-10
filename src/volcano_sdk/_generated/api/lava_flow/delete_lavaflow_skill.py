from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
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
        "method": "delete",
        "url": "/lavaflow/skills/{skill_id}".format(skill_id=quote(str(skill_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
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

) -> Response[Any | Error]:
    """ Delete a LavaFlow skill

     Deletes a skill and every version of its text. A record that it
    existed stays, without its text. Only the project's owner deletes a
    skill, signed in as a person: with a `volcano
    login` token whose sign-in is live, or a platform token with an
    expiry. A project access token, MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Deleting needs no repository, and works while the
    project's `lavaflow.skills` capability is unavailable.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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

) -> Any | Error | None:
    """ Delete a LavaFlow skill

     Deletes a skill and every version of its text. A record that it
    existed stays, without its text. Only the project's owner deletes a
    skill, signed in as a person: with a `volcano
    login` token whose sign-in is live, or a platform token with an
    expiry. A project access token, MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Deleting needs no repository, and works while the
    project's `lavaflow.skills` capability is unavailable.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
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

) -> Response[Any | Error]:
    """ Delete a LavaFlow skill

     Deletes a skill and every version of its text. A record that it
    existed stays, without its text. Only the project's owner deletes a
    skill, signed in as a person: with a `volcano
    login` token whose sign-in is live, or a platform token with an
    expiry. A project access token, MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Deleting needs no repository, and works while the
    project's `lavaflow.skills` capability is unavailable.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
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

) -> Any | Error | None:
    """ Delete a LavaFlow skill

     Deletes a skill and every version of its text. A record that it
    existed stays, without its text. Only the project's owner deletes a
    skill, signed in as a person: with a `volcano
    login` token whose sign-in is live, or a platform token with an
    expiry. A project access token, MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Deleting needs no repository, and works while the
    project's `lavaflow.skills` capability is unavailable.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
client=client,
project_id=project_id,

    )).parsed
