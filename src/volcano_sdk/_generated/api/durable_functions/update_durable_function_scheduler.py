from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_scheduler import FunctionScheduler
from ...models.update_function_scheduler_request import UpdateFunctionSchedulerRequest
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: str,
    scheduler_id: UUID | str,
    *,
    body: UpdateFunctionSchedulerRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{id}/durable-functions/{function_id}/schedulers/{scheduler_id}".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),scheduler_id=quote(str(scheduler_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionScheduler | None:
    if response.status_code == 200:
        response_200 = FunctionScheduler.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionScheduler]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    function_id: str,
    scheduler_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateFunctionSchedulerRequest,

) -> Response[Error | FunctionScheduler]:
    """ Update a durable function scheduler

    Args:
        id (UUID):
        function_id (str):
        scheduler_id (UUID):
        body (UpdateFunctionSchedulerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionScheduler]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
scheduler_id=scheduler_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    function_id: str,
    scheduler_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateFunctionSchedulerRequest,

) -> Error | FunctionScheduler | None:
    """ Update a durable function scheduler

    Args:
        id (UUID):
        function_id (str):
        scheduler_id (UUID):
        body (UpdateFunctionSchedulerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionScheduler
     """


    return sync_detailed(
        id=id,
function_id=function_id,
scheduler_id=scheduler_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: str,
    scheduler_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateFunctionSchedulerRequest,

) -> Response[Error | FunctionScheduler]:
    """ Update a durable function scheduler

    Args:
        id (UUID):
        function_id (str):
        scheduler_id (UUID):
        body (UpdateFunctionSchedulerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionScheduler]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
scheduler_id=scheduler_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    function_id: str,
    scheduler_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateFunctionSchedulerRequest,

) -> Error | FunctionScheduler | None:
    """ Update a durable function scheduler

    Args:
        id (UUID):
        function_id (str):
        scheduler_id (UUID):
        body (UpdateFunctionSchedulerRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionScheduler
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
scheduler_id=scheduler_id,
client=client,
body=body,

    )).parsed
