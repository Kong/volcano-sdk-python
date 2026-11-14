from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_route_request import CreateFrontendRouteRequest
from ...models.error import Error
from ...models.frontend_route import FrontendRoute
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    body: CreateFrontendRouteRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/frontend-routes".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendRoute | None:
    if response.status_code == 201:
        response_201 = FrontendRoute.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendRoute]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendRouteRequest,

) -> Response[Error | FrontendRoute]:
    """ Mount another Frontend at a path

     Serves `path_prefix` and everything under it on this Frontend's hostnames from another
    Frontend in the same Project. The path is forwarded unchanged, so the mounted Frontend must
    serve its pages under the prefix (page directories or a matching `basePath`). Its root
    `/_next/static` files and `/_next/image` requests are sent to it too. A Frontend may be
    mounted at several prefixes. Function and Frontend routes share one path namespace and the
    64-route limit; the most specific prefix wins. A mounted Frontend's own routes do not apply
    to requests it receives through a route. The route applies to every hostname that resolves
    to this Frontend, including generated, custom-domain, and local hostnames. While the mounted
    Frontend has no active deployment, its paths answer 502, as its own hostname does.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendRoute]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendRouteRequest,

) -> Error | FrontendRoute | None:
    """ Mount another Frontend at a path

     Serves `path_prefix` and everything under it on this Frontend's hostnames from another
    Frontend in the same Project. The path is forwarded unchanged, so the mounted Frontend must
    serve its pages under the prefix (page directories or a matching `basePath`). Its root
    `/_next/static` files and `/_next/image` requests are sent to it too. A Frontend may be
    mounted at several prefixes. Function and Frontend routes share one path namespace and the
    64-route limit; the most specific prefix wins. A mounted Frontend's own routes do not apply
    to requests it receives through a route. The route applies to every hostname that resolves
    to this Frontend, including generated, custom-domain, and local hostnames. While the mounted
    Frontend has no active deployment, its paths answer 502, as its own hostname does.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendRoute
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendRouteRequest,

) -> Response[Error | FrontendRoute]:
    """ Mount another Frontend at a path

     Serves `path_prefix` and everything under it on this Frontend's hostnames from another
    Frontend in the same Project. The path is forwarded unchanged, so the mounted Frontend must
    serve its pages under the prefix (page directories or a matching `basePath`). Its root
    `/_next/static` files and `/_next/image` requests are sent to it too. A Frontend may be
    mounted at several prefixes. Function and Frontend routes share one path namespace and the
    64-route limit; the most specific prefix wins. A mounted Frontend's own routes do not apply
    to requests it receives through a route. The route applies to every hostname that resolves
    to this Frontend, including generated, custom-domain, and local hostnames. While the mounted
    Frontend has no active deployment, its paths answer 502, as its own hostname does.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendRoute]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendRouteRequest,

) -> Error | FrontendRoute | None:
    """ Mount another Frontend at a path

     Serves `path_prefix` and everything under it on this Frontend's hostnames from another
    Frontend in the same Project. The path is forwarded unchanged, so the mounted Frontend must
    serve its pages under the prefix (page directories or a matching `basePath`). Its root
    `/_next/static` files and `/_next/image` requests are sent to it too. A Frontend may be
    mounted at several prefixes. Function and Frontend routes share one path namespace and the
    64-route limit; the most specific prefix wins. A mounted Frontend's own routes do not apply
    to requests it receives through a route. The route applies to every hostname that resolves
    to this Frontend, including generated, custom-domain, and local hostnames. While the mounted
    Frontend has no active deployment, its paths answer 502, as its own hostname does.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendRoute
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed
