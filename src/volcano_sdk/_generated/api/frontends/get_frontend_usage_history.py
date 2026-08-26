from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend_usage_history_response import FrontendUsageHistoryResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    frontend_id: UUID,
    *,
    days: int | Unset = 30,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["days"] = days


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/frontends/{frontend_id}/usage".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendUsageHistoryResponse | None:
    if response.status_code == 200:
        response_200 = FrontendUsageHistoryResponse.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendUsageHistoryResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Error | FrontendUsageHistoryResponse]:
    """ Per-day request and error counts for a single frontend

     Returns a zero-filled daily series of request counts and 5xx
    error counts for one frontend, oldest first. Each entry is one
    UTC day; missing days (no traffic recorded) come back as
    `requests: 0, errors: 0` so the response always has exactly
    `days` entries.

    Backs the Monitoring section on the Frontend detail page in
    volcano-web. `days` defaults to 30 and is capped at 90 to keep
    the (frontend_id, day) index scan bounded.

    Args:
        id (UUID):
        frontend_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendUsageHistoryResponse]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
days=days,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | FrontendUsageHistoryResponse | None:
    """ Per-day request and error counts for a single frontend

     Returns a zero-filled daily series of request counts and 5xx
    error counts for one frontend, oldest first. Each entry is one
    UTC day; missing days (no traffic recorded) come back as
    `requests: 0, errors: 0` so the response always has exactly
    `days` entries.

    Backs the Monitoring section on the Frontend detail page in
    volcano-web. `days` defaults to 30 and is capped at 90 to keep
    the (frontend_id, day) index scan bounded.

    Args:
        id (UUID):
        frontend_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendUsageHistoryResponse
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
days=days,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Response[Error | FrontendUsageHistoryResponse]:
    """ Per-day request and error counts for a single frontend

     Returns a zero-filled daily series of request counts and 5xx
    error counts for one frontend, oldest first. Each entry is one
    UTC day; missing days (no traffic recorded) come back as
    `requests: 0, errors: 0` so the response always has exactly
    `days` entries.

    Backs the Monitoring section on the Frontend detail page in
    volcano-web. `days` defaults to 30 and is capped at 90 to keep
    the (frontend_id, day) index scan bounded.

    Args:
        id (UUID):
        frontend_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendUsageHistoryResponse]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
days=days,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    days: int | Unset = 30,

) -> Error | FrontendUsageHistoryResponse | None:
    """ Per-day request and error counts for a single frontend

     Returns a zero-filled daily series of request counts and 5xx
    error counts for one frontend, oldest first. Each entry is one
    UTC day; missing days (no traffic recorded) come back as
    `requests: 0, errors: 0` so the response always has exactly
    `days` entries.

    Backs the Monitoring section on the Frontend detail page in
    volcano-web. `days` defaults to 30 and is capped at 90 to keep
    the (frontend_id, day) index scan bounded.

    Args:
        id (UUID):
        frontend_id (UUID):
        days (int | Unset):  Default: 30.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendUsageHistoryResponse
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
days=days,

    )).parsed
