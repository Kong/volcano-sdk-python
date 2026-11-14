from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.connector import Connector
from ...models.connector_create import ConnectorCreate
from ...models.error import Error
from typing import cast



def request_kwargs(
    *,
    body: ConnectorCreate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/connectors",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Connector | Error | None:
    if response.status_code == 201:
        response_201 = Connector.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())



        return response_422

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

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
    *,
    client: AuthenticatedClient,
    body: ConnectorCreate,

) -> Response[Connector | Error]:
    """ Connect a service

     Connects an outside service with credentials the caller created there,
    and answers `201` with the connector. Today that is an `aikido`
    workspace, so LavaFlow can fix the security issues Aikido finds on the
    caller's projects. Install the Volcano Slack app with
    `POST /user/slack/installations` instead: it needs the browser.

    For Aikido, create a REST API client in Aikido's settings with read
    access to issues, repositories and the workspace, and a webhook
    signing secret on its webhooks page. Volcano checks the client with
    Aikido, reads which workspace it belongs to, and stores all three
    values encrypted; it never returns them. Then point an Aikido webhook
    for new issues at `https://<api-host>/webhooks/aikido`, and bind
    projects with `POST /lavaflow/connector-bindings`. Volcano writes
    nothing back to Aikido. A workspace connects to one Volcano account at
    a time.

    Connecting Aikido needs LavaFlow and Aikido reports to be available in
    this environment, as the `lavaflow.aikido` capability reports;
    otherwise this answers `404` with code `feature_unavailable`.

    Args:
        body (ConnectorCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | Error]
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
    body: ConnectorCreate,

) -> Connector | Error | None:
    """ Connect a service

     Connects an outside service with credentials the caller created there,
    and answers `201` with the connector. Today that is an `aikido`
    workspace, so LavaFlow can fix the security issues Aikido finds on the
    caller's projects. Install the Volcano Slack app with
    `POST /user/slack/installations` instead: it needs the browser.

    For Aikido, create a REST API client in Aikido's settings with read
    access to issues, repositories and the workspace, and a webhook
    signing secret on its webhooks page. Volcano checks the client with
    Aikido, reads which workspace it belongs to, and stores all three
    values encrypted; it never returns them. Then point an Aikido webhook
    for new issues at `https://<api-host>/webhooks/aikido`, and bind
    projects with `POST /lavaflow/connector-bindings`. Volcano writes
    nothing back to Aikido. A workspace connects to one Volcano account at
    a time.

    Connecting Aikido needs LavaFlow and Aikido reports to be available in
    this environment, as the `lavaflow.aikido` capability reports;
    otherwise this answers `404` with code `feature_unavailable`.

    Args:
        body (ConnectorCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ConnectorCreate,

) -> Response[Connector | Error]:
    """ Connect a service

     Connects an outside service with credentials the caller created there,
    and answers `201` with the connector. Today that is an `aikido`
    workspace, so LavaFlow can fix the security issues Aikido finds on the
    caller's projects. Install the Volcano Slack app with
    `POST /user/slack/installations` instead: it needs the browser.

    For Aikido, create a REST API client in Aikido's settings with read
    access to issues, repositories and the workspace, and a webhook
    signing secret on its webhooks page. Volcano checks the client with
    Aikido, reads which workspace it belongs to, and stores all three
    values encrypted; it never returns them. Then point an Aikido webhook
    for new issues at `https://<api-host>/webhooks/aikido`, and bind
    projects with `POST /lavaflow/connector-bindings`. Volcano writes
    nothing back to Aikido. A workspace connects to one Volcano account at
    a time.

    Connecting Aikido needs LavaFlow and Aikido reports to be available in
    this environment, as the `lavaflow.aikido` capability reports;
    otherwise this answers `404` with code `feature_unavailable`.

    Args:
        body (ConnectorCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Connector | Error]
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
    body: ConnectorCreate,

) -> Connector | Error | None:
    """ Connect a service

     Connects an outside service with credentials the caller created there,
    and answers `201` with the connector. Today that is an `aikido`
    workspace, so LavaFlow can fix the security issues Aikido finds on the
    caller's projects. Install the Volcano Slack app with
    `POST /user/slack/installations` instead: it needs the browser.

    For Aikido, create a REST API client in Aikido's settings with read
    access to issues, repositories and the workspace, and a webhook
    signing secret on its webhooks page. Volcano checks the client with
    Aikido, reads which workspace it belongs to, and stores all three
    values encrypted; it never returns them. Then point an Aikido webhook
    for new issues at `https://<api-host>/webhooks/aikido`, and bind
    projects with `POST /lavaflow/connector-bindings`. Volcano writes
    nothing back to Aikido. A workspace connects to one Volcano account at
    a time.

    Connecting Aikido needs LavaFlow and Aikido reports to be available in
    this environment, as the `lavaflow.aikido` capability reports;
    otherwise this answers `404` with code `feature_unavailable`.

    Args:
        body (ConnectorCreate):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Connector | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
