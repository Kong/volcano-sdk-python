from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...types import File, FileTypes
from io import BytesIO
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/logo".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | File | None:
    if response.status_code == 200:
        response_200 = File(
             payload = BytesIO(response.content)
        )



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | File]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | File]:
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
        Response[Error | File]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient | Client,

) -> Error | File | None:
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
        Error | File
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | File]:
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
        Response[Error | File]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient | Client,

) -> Error | File | None:
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
        Error | File
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
