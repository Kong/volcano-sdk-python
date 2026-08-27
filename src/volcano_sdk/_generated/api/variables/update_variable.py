from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.update_variable_request import UpdateVariableRequest
from ...models.variable import Variable
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    name: str,
    *,
    body: UpdateVariableRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/variables/{name}".format(id=quote(str(id), safe=""),name=quote(str(name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Variable | None:
    if response.status_code == 200:
        response_200 = Variable.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Variable]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateVariableRequest,

) -> Response[Error | Variable]:
    """ Update a variable

     Updates a project-level environment variable and triggers asynchronous propagation
    to deployed functions and frontends in the project's configured regions.

    Args:
        id (UUID):
        name (str):
        body (UpdateVariableRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Variable]
     """


    kwargs = _get_kwargs(
        id=id,
name=name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateVariableRequest,

) -> Error | Variable | None:
    """ Update a variable

     Updates a project-level environment variable and triggers asynchronous propagation
    to deployed functions and frontends in the project's configured regions.

    Args:
        id (UUID):
        name (str):
        body (UpdateVariableRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Variable
     """


    return sync_detailed(
        id=id,
name=name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateVariableRequest,

) -> Response[Error | Variable]:
    """ Update a variable

     Updates a project-level environment variable and triggers asynchronous propagation
    to deployed functions and frontends in the project's configured regions.

    Args:
        id (UUID):
        name (str):
        body (UpdateVariableRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Variable]
     """


    kwargs = _get_kwargs(
        id=id,
name=name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateVariableRequest,

) -> Error | Variable | None:
    """ Update a variable

     Updates a project-level environment variable and triggers asynchronous propagation
    to deployed functions and frontends in the project's configured regions.

    Args:
        id (UUID):
        name (str):
        body (UpdateVariableRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Variable
     """


    return (await asyncio_detailed(
        id=id,
name=name,
client=client,
body=body,

    )).parsed
