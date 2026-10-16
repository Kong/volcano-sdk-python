from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_message_direction import check_durable_message_direction
from ...models.durable_message_direction import DurableMessageDirection
from ...models.durable_message_list import DurableMessageList
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    direction: DurableMessageDirection | Unset = UNSET,
    name: str | Unset = UNSET,
    after: int | Unset = 0,
    limit: int | Unset = 100,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_direction: str | Unset = UNSET
    if not isinstance(direction, Unset):
        json_direction = direction

    params["direction"] = json_direction

    params["name"] = name

    params["after"] = after

    params["limit"] = limit


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/durable-functions/{function_id}/executions/{execution_id}/messages".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableMessageList | Error | None:
    if response.status_code == 200:
        response_200 = DurableMessageList.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableMessageList | Error]:
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
    direction: DurableMessageDirection | Unset = UNSET,
    name: str | Unset = UNSET,
    after: int | Unset = 0,
    limit: int | Unset = 100,

) -> Response[DurableMessageList | Error]:
    """ List a durable execution's messages

     Lists the messages sent to and published by an execution, oldest
    first. Pass the last `seq` you read as `after` to read only what came
    next.

    Project access tokens can list messages, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):
        direction (DurableMessageDirection | Unset): `in` is a message sent to the execution.
            `out` is one the execution
            published.
        name (str | Unset): The name a workflow waits on or publishes under: up to 237 printable
            ASCII characters.
        after (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageList | Error]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
execution_id=execution_id,
direction=direction,
name=name,
after=after,
limit=limit,

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
    direction: DurableMessageDirection | Unset = UNSET,
    name: str | Unset = UNSET,
    after: int | Unset = 0,
    limit: int | Unset = 100,

) -> DurableMessageList | Error | None:
    """ List a durable execution's messages

     Lists the messages sent to and published by an execution, oldest
    first. Pass the last `seq` you read as `after` to read only what came
    next.

    Project access tokens can list messages, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):
        direction (DurableMessageDirection | Unset): `in` is a message sent to the execution.
            `out` is one the execution
            published.
        name (str | Unset): The name a workflow waits on or publishes under: up to 237 printable
            ASCII characters.
        after (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageList | Error
     """


    return sync_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,
direction=direction,
name=name,
after=after,
limit=limit,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    direction: DurableMessageDirection | Unset = UNSET,
    name: str | Unset = UNSET,
    after: int | Unset = 0,
    limit: int | Unset = 100,

) -> Response[DurableMessageList | Error]:
    """ List a durable execution's messages

     Lists the messages sent to and published by an execution, oldest
    first. Pass the last `seq` you read as `after` to read only what came
    next.

    Project access tokens can list messages, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):
        direction (DurableMessageDirection | Unset): `in` is a message sent to the execution.
            `out` is one the execution
            published.
        name (str | Unset): The name a workflow waits on or publishes under: up to 237 printable
            ASCII characters.
        after (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageList | Error]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
execution_id=execution_id,
direction=direction,
name=name,
after=after,
limit=limit,

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
    direction: DurableMessageDirection | Unset = UNSET,
    name: str | Unset = UNSET,
    after: int | Unset = 0,
    limit: int | Unset = 100,

) -> DurableMessageList | Error | None:
    """ List a durable execution's messages

     Lists the messages sent to and published by an execution, oldest
    first. Pass the last `seq` you read as `after` to read only what came
    next.

    Project access tokens can list messages, including read-only ones.

    Args:
        id (UUID):
        function_id (str):
        execution_id (UUID):
        direction (DurableMessageDirection | Unset): `in` is a message sent to the execution.
            `out` is one the execution
            published.
        name (str | Unset): The name a workflow waits on or publishes under: up to 237 printable
            ASCII characters.
        after (int | Unset):  Default: 0.
        limit (int | Unset):  Default: 100.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageList | Error
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
execution_id=execution_id,
client=client,
direction=direction,
name=name,
after=after,
limit=limit,

    )).parsed
