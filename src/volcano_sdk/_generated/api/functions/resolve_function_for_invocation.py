from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.resolve_function_response import ResolveFunctionResponse
from typing import cast



def _get_kwargs(
    *,
    name: str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["name"] = name


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/functions/resolve",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ResolveFunctionResponse | None:
    if response.status_code == 200:
        response_200 = ResolveFunctionResponse.from_dict(response.json())



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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ResolveFunctionResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    name: str,

) -> Response[Error | ResolveFunctionResponse]:
    """ Resolve function name for invocation

     Resolves a DNS-safe function name to its function ID within the caller's project.

    SDKs use this endpoint internally to invoke by function name while routing by function ID.

    **With Service Key**:
    - Allowed

    **With Auth User Token**:
    - Allowed

    **With Anon Key**:
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResolveFunctionResponse]
     """


    kwargs = _get_kwargs(
        name=name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    name: str,

) -> Error | ResolveFunctionResponse | None:
    """ Resolve function name for invocation

     Resolves a DNS-safe function name to its function ID within the caller's project.

    SDKs use this endpoint internally to invoke by function name while routing by function ID.

    **With Service Key**:
    - Allowed

    **With Auth User Token**:
    - Allowed

    **With Anon Key**:
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResolveFunctionResponse
     """


    return sync_detailed(
        client=client,
name=name,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    name: str,

) -> Response[Error | ResolveFunctionResponse]:
    """ Resolve function name for invocation

     Resolves a DNS-safe function name to its function ID within the caller's project.

    SDKs use this endpoint internally to invoke by function name while routing by function ID.

    **With Service Key**:
    - Allowed

    **With Auth User Token**:
    - Allowed

    **With Anon Key**:
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ResolveFunctionResponse]
     """


    kwargs = _get_kwargs(
        name=name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    name: str,

) -> Error | ResolveFunctionResponse | None:
    """ Resolve function name for invocation

     Resolves a DNS-safe function name to its function ID within the caller's project.

    SDKs use this endpoint internally to invoke by function name while routing by function ID.

    **With Service Key**:
    - Allowed

    **With Auth User Token**:
    - Allowed

    **With Anon Key**:
    - Requires anon key permission: `functions.invoke`
    - Function must have `is_public: true`

    Args:
        name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ResolveFunctionResponse
     """


    return (await asyncio_detailed(
        client=client,
name=name,

    )).parsed
