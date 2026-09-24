from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_command_request import SandboxCommandRequest
from ...models.sandbox_command_result import SandboxCommandResult
from typing import cast
from uuid import UUID



def _get_kwargs(
    session_id: UUID,
    *,
    body: SandboxCommandRequest,
    idempotency_key: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandbox-sessions/{session_id}/exec".format(session_id=quote(str(session_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxCommandResult:
    if response.status_code == 200:
        response_200 = SandboxCommandResult.from_dict(response.json())



        return response_200

    response_default = Error.from_dict(response.json())



    return response_default



def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxCommandResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SandboxCommandRequest,
    idempotency_key: UUID,

) -> Response[Error | SandboxCommandResult]:
    """ Execute a command within a session

    Args:
        session_id (UUID):
        idempotency_key (UUID):
        body (SandboxCommandRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxCommandResult]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SandboxCommandRequest,
    idempotency_key: UUID,

) -> Error | SandboxCommandResult | None:
    """ Execute a command within a session

    Args:
        session_id (UUID):
        idempotency_key (UUID):
        body (SandboxCommandRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxCommandResult
     """


    return sync_detailed(
        session_id=session_id,
client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SandboxCommandRequest,
    idempotency_key: UUID,

) -> Response[Error | SandboxCommandResult]:
    """ Execute a command within a session

    Args:
        session_id (UUID):
        idempotency_key (UUID):
        body (SandboxCommandRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxCommandResult]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient,
    body: SandboxCommandRequest,
    idempotency_key: UUID,

) -> Error | SandboxCommandResult | None:
    """ Execute a command within a session

    Args:
        session_id (UUID):
        idempotency_key (UUID):
        body (SandboxCommandRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxCommandResult
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
