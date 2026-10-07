from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_deployment import SandboxDeployment
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,

) -> dict[str, Any]:






    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/sandboxes/{sandbox_id}/deployments/{deployment_id}".format(id=quote(str(id), safe=""),sandbox_id=quote(str(sandbox_id), safe=""),deployment_id=quote(str(deployment_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxDeployment:
    if response.status_code == 200:
        response_200 = SandboxDeployment.from_dict(response.json())



        return response_200

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxDeployment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | SandboxDeployment]:
    """ Get a sandbox deployment

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeployment]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | SandboxDeployment | None:
    """ Get a sandbox deployment

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeployment
     """


    return sync_detailed(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | SandboxDeployment]:
    """ Get a sandbox deployment

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeployment]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | SandboxDeployment | None:
    """ Get a sandbox deployment

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeployment
     """


    return (await asyncio_detailed(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
client=client,

    )).parsed
