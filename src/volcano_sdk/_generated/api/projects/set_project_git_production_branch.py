from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_git_connection import ProjectGitConnection
from ...models.set_project_git_production_branch_request import SetProjectGitProductionBranchRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: SetProjectGitProductionBranchRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/git-connection/production-branch".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectGitConnection | None:
    if response.status_code == 200:
        response_200 = ProjectGitConnection.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectGitConnection]:
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
    body: SetProjectGitProductionBranchRequest,

) -> Response[Error | ProjectGitConnection]:
    """ Set the branch a project deploys from

     Changes only the production branch, leaving the repository binding
    alone. PUT /projects/{id}/git-connection can also set it, but that is a
    full rebind: it needs connection_id, installation_id and a repository
    selector resent, and re-resolves the repository against GitHub for a
    field that does not depend on it.

    The branch does not have to exist. It is validated as a Git branch name
    and nothing more, so a project can be pointed at a branch that is about
    to be pushed — the case a repository created empty depends on.

    Setting the branch here marks it as the project's own choice, so a later
    default-branch rename on GitHub no longer moves it. Projects that never
    set one keep following the repository's default branch.

    Args:
        id (UUID):
        body (SetProjectGitProductionBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectGitConnection]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: SetProjectGitProductionBranchRequest,

) -> Error | ProjectGitConnection | None:
    """ Set the branch a project deploys from

     Changes only the production branch, leaving the repository binding
    alone. PUT /projects/{id}/git-connection can also set it, but that is a
    full rebind: it needs connection_id, installation_id and a repository
    selector resent, and re-resolves the repository against GitHub for a
    field that does not depend on it.

    The branch does not have to exist. It is validated as a Git branch name
    and nothing more, so a project can be pointed at a branch that is about
    to be pushed — the case a repository created empty depends on.

    Setting the branch here marks it as the project's own choice, so a later
    default-branch rename on GitHub no longer moves it. Projects that never
    set one keep following the repository's default branch.

    Args:
        id (UUID):
        body (SetProjectGitProductionBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectGitConnection
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: SetProjectGitProductionBranchRequest,

) -> Response[Error | ProjectGitConnection]:
    """ Set the branch a project deploys from

     Changes only the production branch, leaving the repository binding
    alone. PUT /projects/{id}/git-connection can also set it, but that is a
    full rebind: it needs connection_id, installation_id and a repository
    selector resent, and re-resolves the repository against GitHub for a
    field that does not depend on it.

    The branch does not have to exist. It is validated as a Git branch name
    and nothing more, so a project can be pointed at a branch that is about
    to be pushed — the case a repository created empty depends on.

    Setting the branch here marks it as the project's own choice, so a later
    default-branch rename on GitHub no longer moves it. Projects that never
    set one keep following the repository's default branch.

    Args:
        id (UUID):
        body (SetProjectGitProductionBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectGitConnection]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: SetProjectGitProductionBranchRequest,

) -> Error | ProjectGitConnection | None:
    """ Set the branch a project deploys from

     Changes only the production branch, leaving the repository binding
    alone. PUT /projects/{id}/git-connection can also set it, but that is a
    full rebind: it needs connection_id, installation_id and a repository
    selector resent, and re-resolves the repository against GitHub for a
    field that does not depend on it.

    The branch does not have to exist. It is validated as a Git branch name
    and nothing more, so a project can be pointed at a branch that is about
    to be pushed — the case a repository created empty depends on.

    Setting the branch here marks it as the project's own choice, so a later
    default-branch rename on GitHub no longer moves it. Projects that never
    set one keep following the repository's default branch.

    Args:
        id (UUID):
        body (SetProjectGitProductionBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectGitConnection
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
