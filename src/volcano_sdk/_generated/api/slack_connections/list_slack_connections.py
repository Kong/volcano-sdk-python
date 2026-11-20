from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.slack_connections_response import SlackConnectionsResponse
from typing import cast



def request_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/slack/connections",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SlackConnectionsResponse | None:
    if response.status_code == 200:
        response_200 = SlackConnectionsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SlackConnectionsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SlackConnectionsResponse]:
    """ List connected Slack identities

     Lists the caller's connected Slack identities. It answers whether or
    not reporting problems from Slack is available in this environment, so
    turning it off strands no connection.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackConnectionsResponse]
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

) -> Error | SlackConnectionsResponse | None:
    """ List connected Slack identities

     Lists the caller's connected Slack identities. It answers whether or
    not reporting problems from Slack is available in this environment, so
    turning it off strands no connection.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackConnectionsResponse
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Error | SlackConnectionsResponse]:
    """ List connected Slack identities

     Lists the caller's connected Slack identities. It answers whether or
    not reporting problems from Slack is available in this environment, so
    turning it off strands no connection.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackConnectionsResponse]
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

) -> Error | SlackConnectionsResponse | None:
    """ List connected Slack identities

     Lists the caller's connected Slack identities. It answers whether or
    not reporting problems from Slack is available in this environment, so
    turning it off strands no connection.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackConnectionsResponse
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
