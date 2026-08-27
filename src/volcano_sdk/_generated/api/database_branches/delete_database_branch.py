from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_database_branch_response_202 import DeleteDatabaseBranchResponse202
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    branch_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/databases/{database_name}/branches/{branch_name}".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),branch_name=quote(str(branch_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteDatabaseBranchResponse202 | Error | None:
    if response.status_code == 202:
        response_202 = DeleteDatabaseBranchResponse202.from_dict(response.json())



        return response_202

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteDatabaseBranchResponse202 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteDatabaseBranchResponse202 | Error]:
    """ Delete a branch

     Marks the branch for teardown and returns immediately. The branch stops
    accepting connections at once; its fork and its row are removed by a
    background job, so a provider outage cannot leave the call hanging or the
    branch half-deleted.

    Deleting a branch that is still provisioning is allowed and stops the
    build, and repeating the call while teardown is in progress is accepted
    again. Once the branch is gone the call returns `404`.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDatabaseBranchResponse202 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
branch_name=branch_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteDatabaseBranchResponse202 | Error | None:
    """ Delete a branch

     Marks the branch for teardown and returns immediately. The branch stops
    accepting connections at once; its fork and its row are removed by a
    background job, so a provider outage cannot leave the call hanging or the
    branch half-deleted.

    Deleting a branch that is still provisioning is allowed and stops the
    build, and repeating the call while teardown is in progress is accepted
    again. Once the branch is gone the call returns `404`.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDatabaseBranchResponse202 | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
branch_name=branch_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteDatabaseBranchResponse202 | Error]:
    """ Delete a branch

     Marks the branch for teardown and returns immediately. The branch stops
    accepting connections at once; its fork and its row are removed by a
    background job, so a provider outage cannot leave the call hanging or the
    branch half-deleted.

    Deleting a branch that is still provisioning is allowed and stops the
    build, and repeating the call while teardown is in progress is accepted
    again. Once the branch is gone the call returns `404`.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDatabaseBranchResponse202 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
branch_name=branch_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteDatabaseBranchResponse202 | Error | None:
    """ Delete a branch

     Marks the branch for teardown and returns immediately. The branch stops
    accepting connections at once; its fork and its row are removed by a
    background job, so a provider outage cannot leave the call hanging or the
    branch half-deleted.

    Deleting a branch that is still provisioning is allowed and stops the
    build, and repeating the call while teardown is in progress is accepted
    again. Once the branch is gone the call returns `404`.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDatabaseBranchResponse202 | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
branch_name=branch_name,
client=client,

    )).parsed
