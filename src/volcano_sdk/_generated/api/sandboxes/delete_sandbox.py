from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    sandbox_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/sandboxes/{sandbox_id}".format(id=quote(str(id), safe=""),sandbox_id=quote(str(sandbox_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error:
    if response.status_code == 202:
        response_202 = cast(Any, None)
        return response_202

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Retire a template and terminate its sessions

    Args:
        id (UUID):
        sandbox_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Retire a template and terminate its sessions

    Args:
        id (UUID):
        sandbox_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Retire a template and terminate its sessions

    Args:
        id (UUID):
        sandbox_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Retire a template and terminate its sessions

    Args:
        id (UUID):
        sandbox_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,

    )).parsed
