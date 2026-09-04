from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_database_backup_response_200 import DeleteDatabaseBackupResponse200
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    backup_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/databases/{database_name}/backups/{backup_name}".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),backup_name=quote(str(backup_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DeleteDatabaseBackupResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = DeleteDatabaseBackupResponse200.from_dict(response.json())



        return response_200

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DeleteDatabaseBackupResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    database_name: str,
    backup_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteDatabaseBackupResponse200 | Error]:
    """ Delete a backup

     Deletes the backup and frees its storage. Scheduled backups can be
    deleted too. A backup that is already gone reports `404`, so a name
    that never existed and a name that no longer does read the same.
    Refused with `409` while the database is being restored.

    Args:
        id (UUID):
        database_name (str):
        backup_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDatabaseBackupResponse200 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
backup_name=backup_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    backup_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteDatabaseBackupResponse200 | Error | None:
    """ Delete a backup

     Deletes the backup and frees its storage. Scheduled backups can be
    deleted too. A backup that is already gone reports `404`, so a name
    that never existed and a name that no longer does read the same.
    Refused with `409` while the database is being restored.

    Args:
        id (UUID):
        database_name (str):
        backup_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDatabaseBackupResponse200 | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
backup_name=backup_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    backup_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DeleteDatabaseBackupResponse200 | Error]:
    """ Delete a backup

     Deletes the backup and frees its storage. Scheduled backups can be
    deleted too. A backup that is already gone reports `404`, so a name
    that never existed and a name that no longer does read the same.
    Refused with `409` while the database is being restored.

    Args:
        id (UUID):
        database_name (str):
        backup_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DeleteDatabaseBackupResponse200 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
backup_name=backup_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    backup_name: str,
    *,
    client: AuthenticatedClient,

) -> DeleteDatabaseBackupResponse200 | Error | None:
    """ Delete a backup

     Deletes the backup and frees its storage. Scheduled backups can be
    deleted too. A backup that is already gone reports `404`, so a name
    that never existed and a name that no longer does read the same.
    Refused with `409` while the database is being restored.

    Args:
        id (UUID):
        database_name (str):
        backup_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DeleteDatabaseBackupResponse200 | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
backup_name=backup_name,
client=client,

    )).parsed
