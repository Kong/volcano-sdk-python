from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.connectors_response import ConnectorsResponse
from ...models.error import Error
from typing import cast



def request_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/connectors",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ConnectorsResponse | Error | None:
    if response.status_code == 200:
        response_200 = ConnectorsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ConnectorsResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ConnectorsResponse | Error]:
    """ List connectors

     Lists the connectors the caller can use. A connector links Volcano to
    an outside service. A `slack` connector is a Slack workspace the
    Volcano app is installed in: it is listed to the person who installed
    it there, and to anyone with a Slack identity in that workspace
    connected to their Volcano account. Add one with
    `POST /user/slack/installations`. The list answers whether or not
    reporting problems from Slack is available in this environment, so
    turning it off strands no connector.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorsResponse | Error]
     """


    kwargs = request_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> ConnectorsResponse | Error | None:
    """ List connectors

     Lists the connectors the caller can use. A connector links Volcano to
    an outside service. A `slack` connector is a Slack workspace the
    Volcano app is installed in: it is listed to the person who installed
    it there, and to anyone with a Slack identity in that workspace
    connected to their Volcano account. Add one with
    `POST /user/slack/installations`. The list answers whether or not
    reporting problems from Slack is available in this environment, so
    turning it off strands no connector.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorsResponse | Error
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[ConnectorsResponse | Error]:
    """ List connectors

     Lists the connectors the caller can use. A connector links Volcano to
    an outside service. A `slack` connector is a Slack workspace the
    Volcano app is installed in: it is listed to the person who installed
    it there, and to anyone with a Slack identity in that workspace
    connected to their Volcano account. Add one with
    `POST /user/slack/installations`. The list answers whether or not
    reporting problems from Slack is available in this environment, so
    turning it off strands no connector.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConnectorsResponse | Error]
     """


    kwargs = request_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> ConnectorsResponse | Error | None:
    """ List connectors

     Lists the connectors the caller can use. A connector links Volcano to
    an outside service. A `slack` connector is a Slack workspace the
    Volcano app is installed in: it is listed to the person who installed
    it there, and to anyone with a Slack identity in that workspace
    connected to their Volcano account. Add one with
    `POST /user/slack/installations`. The list answers whether or not
    reporting problems from Slack is available in this environment, so
    turning it off strands no connector.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConnectorsResponse | Error
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
