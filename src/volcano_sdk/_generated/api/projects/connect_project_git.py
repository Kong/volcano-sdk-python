from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.connect_project_git_request import ConnectProjectGitRequest
from ...models.error import Error
from ...models.project_git_connection import ProjectGitConnection
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: ConnectProjectGitRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/git-connection".format(id=quote(str(id), safe=""),),
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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

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
    body: ConnectProjectGitRequest,

) -> Response[Error | ProjectGitConnection]:
    """ Connect or update a project's repo connection

     Full replace, following Vercel's model: many projects may point at the
    same repo, so this only binds the project — it never creates or
    deletes git-provider state. Used for both the initial connect and
    later edits (repo change, root directory, production branch).
    Resolves the repository_id or repo_full_name selector against the repos
    accessible through installation_id via connection_id's stored GitHub
    user token, then persists repository metadata only from that validated
    GitHub response.

    Args:
        id (UUID):
        body (ConnectProjectGitRequest):

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
    body: ConnectProjectGitRequest,

) -> Error | ProjectGitConnection | None:
    """ Connect or update a project's repo connection

     Full replace, following Vercel's model: many projects may point at the
    same repo, so this only binds the project — it never creates or
    deletes git-provider state. Used for both the initial connect and
    later edits (repo change, root directory, production branch).
    Resolves the repository_id or repo_full_name selector against the repos
    accessible through installation_id via connection_id's stored GitHub
    user token, then persists repository metadata only from that validated
    GitHub response.

    Args:
        id (UUID):
        body (ConnectProjectGitRequest):

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
    body: ConnectProjectGitRequest,

) -> Response[Error | ProjectGitConnection]:
    """ Connect or update a project's repo connection

     Full replace, following Vercel's model: many projects may point at the
    same repo, so this only binds the project — it never creates or
    deletes git-provider state. Used for both the initial connect and
    later edits (repo change, root directory, production branch).
    Resolves the repository_id or repo_full_name selector against the repos
    accessible through installation_id via connection_id's stored GitHub
    user token, then persists repository metadata only from that validated
    GitHub response.

    Args:
        id (UUID):
        body (ConnectProjectGitRequest):

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
    body: ConnectProjectGitRequest,

) -> Error | ProjectGitConnection | None:
    """ Connect or update a project's repo connection

     Full replace, following Vercel's model: many projects may point at the
    same repo, so this only binds the project — it never creates or
    deletes git-provider state. Used for both the initial connect and
    later edits (repo change, root directory, production branch).
    Resolves the repository_id or repo_full_name selector against the repos
    accessible through installation_id via connection_id's stored GitHub
    user token, then persists repository metadata only from that validated
    GitHub response.

    Args:
        id (UUID):
        body (ConnectProjectGitRequest):

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
