from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_execution import DurableExecution
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    function_id: str,
    execution_id: UUID | str,
    *,
    x_volcano_client_token: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_volcano_client_token, Unset):
        headers["X-Volcano-Client-Token"] = x_volcano_client_token



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-functions/{function_id}/executions/{execution_id}/stop".format(function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableExecution | Error | None:
    if response.status_code == 200:
        response_200 = DurableExecution.from_dict(response.json())



        return response_200

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableExecution | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    x_volcano_client_token: str | Unset = UNSET,

) -> Response[DurableExecution | Error]:
    """ Stop a durable execution from an application

     Cancels a running execution with the credential that started it. Its
    completed steps are not undone.

    Access follows the same rules as reading the execution.

    The call is accepted rather than awaited: the response reports the
    execution as it was read back and may still say `running`. Poll
    `GET /durable-functions/{functionId}/executions/{executionId}` to see
    it settle into `stopped`.

    Stopping an execution that already finished is not an error: the
    response carries the state it settled in.

    Args:
        function_id (str):
        execution_id (UUID):
        x_volcano_client_token (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = request_kwargs(
        function_id=function_id,
execution_id=execution_id,
x_volcano_client_token=x_volcano_client_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    x_volcano_client_token: str | Unset = UNSET,

) -> DurableExecution | Error | None:
    """ Stop a durable execution from an application

     Cancels a running execution with the credential that started it. Its
    completed steps are not undone.

    Access follows the same rules as reading the execution.

    The call is accepted rather than awaited: the response reports the
    execution as it was read back and may still say `running`. Poll
    `GET /durable-functions/{functionId}/executions/{executionId}` to see
    it settle into `stopped`.

    Stopping an execution that already finished is not an error: the
    response carries the state it settled in.

    Args:
        function_id (str):
        execution_id (UUID):
        x_volcano_client_token (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return sync_detailed(
        function_id=function_id,
execution_id=execution_id,
client=client,
x_volcano_client_token=x_volcano_client_token,

    ).parsed

async def asyncio_detailed(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    x_volcano_client_token: str | Unset = UNSET,

) -> Response[DurableExecution | Error]:
    """ Stop a durable execution from an application

     Cancels a running execution with the credential that started it. Its
    completed steps are not undone.

    Access follows the same rules as reading the execution.

    The call is accepted rather than awaited: the response reports the
    execution as it was read back and may still say `running`. Poll
    `GET /durable-functions/{functionId}/executions/{executionId}` to see
    it settle into `stopped`.

    Stopping an execution that already finished is not an error: the
    response carries the state it settled in.

    Args:
        function_id (str):
        execution_id (UUID):
        x_volcano_client_token (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecution | Error]
     """


    kwargs = request_kwargs(
        function_id=function_id,
execution_id=execution_id,
x_volcano_client_token=x_volcano_client_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    x_volcano_client_token: str | Unset = UNSET,

) -> DurableExecution | Error | None:
    """ Stop a durable execution from an application

     Cancels a running execution with the credential that started it. Its
    completed steps are not undone.

    Access follows the same rules as reading the execution.

    The call is accepted rather than awaited: the response reports the
    execution as it was read back and may still say `running`. Poll
    `GET /durable-functions/{functionId}/executions/{executionId}` to see
    it settle into `stopped`.

    Stopping an execution that already finished is not an error: the
    response carries the state it settled in.

    Args:
        function_id (str):
        execution_id (UUID):
        x_volcano_client_token (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecution | Error
     """


    return (await asyncio_detailed(
        function_id=function_id,
execution_id=execution_id,
client=client,
x_volcano_client_token=x_volcano_client_token,

    )).parsed
