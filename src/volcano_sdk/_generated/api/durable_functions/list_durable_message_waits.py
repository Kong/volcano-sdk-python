from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_message_wait_list import DurableMessageWaitList
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
        "url": "/projects/{id}/durable-functions/{function_id}/executions/{execution_id}/message-waits".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableMessageWaitList | Error | None:
    if response.status_code == 200:
        response_200 = DurableMessageWaitList.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableMessageWaitList | Error]:
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

) -> Response[DurableMessageWaitList | Error]:
    """ List a durable execution's open message waits

     Lists the waits an execution has open in `ctx.waitForMessage`, oldest
    first, so you can see which message names it is waiting for.

    Project access tokens can list waits, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageWaitList | Error]
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

) -> DurableMessageWaitList | Error | None:
    """ List a durable execution's open message waits

     Lists the waits an execution has open in `ctx.waitForMessage`, oldest
    first, so you can see which message names it is waiting for.

    Project access tokens can list waits, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageWaitList | Error
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

) -> Response[DurableMessageWaitList | Error]:
    """ List a durable execution's open message waits

     Lists the waits an execution has open in `ctx.waitForMessage`, oldest
    first, so you can see which message names it is waiting for.

    Project access tokens can list waits, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageWaitList | Error]
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

) -> DurableMessageWaitList | Error | None:
    """ List a durable execution's open message waits

     Lists the waits an execution has open in `ctx.waitForMessage`, oldest
    first, so you can see which message names it is waiting for.

    Project access tokens can list waits, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageWaitList | Error
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,

    )).parsed
