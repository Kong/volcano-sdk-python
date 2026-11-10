from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_migration_baseline import DatabaseMigrationBaseline
from ...models.database_migration_conflict_error import DatabaseMigrationConflictError
from ...models.database_migration_files_request import DatabaseMigrationFilesRequest
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    database_name: str,
    *,
    body: DatabaseMigrationFilesRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/migrations/baseline".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseMigrationBaseline.from_dict(response.json())



        return response_200

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error]:
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

) -> Response[DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error]:
    """ Record migrations as applied without running them

     Records each file in the database's migration history as applied,
    without running it. Use it once for a database whose schema already
    reflects the files, such as one migrated before Volcano tracked its
    migrations, so later runs apply only newer files. It is refused while
    a run is queued or running, and no run starts while it records. It
    does not queue: while another request is changing the database, or the
    database holds it up, such as with a lock on the migration history, it
    answers `409` with code `database_busy`.

    Files the history already records with the same checksum are skipped, so
    repeating the request changes nothing. A file recorded with a different
    checksum is refused, and nothing is recorded.

    It also rebuilds a history that was lost (`history_missing`): send
    exactly the files that were already applied, and later runs apply only
    the rest.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
body=body,

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

) -> DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error | None:
    """ Record migrations as applied without running them

     Records each file in the database's migration history as applied,
    without running it. Use it once for a database whose schema already
    reflects the files, such as one migrated before Volcano tracked its
    migrations, so later runs apply only newer files. It is refused while
    a run is queued or running, and no run starts while it records. It
    does not queue: while another request is changing the database, or the
    database holds it up, such as with a lock on the migration history, it
    answers `409` with code `database_busy`.

    Files the history already records with the same checksum are skipped, so
    repeating the request changes nothing. A file recorded with a different
    checksum is refused, and nothing is recorded.

    It also rebuilds a history that was lost (`history_missing`): send
    exactly the files that were already applied, and later runs apply only
    the rest.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseMigrationFilesRequest,

) -> Response[DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error]:
    """ Record migrations as applied without running them

     Records each file in the database's migration history as applied,
    without running it. Use it once for a database whose schema already
    reflects the files, such as one migrated before Volcano tracked its
    migrations, so later runs apply only newer files. It is refused while
    a run is queued or running, and no run starts while it records. It
    does not queue: while another request is changing the database, or the
    database holds it up, such as with a lock on the migration history, it
    answers `409` with code `database_busy`.

    Files the history already records with the same checksum are skipped, so
    repeating the request changes nothing. A file recorded with a different
    checksum is refused, and nothing is recorded.

    It also rebuilds a history that was lost (`history_missing`): send
    exactly the files that were already applied, and later runs apply only
    the rest.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
body=body,

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

) -> DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error | None:
    """ Record migrations as applied without running them

     Records each file in the database's migration history as applied,
    without running it. Use it once for a database whose schema already
    reflects the files, such as one migrated before Volcano tracked its
    migrations, so later runs apply only newer files. It is refused while
    a run is queued or running, and no run starts while it records. It
    does not queue: while another request is changing the database, or the
    database holds it up, such as with a lock on the migration history, it
    answers `409` with code `database_busy`.

    Files the history already records with the same checksum are skipped, so
    repeating the request changes nothing. A file recorded with a different
    checksum is refused, and nothing is recorded.

    It also rebuilds a history that was lost (`history_missing`): send
    exactly the files that were already applied, and later runs apply only
    the rest.

    Where migration runs are not available, answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        database_name (str):
        body (DatabaseMigrationFilesRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationBaseline | DatabaseMigrationConflictError | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,
body=body,

    )).parsed
