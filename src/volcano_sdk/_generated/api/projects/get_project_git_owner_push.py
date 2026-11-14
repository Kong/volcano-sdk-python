from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_git_owner_push import ProjectGitOwnerPush
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/git-connection/owner-push".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectGitOwnerPush | None:
    if response.status_code == 200:
        response_200 = ProjectGitOwnerPush.from_dict(response.json())



        return response_200

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectGitOwnerPush]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectGitOwnerPush]:
    """ Check whether the project owner can push to the connected repository

     Answers whether the project owner's GitHub account can push to the
    repository the project is connected to. Volcano makes the same check
    before it writes to that repository for the project. The repository is
    always the project's connected one; the route takes no repository.

    When `can_push` is false, `reason` says why. The answer can be a few
    seconds old: repeated checks within that time are answered without
    asking GitHub again.

    Checks that ask GitHub draw on an hourly budget for the project and
    another for its owner, shared by all of the owner's projects. Over
    either, the route answers `429` with `Retry-After`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectGitOwnerPush]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectGitOwnerPush | None:
    """ Check whether the project owner can push to the connected repository

     Answers whether the project owner's GitHub account can push to the
    repository the project is connected to. Volcano makes the same check
    before it writes to that repository for the project. The repository is
    always the project's connected one; the route takes no repository.

    When `can_push` is false, `reason` says why. The answer can be a few
    seconds old: repeated checks within that time are answered without
    asking GitHub again.

    Checks that ask GitHub draw on an hourly budget for the project and
    another for its owner, shared by all of the owner's projects. Over
    either, the route answers `429` with `Retry-After`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectGitOwnerPush
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectGitOwnerPush]:
    """ Check whether the project owner can push to the connected repository

     Answers whether the project owner's GitHub account can push to the
    repository the project is connected to. Volcano makes the same check
    before it writes to that repository for the project. The repository is
    always the project's connected one; the route takes no repository.

    When `can_push` is false, `reason` says why. The answer can be a few
    seconds old: repeated checks within that time are answered without
    asking GitHub again.

    Checks that ask GitHub draw on an hourly budget for the project and
    another for its owner, shared by all of the owner's projects. Over
    either, the route answers `429` with `Retry-After`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectGitOwnerPush]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectGitOwnerPush | None:
    """ Check whether the project owner can push to the connected repository

     Answers whether the project owner's GitHub account can push to the
    repository the project is connected to. Volcano makes the same check
    before it writes to that repository for the project. The repository is
    always the project's connected one; the route takes no repository.

    When `can_push` is false, `reason` says why. The answer can be a few
    seconds old: repeated checks within that time are answered without
    asking GitHub again.

    Checks that ask GitHub draw on an hourly budget for the project and
    another for its owner, shared by all of the owner's projects. Over
    either, the route answers `429` with `Retry-After`.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectGitOwnerPush
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
