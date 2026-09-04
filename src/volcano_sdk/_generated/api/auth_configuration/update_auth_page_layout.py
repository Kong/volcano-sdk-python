from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.hosted_auth_page_type import check_hosted_auth_page_type
from ...models.hosted_auth_page_type import HostedAuthPageType
from ...models.update_auth_page_layout_request import UpdateAuthPageLayoutRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    page_type: HostedAuthPageType,
    *,
    body: UpdateAuthPageLayoutRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/auth/pages/{page_type}/layout".format(id=quote(str(id), safe=""),page_type=quote(str(page_type), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | UpdateAuthPageLayoutRequest | None:
    if response.status_code == 200:
        response_200 = UpdateAuthPageLayoutRequest.from_dict(response.json())



        return response_200

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | UpdateAuthPageLayoutRequest]:
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
    body: UpdateAuthPageLayoutRequest,

) -> Response[Error | UpdateAuthPageLayoutRequest]:
    """ Save one managed auth page layout

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthPageLayoutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAuthPageLayoutRequest]
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
    body: UpdateAuthPageLayoutRequest,

) -> Error | UpdateAuthPageLayoutRequest | None:
    """ Save one managed auth page layout

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthPageLayoutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAuthPageLayoutRequest
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
    body: UpdateAuthPageLayoutRequest,

) -> Response[Error | UpdateAuthPageLayoutRequest]:
    """ Save one managed auth page layout

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthPageLayoutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | UpdateAuthPageLayoutRequest]
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
    body: UpdateAuthPageLayoutRequest,

) -> Error | UpdateAuthPageLayoutRequest | None:
    """ Save one managed auth page layout

    Args:
        id (UUID):
        page_type (HostedAuthPageType):
        body (UpdateAuthPageLayoutRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | UpdateAuthPageLayoutRequest
     """


    return (await asyncio_detailed(
        id=id,
page_type=page_type,
client=client,
body=body,

    )).parsed
