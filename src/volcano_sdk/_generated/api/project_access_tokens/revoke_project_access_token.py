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
    token_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/access-tokens/{token_id}".format(id=quote(str(id), safe=""),token_id=quote(str(token_id), safe=""),),
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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Revoke a project access token

     Revokes the token. It stops authenticating immediately in the region
    handling this call and within seconds across Volcano's other regions.

    The record is kept rather than deleted, so the token's name, prefix, last
    use, and request history stay available — which is what you need if you
    are revoking because a secret leaked. Revoking an already-revoked token
    succeeds.

    Revoking does not undo anything the token already did. Treat whatever it
    could reach as exposed and rotate accordingly.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        id=id,
token_id=token_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Revoke a project access token

     Revokes the token. It stops authenticating immediately in the region
    handling this call and within seconds across Volcano's other regions.

    The record is kept rather than deleted, so the token's name, prefix, last
    use, and request history stay available — which is what you need if you
    are revoking because a secret leaked. Revoking an already-revoked token
    succeeds.

    Revoking does not undo anything the token already did. Treat whatever it
    could reach as exposed and rotate accordingly.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        id=id,
token_id=token_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Revoke a project access token

     Revokes the token. It stops authenticating immediately in the region
    handling this call and within seconds across Volcano's other regions.

    The record is kept rather than deleted, so the token's name, prefix, last
    use, and request history stay available — which is what you need if you
    are revoking because a secret leaked. Revoking an already-revoked token
    succeeds.

    Revoking does not undo anything the token already did. Treat whatever it
    could reach as exposed and rotate accordingly.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        id=id,
token_id=token_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    token_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Revoke a project access token

     Revokes the token. It stops authenticating immediately in the region
    handling this call and within seconds across Volcano's other regions.

    The record is kept rather than deleted, so the token's name, prefix, last
    use, and request history stay available — which is what you need if you
    are revoking because a secret leaked. Revoking an already-revoked token
    succeeds.

    Revoking does not undo anything the token already did. Treat whatever it
    could reach as exposed and rotate accordingly.

    Requires a platform token.

    Args:
        id (UUID):
        token_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        id=id,
token_id=token_id,
client=client,

    )).parsed
