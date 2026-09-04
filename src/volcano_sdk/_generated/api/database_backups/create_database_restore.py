from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_database_restore_request import CreateDatabaseRestoreRequest
from ...models.database_restore import DatabaseRestore
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    *,
    body: CreateDatabaseRestoreRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/restores".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseRestore | Error | None:
    if response.status_code == 202:
        response_202 = DatabaseRestore.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseRestore | Error]:
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
    body: CreateDatabaseRestoreRequest,

) -> Response[DatabaseRestore | Error]:
    """ Restore a database

     Replaces the database's data, either with a named backup or with its
    state at a point in time. This is destructive: everything written after
    that point is discarded.

    Asynchronous: the response is `202` with the restore `pending` and the
    database `restoring`. The database does not accept connections until the
    restore reports `completed`; its connection string is unchanged
    throughout, so nothing holding it needs updating.

    Restores are in place. There is no way to restore into a second
    database, and a database's branches are never restored — they keep
    serving their own data, but resetting a branch from its parent is
    refused by the storage provider for up to 24 hours afterwards.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseRestoreRequest): Names what to restore. Supply exactly one of
            `backup_name` or
            `restore_to`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseRestore | Error]
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
    body: CreateDatabaseRestoreRequest,

) -> DatabaseRestore | Error | None:
    """ Restore a database

     Replaces the database's data, either with a named backup or with its
    state at a point in time. This is destructive: everything written after
    that point is discarded.

    Asynchronous: the response is `202` with the restore `pending` and the
    database `restoring`. The database does not accept connections until the
    restore reports `completed`; its connection string is unchanged
    throughout, so nothing holding it needs updating.

    Restores are in place. There is no way to restore into a second
    database, and a database's branches are never restored — they keep
    serving their own data, but resetting a branch from its parent is
    refused by the storage provider for up to 24 hours afterwards.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseRestoreRequest): Names what to restore. Supply exactly one of
            `backup_name` or
            `restore_to`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseRestore | Error
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
    body: CreateDatabaseRestoreRequest,

) -> Response[DatabaseRestore | Error]:
    """ Restore a database

     Replaces the database's data, either with a named backup or with its
    state at a point in time. This is destructive: everything written after
    that point is discarded.

    Asynchronous: the response is `202` with the restore `pending` and the
    database `restoring`. The database does not accept connections until the
    restore reports `completed`; its connection string is unchanged
    throughout, so nothing holding it needs updating.

    Restores are in place. There is no way to restore into a second
    database, and a database's branches are never restored — they keep
    serving their own data, but resetting a branch from its parent is
    refused by the storage provider for up to 24 hours afterwards.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseRestoreRequest): Names what to restore. Supply exactly one of
            `backup_name` or
            `restore_to`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseRestore | Error]
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
    body: CreateDatabaseRestoreRequest,

) -> DatabaseRestore | Error | None:
    """ Restore a database

     Replaces the database's data, either with a named backup or with its
    state at a point in time. This is destructive: everything written after
    that point is discarded.

    Asynchronous: the response is `202` with the restore `pending` and the
    database `restoring`. The database does not accept connections until the
    restore reports `completed`; its connection string is unchanged
    throughout, so nothing holding it needs updating.

    Restores are in place. There is no way to restore into a second
    database, and a database's branches are never restored — they keep
    serving their own data, but resetting a branch from its parent is
    refused by the storage provider for up to 24 hours afterwards.

    Args:
        id (UUID):
        database_name (str):
        body (CreateDatabaseRestoreRequest): Names what to restore. Supply exactly one of
            `backup_name` or
            `restore_to`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseRestore | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,

    )).parsed
