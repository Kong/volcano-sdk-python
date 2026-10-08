from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_execution_operation_list import DurableExecutionOperationList
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
        "url": "/projects/{id}/durable-functions/{function_id}/executions/{execution_id}/operations".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableExecutionOperationList | Error | None:
    if response.status_code == 200:
        response_200 = DurableExecutionOperationList.from_dict(response.json())



        return response_200

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableExecutionOperationList | Error]:
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

) -> Response[DurableExecutionOperationList | Error]:
    """ List a durable execution's operations

     Returns the execution's trace: every operation it began — each step,
    wait, poll, child context, map item and parallel branch — with when it
    started and ended, how it ended, and each attempt of a retried step.
    `invocations` are the windows the function's code was actually running;
    the gaps between them are time the execution spent suspended, which is
    not charged.

    A finished execution's trace is final and `complete` is `true`. A
    running one is refreshed when it is read, and can be up to about ten
    seconds behind; `synced_at` says when it was last refreshed. Inputs,
    results and other payloads are never included.

    The list is not paginated: an execution is limited to 3,000
    operations, and a trace is read whole.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecutionOperationList | Error]
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

) -> DurableExecutionOperationList | Error | None:
    """ List a durable execution's operations

     Returns the execution's trace: every operation it began — each step,
    wait, poll, child context, map item and parallel branch — with when it
    started and ended, how it ended, and each attempt of a retried step.
    `invocations` are the windows the function's code was actually running;
    the gaps between them are time the execution spent suspended, which is
    not charged.

    A finished execution's trace is final and `complete` is `true`. A
    running one is refreshed when it is read, and can be up to about ten
    seconds behind; `synced_at` says when it was last refreshed. Inputs,
    results and other payloads are never included.

    The list is not paginated: an execution is limited to 3,000
    operations, and a trace is read whole.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecutionOperationList | Error
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

) -> Response[DurableExecutionOperationList | Error]:
    """ List a durable execution's operations

     Returns the execution's trace: every operation it began — each step,
    wait, poll, child context, map item and parallel branch — with when it
    started and ended, how it ended, and each attempt of a retried step.
    `invocations` are the windows the function's code was actually running;
    the gaps between them are time the execution spent suspended, which is
    not charged.

    A finished execution's trace is final and `complete` is `true`. A
    running one is refreshed when it is read, and can be up to about ten
    seconds behind; `synced_at` says when it was last refreshed. Inputs,
    results and other payloads are never included.

    The list is not paginated: an execution is limited to 3,000
    operations, and a trace is read whole.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableExecutionOperationList | Error]
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

) -> DurableExecutionOperationList | Error | None:
    """ List a durable execution's operations

     Returns the execution's trace: every operation it began — each step,
    wait, poll, child context, map item and parallel branch — with when it
    started and ended, how it ended, and each attempt of a retried step.
    `invocations` are the windows the function's code was actually running;
    the gaps between them are time the execution spent suspended, which is
    not charged.

    A finished execution's trace is final and `complete` is `true`. A
    running one is refreshed when it is read, and can be up to about ten
    seconds behind; `synced_at` says when it was last refreshed. Inputs,
    results and other payloads are never included.

    The list is not paginated: an execution is limited to 3,000
    operations, and a trace is read whole.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableExecutionOperationList | Error
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,

    )).parsed
