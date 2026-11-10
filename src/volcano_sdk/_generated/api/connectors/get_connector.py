from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.connector import Connector
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    connector_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/connectors/{connector_id}".format(connector_id=quote(str(connector_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Connector | Error | None:
    if response.status_code == 200:
        response_200 = Connector.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Connector | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Connector | Error]:
    """ Get a connector

     Returns one connector the caller can use, as listing connectors shows
    it. A connector the caller cannot see answers like one that doesn't
    exist.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | Error]
     """


    kwargs = request_kwargs(
        connector_id=connector_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Connector | Error | None:
    """ Get a connector

     Returns one connector the caller can use, as listing connectors shows
    it. A connector the caller cannot see answers like one that doesn't
    exist.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | Error
     """


    return sync_detailed(
        connector_id=connector_id,
client=client,

    ).parsed

async def asyncio_detailed(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Connector | Error]:
    """ Get a connector

     Returns one connector the caller can use, as listing connectors shows
    it. A connector the caller cannot see answers like one that doesn't
    exist.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | Error]
     """


    kwargs = request_kwargs(
        connector_id=connector_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Connector | Error | None:
    """ Get a connector

     Returns one connector the caller can use, as listing connectors shows
    it. A connector the caller cannot see answers like one that doesn't
    exist.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | Error
     """


    return (await asyncio_detailed(
        connector_id=connector_id,
client=client,

    )).parsed
