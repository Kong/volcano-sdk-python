from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_migration_conflict_error import DatabaseMigrationConflictError
from ...models.database_migration_files_request import DatabaseMigrationFilesRequest
from ...models.database_migration_run import DatabaseMigrationRun
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    database_name: str,
    *,
    body: DatabaseMigrationFilesRequest,
    idempotency_key: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/migration-runs".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseMigrationConflictError | DatabaseMigrationRun | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseMigrationRun.from_dict(response.json())



        return response_200

    if response.status_code == 202:
        response_202 = DatabaseMigrationRun.from_dict(response.json())



        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = DatabaseMigrationConflictError.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseMigrationConflictError | DatabaseMigrationRun | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseMigrationFilesRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[DatabaseMigrationConflictError | DatabaseMigrationRun | Error]:
    """ Apply migrations to a database

     Starts a migration run: Volcano compares the files with the database's
    history, rehearses the pending ones on a short-lived branch of the
    database, takes a backup, and applies them in name order. Files the
    history already records with the same checksum are skipped.

    Asynchronous: the response is `202` with the run `queued`. Poll the run
    until its `status` is `succeeded` or `failed`.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key this
    database has seen returns that run with `200` and starts nothing. A
    database runs one migration run at a time.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        idempotency_key (str | Unset):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationConflictError | DatabaseMigrationRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseMigrationFilesRequest,
    idempotency_key: str | Unset = UNSET,

) -> DatabaseMigrationConflictError | DatabaseMigrationRun | Error | None:
    """ Apply migrations to a database

     Starts a migration run: Volcano compares the files with the database's
    history, rehearses the pending ones on a short-lived branch of the
    database, takes a backup, and applies them in name order. Files the
    history already records with the same checksum are skipped.

    Asynchronous: the response is `202` with the run `queued`. Poll the run
    until its `status` is `succeeded` or `failed`.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key this
    database has seen returns that run with `200` and starts nothing. A
    database runs one migration run at a time.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        idempotency_key (str | Unset):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationConflictError | DatabaseMigrationRun | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseMigrationFilesRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[DatabaseMigrationConflictError | DatabaseMigrationRun | Error]:
    """ Apply migrations to a database

     Starts a migration run: Volcano compares the files with the database's
    history, rehearses the pending ones on a short-lived branch of the
    database, takes a backup, and applies them in name order. Files the
    history already records with the same checksum are skipped.

    Asynchronous: the response is `202` with the run `queued`. Poll the run
    until its `status` is `succeeded` or `failed`.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key this
    database has seen returns that run with `200` and starts nothing. A
    database runs one migration run at a time.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        idempotency_key (str | Unset):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationConflictError | DatabaseMigrationRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseMigrationFilesRequest,
    idempotency_key: str | Unset = UNSET,

) -> DatabaseMigrationConflictError | DatabaseMigrationRun | Error | None:
    """ Apply migrations to a database

     Starts a migration run: Volcano compares the files with the database's
    history, rehearses the pending ones on a short-lived branch of the
    database, takes a backup, and applies them in name order. Files the
    history already records with the same checksum are skipped.

    Asynchronous: the response is `202` with the run `queued`. Poll the run
    until its `status` is `succeeded` or `failed`.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key this
    database has seen returns that run with `200` and starts nothing. A
    database runs one migration run at a time.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        idempotency_key (str | Unset):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationConflictError | DatabaseMigrationRun | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
