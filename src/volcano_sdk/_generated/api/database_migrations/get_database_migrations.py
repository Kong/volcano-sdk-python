from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_migrations import DatabaseMigrations
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    database_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases/{database_name}/migrations".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseMigrations | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseMigrations.from_dict(response.json())



        return response_200

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseMigrations | Error]:
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

) -> Response[DatabaseMigrations | Error]:
    """ Get a database's migration history

     Returns the migrations the database has recorded, in name order, read
    from the database's own `_volcano_migrations.history` table. The history
    is empty until a migration run or a baseline first records a file.

    `active_run_id` is the run that is queued or running, if any.

    If the history table is gone from a database where migrations ran,
    answers `409` with code `history_missing`, and every run fails with
    that code, rather than running files again. Record a baseline of the
    files that were already applied to rebuild it. Dropping the whole
    `_volcano_migrations` schema is not supported: the database then reads
    as new, and the next run applies every file again.

    Volcano reads at most 1,000 history entries, as many files as one run
    may carry. A history with more answers `409` with code
    `history_too_large`. A baseline is refused with that code, and a run
    fails with it. Deleting the entries of files no longer among your
    migrations brings the history back under the bound.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrations | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,

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

) -> DatabaseMigrations | Error | None:
    """ Get a database's migration history

     Returns the migrations the database has recorded, in name order, read
    from the database's own `_volcano_migrations.history` table. The history
    is empty until a migration run or a baseline first records a file.

    `active_run_id` is the run that is queued or running, if any.

    If the history table is gone from a database where migrations ran,
    answers `409` with code `history_missing`, and every run fails with
    that code, rather than running files again. Record a baseline of the
    files that were already applied to rebuild it. Dropping the whole
    `_volcano_migrations` schema is not supported: the database then reads
    as new, and the next run applies every file again.

    Volcano reads at most 1,000 history entries, as many files as one run
    may carry. A history with more answers `409` with code
    `history_too_large`. A baseline is refused with that code, and a run
    fails with it. Deleting the entries of files no longer among your
    migrations brings the history back under the bound.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrations | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseMigrations | Error]:
    """ Get a database's migration history

     Returns the migrations the database has recorded, in name order, read
    from the database's own `_volcano_migrations.history` table. The history
    is empty until a migration run or a baseline first records a file.

    `active_run_id` is the run that is queued or running, if any.

    If the history table is gone from a database where migrations ran,
    answers `409` with code `history_missing`, and every run fails with
    that code, rather than running files again. Record a baseline of the
    files that were already applied to rebuild it. Dropping the whole
    `_volcano_migrations` schema is not supported: the database then reads
    as new, and the next run applies every file again.

    Volcano reads at most 1,000 history entries, as many files as one run
    may carry. A history with more answers `409` with code
    `history_too_large`. A baseline is refused with that code, and a run
    fails with it. Deleting the entries of files no longer among your
    migrations brings the history back under the bound.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrations | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,

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

) -> DatabaseMigrations | Error | None:
    """ Get a database's migration history

     Returns the migrations the database has recorded, in name order, read
    from the database's own `_volcano_migrations.history` table. The history
    is empty until a migration run or a baseline first records a file.

    `active_run_id` is the run that is queued or running, if any.

    If the history table is gone from a database where migrations ran,
    answers `409` with code `history_missing`, and every run fails with
    that code, rather than running files again. Record a baseline of the
    files that were already applied to rebuild it. Dropping the whole
    `_volcano_migrations` schema is not supported: the database then reads
    as new, and the next run applies every file again.

    Volcano reads at most 1,000 history entries, as many files as one run
    may carry. A history with more answers `409` with code
    `history_too_large`. A baseline is refused with that code, and a run
    fails with it. Deleting the entries of files no longer among your
    migrations brings the history back under the bound.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrations | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,

    )).parsed
