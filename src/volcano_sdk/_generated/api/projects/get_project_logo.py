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



def _get_kwargs(
    id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/logo".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | None:
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error]:
    """ Get the project logo image

     Returns the raw logo image stored in the project's storage folder. This
    endpoint is unauthenticated so the asset can be rendered directly in an
    `<img>` tag; project IDs are unguessable UUIDs and logos are
    non-sensitive branding. The `Project.logo_url` field exposes a versioned
    path to this endpoint.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Error | None:
    """ Get the project logo image

     Returns the raw logo image stored in the project's storage folder. This
    endpoint is unauthenticated so the asset can be rendered directly in an
    `<img>` tag; project IDs are unguessable UUIDs and logos are
    non-sensitive branding. The `Project.logo_url` field exposes a versioned
    path to this endpoint.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error]:
    """ Get the project logo image

     Returns the raw logo image stored in the project's storage folder. This
    endpoint is unauthenticated so the asset can be rendered directly in an
    `<img>` tag; project IDs are unguessable UUIDs and logos are
    non-sensitive branding. The `Project.logo_url` field exposes a versioned
    path to this endpoint.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Error | None:
    """ Get the project logo image

     Returns the raw logo image stored in the project's storage folder. This
    endpoint is unauthenticated so the asset can be rendered directly in an
    `<img>` tag; project IDs are unguessable UUIDs and logos are
    non-sensitive branding. The `Project.logo_url` field exposes a versioned
    path to this endpoint.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
