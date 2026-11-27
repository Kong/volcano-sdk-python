from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.update_sandbox_session_activity_body import UpdateSandboxSessionActivityBody
from typing import cast
from uuid import UUID



def request_kwargs(
    session_id: UUID | str,
    *,
    body: UpdateSandboxSessionActivityBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}






    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/sandbox-sessions/{session_id}".format(session_id=quote(str(session_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateSandboxSessionActivityBody,

) -> Response[Any | Error]:
    """ Report sandbox session activity

     Updates the session activity with one complete, ordered report. Other session fields keep their
    values. A scoped service key needs the `sandboxes.sessions.activity` permission. Send new events
    while the session is running, using a strictly increasing sequence per session. For `idle: true`,
    send a positive `idle_timeout_seconds` to set or replace the deadline. For `idle: false`, omit
    `idle_timeout_seconds`. Accepting this active report clears any existing idle deadline. Before
    expiry, an exact retry of the latest event preserves its deadline. Reads leave the timer alone.
    Suspension preserves it, and the original session lifetime still applies. At the idle deadline, live
    access ends. When Volcano terminates the VM for idle expiry, its local files are lost and the
    session records `sandbox_idle_expired` in `last_error_code`.

    Args:
        session_id (UUID):
        body (UpdateSandboxSessionActivityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        session_id=session_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    session_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateSandboxSessionActivityBody,

) -> Any | Error | None:
    """ Report sandbox session activity

     Updates the session activity with one complete, ordered report. Other session fields keep their
    values. A scoped service key needs the `sandboxes.sessions.activity` permission. Send new events
    while the session is running, using a strictly increasing sequence per session. For `idle: true`,
    send a positive `idle_timeout_seconds` to set or replace the deadline. For `idle: false`, omit
    `idle_timeout_seconds`. Accepting this active report clears any existing idle deadline. Before
    expiry, an exact retry of the latest event preserves its deadline. Reads leave the timer alone.
    Suspension preserves it, and the original session lifetime still applies. At the idle deadline, live
    access ends. When Volcano terminates the VM for idle expiry, its local files are lost and the
    session records `sandbox_idle_expired` in `last_error_code`.

    Args:
        session_id (UUID):
        body (UpdateSandboxSessionActivityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        session_id=session_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    session_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateSandboxSessionActivityBody,

) -> Response[Any | Error]:
    """ Report sandbox session activity

     Updates the session activity with one complete, ordered report. Other session fields keep their
    values. A scoped service key needs the `sandboxes.sessions.activity` permission. Send new events
    while the session is running, using a strictly increasing sequence per session. For `idle: true`,
    send a positive `idle_timeout_seconds` to set or replace the deadline. For `idle: false`, omit
    `idle_timeout_seconds`. Accepting this active report clears any existing idle deadline. Before
    expiry, an exact retry of the latest event preserves its deadline. Reads leave the timer alone.
    Suspension preserves it, and the original session lifetime still applies. At the idle deadline, live
    access ends. When Volcano terminates the VM for idle expiry, its local files are lost and the
    session records `sandbox_idle_expired` in `last_error_code`.

    Args:
        session_id (UUID):
        body (UpdateSandboxSessionActivityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        session_id=session_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    session_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateSandboxSessionActivityBody,

) -> Any | Error | None:
    """ Report sandbox session activity

     Updates the session activity with one complete, ordered report. Other session fields keep their
    values. A scoped service key needs the `sandboxes.sessions.activity` permission. Send new events
    while the session is running, using a strictly increasing sequence per session. For `idle: true`,
    send a positive `idle_timeout_seconds` to set or replace the deadline. For `idle: false`, omit
    `idle_timeout_seconds`. Accepting this active report clears any existing idle deadline. Before
    expiry, an exact retry of the latest event preserves its deadline. Reads leave the timer alone.
    Suspension preserves it, and the original session lifetime still applies. At the idle deadline, live
    access ends. When Volcano terminates the VM for idle expiry, its local files are lost and the
    session records `sandbox_idle_expired` in `last_error_code`.

    Args:
        session_id (UUID):
        body (UpdateSandboxSessionActivityBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,

    )).parsed
