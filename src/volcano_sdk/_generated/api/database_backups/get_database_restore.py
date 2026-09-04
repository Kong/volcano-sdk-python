from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_restore import DatabaseRestore
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    restore_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases/{database_name}/restores/{restore_id}".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),restore_id=quote(str(restore_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseRestore | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseRestore.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

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
    restore_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseRestore | Error]:
    """ Get a restore

     Returns the restore. Poll this after starting one; the database is
    connectable again once it reports `completed`.

    Args:
        id (UUID):
        database_name (str):
        restore_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseRestore | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
restore_id=restore_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    restore_id: UUID,
    *,
    client: AuthenticatedClient,

) -> DatabaseRestore | Error | None:
    """ Get a restore

     Returns the restore. Poll this after starting one; the database is
    connectable again once it reports `completed`.

    Args:
        id (UUID):
        database_name (str):
        restore_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseRestore | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
restore_id=restore_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    restore_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseRestore | Error]:
    """ Get a restore

     Returns the restore. Poll this after starting one; the database is
    connectable again once it reports `completed`.

    Args:
        id (UUID):
        database_name (str):
        restore_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseRestore | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
restore_id=restore_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    restore_id: UUID,
    *,
    client: AuthenticatedClient,

) -> DatabaseRestore | Error | None:
    """ Get a restore

     Returns the restore. Poll this after starting one; the database is
    connectable again once it reports `completed`.

    Args:
        id (UUID):
        database_name (str):
        restore_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseRestore | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
restore_id=restore_id,
client=client,

    )).parsed
