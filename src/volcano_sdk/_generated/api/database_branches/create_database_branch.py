from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_database_branch_request import CreateDatabaseBranchRequest
from ...models.database_branch import DatabaseBranch
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    *,
    body: CreateDatabaseBranchRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/branches".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseBranch | Error | None:
    if response.status_code == 202:
        response_202 = DatabaseBranch.from_dict(response.json())



        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseBranch | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseBranchRequest,

) -> Response[DatabaseBranch | Error]:
    """ Create a branch of a database

     Forks the database into a new branch. The branch starts as an exact copy
    of the parent's data and diverges from there.

    Provisioning is asynchronous: the response is `202` with the branch in
    `provisioning` and no connection string. Poll the branch until it reports
    `active`, at which point it carries its own connection string.

    Retrying a create with a name that already exists returns `409` rather
    than a second branch, so a retried request cannot silently consume two
    slots of the branch allowance.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseBranch | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseBranchRequest,

) -> DatabaseBranch | Error | None:
    """ Create a branch of a database

     Forks the database into a new branch. The branch starts as an exact copy
    of the parent's data and diverges from there.

    Provisioning is asynchronous: the response is `202` with the branch in
    `provisioning` and no connection string. Poll the branch until it reports
    `active`, at which point it carries its own connection string.

    Retrying a create with a name that already exists returns `409` rather
    than a second branch, so a retried request cannot silently consume two
    slots of the branch allowance.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseBranch | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseBranchRequest,

) -> Response[DatabaseBranch | Error]:
    """ Create a branch of a database

     Forks the database into a new branch. The branch starts as an exact copy
    of the parent's data and diverges from there.

    Provisioning is asynchronous: the response is `202` with the branch in
    `provisioning` and no connection string. Poll the branch until it reports
    `active`, at which point it carries its own connection string.

    Retrying a create with a name that already exists returns `409` rather
    than a second branch, so a retried request cannot silently consume two
    slots of the branch allowance.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseBranch | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseBranchRequest,

) -> DatabaseBranch | Error | None:
    """ Create a branch of a database

     Forks the database into a new branch. The branch starts as an exact copy
    of the parent's data and diverges from there.

    Provisioning is asynchronous: the response is `202` with the branch in
    `provisioning` and no connection string. Poll the branch until it reports
    `active`, at which point it carries its own connection string.

    Retrying a create with a name that already exists returns `409` rather
    than a second branch, so a retried request cannot silently consume two
    slots of the branch allowance.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseBranchRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseBranch | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,

    )).parsed
