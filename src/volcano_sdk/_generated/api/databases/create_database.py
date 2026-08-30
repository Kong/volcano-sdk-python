from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_database_request import CreateDatabaseRequest
from ...models.database import Database
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateDatabaseRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Database | Error | None:
    if response.status_code == 201:
        response_201 = Database.from_dict(response.json())



        return response_201

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Database | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseRequest,

) -> Response[Database | Error]:
    """ Create a new serverless PostgreSQL database

     Creates a serverless PostgreSQL database in the project.
    Each project can hold 1 database on Free and up to 10,000 on Pro.
    Requests over the plan's cap return 403.

    Args:
        id (UUID):
        body (CreateDatabaseRequest): Create a new PostgreSQL database. Volcano automatically sets
            up:
            - Auth helpers (auth.uid(), auth.email(), auth.role())
            - Database roles (anon for unauthenticated, authenticated for signed-in users)
            - Secure multi-tenant isolation
            - Ready for Row-Level Security

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Database | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseRequest,

) -> Database | Error | None:
    """ Create a new serverless PostgreSQL database

     Creates a serverless PostgreSQL database in the project.
    Each project can hold 1 database on Free and up to 10,000 on Pro.
    Requests over the plan's cap return 403.

    Args:
        id (UUID):
        body (CreateDatabaseRequest): Create a new PostgreSQL database. Volcano automatically sets
            up:
            - Auth helpers (auth.uid(), auth.email(), auth.role())
            - Database roles (anon for unauthenticated, authenticated for signed-in users)
            - Secure multi-tenant isolation
            - Ready for Row-Level Security

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Database | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseRequest,

) -> Response[Database | Error]:
    """ Create a new serverless PostgreSQL database

     Creates a serverless PostgreSQL database in the project.
    Each project can hold 1 database on Free and up to 10,000 on Pro.
    Requests over the plan's cap return 403.

    Args:
        id (UUID):
        body (CreateDatabaseRequest): Create a new PostgreSQL database. Volcano automatically sets
            up:
            - Auth helpers (auth.uid(), auth.email(), auth.role())
            - Database roles (anon for unauthenticated, authenticated for signed-in users)
            - Secure multi-tenant isolation
            - Ready for Row-Level Security

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Database | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateDatabaseRequest,

) -> Database | Error | None:
    """ Create a new serverless PostgreSQL database

     Creates a serverless PostgreSQL database in the project.
    Each project can hold 1 database on Free and up to 10,000 on Pro.
    Requests over the plan's cap return 403.

    Args:
        id (UUID):
        body (CreateDatabaseRequest): Create a new PostgreSQL database. Volcano automatically sets
            up:
            - Auth helpers (auth.uid(), auth.email(), auth.role())
            - Database roles (anon for unauthenticated, authenticated for signed-in users)
            - Secure multi-tenant isolation
            - Ready for Row-Level Security

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Database | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
