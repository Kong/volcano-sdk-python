from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_database_response_202 import DeleteDatabaseResponse202
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/databases/{database_name}".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | DeleteDatabaseResponse202 | Error | None:
    if response.status_code == 202:
        response_202 = DeleteDatabaseResponse202.from_dict(response.json())



        return response_202

    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | DeleteDatabaseResponse202 | Error]:
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

) -> Response[Any | DeleteDatabaseResponse202 | Error]:
    """ Delete a database

     Deletes a database and the instance backing it. When the instance is
    removed synchronously the database row is deleted and the response is
    `204`. If the instance cannot be deleted right away, the database row
    is retained (status `deleting`) and its teardown is handed to the
    background reconciler, which retries the deletion and removes the row
    once the instance is gone; in that case the response is `202`. The database row is
    never dropped while its instance still exists, so an instance is
    never orphaned without a record to retry from.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteDatabaseResponse202 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,

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

) -> Any | DeleteDatabaseResponse202 | Error | None:
    """ Delete a database

     Deletes a database and the instance backing it. When the instance is
    removed synchronously the database row is deleted and the response is
    `204`. If the instance cannot be deleted right away, the database row
    is retained (status `deleting`) and its teardown is handed to the
    background reconciler, which retries the deletion and removes the row
    once the instance is gone; in that case the response is `202`. The database row is
    never dropped while its instance still exists, so an instance is
    never orphaned without a record to retry from.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteDatabaseResponse202 | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | DeleteDatabaseResponse202 | Error]:
    """ Delete a database

     Deletes a database and the instance backing it. When the instance is
    removed synchronously the database row is deleted and the response is
    `204`. If the instance cannot be deleted right away, the database row
    is retained (status `deleting`) and its teardown is handed to the
    background reconciler, which retries the deletion and removes the row
    once the instance is gone; in that case the response is `202`. The database row is
    never dropped while its instance still exists, so an instance is
    never orphaned without a record to retry from.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | DeleteDatabaseResponse202 | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,

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

) -> Any | DeleteDatabaseResponse202 | Error | None:
    """ Delete a database

     Deletes a database and the instance backing it. When the instance is
    removed synchronously the database row is deleted and the response is
    `204`. If the instance cannot be deleted right away, the database row
    is retained (status `deleting`) and its teardown is handed to the
    background reconciler, which retries the deletion and removes the row
    once the instance is gone; in that case the response is `202`. The database row is
    never dropped while its instance still exists, so an instance is
    never orphaned without a record to retry from.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | DeleteDatabaseResponse202 | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,

    )).parsed
