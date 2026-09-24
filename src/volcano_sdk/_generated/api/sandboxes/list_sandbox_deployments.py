from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_deployment_page import SandboxDeploymentPage
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/sandboxes/{sandbox_id}/deployments".format(id=quote(str(id), safe=""),sandbox_id=quote(str(sandbox_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxDeploymentPage:
    if response.status_code == 200:
        response_200 = SandboxDeploymentPage.from_dict(response.json())



        return response_200

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxDeploymentPage]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Response[Error | SandboxDeploymentPage]:
    """ List sandbox deployment history

    Args:
        id (UUID):
        sandbox_id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeploymentPage]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Error | SandboxDeploymentPage | None:
    """ List sandbox deployment history

    Args:
        id (UUID):
        sandbox_id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeploymentPage
     """


    return sync_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Response[Error | SandboxDeploymentPage]:
    """ List sandbox deployment history

    Args:
        id (UUID):
        sandbox_id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeploymentPage]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,

) -> Error | SandboxDeploymentPage | None:
    """ List sandbox deployment history

    Args:
        id (UUID):
        sandbox_id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeploymentPage
     """


    return (await asyncio_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,
limit=limit,
cursor=cursor,

    )).parsed
