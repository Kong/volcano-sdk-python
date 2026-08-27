from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.storage_bucket import StorageBucket
from ...models.update_storage_bucket_request import UpdateStorageBucketRequest
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    bucket_name: str,
    *,
    body: UpdateStorageBucketRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{id}/storage/buckets/{bucket_name}".format(id=quote(str(id), safe=""),bucket_name=quote(str(bucket_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> StorageBucket | None:
    if response.status_code == 200:
        response_200 = StorageBucket.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[StorageBucket]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateStorageBucketRequest,

) -> Response[StorageBucket]:
    """ Update storage bucket settings

    Args:
        id (UUID):
        bucket_name (str):
        body (UpdateStorageBucketRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StorageBucket]
     """


    kwargs = _get_kwargs(
        id=id,
bucket_name=bucket_name,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateStorageBucketRequest,

) -> StorageBucket | None:
    """ Update storage bucket settings

    Args:
        id (UUID):
        bucket_name (str):
        body (UpdateStorageBucketRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StorageBucket
     """


    return sync_detailed(
        id=id,
bucket_name=bucket_name,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateStorageBucketRequest,

) -> Response[StorageBucket]:
    """ Update storage bucket settings

    Args:
        id (UUID):
        bucket_name (str):
        body (UpdateStorageBucketRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StorageBucket]
     """


    kwargs = _get_kwargs(
        id=id,
bucket_name=bucket_name,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    bucket_name: str,
    *,
    client: AuthenticatedClient,
    body: UpdateStorageBucketRequest,

) -> StorageBucket | None:
    """ Update storage bucket settings

    Args:
        id (UUID):
        bucket_name (str):
        body (UpdateStorageBucketRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StorageBucket
     """


    return (await asyncio_detailed(
        id=id,
bucket_name=bucket_name,
client=client,
body=body,

    )).parsed
