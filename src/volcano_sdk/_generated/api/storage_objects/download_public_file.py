from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    project_id: UUID,
    bucket_name: str,
    path: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/public/{project_id}/{bucket_name}/{path}".format(project_id=quote(str(project_id), safe=""),bucket_name=quote(str(bucket_name), safe=""),path=quote(str(path), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 206:
        response_206 = cast(Any, None)
        return response_206

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    project_id: UUID,
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | Error]:
    """ Download a public file (no authentication required)

     Download a file that has been marked as public. This endpoint requires NO authentication.

    **Access Requirements:**
    - The file must have `is_public: true` set via the visibility endpoint
    - Private files will return 403 Forbidden

    **Use Cases:**
    - Shareable public URLs for profile pictures, public documents, etc.
    - Embedding public files on external websites
    - Direct linking without requiring SDK or authentication

    **URL Format:**
    ```
    GET /public/{projectId}/{bucketName}/{path}
    ```

    **Example:**
    ```
    https://api.volcano.dev/public/abc123/avatars/user-photo.jpg
    ```

    **CORS:**
    This endpoint allows all origins since the file is already public.

    Args:
        project_id (UUID):
        bucket_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
bucket_name=bucket_name,
path=path,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    project_id: UUID,
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient | Client,

) -> Any | Error | None:
    """ Download a public file (no authentication required)

     Download a file that has been marked as public. This endpoint requires NO authentication.

    **Access Requirements:**
    - The file must have `is_public: true` set via the visibility endpoint
    - Private files will return 403 Forbidden

    **Use Cases:**
    - Shareable public URLs for profile pictures, public documents, etc.
    - Embedding public files on external websites
    - Direct linking without requiring SDK or authentication

    **URL Format:**
    ```
    GET /public/{projectId}/{bucketName}/{path}
    ```

    **Example:**
    ```
    https://api.volcano.dev/public/abc123/avatars/user-photo.jpg
    ```

    **CORS:**
    This endpoint allows all origins since the file is already public.

    Args:
        project_id (UUID):
        bucket_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        project_id=project_id,
bucket_name=bucket_name,
path=path,
client=client,

    ).parsed

async def asyncio_detailed(
    project_id: UUID,
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Any | Error]:
    """ Download a public file (no authentication required)

     Download a file that has been marked as public. This endpoint requires NO authentication.

    **Access Requirements:**
    - The file must have `is_public: true` set via the visibility endpoint
    - Private files will return 403 Forbidden

    **Use Cases:**
    - Shareable public URLs for profile pictures, public documents, etc.
    - Embedding public files on external websites
    - Direct linking without requiring SDK or authentication

    **URL Format:**
    ```
    GET /public/{projectId}/{bucketName}/{path}
    ```

    **Example:**
    ```
    https://api.volcano.dev/public/abc123/avatars/user-photo.jpg
    ```

    **CORS:**
    This endpoint allows all origins since the file is already public.

    Args:
        project_id (UUID):
        bucket_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        project_id=project_id,
bucket_name=bucket_name,
path=path,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    project_id: UUID,
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient | Client,

) -> Any | Error | None:
    """ Download a public file (no authentication required)

     Download a file that has been marked as public. This endpoint requires NO authentication.

    **Access Requirements:**
    - The file must have `is_public: true` set via the visibility endpoint
    - Private files will return 403 Forbidden

    **Use Cases:**
    - Shareable public URLs for profile pictures, public documents, etc.
    - Embedding public files on external websites
    - Direct linking without requiring SDK or authentication

    **URL Format:**
    ```
    GET /public/{projectId}/{bucketName}/{path}
    ```

    **Example:**
    ```
    https://api.volcano.dev/public/abc123/avatars/user-photo.jpg
    ```

    **CORS:**
    This endpoint allows all origins since the file is already public.

    Args:
        project_id (UUID):
        bucket_name (str):
        path (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        project_id=project_id,
bucket_name=bucket_name,
path=path,
client=client,

    )).parsed
