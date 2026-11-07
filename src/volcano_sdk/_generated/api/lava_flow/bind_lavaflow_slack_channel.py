from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_slack_channel import LavaflowSlackChannel
from ...models.lavaflow_slack_channel_binding import LavaflowSlackChannelBinding
from typing import cast



def request_kwargs(
    *,
    body: LavaflowSlackChannelBinding,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/lavaflow/slack-channels",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSlackChannel | None:
    if response.status_code == 200:
        response_200 = LavaflowSlackChannel.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = LavaflowSlackChannel.from_dict(response.json())



        return response_201

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

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSlackChannel]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowSlackChannelBinding,

) -> Response[Error | LavaflowSlackChannel]:
    """ Add a Slack channel to the project

     Binds a Slack channel, so it reports problems to LavaFlow for the
    project, and answers `201`. Binding a channel that is already bound
    answers `200` with that binding, and makes the current owner the one
    who bound it, so a retry is safe. The workspace must have the
    Volcano app installed, and one of the Slack identities the caller's
    sign-in session signed in as must belong to it and be a member of the
    channel, so on an account several people share, each binds only
    channels they are in. The channel must be one the picker lists: one
    the Volcano app is in, and not archived, a Slack Connect channel, or
    shared across an organization.

    Only the project's owner can bind, with a platform token. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding needs the project's `lavaflow.slack`
    capability: where it is unavailable, this answers `404` with code
    `feature_unavailable`, or `403` with code `plan_required` when the
    owner's plan does not include LavaFlow.

    Args:
        body (LavaflowSlackChannelBinding):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSlackChannel]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: LavaflowSlackChannelBinding,

) -> Error | LavaflowSlackChannel | None:
    """ Add a Slack channel to the project

     Binds a Slack channel, so it reports problems to LavaFlow for the
    project, and answers `201`. Binding a channel that is already bound
    answers `200` with that binding, and makes the current owner the one
    who bound it, so a retry is safe. The workspace must have the
    Volcano app installed, and one of the Slack identities the caller's
    sign-in session signed in as must belong to it and be a member of the
    channel, so on an account several people share, each binds only
    channels they are in. The channel must be one the picker lists: one
    the Volcano app is in, and not archived, a Slack Connect channel, or
    shared across an organization.

    Only the project's owner can bind, with a platform token. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding needs the project's `lavaflow.slack`
    capability: where it is unavailable, this answers `404` with code
    `feature_unavailable`, or `403` with code `plan_required` when the
    owner's plan does not include LavaFlow.

    Args:
        body (LavaflowSlackChannelBinding):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSlackChannel
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowSlackChannelBinding,

) -> Response[Error | LavaflowSlackChannel]:
    """ Add a Slack channel to the project

     Binds a Slack channel, so it reports problems to LavaFlow for the
    project, and answers `201`. Binding a channel that is already bound
    answers `200` with that binding, and makes the current owner the one
    who bound it, so a retry is safe. The workspace must have the
    Volcano app installed, and one of the Slack identities the caller's
    sign-in session signed in as must belong to it and be a member of the
    channel, so on an account several people share, each binds only
    channels they are in. The channel must be one the picker lists: one
    the Volcano app is in, and not archived, a Slack Connect channel, or
    shared across an organization.

    Only the project's owner can bind, with a platform token. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding needs the project's `lavaflow.slack`
    capability: where it is unavailable, this answers `404` with code
    `feature_unavailable`, or `403` with code `plan_required` when the
    owner's plan does not include LavaFlow.

    Args:
        body (LavaflowSlackChannelBinding):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSlackChannel]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: LavaflowSlackChannelBinding,

) -> Error | LavaflowSlackChannel | None:
    """ Add a Slack channel to the project

     Binds a Slack channel, so it reports problems to LavaFlow for the
    project, and answers `201`. Binding a channel that is already bound
    answers `200` with that binding, and makes the current owner the one
    who bound it, so a retry is safe. The workspace must have the
    Volcano app installed, and one of the Slack identities the caller's
    sign-in session signed in as must belong to it and be a member of the
    channel, so on an account several people share, each binds only
    channels they are in. The channel must be one the picker lists: one
    the Volcano app is in, and not archived, a Slack Connect channel, or
    shared across an organization.

    Only the project's owner can bind, with a platform token. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding needs the project's `lavaflow.slack`
    capability: where it is unavailable, this answers `404` with code
    `feature_unavailable`, or `403` with code `plan_required` when the
    owner's plan does not include LavaFlow.

    Args:
        body (LavaflowSlackChannelBinding):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSlackChannel
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
