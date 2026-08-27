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
from ...models.update_auth_hosted_page_request import UpdateAuthHostedPageRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    body: UpdateAuthHostedPageRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/auth/hosted-pages/{page_type}".format(id=quote(str(id), safe=""),page_type=quote(str(page_type), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthHostedPageResponse | None:
    if response.status_code == 200:
        response_200 = AuthHostedPageResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthHostedPageResponse]:
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
    body: UpdateAuthHostedPageRequest,

) -> Response[Any | AuthHostedPageResponse]:
    """ Update hosted auth page

     Saves the current HTML/CSS for this page type.
    Security validation rejects script tags, javascript: URLs, inline event handlers,
    iframe/object/embed/meta/link tags in HTML,
    and closing style/head tags in CSS.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthHostedPageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthHostedPageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,
body=body,

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
    body: UpdateAuthHostedPageRequest,

) -> Any | AuthHostedPageResponse | None:
    """ Update hosted auth page

     Saves the current HTML/CSS for this page type.
    Security validation rejects script tags, javascript: URLs, inline event handlers,
    iframe/object/embed/meta/link tags in HTML,
    and closing style/head tags in CSS.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthHostedPageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthHostedPageResponse
     """


    return sync_detailed(
        id=id,
page_type=page_type,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient,
    body: UpdateAuthHostedPageRequest,

) -> Response[Any | AuthHostedPageResponse]:
    """ Update hosted auth page

     Saves the current HTML/CSS for this page type.
    Security validation rejects script tags, javascript: URLs, inline event handlers,
    iframe/object/embed/meta/link tags in HTML,
    and closing style/head tags in CSS.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthHostedPageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthHostedPageResponse]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,
body=body,

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
    body: UpdateAuthHostedPageRequest,

) -> Any | AuthHostedPageResponse | None:
    """ Update hosted auth page

     Saves the current HTML/CSS for this page type.
    Security validation rejects script tags, javascript: URLs, inline event handlers,
    iframe/object/embed/meta/link tags in HTML,
    and closing style/head tags in CSS.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthHostedPageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthHostedPageResponse
     """


    return (await asyncio_detailed(
        id=id,
page_type=page_type,
client=client,
body=body,

    )).parsed
