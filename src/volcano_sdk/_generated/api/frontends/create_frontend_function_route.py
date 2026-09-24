from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_function_route_request import CreateFrontendFunctionRouteRequest
from ...models.error import Error
from ...models.frontend_function_route import FrontendFunctionRoute
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    frontend_id: UUID,
    *,
    body: CreateFrontendFunctionRouteRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/function-routes".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendFunctionRoute | None:
    if response.status_code == 201:
        response_201 = FrontendFunctionRoute.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendFunctionRoute]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendFunctionRouteRequest,

) -> Response[Error | FrontendFunctionRoute]:
    """ Route a Frontend path to an HTTP Function

     The Frontend and Function must belong to this Project. The Function may be private but must use HTTP
    invocation mode. The route applies to every hostname that resolves to the Frontend, including
    generated, custom-domain, preview, and local hostnames.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendFunctionRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendFunctionRoute]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendFunctionRouteRequest,

) -> Error | FrontendFunctionRoute | None:
    """ Route a Frontend path to an HTTP Function

     The Frontend and Function must belong to this Project. The Function may be private but must use HTTP
    invocation mode. The route applies to every hostname that resolves to the Frontend, including
    generated, custom-domain, preview, and local hostnames.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendFunctionRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendFunctionRoute
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendFunctionRouteRequest,

) -> Response[Error | FrontendFunctionRoute]:
    """ Route a Frontend path to an HTTP Function

     The Frontend and Function must belong to this Project. The Function may be private but must use HTTP
    invocation mode. The route applies to every hostname that resolves to the Frontend, including
    generated, custom-domain, preview, and local hostnames.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendFunctionRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendFunctionRoute]
     """


    kwargs = _get_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    frontend_id: UUID,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendFunctionRouteRequest,

) -> Error | FrontendFunctionRoute | None:
    """ Route a Frontend path to an HTTP Function

     The Frontend and Function must belong to this Project. The Function may be private but must use HTTP
    invocation mode. The route applies to every hostname that resolves to the Frontend, including
    generated, custom-domain, preview, and local hostnames.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendFunctionRouteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendFunctionRoute
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed
