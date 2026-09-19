from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.paginated_project_access_tokens import PaginatedProjectAccessTokens
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,
    include_revoked: bool | Unset = False,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["search"] = search

    params["include_revoked"] = include_revoked


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/access-tokens".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedProjectAccessTokens | None:
    if response.status_code == 200:
        response_200 = PaginatedProjectAccessTokens.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedProjectAccessTokens]:
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,
    include_revoked: bool | Unset = False,

) -> Response[Error | PaginatedProjectAccessTokens]:
    """ List a project's access tokens

     Lists the project's access tokens, newest first. Secrets are never
    returned: only a hash is stored, so a token's value exists solely in the
    response to the create call.

    Only tokens that can still authenticate are returned by default, so
    revoked and expired ones are hidden. Pass `include_revoked=true` to see
    them, which is how you find out what a key did before it stopped working.

    Requires a platform token. A project access token cannot manage project
    access tokens, so a leaked credential cannot enumerate or replace itself.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):
        include_revoked (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectAccessTokens]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
search=search,
include_revoked=include_revoked,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,
    include_revoked: bool | Unset = False,

) -> Error | PaginatedProjectAccessTokens | None:
    """ List a project's access tokens

     Lists the project's access tokens, newest first. Secrets are never
    returned: only a hash is stored, so a token's value exists solely in the
    response to the create call.

    Only tokens that can still authenticate are returned by default, so
    revoked and expired ones are hidden. Pass `include_revoked=true` to see
    them, which is how you find out what a key did before it stopped working.

    Requires a platform token. A project access token cannot manage project
    access tokens, so a leaked credential cannot enumerate or replace itself.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):
        include_revoked (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectAccessTokens
     """


    return sync_detailed(
        id=id,
client=client,
page=page,
limit=limit,
search=search,
include_revoked=include_revoked,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,
    include_revoked: bool | Unset = False,

) -> Response[Error | PaginatedProjectAccessTokens]:
    """ List a project's access tokens

     Lists the project's access tokens, newest first. Secrets are never
    returned: only a hash is stored, so a token's value exists solely in the
    response to the create call.

    Only tokens that can still authenticate are returned by default, so
    revoked and expired ones are hidden. Pass `include_revoked=true` to see
    them, which is how you find out what a key did before it stopped working.

    Requires a platform token. A project access token cannot manage project
    access tokens, so a leaked credential cannot enumerate or replace itself.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):
        include_revoked (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectAccessTokens]
     """


    kwargs = _get_kwargs(
        id=id,
page=page,
limit=limit,
search=search,
include_revoked=include_revoked,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    search: str | Unset = UNSET,
    include_revoked: bool | Unset = False,

) -> Error | PaginatedProjectAccessTokens | None:
    """ List a project's access tokens

     Lists the project's access tokens, newest first. Secrets are never
    returned: only a hash is stored, so a token's value exists solely in the
    response to the create call.

    Only tokens that can still authenticate are returned by default, so
    revoked and expired ones are hidden. Pass `include_revoked=true` to see
    them, which is how you find out what a key did before it stopped working.

    Requires a platform token. A project access token cannot manage project
    access tokens, so a leaked credential cannot enumerate or replace itself.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        search (str | Unset):
        include_revoked (bool | Unset):  Default: False.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectAccessTokens
     """


    return (await asyncio_detailed(
        id=id,
client=client,
page=page,
limit=limit,
search=search,
include_revoked=include_revoked,

    )).parsed
