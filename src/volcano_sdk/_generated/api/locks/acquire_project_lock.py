from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_lock_lease import ProjectLockLease
from ...models.project_lock_lease_request import ProjectLockLeaseRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    key: str,
    *,
    body: ProjectLockLeaseRequest,
    x_volcano_lock_token: UUID,
    x_volcano_request_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Volcano-Lock-Token"] = x_volcano_lock_token

    headers["X-Volcano-Request-Id"] = x_volcano_request_id



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/locks/{key}/lease".format(key=quote(str(key), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectLockLease | None:
    if response.status_code == 201:
        response_201 = ProjectLockLease.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectLockLease]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: ProjectLockLeaseRequest,
    x_volcano_lock_token: UUID,
    x_volcano_request_id: UUID,

) -> Response[Error | ProjectLockLease]:
    """ Acquire a project lock

     Acquires a project-scoped lease using the project embedded in the service-role key.
    The caller must hold the `locks.manage` permission. Repeating the request with the
    same lock token is idempotent and resets that lease to the requested TTL. A different
    live owner receives `409 lock_held`; a caller whose own lease already lapsed receives
    `409 lock_ownership_lost`.

    Args:
        key (str):
        x_volcano_lock_token (UUID):
        x_volcano_request_id (UUID):
        body (ProjectLockLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectLockLease]
     """


    kwargs = _get_kwargs(
        key=key,
body=body,
x_volcano_lock_token=x_volcano_lock_token,
x_volcano_request_id=x_volcano_request_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    key: str,
    *,
    client: AuthenticatedClient,
    body: ProjectLockLeaseRequest,
    x_volcano_lock_token: UUID,
    x_volcano_request_id: UUID,

) -> Error | ProjectLockLease | None:
    """ Acquire a project lock

     Acquires a project-scoped lease using the project embedded in the service-role key.
    The caller must hold the `locks.manage` permission. Repeating the request with the
    same lock token is idempotent and resets that lease to the requested TTL. A different
    live owner receives `409 lock_held`; a caller whose own lease already lapsed receives
    `409 lock_ownership_lost`.

    Args:
        key (str):
        x_volcano_lock_token (UUID):
        x_volcano_request_id (UUID):
        body (ProjectLockLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectLockLease
     """


    return sync_detailed(
        key=key,
client=client,
body=body,
x_volcano_lock_token=x_volcano_lock_token,
x_volcano_request_id=x_volcano_request_id,

    ).parsed

async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    body: ProjectLockLeaseRequest,
    x_volcano_lock_token: UUID,
    x_volcano_request_id: UUID,

) -> Response[Error | ProjectLockLease]:
    """ Acquire a project lock

     Acquires a project-scoped lease using the project embedded in the service-role key.
    The caller must hold the `locks.manage` permission. Repeating the request with the
    same lock token is idempotent and resets that lease to the requested TTL. A different
    live owner receives `409 lock_held`; a caller whose own lease already lapsed receives
    `409 lock_ownership_lost`.

    Args:
        key (str):
        x_volcano_lock_token (UUID):
        x_volcano_request_id (UUID):
        body (ProjectLockLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectLockLease]
     """


    kwargs = _get_kwargs(
        key=key,
body=body,
x_volcano_lock_token=x_volcano_lock_token,
x_volcano_request_id=x_volcano_request_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    key: str,
    *,
    client: AuthenticatedClient,
    body: ProjectLockLeaseRequest,
    x_volcano_lock_token: UUID,
    x_volcano_request_id: UUID,

) -> Error | ProjectLockLease | None:
    """ Acquire a project lock

     Acquires a project-scoped lease using the project embedded in the service-role key.
    The caller must hold the `locks.manage` permission. Repeating the request with the
    same lock token is idempotent and resets that lease to the requested TTL. A different
    live owner receives `409 lock_held`; a caller whose own lease already lapsed receives
    `409 lock_ownership_lost`.

    Args:
        key (str):
        x_volcano_lock_token (UUID):
        x_volcano_request_id (UUID):
        body (ProjectLockLeaseRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectLockLease
     """


    return (await asyncio_detailed(
        key=key,
client=client,
body=body,
x_volcano_lock_token=x_volcano_lock_token,
x_volcano_request_id=x_volcano_request_id,

    )).parsed
