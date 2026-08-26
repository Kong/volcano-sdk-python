from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    frontend_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/frontends/{frontend_id}".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 202:
        response_202 = cast(Any, None)
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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
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

) -> Response[Any | Error]:
    """ Delete a frontend

     Schedules asynchronous frontend deletion. If another deployment is running, the frontend
    preserves its current status and exposes the queued deletion through `pending_deployment_id`.
    Its status changes to `deleting` when cleanup starts. After cleanup, it returns 404 and no
    longer appears in frontend lists.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,

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

) -> Any | Error | None:
    """ Delete a frontend

     Schedules asynchronous frontend deletion. If another deployment is running, the frontend
    preserves its current status and exposes the queued deletion through `pending_deployment_id`.
    Its status changes to `deleting` when cleanup starts. After cleanup, it returns 404 and no
    longer appears in frontend lists.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Delete a frontend

     Schedules asynchronous frontend deletion. If another deployment is running, the frontend
    preserves its current status and exposes the queued deletion through `pending_deployment_id`.
    Its status changes to `deleting` when cleanup starts. After cleanup, it returns 404 and no
    longer appears in frontend lists.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,

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

) -> Any | Error | None:
    """ Delete a frontend

     Schedules asynchronous frontend deletion. If another deployment is running, the frontend
    preserves its current status and exposes the queued deletion through `pending_deployment_id`.
    Its status changes to `deleting` when cleanup starts. After cleanup, it returns 404 and no
    longer appears in frontend lists.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,

    )).parsed
