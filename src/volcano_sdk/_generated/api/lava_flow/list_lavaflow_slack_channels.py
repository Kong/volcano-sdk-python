from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_slack_channels_response import LavaflowSlackChannelsResponse
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/slack-channels",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSlackChannelsResponse | None:
    if response.status_code == 200:
        response_200 = LavaflowSlackChannelsResponse.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSlackChannelsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | LavaflowSlackChannelsResponse]:
    """ List the project's Slack channels

     Lists the Slack channels that report problems to LavaFlow for the
    project. In a listed channel, someone whose Slack identity is connected
    to the project owner's account can mention the Volcano app to report a
    problem. Project access tokens can read the list, including read-only
    ones, and so can MCP, as `get_lavaflow_slack_channels`. The list
    answers whether or not the project's `lavaflow.slack` capability is
    available.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSlackChannelsResponse]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | LavaflowSlackChannelsResponse | None:
    """ List the project's Slack channels

     Lists the Slack channels that report problems to LavaFlow for the
    project. In a listed channel, someone whose Slack identity is connected
    to the project owner's account can mention the Volcano app to report a
    problem. Project access tokens can read the list, including read-only
    ones, and so can MCP, as `get_lavaflow_slack_channels`. The list
    answers whether or not the project's `lavaflow.slack` capability is
    available.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSlackChannelsResponse
     """


    return sync_detailed(
        client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | LavaflowSlackChannelsResponse]:
    """ List the project's Slack channels

     Lists the Slack channels that report problems to LavaFlow for the
    project. In a listed channel, someone whose Slack identity is connected
    to the project owner's account can mention the Volcano app to report a
    problem. Project access tokens can read the list, including read-only
    ones, and so can MCP, as `get_lavaflow_slack_channels`. The list
    answers whether or not the project's `lavaflow.slack` capability is
    available.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSlackChannelsResponse]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | LavaflowSlackChannelsResponse | None:
    """ List the project's Slack channels

     Lists the Slack channels that report problems to LavaFlow for the
    project. In a listed channel, someone whose Slack identity is connected
    to the project owner's account can mention the Volcano app to report a
    problem. Project access tokens can read the list, including read-only
    ones, and so can MCP, as `get_lavaflow_slack_channels`. The list
    answers whether or not the project's `lavaflow.slack` capability is
    available.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSlackChannelsResponse
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,

    )).parsed
