from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_migration_run_list import DatabaseMigrationRunList
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    database_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases/{database_name}/migration-runs".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseMigrationRunList | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseMigrationRunList.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseMigrationRunList | Error]:
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

) -> Response[DatabaseMigrationRunList | Error]:
    """ List a database's migration runs

     Returns the database's 50 most recent migration runs, newest first,
    without their files; get a run for its files. There is no pagination.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationRunList | Error]
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

) -> DatabaseMigrationRunList | Error | None:
    """ List a database's migration runs

     Returns the database's 50 most recent migration runs, newest first,
    without their files; get a run for its files. There is no pagination.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationRunList | Error
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

) -> Response[DatabaseMigrationRunList | Error]:
    """ List a database's migration runs

     Returns the database's 50 most recent migration runs, newest first,
    without their files; get a run for its files. There is no pagination.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseMigrationRunList | Error]
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

) -> DatabaseMigrationRunList | Error | None:
    """ List a database's migration runs

     Returns the database's 50 most recent migration runs, newest first,
    without their files; get a run for its files. There is no pagination.

    Available whether or not migration runs are.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseMigrationRunList | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,

    )).parsed
