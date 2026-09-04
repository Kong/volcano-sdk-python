from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hosted_renderable_page_type import check_hosted_renderable_page_type
from ...models.hosted_renderable_page_type import HostedRenderablePageType
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    page_type: HostedRenderablePageType,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/hosted/{page_type}".format(id=quote(str(id), safe=""),page_type=quote(str(page_type), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    page_type: HostedRenderablePageType,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | str]:
    """ Render a managed auth page

     Public HTML endpoint for signup, forgot-password, device approval,
    verify-email, and reset-password pages. Login uses the path without a
    page type.
    Requires `Accept: text/html`.
    Returns 404 when managed hosted pages are disabled for the project.

    Args:
        id (UUID):
        page_type (HostedRenderablePageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | str]
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
    page_type: HostedRenderablePageType,
    *,
    client: AuthenticatedClient | Client,

) -> Any | str | None:
    """ Render a managed auth page

     Public HTML endpoint for signup, forgot-password, device approval,
    verify-email, and reset-password pages. Login uses the path without a
    page type.
    Requires `Accept: text/html`.
    Returns 404 when managed hosted pages are disabled for the project.

    Args:
        id (UUID):
        page_type (HostedRenderablePageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | str
     """


    return sync_detailed(
        id=id,
page_type=page_type,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    page_type: HostedRenderablePageType,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | str]:
    """ Render a managed auth page

     Public HTML endpoint for signup, forgot-password, device approval,
    verify-email, and reset-password pages. Login uses the path without a
    page type.
    Requires `Accept: text/html`.
    Returns 404 when managed hosted pages are disabled for the project.

    Args:
        id (UUID):
        page_type (HostedRenderablePageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | str]
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
    page_type: HostedRenderablePageType,
    *,
    client: AuthenticatedClient | Client,

) -> Any | str | None:
    """ Render a managed auth page

     Public HTML endpoint for signup, forgot-password, device approval,
    verify-email, and reset-password pages. Login uses the path without a
    page type.
    Requires `Accept: text/html`.
    Returns 404 when managed hosted pages are disabled for the project.

    Args:
        id (UUID):
        page_type (HostedRenderablePageType):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | str
     """


    return (await asyncio_detailed(
        id=id,
page_type=page_type,
client=client,

    )).parsed
