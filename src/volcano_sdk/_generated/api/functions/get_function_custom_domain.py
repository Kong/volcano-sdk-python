from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_custom_domain_response import FunctionCustomDomainResponse
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    function_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/functions/{function_id}/domain".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionCustomDomainResponse | None | None:
    if response.status_code == 200:
        def _parse_response_200(data: object) -> FunctionCustomDomainResponse | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_1 = FunctionCustomDomainResponse.from_dict(data)



                return response_200_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FunctionCustomDomainResponse | None, data)

        response_200 = _parse_response_200(response.json())

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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionCustomDomainResponse | None]:
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

) -> Response[Error | FunctionCustomDomainResponse | None]:
    """ Get a function custom domain

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCustomDomainResponse | None]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,

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

) -> Error | FunctionCustomDomainResponse | None | None:
    """ Get a function custom domain

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCustomDomainResponse | None
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    function_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | FunctionCustomDomainResponse | None]:
    """ Get a function custom domain

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCustomDomainResponse | None]
     """


    kwargs = _get_kwargs(
        id=id,
function_id=function_id,

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

) -> Error | FunctionCustomDomainResponse | None | None:
    """ Get a function custom domain

    Args:
        id (UUID):
        function_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCustomDomainResponse | None
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,

    )).parsed
