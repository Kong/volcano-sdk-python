from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_delete_request import DatabaseDeleteRequest
from ...models.database_query_result import DatabaseQueryResult
from ...models.error import Error
from typing import cast



def _get_kwargs(
    database_name: str,
    *,
    body: DatabaseDeleteRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/databases/{database_name}/query/delete".format(database_name=quote(str(database_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseQueryResult | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseQueryResult.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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
    body: DatabaseDeleteRequest,

) -> Response[DatabaseQueryResult | Error]:
    """ Delete data from database (REST API)

     Delete rows from your database using REST API.

    **Safety:** Requires at least one filter to prevent accidental mass deletions

    **Security:** Row-Level Security ensures you can only delete data you have access to

    **Note:** If RLS blocks the delete, an empty result is returned (not an error)

    Args:
        database_name (str):
        body (DatabaseDeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseQueryResult | Error]
     """


    kwargs = _get_kwargs(
        database_name=database_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseDeleteRequest,

) -> DatabaseQueryResult | Error | None:
    """ Delete data from database (REST API)

     Delete rows from your database using REST API.

    **Safety:** Requires at least one filter to prevent accidental mass deletions

    **Security:** Row-Level Security ensures you can only delete data you have access to

    **Note:** If RLS blocks the delete, an empty result is returned (not an error)

    Args:
        database_name (str):
        body (DatabaseDeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseQueryResult | Error
     """


    return sync_detailed(
        database_name=database_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseDeleteRequest,

) -> Response[DatabaseQueryResult | Error]:
    """ Delete data from database (REST API)

     Delete rows from your database using REST API.

    **Safety:** Requires at least one filter to prevent accidental mass deletions

    **Security:** Row-Level Security ensures you can only delete data you have access to

    **Note:** If RLS blocks the delete, an empty result is returned (not an error)

    Args:
        database_name (str):
        body (DatabaseDeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseQueryResult | Error]
     """


    kwargs = _get_kwargs(
        database_name=database_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    database_name: str,
    *,
    client: AuthenticatedClient,
    body: DatabaseDeleteRequest,

) -> DatabaseQueryResult | Error | None:
    """ Delete data from database (REST API)

     Delete rows from your database using REST API.

    **Safety:** Requires at least one filter to prevent accidental mass deletions

    **Security:** Row-Level Security ensures you can only delete data you have access to

    **Note:** If RLS blocks the delete, an empty result is returned (not an error)

    Args:
        database_name (str):
        body (DatabaseDeleteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseQueryResult | Error
     """


    return (await asyncio_detailed(
        database_name=database_name,
client=client,
body=body,

    )).parsed
