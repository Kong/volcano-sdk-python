from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.log_search_request import LogSearchRequest
from ...models.log_search_response import LogSearchResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: LogSearchRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/logs/search".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LogSearchResponse | None:
    if response.status_code == 200:
        response_200 = LogSearchResponse.from_dict(response.json())



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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LogSearchResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogSearchRequest,

) -> Response[Error | LogSearchResponse]:
    """ Search project logs

     Search or filter logs for one resource type in the project. Set
    `resource.type` to `function`, `frontend`, or `database`. Add
    `resource.ids` to filter to one or more resources, and add
    `resource.deployments.ids` to read deployment logs instead of runtime
    logs for functions and frontends. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; requests for
    `resource.type=database` from a FREE-plan project owner return 403.
    Log history (runtime and deployment) is limited to the plan's retention
    window (FREE: 1 day, PRO: 30 days); older time ranges are clamped to that
    window.

    Args:
        id (UUID):
        body (LogSearchRequest): Search request for project logs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LogSearchResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogSearchRequest,

) -> Error | LogSearchResponse | None:
    """ Search project logs

     Search or filter logs for one resource type in the project. Set
    `resource.type` to `function`, `frontend`, or `database`. Add
    `resource.ids` to filter to one or more resources, and add
    `resource.deployments.ids` to read deployment logs instead of runtime
    logs for functions and frontends. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; requests for
    `resource.type=database` from a FREE-plan project owner return 403.
    Log history (runtime and deployment) is limited to the plan's retention
    window (FREE: 1 day, PRO: 30 days); older time ranges are clamped to that
    window.

    Args:
        id (UUID):
        body (LogSearchRequest): Search request for project logs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LogSearchResponse
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogSearchRequest,

) -> Response[Error | LogSearchResponse]:
    """ Search project logs

     Search or filter logs for one resource type in the project. Set
    `resource.type` to `function`, `frontend`, or `database`. Add
    `resource.ids` to filter to one or more resources, and add
    `resource.deployments.ids` to read deployment logs instead of runtime
    logs for functions and frontends. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; requests for
    `resource.type=database` from a FREE-plan project owner return 403.
    Log history (runtime and deployment) is limited to the plan's retention
    window (FREE: 1 day, PRO: 30 days); older time ranges are clamped to that
    window.

    Args:
        id (UUID):
        body (LogSearchRequest): Search request for project logs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LogSearchResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: LogSearchRequest,

) -> Error | LogSearchResponse | None:
    """ Search project logs

     Search or filter logs for one resource type in the project. Set
    `resource.type` to `function`, `frontend`, or `database`. Add
    `resource.ids` to filter to one or more resources, and add
    `resource.deployments.ids` to read deployment logs instead of runtime
    logs for functions and frontends. Deployment logs are not supported for
    databases. Database logs are a PRO-plan feature; requests for
    `resource.type=database` from a FREE-plan project owner return 403.
    Log history (runtime and deployment) is limited to the plan's retention
    window (FREE: 1 day, PRO: 30 days); older time ranges are clamped to that
    window.

    Args:
        id (UUID):
        body (LogSearchRequest): Search request for project logs.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LogSearchResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
