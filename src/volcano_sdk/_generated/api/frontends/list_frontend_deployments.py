from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_frontend_deployments import PaginatedFrontendDeployments
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    frontend_id: UUID,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/frontends/{frontend_id}/deployments".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedFrontendDeployments | None:
    if response.status_code == 200:
        response_200 = PaginatedFrontendDeployments.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedFrontendDeployments]:
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,

) -> Response[Error | PaginatedFrontendDeployments]:
    """ List frontend deployments

    Args:
        id (UUID):
        frontend_id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedFrontendDeployments]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
page=page,
limit=limit,

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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,

) -> Error | PaginatedFrontendDeployments | None:
    """ List frontend deployments

    Args:
        id (UUID):
        frontend_id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedFrontendDeployments
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
page=page,
limit=limit,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,

) -> Response[Error | PaginatedFrontendDeployments]:
    """ List frontend deployments

    Args:
        id (UUID):
        frontend_id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedFrontendDeployments]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
page=page,
limit=limit,

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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,

) -> Error | PaginatedFrontendDeployments | None:
    """ List frontend deployments

    Args:
        id (UUID):
        frontend_id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedFrontendDeployments
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
page=page,
limit=limit,

    )).parsed
