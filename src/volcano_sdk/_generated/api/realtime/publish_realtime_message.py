from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.realtime_publish_request import RealtimePublishRequest
from ...models.realtime_publish_result import RealtimePublishResult
from typing import cast



def request_kwargs(
    *,
    body: RealtimePublishRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/realtime/v1/publish",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | RealtimePublishResult | None:
    if response.status_code == 202:
        response_202 = RealtimePublishResult.from_dict(response.json())



        return response_202

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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | RealtimePublishResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: RealtimePublishRequest,

) -> Response[Error | RealtimePublishResult]:
    """ Publish a message to a Realtime channel

     Sends one message to a broadcast or grant channel of the project
    embedded in the service-role key, for a backend that holds no
    WebSocket, such as a function. The key needs `realtime.publish`.

    `channel` is a client channel: `broadcast:<name>`, or
    `grant:<name>` for a channel only Realtime grant holders watch. Every
    subscriber receives `{"type": <event>, "payload": <payload>}` as the
    message data, the shape `channel.on(<event>, ...)` matches.

    The publish is metered like any server publish: the publish plus one
    per subscriber it reaches. Messages are not stored; a subscriber that
    was not connected misses it. A project's publishes share the rate a
    WebSocket client publishes at; over it the answer is 429
    `realtime_publish_rate_limited`.

    Args:
        body (RealtimePublishRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RealtimePublishResult]
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
    body: RealtimePublishRequest,

) -> Error | RealtimePublishResult | None:
    """ Publish a message to a Realtime channel

     Sends one message to a broadcast or grant channel of the project
    embedded in the service-role key, for a backend that holds no
    WebSocket, such as a function. The key needs `realtime.publish`.

    `channel` is a client channel: `broadcast:<name>`, or
    `grant:<name>` for a channel only Realtime grant holders watch. Every
    subscriber receives `{"type": <event>, "payload": <payload>}` as the
    message data, the shape `channel.on(<event>, ...)` matches.

    The publish is metered like any server publish: the publish plus one
    per subscriber it reaches. Messages are not stored; a subscriber that
    was not connected misses it. A project's publishes share the rate a
    WebSocket client publishes at; over it the answer is 429
    `realtime_publish_rate_limited`.

    Args:
        body (RealtimePublishRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RealtimePublishResult
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: RealtimePublishRequest,

) -> Response[Error | RealtimePublishResult]:
    """ Publish a message to a Realtime channel

     Sends one message to a broadcast or grant channel of the project
    embedded in the service-role key, for a backend that holds no
    WebSocket, such as a function. The key needs `realtime.publish`.

    `channel` is a client channel: `broadcast:<name>`, or
    `grant:<name>` for a channel only Realtime grant holders watch. Every
    subscriber receives `{"type": <event>, "payload": <payload>}` as the
    message data, the shape `channel.on(<event>, ...)` matches.

    The publish is metered like any server publish: the publish plus one
    per subscriber it reaches. Messages are not stored; a subscriber that
    was not connected misses it. A project's publishes share the rate a
    WebSocket client publishes at; over it the answer is 429
    `realtime_publish_rate_limited`.

    Args:
        body (RealtimePublishRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | RealtimePublishResult]
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
    body: RealtimePublishRequest,

) -> Error | RealtimePublishResult | None:
    """ Publish a message to a Realtime channel

     Sends one message to a broadcast or grant channel of the project
    embedded in the service-role key, for a backend that holds no
    WebSocket, such as a function. The key needs `realtime.publish`.

    `channel` is a client channel: `broadcast:<name>`, or
    `grant:<name>` for a channel only Realtime grant holders watch. Every
    subscriber receives `{"type": <event>, "payload": <payload>}` as the
    message data, the shape `channel.on(<event>, ...)` matches.

    The publish is metered like any server publish: the publish plus one
    per subscriber it reaches. Messages are not stored; a subscriber that
    was not connected misses it. A project's publishes share the rate a
    WebSocket client publishes at; over it the answer is 429
    `realtime_publish_rate_limited`.

    Args:
        body (RealtimePublishRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | RealtimePublishResult
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
