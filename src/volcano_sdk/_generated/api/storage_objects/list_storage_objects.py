from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.storage_list_response import StorageListResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    bucket_name: str,
    *,
    prefix: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["prefix"] = prefix

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/storage/{bucket_name}".format(bucket_name=quote(str(bucket_name), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | StorageListResponse | None:
    if response.status_code == 200:
        response_200 = StorageListResponse.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error | StorageListResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[Any | Error | StorageListResponse]:
    """ List objects in a bucket

    Args:
        bucket_name (str):
        prefix (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | StorageListResponse]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
prefix=prefix,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Any | Error | StorageListResponse | None:
    """ List objects in a bucket

    Args:
        bucket_name (str):
        prefix (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | StorageListResponse
     """


    return sync_detailed(
        bucket_name=bucket_name,
client=client,
prefix=prefix,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Response[Any | Error | StorageListResponse]:
    """ List objects in a bucket

    Args:
        bucket_name (str):
        prefix (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | StorageListResponse]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
prefix=prefix,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    prefix: str | Unset = UNSET,
    limit: int | Unset = 50,
    cursor: str | Unset = UNSET,

) -> Any | Error | StorageListResponse | None:
    """ List objects in a bucket

    Args:
        bucket_name (str):
        prefix (str | Unset):
        limit (int | Unset):  Default: 50.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | StorageListResponse
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
client=client,
prefix=prefix,
limit=limit,
cursor=cursor,

    )).parsed
