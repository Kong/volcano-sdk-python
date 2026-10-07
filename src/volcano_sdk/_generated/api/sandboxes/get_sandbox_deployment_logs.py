from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_build_log_page import SandboxBuildLogPage
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    region: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> dict[str, Any]:




    params: dict[str, Any] = {}

    params["region"] = region

    params["cursor"] = cursor

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/sandboxes/{sandbox_id}/deployments/{deployment_id}/logs".format(id=quote(str(id), safe=""),sandbox_id=quote(str(sandbox_id), safe=""),deployment_id=quote(str(deployment_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxBuildLogPage:
    if response.status_code == 200:
        response_200 = SandboxBuildLogPage.from_dict(response.json())



        return response_200

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxBuildLogPage]:
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
    region: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[Error | SandboxBuildLogPage]:
    """ Read sandbox deployment build logs

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):
        region (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxBuildLogPage]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
region=region,
cursor=cursor,
limit=limit,

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
    region: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Error | SandboxBuildLogPage | None:
    """ Read sandbox deployment build logs

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):
        region (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxBuildLogPage
     """


    return sync_detailed(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
client=client,
region=region,
cursor=cursor,
limit=limit,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    deployment_id: UUID | str,
    *,
    client: AuthenticatedClient,
    region: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Response[Error | SandboxBuildLogPage]:
    """ Read sandbox deployment build logs

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):
        region (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxBuildLogPage]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
region=region,
cursor=cursor,
limit=limit,

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
    region: str,
    cursor: str | Unset = UNSET,
    limit: int | Unset = 100,

) -> Error | SandboxBuildLogPage | None:
    """ Read sandbox deployment build logs

    Args:
        id (UUID):
        sandbox_id (UUID):
        deployment_id (UUID):
        region (str):
        cursor (str | Unset):
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxBuildLogPage
     """


    return (await asyncio_detailed(
        id=id,
sandbox_id=sandbox_id,
deployment_id=deployment_id,
client=client,
region=region,
cursor=cursor,
limit=limit,

    )).parsed
