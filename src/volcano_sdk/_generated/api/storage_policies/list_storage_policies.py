from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.storage_policy import StoragePolicy
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    bucket_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/storage/buckets/{bucket_name}/policies".format(id=quote(str(id), safe=""),bucket_name=quote(str(bucket_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> list[StoragePolicy] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in (_response_200):
            response_200_item = StoragePolicy.from_dict(response_200_item_data)



            response_200.append(response_200_item)

        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[list[StoragePolicy]]:
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

) -> Response[list[StoragePolicy]]:
    """ List storage policies for a bucket

    Args:
        id (UUID):
        bucket_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StoragePolicy]]
     """


    kwargs = _get_kwargs(
        id=id,
bucket_name=bucket_name,

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

) -> list[StoragePolicy] | None:
    """ List storage policies for a bucket

    Args:
        id (UUID):
        bucket_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StoragePolicy]
     """


    return sync_detailed(
        id=id,
bucket_name=bucket_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    bucket_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[list[StoragePolicy]]:
    """ List storage policies for a bucket

    Args:
        id (UUID):
        bucket_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list[StoragePolicy]]
     """


    kwargs = _get_kwargs(
        id=id,
bucket_name=bucket_name,

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

) -> list[StoragePolicy] | None:
    """ List storage policies for a bucket

    Args:
        id (UUID):
        bucket_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list[StoragePolicy]
     """


    return (await asyncio_detailed(
        id=id,
bucket_name=bucket_name,
client=client,

    )).parsed
