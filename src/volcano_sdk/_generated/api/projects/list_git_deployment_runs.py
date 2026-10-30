from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.git_deployment_run_status import check_git_deployment_run_status
from ...models.git_deployment_run_status import GitDeploymentRunStatus
from ...models.paginated_git_deployment_runs import PaginatedGitDeploymentRuns
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: GitDeploymentRunStatus | Unset = UNSET,
    branch: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status

    params["branch"] = branch


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/git-deployment-runs".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedGitDeploymentRuns | None:
    if response.status_code == 200:
        response_200 = PaginatedGitDeploymentRuns.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedGitDeploymentRuns]:
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
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: GitDeploymentRunStatus | Unset = UNSET,
    branch: str | Unset = UNSET,

) -> Response[Error | PaginatedGitDeploymentRuns]:
    """ List a project's Git deployment runs

     Lists the deployment runs Git auto deploy recorded for the project,
    newest push first. Each push to the production branch records one run,
    which says whether the push deployed and, when it failed or was
    skipped, why.

    A run that applied migrations names the migration run it started on
    each database. Get one at
    `GET /projects/{id}/databases/{databaseName}/migration-runs/{runId}`
    for its files.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (GitDeploymentRunStatus | Unset): Where a run is. `pending` and `running` have not
            ended. `succeeded`: every deployment the run dispatched succeeded, or the commit only had
            migrations to apply. `failed`: `error` says why. `superseded`: a newer push replaced the
            run before it started. `skipped`: there was nothing to deploy; `error` says why.
        branch (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedGitDeploymentRuns]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
status=status,
branch=branch,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: GitDeploymentRunStatus | Unset = UNSET,
    branch: str | Unset = UNSET,

) -> Error | PaginatedGitDeploymentRuns | None:
    """ List a project's Git deployment runs

     Lists the deployment runs Git auto deploy recorded for the project,
    newest push first. Each push to the production branch records one run,
    which says whether the push deployed and, when it failed or was
    skipped, why.

    A run that applied migrations names the migration run it started on
    each database. Get one at
    `GET /projects/{id}/databases/{databaseName}/migration-runs/{runId}`
    for its files.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (GitDeploymentRunStatus | Unset): Where a run is. `pending` and `running` have not
            ended. `succeeded`: every deployment the run dispatched succeeded, or the commit only had
            migrations to apply. `failed`: `error` says why. `superseded`: a newer push replaced the
            run before it started. `skipped`: there was nothing to deploy; `error` says why.
        branch (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedGitDeploymentRuns
     """


    return sync_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
status=status,
branch=branch,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: GitDeploymentRunStatus | Unset = UNSET,
    branch: str | Unset = UNSET,

) -> Response[Error | PaginatedGitDeploymentRuns]:
    """ List a project's Git deployment runs

     Lists the deployment runs Git auto deploy recorded for the project,
    newest push first. Each push to the production branch records one run,
    which says whether the push deployed and, when it failed or was
    skipped, why.

    A run that applied migrations names the migration run it started on
    each database. Get one at
    `GET /projects/{id}/databases/{databaseName}/migration-runs/{runId}`
    for its files.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (GitDeploymentRunStatus | Unset): Where a run is. `pending` and `running` have not
            ended. `succeeded`: every deployment the run dispatched succeeded, or the commit only had
            migrations to apply. `failed`: `error` says why. `superseded`: a newer push replaced the
            run before it started. `skipped`: there was nothing to deploy; `error` says why.
        branch (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedGitDeploymentRuns]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
status=status,
branch=branch,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: GitDeploymentRunStatus | Unset = UNSET,
    branch: str | Unset = UNSET,

) -> Error | PaginatedGitDeploymentRuns | None:
    """ List a project's Git deployment runs

     Lists the deployment runs Git auto deploy recorded for the project,
    newest push first. Each push to the production branch records one run,
    which says whether the push deployed and, when it failed or was
    skipped, why.

    A run that applied migrations names the migration run it started on
    each database. Get one at
    `GET /projects/{id}/databases/{databaseName}/migration-runs/{runId}`
    for its files.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (GitDeploymentRunStatus | Unset): Where a run is. `pending` and `running` have not
            ended. `succeeded`: every deployment the run dispatched succeeded, or the commit only had
            migrations to apply. `failed`: `error` says why. `superseded`: a newer push replaced the
            run before it started. `skipped`: there was nothing to deploy; `error` says why.
        branch (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedGitDeploymentRuns
     """


    return (await asyncio_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
status=status,
branch=branch,

    )).parsed
