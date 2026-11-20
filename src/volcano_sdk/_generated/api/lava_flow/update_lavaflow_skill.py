from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_skill import LavaflowSkill
from ...models.lavaflow_skill_error import LavaflowSkillError
from ...models.lavaflow_skill_update import LavaflowSkillUpdate
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    skill_id: UUID | str,
    *,
    body: LavaflowSkillUpdate,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/lavaflow/skills/{skill_id}".format(skill_id=quote(str(skill_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSkill | LavaflowSkillError | None:
    if response.status_code == 200:
        response_200 = LavaflowSkill.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = LavaflowSkillError.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSkill | LavaflowSkillError]:
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
    body: LavaflowSkillUpdate,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowSkill | LavaflowSkillError]:
    """ Change a LavaFlow skill

     Changes only the fields you send: a skill's `description`, `body` or
    `applies_to`, or its `status`: `active` activates a proposed skill or
    restores a retired one, and `retired` retires it. `applies_to` merges
    member by member: an omitted member keeps its value, and a list you
    send replaces it, so `[]` clears it. Citations can't be changed.
    A skill is a standing instruction to LavaFlow, so only the project's
    owner changes one, signed in as a person: with a
    `volcano login` token whose sign-in is live, or a platform token with
    an expiry. A change other than retiring also needs the owner's GitHub
    account to be able to push to the project's repository. A project
    access token, MCP, a platform token that never expires, a sign-in
    that ended, an owner who can't push, and a project with no repository
    get `403` with code `person_required`, and nothing is saved. Retiring
    needs no repository. Nothing is saved either when the push check
    can't be answered (`429` or `503`, with `Retry-After`).

    A project keeps its 200 most recently retired skills: retiring
    another deletes the oldest retired skill and its versions.

    Every change but retiring passes the skill check. Only a change to
    the text adds a version; activating or restoring doesn't. Text that
    holds a credential, a project secret value, an email address, a link
    or a host name, an invisible or control character, a CI-skip
    directive, or an instruction to skip or weaken tests, CI or
    LavaFlow's rules answers `400` with code `skill_refused` and the
    `rules` it failed; nothing is saved, and the text is not kept. When
    the check can't run, the change answers `503` with code
    `scan_unavailable` and `Retry-After`.

    Retiring works while the project's `lavaflow.skills` capability is
    unavailable. Any other change answers `400` with code
    `feature_unavailable` then.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):
        body (LavaflowSkillUpdate): The fields to change. An omitted field keeps its value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkill | LavaflowSkillError]
     """


    kwargs = request_kwargs(
        skill_id=skill_id,
body=body,
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
    body: LavaflowSkillUpdate,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowSkill | LavaflowSkillError | None:
    """ Change a LavaFlow skill

     Changes only the fields you send: a skill's `description`, `body` or
    `applies_to`, or its `status`: `active` activates a proposed skill or
    restores a retired one, and `retired` retires it. `applies_to` merges
    member by member: an omitted member keeps its value, and a list you
    send replaces it, so `[]` clears it. Citations can't be changed.
    A skill is a standing instruction to LavaFlow, so only the project's
    owner changes one, signed in as a person: with a
    `volcano login` token whose sign-in is live, or a platform token with
    an expiry. A change other than retiring also needs the owner's GitHub
    account to be able to push to the project's repository. A project
    access token, MCP, a platform token that never expires, a sign-in
    that ended, an owner who can't push, and a project with no repository
    get `403` with code `person_required`, and nothing is saved. Retiring
    needs no repository. Nothing is saved either when the push check
    can't be answered (`429` or `503`, with `Retry-After`).

    A project keeps its 200 most recently retired skills: retiring
    another deletes the oldest retired skill and its versions.

    Every change but retiring passes the skill check. Only a change to
    the text adds a version; activating or restoring doesn't. Text that
    holds a credential, a project secret value, an email address, a link
    or a host name, an invisible or control character, a CI-skip
    directive, or an instruction to skip or weaken tests, CI or
    LavaFlow's rules answers `400` with code `skill_refused` and the
    `rules` it failed; nothing is saved, and the text is not kept. When
    the check can't run, the change answers `503` with code
    `scan_unavailable` and `Retry-After`.

    Retiring works while the project's `lavaflow.skills` capability is
    unavailable. Any other change answers `400` with code
    `feature_unavailable` then.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):
        body (LavaflowSkillUpdate): The fields to change. An omitted field keeps its value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkill | LavaflowSkillError
     """


    return sync_detailed(
        skill_id=skill_id,
client=client,
body=body,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    skill_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: LavaflowSkillUpdate,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowSkill | LavaflowSkillError]:
    """ Change a LavaFlow skill

     Changes only the fields you send: a skill's `description`, `body` or
    `applies_to`, or its `status`: `active` activates a proposed skill or
    restores a retired one, and `retired` retires it. `applies_to` merges
    member by member: an omitted member keeps its value, and a list you
    send replaces it, so `[]` clears it. Citations can't be changed.
    A skill is a standing instruction to LavaFlow, so only the project's
    owner changes one, signed in as a person: with a
    `volcano login` token whose sign-in is live, or a platform token with
    an expiry. A change other than retiring also needs the owner's GitHub
    account to be able to push to the project's repository. A project
    access token, MCP, a platform token that never expires, a sign-in
    that ended, an owner who can't push, and a project with no repository
    get `403` with code `person_required`, and nothing is saved. Retiring
    needs no repository. Nothing is saved either when the push check
    can't be answered (`429` or `503`, with `Retry-After`).

    A project keeps its 200 most recently retired skills: retiring
    another deletes the oldest retired skill and its versions.

    Every change but retiring passes the skill check. Only a change to
    the text adds a version; activating or restoring doesn't. Text that
    holds a credential, a project secret value, an email address, a link
    or a host name, an invisible or control character, a CI-skip
    directive, or an instruction to skip or weaken tests, CI or
    LavaFlow's rules answers `400` with code `skill_refused` and the
    `rules` it failed; nothing is saved, and the text is not kept. When
    the check can't run, the change answers `503` with code
    `scan_unavailable` and `Retry-After`.

    Retiring works while the project's `lavaflow.skills` capability is
    unavailable. Any other change answers `400` with code
    `feature_unavailable` then.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):
        body (LavaflowSkillUpdate): The fields to change. An omitted field keeps its value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSkill | LavaflowSkillError]
     """


    kwargs = request_kwargs(
        skill_id=skill_id,
body=body,
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
    body: LavaflowSkillUpdate,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowSkill | LavaflowSkillError | None:
    """ Change a LavaFlow skill

     Changes only the fields you send: a skill's `description`, `body` or
    `applies_to`, or its `status`: `active` activates a proposed skill or
    restores a retired one, and `retired` retires it. `applies_to` merges
    member by member: an omitted member keeps its value, and a list you
    send replaces it, so `[]` clears it. Citations can't be changed.
    A skill is a standing instruction to LavaFlow, so only the project's
    owner changes one, signed in as a person: with a
    `volcano login` token whose sign-in is live, or a platform token with
    an expiry. A change other than retiring also needs the owner's GitHub
    account to be able to push to the project's repository. A project
    access token, MCP, a platform token that never expires, a sign-in
    that ended, an owner who can't push, and a project with no repository
    get `403` with code `person_required`, and nothing is saved. Retiring
    needs no repository. Nothing is saved either when the push check
    can't be answered (`429` or `503`, with `Retry-After`).

    A project keeps its 200 most recently retired skills: retiring
    another deletes the oldest retired skill and its versions.

    Every change but retiring passes the skill check. Only a change to
    the text adds a version; activating or restoring doesn't. Text that
    holds a credential, a project secret value, an email address, a link
    or a host name, an invisible or control character, a CI-skip
    directive, or an instruction to skip or weaken tests, CI or
    LavaFlow's rules answers `400` with code `skill_refused` and the
    `rules` it failed; nothing is saved, and the text is not kept. When
    the check can't run, the change answers `503` with code
    `scan_unavailable` and `Retry-After`.

    Retiring works while the project's `lavaflow.skills` capability is
    unavailable. Any other change answers `400` with code
    `feature_unavailable` then.

    Args:
        skill_id (UUID):
        project_id (UUID | Unset):
        body (LavaflowSkillUpdate): The fields to change. An omitted field keeps its value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSkill | LavaflowSkillError
     """


    return (await asyncio_detailed(
        skill_id=skill_id,
client=client,
body=body,
project_id=project_id,

    )).parsed
