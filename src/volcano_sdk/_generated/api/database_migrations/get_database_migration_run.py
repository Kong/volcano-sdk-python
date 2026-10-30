from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_migration_run import DatabaseMigrationRun
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    database_name: str,
    run_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases/{database_name}/migration-runs/{run_id}".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),run_id=quote(str(run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseMigrationRun | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseMigrationRun.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseMigrationRun | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    database_name: str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseMigrationRun | Error]:
    """ Get a migration run

     Returns the run with each file's outcome. Poll this after starting a
    run.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
run_id=run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    database_name: str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> DatabaseMigrationRun | Error | None:
    """ Get a migration run

     Returns the run with each file's outcome. Poll this after starting a
    run.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationRun | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
run_id=run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    database_name: str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseMigrationRun | Error]:
    """ Get a migration run

     Returns the run with each file's outcome. Poll this after starting a
    run.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
database_name=database_name,
run_id=run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    database_name: str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> DatabaseMigrationRun | Error | None:
    """ Get a migration run

     Returns the run with each file's outcome. Poll this after starting a
    run.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationRun | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
run_id=run_id,
client=client,

    )).parsed
