from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend import Frontend
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    frontend_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/redeploy".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Frontend | None:
    if response.status_code == 200:
        response_200 = Frontend.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Frontend]:
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

) -> Response[Error | Frontend]:
    """ Redeploy frontend using latest uploaded artifact

     Starts a new frontend workflow using the latest stored artifact. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. An overlapping deployment preserves the frontend's current status, is exposed through
    `pending_deployment_id`, and supersedes any older queued deployment. The previous runtime and its
    published static assets remain available during provisioning, and a failed redeploy restores the
    regional runtimes to that build and keeps it serving while the attempted deployment is recorded as
    failed.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
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

) -> Error | Frontend | None:
    """ Redeploy frontend using latest uploaded artifact

     Starts a new frontend workflow using the latest stored artifact. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. An overlapping deployment preserves the frontend's current status, is exposed through
    `pending_deployment_id`, and supersedes any older queued deployment. The previous runtime and its
    published static assets remain available during provisioning, and a failed redeploy restores the
    regional runtimes to that build and keeps it serving while the attempted deployment is recorded as
    failed.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
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

) -> Response[Error | Frontend]:
    """ Redeploy frontend using latest uploaded artifact

     Starts a new frontend workflow using the latest stored artifact. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. An overlapping deployment preserves the frontend's current status, is exposed through
    `pending_deployment_id`, and supersedes any older queued deployment. The previous runtime and its
    published static assets remain available during provisioning, and a failed redeploy restores the
    regional runtimes to that build and keeps it serving while the attempted deployment is recorded as
    failed.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
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

) -> Error | Frontend | None:
    """ Redeploy frontend using latest uploaded artifact

     Starts a new frontend workflow using the latest stored artifact. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. An overlapping deployment preserves the frontend's current status, is exposed through
    `pending_deployment_id`, and supersedes any older queued deployment. The previous runtime and its
    published static assets remain available during provisioning, and a failed redeploy restores the
    regional runtimes to that build and keeps it serving while the attempted deployment is recorded as
    failed.

    Args:
        id (UUID):
        frontend_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,

    )).parsed
