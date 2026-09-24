from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_project_access_token_request import CreateProjectAccessTokenRequest
from ...models.created_project_access_token import CreatedProjectAccessToken
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    body: CreateProjectAccessTokenRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/access-tokens".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CreatedProjectAccessToken | Error | None:
    if response.status_code == 201:
        response_201 = CreatedProjectAccessToken.from_dict(response.json())



        return response_201

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CreatedProjectAccessToken | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectAccessTokenRequest,

) -> Response[CreatedProjectAccessToken | Error]:
    """ Create a project access token

     Creates a project access token and returns its secret.

    The secret is in this response and nowhere else. Only its hash is
    stored, so it cannot be retrieved, displayed, or recovered later — save
    it when you create it.

    The name must be unique within the project, so a retry cannot mint a
    second credential. It cannot recover the first one either. A retry that
    returns `409` with code `access_token_name_exists` means the original
    create committed and its secret is unrecoverable: list the project's
    tokens, revoke the one holding that name, and create it again.

    Requires a platform token.

    Args:
        id (UUID):
        body (CreateProjectAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreatedProjectAccessToken | Error]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectAccessTokenRequest,

) -> CreatedProjectAccessToken | Error | None:
    """ Create a project access token

     Creates a project access token and returns its secret.

    The secret is in this response and nowhere else. Only its hash is
    stored, so it cannot be retrieved, displayed, or recovered later — save
    it when you create it.

    The name must be unique within the project, so a retry cannot mint a
    second credential. It cannot recover the first one either. A retry that
    returns `409` with code `access_token_name_exists` means the original
    create committed and its secret is unrecoverable: list the project's
    tokens, revoke the one holding that name, and create it again.

    Requires a platform token.

    Args:
        id (UUID):
        body (CreateProjectAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreatedProjectAccessToken | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectAccessTokenRequest,

) -> Response[CreatedProjectAccessToken | Error]:
    """ Create a project access token

     Creates a project access token and returns its secret.

    The secret is in this response and nowhere else. Only its hash is
    stored, so it cannot be retrieved, displayed, or recovered later — save
    it when you create it.

    The name must be unique within the project, so a retry cannot mint a
    second credential. It cannot recover the first one either. A retry that
    returns `409` with code `access_token_name_exists` means the original
    create committed and its secret is unrecoverable: list the project's
    tokens, revoke the one holding that name, and create it again.

    Requires a platform token.

    Args:
        id (UUID):
        body (CreateProjectAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CreatedProjectAccessToken | Error]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateProjectAccessTokenRequest,

) -> CreatedProjectAccessToken | Error | None:
    """ Create a project access token

     Creates a project access token and returns its secret.

    The secret is in this response and nowhere else. Only its hash is
    stored, so it cannot be retrieved, displayed, or recovered later — save
    it when you create it.

    The name must be unique within the project, so a retry cannot mint a
    second credential. It cannot recover the first one either. A retry that
    returns `409` with code `access_token_name_exists` means the original
    create committed and its secret is unrecoverable: list the project's
    tokens, revoke the one holding that name, and create it again.

    Requires a platform token.

    Args:
        id (UUID):
        body (CreateProjectAccessTokenRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CreatedProjectAccessToken | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
