from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_service_key_body import CreateServiceKeyBody
from ...models.service_key import ServiceKey
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateServiceKeyBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/service-keys".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | ServiceKey | None:
    if response.status_code == 201:
        response_201 = ServiceKey.from_dict(response.json())



        return response_201

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | ServiceKey]:
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
    body: CreateServiceKeyBody,

) -> Response[Any | ServiceKey]:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ServiceKey]
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
    body: CreateServiceKeyBody,

) -> Any | ServiceKey | None:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ServiceKey
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
    body: CreateServiceKeyBody,

) -> Response[Any | ServiceKey]:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | ServiceKey]
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
    body: CreateServiceKeyBody,

) -> Any | ServiceKey | None:
    """ Create service key

     Create a new service role key for admin operations.

    **WARNING:** Service keys bypass all RLS policies!
    Store securely and NEVER expose in frontend code.

    Args:
        id (UUID):
        body (CreateServiceKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | ServiceKey
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
