from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_connector_binding import LavaflowConnectorBinding
from typing import cast



def request_kwargs(
    *,
    body: Any,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/lavaflow/connector-bindings",
    }

    
    _kwargs["json"] = body

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowConnectorBinding | None:
    if response.status_code == 200:
        response_200 = LavaflowConnectorBinding.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = LavaflowConnectorBinding.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowConnectorBinding]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,

) -> Response[Error | LavaflowConnectorBinding]:
    """ Bind a connector to the project

     Binds a place in a connector to the project, so problems reported
    there reach LavaFlow for it, and answers `201`. Send `slack` for a
    `slack` connector and `aikido` for an `aikido` one. For a `slack`
    connector the place is a channel. Binding a channel that is already
    bound answers `200` with that binding, and makes the current owner the
    one who bound it, so a retry is safe. One of the Slack identities the
    caller's sign-in session signed in as must belong to the connector's
    workspace and be a member of the channel, so on an account several
    people share, each binds only channels they are in. The channel must
    be one the picker (`GET /user/slack/channels`) lists: one the Volcano
    app is in, and not archived, a Slack Connect channel, or shared
    across an organization.

    For an `aikido` connector the place is the workspace's new code
    (SAST) issues on the project's GitHub repository, at or above
    `min_severity`. The caller must have
    connected the workspace. Binding it again answers `200` and sets the
    new minimum. Each issue starts a LavaFlow run that stops at a pull
    request for review.

    Only the project's owner can bind, with a platform token or a live
    dashboard sign-in session. A session must come from the dashboard's
    own configured project; another project's session gets `403`. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding a Slack channel needs the project's
    `lavaflow.slack` capability, and binding Aikido its
    `lavaflow.aikido` capability: where it is unavailable, this answers
    `404` with code `feature_unavailable`, or `403` with code
    `plan_required` when the owner's plan does not include LavaFlow.

    Args:
        body (Any): Send exactly one of `slack` and `aikido`, matching the connector's type.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowConnectorBinding]
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
    body: Any,

) -> Error | LavaflowConnectorBinding | None:
    """ Bind a connector to the project

     Binds a place in a connector to the project, so problems reported
    there reach LavaFlow for it, and answers `201`. Send `slack` for a
    `slack` connector and `aikido` for an `aikido` one. For a `slack`
    connector the place is a channel. Binding a channel that is already
    bound answers `200` with that binding, and makes the current owner the
    one who bound it, so a retry is safe. One of the Slack identities the
    caller's sign-in session signed in as must belong to the connector's
    workspace and be a member of the channel, so on an account several
    people share, each binds only channels they are in. The channel must
    be one the picker (`GET /user/slack/channels`) lists: one the Volcano
    app is in, and not archived, a Slack Connect channel, or shared
    across an organization.

    For an `aikido` connector the place is the workspace's new code
    (SAST) issues on the project's GitHub repository, at or above
    `min_severity`. The caller must have
    connected the workspace. Binding it again answers `200` and sets the
    new minimum. Each issue starts a LavaFlow run that stops at a pull
    request for review.

    Only the project's owner can bind, with a platform token or a live
    dashboard sign-in session. A session must come from the dashboard's
    own configured project; another project's session gets `403`. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding a Slack channel needs the project's
    `lavaflow.slack` capability, and binding Aikido its
    `lavaflow.aikido` capability: where it is unavailable, this answers
    `404` with code `feature_unavailable`, or `403` with code
    `plan_required` when the owner's plan does not include LavaFlow.

    Args:
        body (Any): Send exactly one of `slack` and `aikido`, matching the connector's type.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowConnectorBinding
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: Any,

) -> Response[Error | LavaflowConnectorBinding]:
    """ Bind a connector to the project

     Binds a place in a connector to the project, so problems reported
    there reach LavaFlow for it, and answers `201`. Send `slack` for a
    `slack` connector and `aikido` for an `aikido` one. For a `slack`
    connector the place is a channel. Binding a channel that is already
    bound answers `200` with that binding, and makes the current owner the
    one who bound it, so a retry is safe. One of the Slack identities the
    caller's sign-in session signed in as must belong to the connector's
    workspace and be a member of the channel, so on an account several
    people share, each binds only channels they are in. The channel must
    be one the picker (`GET /user/slack/channels`) lists: one the Volcano
    app is in, and not archived, a Slack Connect channel, or shared
    across an organization.

    For an `aikido` connector the place is the workspace's new code
    (SAST) issues on the project's GitHub repository, at or above
    `min_severity`. The caller must have
    connected the workspace. Binding it again answers `200` and sets the
    new minimum. Each issue starts a LavaFlow run that stops at a pull
    request for review.

    Only the project's owner can bind, with a platform token or a live
    dashboard sign-in session. A session must come from the dashboard's
    own configured project; another project's session gets `403`. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding a Slack channel needs the project's
    `lavaflow.slack` capability, and binding Aikido its
    `lavaflow.aikido` capability: where it is unavailable, this answers
    `404` with code `feature_unavailable`, or `403` with code
    `plan_required` when the owner's plan does not include LavaFlow.

    Args:
        body (Any): Send exactly one of `slack` and `aikido`, matching the connector's type.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowConnectorBinding]
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
    body: Any,

) -> Error | LavaflowConnectorBinding | None:
    """ Bind a connector to the project

     Binds a place in a connector to the project, so problems reported
    there reach LavaFlow for it, and answers `201`. Send `slack` for a
    `slack` connector and `aikido` for an `aikido` one. For a `slack`
    connector the place is a channel. Binding a channel that is already
    bound answers `200` with that binding, and makes the current owner the
    one who bound it, so a retry is safe. One of the Slack identities the
    caller's sign-in session signed in as must belong to the connector's
    workspace and be a member of the channel, so on an account several
    people share, each binds only channels they are in. The channel must
    be one the picker (`GET /user/slack/channels`) lists: one the Volcano
    app is in, and not archived, a Slack Connect channel, or shared
    across an organization.

    For an `aikido` connector the place is the workspace's new code
    (SAST) issues on the project's GitHub repository, at or above
    `min_severity`. The caller must have
    connected the workspace. Binding it again answers `200` and sets the
    new minimum. Each issue starts a LavaFlow run that stops at a pull
    request for review.

    Only the project's owner can bind, with a platform token or a live
    dashboard sign-in session. A session must come from the dashboard's
    own configured project; another project's session gets `403`. A project
    access token, or a request made through MCP, gets `403` with code
    `person_required`. Binding a Slack channel needs the project's
    `lavaflow.slack` capability, and binding Aikido its
    `lavaflow.aikido` capability: where it is unavailable, this answers
    `404` with code `feature_unavailable`, or `403` with code
    `plan_required` when the owner's plan does not include LavaFlow.

    Args:
        body (Any): Send exactly one of `slack` and `aikido`, matching the connector's type.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowConnectorBinding
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
