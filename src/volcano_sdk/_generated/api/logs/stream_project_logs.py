from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.log_stream_request import LogStreamRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: LogStreamRequest,
    last_event_id_query: str | Unset = UNSET,
    last_event_id_header: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(last_event_id_header, Unset):
        headers["Last-Event-ID"] = last_event_id_header



    

    params: dict[str, Any] = {}

    params["last_event_id"] = last_event_id_query


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/logs/stream".format(id=quote(str(id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | str | None:
    if response.status_code == 200:
        response_200 = response.text
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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogStreamRequest,
    last_event_id_query: str | Unset = UNSET,
    last_event_id_header: str | Unset = UNSET,

) -> Response[Error | str]:
    """ Stream project logs

     Live-tail project logs as Server-Sent Events. The request body uses the
    resource selector plus `q`, `start_time`, and `limit`,
    including runtime logs and function/frontend deployment logs selected
    with `resource.deployments`. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; `resource.type=database`
    from a FREE-plan project owner returns 403. The `q` field uses the same
    syntax as search and activity requests. Do not send `cursor` or
    `end_time`; use `/logs/search` for range backfills.
    Explicit historical `start_time` values are limited to the plan's
    retention window (FREE: 1 day, PRO: 30 days). Resume with
    `Last-Event-ID` or the `last_event_id` query parameter. The cursor is
    bound to the request body: the resource selector and every filter must
    match the original request when reconnecting, otherwise the request is
    rejected with `400`.

    This is a live tail, not a gap-free backfill. On connect or reconnect the
    server delivers at most `limit` of the most recent matching events from
    the cursor position and then follows new events; events older than that
    window are not replayed. Use `/logs/search` to backfill a time range.

    Args:
        id (UUID):
        last_event_id_query (str | Unset):
        last_event_id_header (str | Unset):
        body (LogStreamRequest): Stream request for live project logs. Pagination cursors and
            fixed end times are not supported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,
last_event_id_query=last_event_id_query,
last_event_id_header=last_event_id_header,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogStreamRequest,
    last_event_id_query: str | Unset = UNSET,
    last_event_id_header: str | Unset = UNSET,

) -> Error | str | None:
    """ Stream project logs

     Live-tail project logs as Server-Sent Events. The request body uses the
    resource selector plus `q`, `start_time`, and `limit`,
    including runtime logs and function/frontend deployment logs selected
    with `resource.deployments`. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; `resource.type=database`
    from a FREE-plan project owner returns 403. The `q` field uses the same
    syntax as search and activity requests. Do not send `cursor` or
    `end_time`; use `/logs/search` for range backfills.
    Explicit historical `start_time` values are limited to the plan's
    retention window (FREE: 1 day, PRO: 30 days). Resume with
    `Last-Event-ID` or the `last_event_id` query parameter. The cursor is
    bound to the request body: the resource selector and every filter must
    match the original request when reconnecting, otherwise the request is
    rejected with `400`.

    This is a live tail, not a gap-free backfill. On connect or reconnect the
    server delivers at most `limit` of the most recent matching events from
    the cursor position and then follows new events; events older than that
    window are not replayed. Use `/logs/search` to backfill a time range.

    Args:
        id (UUID):
        last_event_id_query (str | Unset):
        last_event_id_header (str | Unset):
        body (LogStreamRequest): Stream request for live project logs. Pagination cursors and
            fixed end times are not supported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
     """


    return sync_detailed(
        id=id,
client=client,
body=body,
last_event_id_query=last_event_id_query,
last_event_id_header=last_event_id_header,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogStreamRequest,
    last_event_id_query: str | Unset = UNSET,
    last_event_id_header: str | Unset = UNSET,

) -> Response[Error | str]:
    """ Stream project logs

     Live-tail project logs as Server-Sent Events. The request body uses the
    resource selector plus `q`, `start_time`, and `limit`,
    including runtime logs and function/frontend deployment logs selected
    with `resource.deployments`. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; `resource.type=database`
    from a FREE-plan project owner returns 403. The `q` field uses the same
    syntax as search and activity requests. Do not send `cursor` or
    `end_time`; use `/logs/search` for range backfills.
    Explicit historical `start_time` values are limited to the plan's
    retention window (FREE: 1 day, PRO: 30 days). Resume with
    `Last-Event-ID` or the `last_event_id` query parameter. The cursor is
    bound to the request body: the resource selector and every filter must
    match the original request when reconnecting, otherwise the request is
    rejected with `400`.

    This is a live tail, not a gap-free backfill. On connect or reconnect the
    server delivers at most `limit` of the most recent matching events from
    the cursor position and then follows new events; events older than that
    window are not replayed. Use `/logs/search` to backfill a time range.

    Args:
        id (UUID):
        last_event_id_query (str | Unset):
        last_event_id_header (str | Unset):
        body (LogStreamRequest): Stream request for live project logs. Pagination cursors and
            fixed end times are not supported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | str]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,
last_event_id_query=last_event_id_query,
last_event_id_header=last_event_id_header,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogStreamRequest,
    last_event_id_query: str | Unset = UNSET,
    last_event_id_header: str | Unset = UNSET,

) -> Error | str | None:
    """ Stream project logs

     Live-tail project logs as Server-Sent Events. The request body uses the
    resource selector plus `q`, `start_time`, and `limit`,
    including runtime logs and function/frontend deployment logs selected
    with `resource.deployments`. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; `resource.type=database`
    from a FREE-plan project owner returns 403. The `q` field uses the same
    syntax as search and activity requests. Do not send `cursor` or
    `end_time`; use `/logs/search` for range backfills.
    Explicit historical `start_time` values are limited to the plan's
    retention window (FREE: 1 day, PRO: 30 days). Resume with
    `Last-Event-ID` or the `last_event_id` query parameter. The cursor is
    bound to the request body: the resource selector and every filter must
    match the original request when reconnecting, otherwise the request is
    rejected with `400`.

    This is a live tail, not a gap-free backfill. On connect or reconnect the
    server delivers at most `limit` of the most recent matching events from
    the cursor position and then follows new events; events older than that
    window are not replayed. Use `/logs/search` to backfill a time range.

    Args:
        id (UUID):
        last_event_id_query (str | Unset):
        last_event_id_header (str | Unset):
        body (LogStreamRequest): Stream request for live project logs. Pagination cursors and
            fixed end times are not supported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | str
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,
last_event_id_query=last_event_id_query,
last_event_id_header=last_event_id_header,

    )).parsed
