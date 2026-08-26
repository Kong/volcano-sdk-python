from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.reset_database_password_response_200 import ResetDatabasePasswordResponse200
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/reset-password".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ResetDatabasePasswordResponse200 | None:
    if response.status_code == 200:
        response_200 = ResetDatabasePasswordResponse200.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ResetDatabasePasswordResponse200]:
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

) -> Response[ResetDatabasePasswordResponse200]:
    """ Reset database password

     Rotates the Volcano-managed PostgreSQL password used by clients when connecting
    through pgproxy. This does not rotate or expose the internal owner password.
    The returned password and connection string are the only client credentials that
    will authenticate through pgproxy after reset.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResetDatabasePasswordResponse200]
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

) -> ResetDatabasePasswordResponse200 | None:
    """ Reset database password

     Rotates the Volcano-managed PostgreSQL password used by clients when connecting
    through pgproxy. This does not rotate or expose the internal owner password.
    The returned password and connection string are the only client credentials that
    will authenticate through pgproxy after reset.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResetDatabasePasswordResponse200
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

) -> Response[ResetDatabasePasswordResponse200]:
    """ Reset database password

     Rotates the Volcano-managed PostgreSQL password used by clients when connecting
    through pgproxy. This does not rotate or expose the internal owner password.
    The returned password and connection string are the only client credentials that
    will authenticate through pgproxy after reset.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ResetDatabasePasswordResponse200]
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

) -> ResetDatabasePasswordResponse200 | None:
    """ Reset database password

     Rotates the Volcano-managed PostgreSQL password used by clients when connecting
    through pgproxy. This does not rotate or expose the internal owner password.
    The returned password and connection string are the only client credentials that
    will authenticate through pgproxy after reset.

    Args:
        id (UUID):
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ResetDatabasePasswordResponse200
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,

    )).parsed
