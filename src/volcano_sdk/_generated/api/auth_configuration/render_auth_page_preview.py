from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.hosted_auth_page_type import check_hosted_auth_page_type
from ...models.hosted_auth_page_type import HostedAuthPageType
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    ticket: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["ticket"] = ticket


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/pages/{page_type}/preview".format(id=quote(str(id), safe=""),page_type=quote(str(page_type), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 404:
        response_404 = response.text
        return response_404

    if response.status_code == 500:
        response_500 = response.text
        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[str]:
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
    client: AuthenticatedClient | Client,
    ticket: str,

) -> Response[str]:
    """ Render a short-lived managed auth page preview

     Public HTML endpoint for a preview URL returned by the POST operation.
    The signed ticket contains the unsaved appearance, expires shortly, and
    runs the production page runtime against mocked authentication responses.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        ticket (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,
ticket=ticket,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient | Client,
    ticket: str,

) -> str | None:
    """ Render a short-lived managed auth page preview

     Public HTML endpoint for a preview URL returned by the POST operation.
    The signed ticket contains the unsaved appearance, expires shortly, and
    runs the production page runtime against mocked authentication responses.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        ticket (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
     """


    return sync_detailed(
        id=id,
page_type=page_type,
client=client,
ticket=ticket,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient | Client,
    ticket: str,

) -> Response[str]:
    """ Render a short-lived managed auth page preview

     Public HTML endpoint for a preview URL returned by the POST operation.
    The signed ticket contains the unsaved appearance, expires shortly, and
    runs the production page runtime against mocked authentication responses.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        ticket (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
     """


    kwargs = _get_kwargs(
        id=id,
page_type=page_type,
ticket=ticket,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    client: AuthenticatedClient | Client,
    ticket: str,

) -> str | None:
    """ Render a short-lived managed auth page preview

     Public HTML endpoint for a preview URL returned by the POST operation.
    The signed ticket contains the unsaved appearance, expires shortly, and
    runs the production page runtime against mocked authentication responses.

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        ticket (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
     """


    return (await asyncio_detailed(
        id=id,
page_type=page_type,
client=client,
ticket=ticket,

    )).parsed
