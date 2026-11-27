from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_rollback_request import FunctionRollbackRequest
from ...models.function_serving import FunctionServing
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: UUID | str,
    *,
    body: FunctionRollbackRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions/{function_id}/serving/rollback".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionServing | None:
    if response.status_code == 200:
        response_200 = FunctionServing.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionServing]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: FunctionRollbackRequest,

) -> Response[Error | FunctionServing]:
    """ Roll back what a function runs

     Points the function's traffic back at what served it before its last promotion or rollback, or at
    its own build with `to_production`. A rollback is a new activation, so what it leaves becomes what
    a further rollback returns to, and it can itself be undone. Nothing is deployed, so it takes effect
    at once. It names the `revision` the caller read; a competing activation makes it fail with `409`.

    Rolling back to a preview promotes it again and is refused with `409` when promoting it would be,
    and with `404` code `feature_unavailable` while the capability is unavailable. Rolling back to the
    function's own build is not: it never depends on the capability, the project's source mode, or a
    running deployment of the function.

    Args:
        id (UUID):
        function_id (UUID):
        body (FunctionRollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionServing]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: FunctionRollbackRequest,

) -> Error | FunctionServing | None:
    """ Roll back what a function runs

     Points the function's traffic back at what served it before its last promotion or rollback, or at
    its own build with `to_production`. A rollback is a new activation, so what it leaves becomes what
    a further rollback returns to, and it can itself be undone. Nothing is deployed, so it takes effect
    at once. It names the `revision` the caller read; a competing activation makes it fail with `409`.

    Rolling back to a preview promotes it again and is refused with `409` when promoting it would be,
    and with `404` code `feature_unavailable` while the capability is unavailable. Rolling back to the
    function's own build is not: it never depends on the capability, the project's source mode, or a
    running deployment of the function.

    Args:
        id (UUID):
        function_id (UUID):
        body (FunctionRollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionServing
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: FunctionRollbackRequest,

) -> Response[Error | FunctionServing]:
    """ Roll back what a function runs

     Points the function's traffic back at what served it before its last promotion or rollback, or at
    its own build with `to_production`. A rollback is a new activation, so what it leaves becomes what
    a further rollback returns to, and it can itself be undone. Nothing is deployed, so it takes effect
    at once. It names the `revision` the caller read; a competing activation makes it fail with `409`.

    Rolling back to a preview promotes it again and is refused with `409` when promoting it would be,
    and with `404` code `feature_unavailable` while the capability is unavailable. Rolling back to the
    function's own build is not: it never depends on the capability, the project's source mode, or a
    running deployment of the function.

    Args:
        id (UUID):
        function_id (UUID):
        body (FunctionRollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionServing]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: FunctionRollbackRequest,

) -> Error | FunctionServing | None:
    """ Roll back what a function runs

     Points the function's traffic back at what served it before its last promotion or rollback, or at
    its own build with `to_production`. A rollback is a new activation, so what it leaves becomes what
    a further rollback returns to, and it can itself be undone. Nothing is deployed, so it takes effect
    at once. It names the `revision` the caller read; a competing activation makes it fail with `409`.

    Rolling back to a preview promotes it again and is refused with `409` when promoting it would be,
    and with `404` code `feature_unavailable` while the capability is unavailable. Rolling back to the
    function's own build is not: it never depends on the capability, the project's source mode, or a
    running deployment of the function.

    Args:
        id (UUID):
        function_id (UUID):
        body (FunctionRollbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionServing
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    )).parsed
