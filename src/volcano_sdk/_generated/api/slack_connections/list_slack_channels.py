from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.slack_channels_response import SlackChannelsResponse
from typing import cast



def request_kwargs(
    *,
    team_id: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["team_id"] = team_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/user/slack/channels",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SlackChannelsResponse | None:
    if response.status_code == 200:
        response_200 = SlackChannelsResponse.from_dict(response.json())



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

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SlackChannelsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    team_id: str,

) -> Response[Error | SlackChannelsResponse]:
    """ List a workspace's channels for binding

     Lists the channels in a workspace, public and private, that the Volcano
    app and one of the Slack identities the caller's sign-in session signed
    in as are both in, to choose which ones report problems to LavaFlow.
    Invite the app to a channel in Slack to list it. Slack Connect, shared
    and archived channels are left out.

    Args:
        team_id (str): A Slack workspace ID, such as `T0123ABCD`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackChannelsResponse]
     """


    kwargs = request_kwargs(
        team_id=team_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    team_id: str,

) -> Error | SlackChannelsResponse | None:
    """ List a workspace's channels for binding

     Lists the channels in a workspace, public and private, that the Volcano
    app and one of the Slack identities the caller's sign-in session signed
    in as are both in, to choose which ones report problems to LavaFlow.
    Invite the app to a channel in Slack to list it. Slack Connect, shared
    and archived channels are left out.

    Args:
        team_id (str): A Slack workspace ID, such as `T0123ABCD`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackChannelsResponse
     """


    return sync_detailed(
        client=client,
team_id=team_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    team_id: str,

) -> Response[Error | SlackChannelsResponse]:
    """ List a workspace's channels for binding

     Lists the channels in a workspace, public and private, that the Volcano
    app and one of the Slack identities the caller's sign-in session signed
    in as are both in, to choose which ones report problems to LavaFlow.
    Invite the app to a channel in Slack to list it. Slack Connect, shared
    and archived channels are left out.

    Args:
        team_id (str): A Slack workspace ID, such as `T0123ABCD`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackChannelsResponse]
     """


    kwargs = request_kwargs(
        team_id=team_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    team_id: str,

) -> Error | SlackChannelsResponse | None:
    """ List a workspace's channels for binding

     Lists the channels in a workspace, public and private, that the Volcano
    app and one of the Slack identities the caller's sign-in session signed
    in as are both in, to choose which ones report problems to LavaFlow.
    Invite the app to a channel in Slack to list it. Slack Connect, shared
    and archived channels are left out.

    Args:
        team_id (str): A Slack workspace ID, such as `T0123ABCD`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackChannelsResponse
     """


    return (await asyncio_detailed(
        client=client,
team_id=team_id,

    )).parsed
