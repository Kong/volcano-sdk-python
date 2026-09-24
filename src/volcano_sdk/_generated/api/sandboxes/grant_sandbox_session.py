from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_subject_grant_request import SandboxSubjectGrantRequest
from typing import cast
from uuid import UUID



def request_kwargs(
    session_id: UUID | str,
    subject_id: UUID | str,
    *,
    body: SandboxSubjectGrantRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/sandbox-sessions/{session_id}/grants/{subject_id}".format(session_id=quote(str(session_id), safe=""),subject_id=quote(str(subject_id), safe=""),),
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
    subject_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SandboxSubjectGrantRequest,

) -> Response[Any | Error]:
    """ Authorize an authenticated project user for this session

    Args:
        session_id (UUID):
        subject_id (UUID):
        body (SandboxSubjectGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        session_id=session_id,
subject_id=subject_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    session_id: UUID | str,
    subject_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SandboxSubjectGrantRequest,

) -> Any | Error | None:
    """ Authorize an authenticated project user for this session

    Args:
        session_id (UUID):
        subject_id (UUID):
        body (SandboxSubjectGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        session_id=session_id,
subject_id=subject_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    session_id: UUID | str,
    subject_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SandboxSubjectGrantRequest,

) -> Response[Any | Error]:
    """ Authorize an authenticated project user for this session

    Args:
        session_id (UUID):
        subject_id (UUID):
        body (SandboxSubjectGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        session_id=session_id,
subject_id=subject_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    session_id: UUID | str,
    subject_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SandboxSubjectGrantRequest,

) -> Any | Error | None:
    """ Authorize an authenticated project user for this session

    Args:
        session_id (UUID):
        subject_id (UUID):
        body (SandboxSubjectGrantRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        session_id=session_id,
subject_id=subject_id,
client=client,
body=body,

    )).parsed
