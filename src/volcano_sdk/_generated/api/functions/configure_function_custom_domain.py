from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.configure_function_custom_domain_request import ConfigureFunctionCustomDomainRequest
from ...models.error import Error
from ...models.function_custom_domain_response import FunctionCustomDomainResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    function_id: UUID,
    *,
    body: ConfigureFunctionCustomDomainRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions/{function_id}/domain".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionCustomDomainResponse | None:
    if response.status_code == 200:
        response_200 = FunctionCustomDomainResponse.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = FunctionCustomDomainResponse.from_dict(response.json())



        return response_201

    if response.status_code == 202:
        response_202 = FunctionCustomDomainResponse.from_dict(response.json())



        return response_202

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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionCustomDomainResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ConfigureFunctionCustomDomainRequest,

) -> Response[Error | FunctionCustomDomainResponse]:
    """ Configure or rotate a function custom domain

     PRO capability. The function must be public, active, and use HTTP invocation mode.
    Configuration and rotation preserve the function's HTTP authentication mode and stored
    OpenAPI document.

    Args:
        id (UUID):
        function_id (UUID):
        body (ConfigureFunctionCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCustomDomainResponse]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ConfigureFunctionCustomDomainRequest,

) -> Error | FunctionCustomDomainResponse | None:
    """ Configure or rotate a function custom domain

     PRO capability. The function must be public, active, and use HTTP invocation mode.
    Configuration and rotation preserve the function's HTTP authentication mode and stored
    OpenAPI document.

    Args:
        id (UUID):
        function_id (UUID):
        body (ConfigureFunctionCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCustomDomainResponse
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ConfigureFunctionCustomDomainRequest,

) -> Response[Error | FunctionCustomDomainResponse]:
    """ Configure or rotate a function custom domain

     PRO capability. The function must be public, active, and use HTTP invocation mode.
    Configuration and rotation preserve the function's HTTP authentication mode and stored
    OpenAPI document.

    Args:
        id (UUID):
        function_id (UUID):
        body (ConfigureFunctionCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCustomDomainResponse]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,
    body: ConfigureFunctionCustomDomainRequest,

) -> Error | FunctionCustomDomainResponse | None:
    """ Configure or rotate a function custom domain

     PRO capability. The function must be public, active, and use HTTP invocation mode.
    Configuration and rotation preserve the function's HTTP authentication mode and stored
    OpenAPI document.

    Args:
        id (UUID):
        function_id (UUID):
        body (ConfigureFunctionCustomDomainRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCustomDomainResponse
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    )).parsed
