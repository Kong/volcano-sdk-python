from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_execution_status import check_durable_execution_status
from ...models.durable_execution_status import DurableExecutionStatus
from ...models.error import Error
from ...models.paginated_durable_executions import PaginatedDurableExecutions
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    function_id: str,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableExecutionStatus | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/durable-functions/{function_id}/executions".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedDurableExecutions | None:
    if response.status_code == 200:
        response_200 = PaginatedDurableExecutions.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedDurableExecutions]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    function_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableExecutionStatus | Unset = UNSET,

) -> Response[Error | PaginatedDurableExecutions]:
    """ List a durable function's executions

     Returns the platform's last observed status for each execution; listing
    does not poll each one. Fetch a single execution for its live state.

    Args:
        id (UUID):
        function_id (str):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableExecutionStatus | Unset): Lifecycle state of an execution. `pending` covers
            the window between the
            platform reserving the execution name and the function accepting the
            start, and has no counterpart once the execution is under way.
            `succeeded`, `failed`, `timed_out`, `stopped` and `unknown` are
            terminal.

            `unknown` means the execution's outcome cannot be established, so no
            result or error can be given for it. Either it was under way and was
            never seen to finish, or its start failed with a `500` without the
            platform establishing whether the execution began — which is why a
            name whose start returned an error can later read as `unknown` rather
            than not being found. It is terminal because nothing can settle it
            later, and it is rare — treat it as an outcome to retry rather than a
            state to wait on. A retry under the same name picks this execution back
            up instead of starting a second one, and needs a free concurrency slot
            because an `unknown` execution has given its own up. `completed_at` on
            an `unknown` execution is when the platform gave up, not when the work
            ended.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableExecutions]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,
page=page,
limit=limit,
status=status,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    function_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableExecutionStatus | Unset = UNSET,

) -> Error | PaginatedDurableExecutions | None:
    """ List a durable function's executions

     Returns the platform's last observed status for each execution; listing
    does not poll each one. Fetch a single execution for its live state.

    Args:
        id (UUID):
        function_id (str):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableExecutionStatus | Unset): Lifecycle state of an execution. `pending` covers
            the window between the
            platform reserving the execution name and the function accepting the
            start, and has no counterpart once the execution is under way.
            `succeeded`, `failed`, `timed_out`, `stopped` and `unknown` are
            terminal.

            `unknown` means the execution's outcome cannot be established, so no
            result or error can be given for it. Either it was under way and was
            never seen to finish, or its start failed with a `500` without the
            platform establishing whether the execution began — which is why a
            name whose start returned an error can later read as `unknown` rather
            than not being found. It is terminal because nothing can settle it
            later, and it is rare — treat it as an outcome to retry rather than a
            state to wait on. A retry under the same name picks this execution back
            up instead of starting a second one, and needs a free concurrency slot
            because an `unknown` execution has given its own up. `completed_at` on
            an `unknown` execution is when the platform gave up, not when the work
            ended.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableExecutions
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,
page=page,
limit=limit,
status=status,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    function_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableExecutionStatus | Unset = UNSET,

) -> Response[Error | PaginatedDurableExecutions]:
    """ List a durable function's executions

     Returns the platform's last observed status for each execution; listing
    does not poll each one. Fetch a single execution for its live state.

    Args:
        id (UUID):
        function_id (str):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableExecutionStatus | Unset): Lifecycle state of an execution. `pending` covers
            the window between the
            platform reserving the execution name and the function accepting the
            start, and has no counterpart once the execution is under way.
            `succeeded`, `failed`, `timed_out`, `stopped` and `unknown` are
            terminal.

            `unknown` means the execution's outcome cannot be established, so no
            result or error can be given for it. Either it was under way and was
            never seen to finish, or its start failed with a `500` without the
            platform establishing whether the execution began — which is why a
            name whose start returned an error can later read as `unknown` rather
            than not being found. It is terminal because nothing can settle it
            later, and it is rare — treat it as an outcome to retry rather than a
            state to wait on. A retry under the same name picks this execution back
            up instead of starting a second one, and needs a free concurrency slot
            because an `unknown` execution has given its own up. `completed_at` on
            an `unknown` execution is when the platform gave up, not when the work
            ended.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableExecutions]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,
page=page,
limit=limit,
status=status,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    function_id: str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableExecutionStatus | Unset = UNSET,

) -> Error | PaginatedDurableExecutions | None:
    """ List a durable function's executions

     Returns the platform's last observed status for each execution; listing
    does not poll each one. Fetch a single execution for its live state.

    Args:
        id (UUID):
        function_id (str):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableExecutionStatus | Unset): Lifecycle state of an execution. `pending` covers
            the window between the
            platform reserving the execution name and the function accepting the
            start, and has no counterpart once the execution is under way.
            `succeeded`, `failed`, `timed_out`, `stopped` and `unknown` are
            terminal.

            `unknown` means the execution's outcome cannot be established, so no
            result or error can be given for it. Either it was under way and was
            never seen to finish, or its start failed with a `500` without the
            platform establishing whether the execution began — which is why a
            name whose start returned an error can later read as `unknown` rather
            than not being found. It is terminal because nothing can settle it
            later, and it is rare — treat it as an outcome to retry rather than a
            state to wait on. A retry under the same name picks this execution back
            up instead of starting a second one, and needs a free concurrency slot
            because an `unknown` execution has given its own up. `completed_at` on
            an `unknown` execution is when the platform gave up, not when the work
            ended.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableExecutions
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,
page=page,
limit=limit,
status=status,

    )).parsed
