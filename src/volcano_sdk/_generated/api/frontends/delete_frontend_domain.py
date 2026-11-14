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
    frontend_id: UUID | str,
    domain: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/frontends/{frontend_id}/domains/{domain}".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),domain=quote(str(domain), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    domain: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Remove a custom domain from a frontend

     Detaches the domain. A domain other domains redirect to cannot be
    removed until those redirects are removed or retargeted.

    Args:
        id (UUID):
        frontend_id (UUID):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
domain=domain,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    frontend_id: UUID | str,
    domain: str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Remove a custom domain from a frontend

     Detaches the domain. A domain other domains redirect to cannot be
    removed until those redirects are removed or retargeted.

    Args:
        id (UUID):
        frontend_id (UUID):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
domain=domain,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    domain: str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Remove a custom domain from a frontend

     Detaches the domain. A domain other domains redirect to cannot be
    removed until those redirects are removed or retargeted.

    Args:
        id (UUID):
        frontend_id (UUID):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
domain=domain,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    frontend_id: UUID | str,
    domain: str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Remove a custom domain from a frontend

     Detaches the domain. A domain other domains redirect to cannot be
    removed until those redirects are removed or retargeted.

    Args:
        id (UUID):
        frontend_id (UUID):
        domain (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
domain=domain,
client=client,

    )).parsed
