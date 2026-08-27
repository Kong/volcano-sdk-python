from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_storage_policy_request import CreateStoragePolicyRequest
from ...models.storage_policy import StoragePolicy
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    bucket_name: str,
    *,
    body: CreateStoragePolicyRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/storage/buckets/{bucket_name}/policies".format(id=quote(str(id), safe=""),bucket_name=quote(str(bucket_name), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> StoragePolicy | None:
    if response.status_code == 201:
        response_201 = StoragePolicy.from_dict(response.json())



        return response_201

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[StoragePolicy]:
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
    body: CreateStoragePolicyRequest,

) -> Response[StoragePolicy]:
    """ Create a storage policy

    Args:
        id (UUID):
        bucket_name (str):
        body (CreateStoragePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StoragePolicy]
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
    body: CreateStoragePolicyRequest,

) -> StoragePolicy | None:
    """ Create a storage policy

    Args:
        id (UUID):
        bucket_name (str):
        body (CreateStoragePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StoragePolicy
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
    body: CreateStoragePolicyRequest,

) -> Response[StoragePolicy]:
    """ Create a storage policy

    Args:
        id (UUID):
        bucket_name (str):
        body (CreateStoragePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[StoragePolicy]
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
    body: CreateStoragePolicyRequest,

) -> StoragePolicy | None:
    """ Create a storage policy

    Args:
        id (UUID):
        bucket_name (str):
        body (CreateStoragePolicyRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        StoragePolicy
     """


    return (await asyncio_detailed(
        id=id,
bucket_name=bucket_name,
client=client,
body=body,

    )).parsed
