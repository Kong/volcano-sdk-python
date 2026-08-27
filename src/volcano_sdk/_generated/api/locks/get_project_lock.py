from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_lock_state import ProjectLockState
from typing import cast
from uuid import UUID



def _get_kwargs(
    key: str,
    *,
    x_volcano_request_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Volcano-Request-Id"] = x_volcano_request_id



    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/locks/{key}".format(key=quote(str(key), safe=""),),
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectLockState | None:
    if response.status_code == 200:
        response_200 = ProjectLockState.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectLockState]:
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
    x_volcano_request_id: UUID,

) -> Response[Error | ProjectLockState]:
    """ Read a project lock

     Reports whether the lock is currently held, when its lease expires, and the
    holder's fencing token. `held` follows takeover eligibility rather than raw
    expiry, so `held: false` means an acquire would succeed now. No lock token is
    required, making this usable for monitoring and recovery.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectLockState]
     """


    kwargs = _get_kwargs(
        key=key,
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
    x_volcano_request_id: UUID,

) -> Error | ProjectLockState | None:
    """ Read a project lock

     Reports whether the lock is currently held, when its lease expires, and the
    holder's fencing token. `held` follows takeover eligibility rather than raw
    expiry, so `held: false` means an acquire would succeed now. No lock token is
    required, making this usable for monitoring and recovery.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectLockState
     """


    return sync_detailed(
        key=key,
client=client,
x_volcano_request_id=x_volcano_request_id,

    ).parsed

async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    x_volcano_request_id: UUID,

) -> Response[Error | ProjectLockState]:
    """ Read a project lock

     Reports whether the lock is currently held, when its lease expires, and the
    holder's fencing token. `held` follows takeover eligibility rather than raw
    expiry, so `held: false` means an acquire would succeed now. No lock token is
    required, making this usable for monitoring and recovery.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectLockState]
     """


    kwargs = _get_kwargs(
        key=key,
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
    x_volcano_request_id: UUID,

) -> Error | ProjectLockState | None:
    """ Read a project lock

     Reports whether the lock is currently held, when its lease expires, and the
    holder's fencing token. `held` follows takeover eligibility rather than raw
    expiry, so `held: false` means an acquire would succeed now. No lock token is
    required, making this usable for monitoring and recovery.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectLockState
     """


    return (await asyncio_detailed(
        key=key,
client=client,
x_volcano_request_id=x_volcano_request_id,

    )).parsed
