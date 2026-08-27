from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_hosted_page_response import AuthHostedPageResponse
from ...models.hosted_auth_page_type import check_hosted_auth_page_type
from ...models.hosted_auth_page_type import HostedAuthPageType
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    page_type: HostedAuthPageType,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/hosted-pages/{page_type}".format(id=quote(str(id), safe=""),page_type=quote(str(page_type), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthHostedPageResponse | None:
    if response.status_code == 200:
        response_200 = AuthHostedPageResponse.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthHostedPageResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient,

) -> Response[AuthHostedPageResponse]:
    """ Get hosted auth page

     Returns the saved HTML/CSS for the page type, or `page: null` when the
    project has not customized it yet. Always returns `defaults` (the theme
    shell to seed an editor with, which is valid input to the update endpoint)
    and `runtime` (the script the rendered page runs, plus a preview harness).

    Args:
        id (UUID):
        page_type (HostedAuthPageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthHostedPageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient,

) -> AuthHostedPageResponse | None:
    """ Get hosted auth page

     Returns the saved HTML/CSS for the page type, or `page: null` when the
    project has not customized it yet. Always returns `defaults` (the theme
    shell to seed an editor with, which is valid input to the update endpoint)
    and `runtime` (the script the rendered page runs, plus a preview harness).

    Args:
        id (UUID):
        page_type (HostedAuthPageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthHostedPageResponse
     """


    return sync_detailed(
        id=id,
page_type=page_type,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient,

) -> Response[AuthHostedPageResponse]:
    """ Get hosted auth page

     Returns the saved HTML/CSS for the page type, or `page: null` when the
    project has not customized it yet. Always returns `defaults` (the theme
    shell to seed an editor with, which is valid input to the update endpoint)
    and `runtime` (the script the rendered page runs, plus a preview harness).

    Args:
        id (UUID):
        page_type (HostedAuthPageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthHostedPageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient,

) -> AuthHostedPageResponse | None:
    """ Get hosted auth page

     Returns the saved HTML/CSS for the page type, or `page: null` when the
    project has not customized it yet. Always returns `defaults` (the theme
    shell to seed an editor with, which is valid input to the update endpoint)
    and `runtime` (the script the rendered page runs, plus a preview harness).

    Args:
        id (UUID):
        page_type (HostedAuthPageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthHostedPageResponse
     """


    return (await asyncio_detailed(
        id=id,
page_type=page_type,
client=client,

    )).parsed
