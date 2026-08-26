from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.storage_object import StorageObject
from ...models.storage_visibility_request import StorageVisibilityRequest
from typing import cast



def _get_kwargs(
    bucket_name: str,
    path: str,
    *,
    body: StorageVisibilityRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/storage/{bucket_name}/{path}/visibility".format(bucket_name=quote(str(bucket_name), safe=""),path=quote(str(path), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | StorageObject | None:
    if response.status_code == 200:
        response_200 = StorageObject.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | StorageObject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body: StorageVisibilityRequest,

) -> Response[Any | StorageObject]:
    """ Update file visibility (public/private)

     Change whether a file is publicly accessible. Only the file owner or a service key can change
    visibility.
    If the bucket defines UPDATE policies, the owner must also satisfy one of them.

    - Public files can be downloaded with just an anon key (no user authentication required)
    - Private files (default) require authentication and must pass policy checks
    - All downloads go through the Volcano API - there is no direct access to the underlying store

    Args:
        bucket_name (str):
        path (str):
        body (StorageVisibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | StorageObject]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body: StorageVisibilityRequest,

) -> Any | StorageObject | None:
    """ Update file visibility (public/private)

     Change whether a file is publicly accessible. Only the file owner or a service key can change
    visibility.
    If the bucket defines UPDATE policies, the owner must also satisfy one of them.

    - Public files can be downloaded with just an anon key (no user authentication required)
    - Private files (default) require authentication and must pass policy checks
    - All downloads go through the Volcano API - there is no direct access to the underlying store

    Args:
        bucket_name (str):
        path (str):
        body (StorageVisibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | StorageObject
     """


    return sync_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body: StorageVisibilityRequest,

) -> Response[Any | StorageObject]:
    """ Update file visibility (public/private)

     Change whether a file is publicly accessible. Only the file owner or a service key can change
    visibility.
    If the bucket defines UPDATE policies, the owner must also satisfy one of them.

    - Public files can be downloaded with just an anon key (no user authentication required)
    - Private files (default) require authentication and must pass policy checks
    - All downloads go through the Volcano API - there is no direct access to the underlying store

    Args:
        bucket_name (str):
        path (str):
        body (StorageVisibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | StorageObject]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body: StorageVisibilityRequest,

) -> Any | StorageObject | None:
    """ Update file visibility (public/private)

     Change whether a file is publicly accessible. Only the file owner or a service key can change
    visibility.
    If the bucket defines UPDATE policies, the owner must also satisfy one of them.

    - Public files can be downloaded with just an anon key (no user authentication required)
    - Private files (default) require authentication and must pass policy checks
    - All downloads go through the Volcano API - there is no direct access to the underlying store

    Args:
        bucket_name (str):
        path (str):
        body (StorageVisibilityRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | StorageObject
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,

    )).parsed
