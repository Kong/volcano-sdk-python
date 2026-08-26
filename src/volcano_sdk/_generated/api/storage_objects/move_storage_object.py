from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.storage_move_request import StorageMoveRequest
from ...models.storage_object import StorageObject
from typing import cast



def _get_kwargs(
    bucket_name: str,
    *,
    body: StorageMoveRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/storage/{bucket_name}/move".format(bucket_name=quote(str(bucket_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | StorageObject | None:
    if response.status_code == 200:
        response_200 = StorageObject.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error | StorageObject]:
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
    body: StorageMoveRequest,

) -> Response[Any | Error | StorageObject]:
    """ Move/rename an object

    Args:
        bucket_name (str):
        body (StorageMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | StorageObject]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: StorageMoveRequest,

) -> Any | Error | StorageObject | None:
    """ Move/rename an object

    Args:
        bucket_name (str):
        body (StorageMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | StorageObject
     """


    return sync_detailed(
        bucket_name=bucket_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: StorageMoveRequest,

) -> Response[Any | Error | StorageObject]:
    """ Move/rename an object

    Args:
        bucket_name (str):
        body (StorageMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | StorageObject]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: StorageMoveRequest,

) -> Any | Error | StorageObject | None:
    """ Move/rename an object

    Args:
        bucket_name (str):
        body (StorageMoveRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | StorageObject
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
client=client,
body=body,

    )).parsed
