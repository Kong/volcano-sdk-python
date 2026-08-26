from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_query_result import DatabaseQueryResult
from ...models.error import Error
from typing import cast



def _get_kwargs(
    database_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/databases/{database_name}/query/ping".format(database_name=quote(str(database_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseQueryResult | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseQueryResult.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseQueryResult | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseQueryResult | Error]:
    """ Database connectivity probe (REST API)

     Connectivity probe that runs a fixed `SELECT 1` through pgproxy, using the
    same authentication, status/bandwidth gating, and metering as the other
    `/query/*` endpoints.

    Unlike those endpoints, ping takes **no request body** and performs **no
    table-name validation**, so it works on any database — including a freshly
    provisioned, empty one. It is a real committed round-trip through pgproxy,
    so a `200` means the database is reachable and queryable. Used by the
    dashboard's database connection test.

    Args:
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseQueryResult | Error]
     """


    kwargs = _get_kwargs(
        database_name=database_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> DatabaseQueryResult | Error | None:
    """ Database connectivity probe (REST API)

     Connectivity probe that runs a fixed `SELECT 1` through pgproxy, using the
    same authentication, status/bandwidth gating, and metering as the other
    `/query/*` endpoints.

    Unlike those endpoints, ping takes **no request body** and performs **no
    table-name validation**, so it works on any database — including a freshly
    provisioned, empty one. It is a real committed round-trip through pgproxy,
    so a `200` means the database is reachable and queryable. Used by the
    dashboard's database connection test.

    Args:
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseQueryResult | Error
     """


    return sync_detailed(
        database_name=database_name,
client=client,

    ).parsed

async def asyncio_detailed(
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseQueryResult | Error]:
    """ Database connectivity probe (REST API)

     Connectivity probe that runs a fixed `SELECT 1` through pgproxy, using the
    same authentication, status/bandwidth gating, and metering as the other
    `/query/*` endpoints.

    Unlike those endpoints, ping takes **no request body** and performs **no
    table-name validation**, so it works on any database — including a freshly
    provisioned, empty one. It is a real committed round-trip through pgproxy,
    so a `200` means the database is reachable and queryable. Used by the
    dashboard's database connection test.

    Args:
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseQueryResult | Error]
     """


    kwargs = _get_kwargs(
        database_name=database_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    database_name: str,
    *,
    client: AuthenticatedClient,

) -> DatabaseQueryResult | Error | None:
    """ Database connectivity probe (REST API)

     Connectivity probe that runs a fixed `SELECT 1` through pgproxy, using the
    same authentication, status/bandwidth gating, and metering as the other
    `/query/*` endpoints.

    Unlike those endpoints, ping takes **no request body** and performs **no
    table-name validation**, so it works on any database — including a freshly
    provisioned, empty one. It is a real committed round-trip through pgproxy,
    so a `200` means the database is reachable and queryable. Used by the
    dashboard's database connection test.

    Args:
        database_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseQueryResult | Error
     """


    return (await asyncio_detailed(
        database_name=database_name,
client=client,

    )).parsed
