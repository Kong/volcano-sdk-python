from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_execution import DurableExecution
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/durable-functions/{function_id}/executions/{execution_id}".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableExecution | Error | None:
    if response.status_code == 200:
        response_200 = DurableExecution.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableExecution | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[DurableExecution | Error]:
    """ Get a durable execution

     Returns the execution's current state, including its `result` once it has
    succeeded. Poll this to wait for an execution to finish.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
execution_id=execution_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> DurableExecution | Error | None:
    """ Get a durable execution

     Returns the execution's current state, including its `result` once it has
    succeeded. Poll this to wait for an execution to finish.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return sync_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[DurableExecution | Error]:
    """ Get a durable execution

     Returns the execution's current state, including its `result` once it has
    succeeded. Poll this to wait for an execution to finish.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
execution_id=execution_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> DurableExecution | Error | None:
    """ Get a durable execution

     Returns the execution's current state, including its `result` once it has
    succeeded. Poll this to wait for an execution to finish.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,

    )).parsed
