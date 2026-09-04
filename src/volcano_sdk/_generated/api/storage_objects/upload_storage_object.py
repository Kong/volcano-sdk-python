from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.complete_upload_session_response import CompleteUploadSessionResponse
from ...models.create_upload_session_request import CreateUploadSessionRequest
from ...models.create_upload_session_response import CreateUploadSessionResponse
from ...models.error import Error
from ...models.storage_object import StorageObject
from ...models.upload_storage_object_files_body import UploadStorageObjectFilesBody
from ...models.upload_storage_object_x_upload_complete import check_upload_storage_object_x_upload_complete
from ...models.upload_storage_object_x_upload_complete import UploadStorageObjectXUploadComplete
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    bucket_name: str,
    path: str,
    *,
    body:    UploadStorageObjectFilesBody  |     CreateUploadSessionRequest  | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,
    x_upload_complete: UploadStorageObjectXUploadComplete | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(x_upload_session, Unset):
        headers["X-Upload-Session"] = x_upload_session

    if not isinstance(x_upload_complete, Unset):
        headers["X-Upload-Complete"] = str(x_upload_complete)




    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/storage/{bucket_name}/{path}".format(bucket_name=quote(str(bucket_name), safe=""),path=quote(str(path), safe=""),),
    }

    if isinstance(body, UploadStorageObjectFilesBody):
        _kwargs["files"] = body.to_multipart()

        headers["Content-Type"] = "multipart/form-data; boundary=+++"
    if isinstance(body, CreateUploadSessionRequest):
        _kwargs["json"] = body.to_dict()

        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error | None:
    if response.status_code == 200:
        response_200 = CompleteUploadSessionResponse.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        def _parse_response_201(data: object) -> CreateUploadSessionResponse | StorageObject:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_201_type_0 = StorageObject.from_dict(data)



                return response_201_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_201_type_1 = CreateUploadSessionResponse.from_dict(data)



            return response_201_type_1

        response_201 = _parse_response_201(response.json())

        return response_201

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if response.status_code == 413:
        response_413 = cast(Any, None)
        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error]:
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
    body:    UploadStorageObjectFilesBody  |     CreateUploadSessionRequest  | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,
    x_upload_complete: UploadStorageObjectXUploadComplete | Unset = UNSET,

) -> Response[Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error]:
    r""" Upload a file or create resumable session

     Unified endpoint for file uploads. Behavior depends on Content-Type and headers:

    **Simple Upload (multipart/form-data):**
    Upload a complete file in a single request. Best for files under 100MB.

    **Create Resumable Session (application/json):**
    Create a session for chunked uploads. Best for large files or unreliable networks.
    Requires: `Content-Type: application/json` with body `{\"filename\": \"...\", \"content_type\":
    \"...\", \"total_size\": ...}`

    **Complete Resumable Session:**
    Complete a session after all parts are uploaded.
    Requires: `X-Upload-Session` header with session ID and `X-Upload-Complete: true` header.

    **Resumable Session Ownership:**
    A session created with a user access token remains bound to that user. A session
    created with an anon key remains bound to that exact anon key. Reuse the same
    identity or anon key for part uploads, status, completion, and abort requests;
    an ownership mismatch returns `404`.

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str | Unset):
        x_upload_complete (UploadStorageObjectXUploadComplete | Unset):
        body (UploadStorageObjectFilesBody):
        body (CreateUploadSessionRequest): Request to create a resumable upload session

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,
x_upload_session=x_upload_session,
x_upload_complete=x_upload_complete,

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
    body:    UploadStorageObjectFilesBody  |     CreateUploadSessionRequest  | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,
    x_upload_complete: UploadStorageObjectXUploadComplete | Unset = UNSET,

) -> Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error | None:
    r""" Upload a file or create resumable session

     Unified endpoint for file uploads. Behavior depends on Content-Type and headers:

    **Simple Upload (multipart/form-data):**
    Upload a complete file in a single request. Best for files under 100MB.

    **Create Resumable Session (application/json):**
    Create a session for chunked uploads. Best for large files or unreliable networks.
    Requires: `Content-Type: application/json` with body `{\"filename\": \"...\", \"content_type\":
    \"...\", \"total_size\": ...}`

    **Complete Resumable Session:**
    Complete a session after all parts are uploaded.
    Requires: `X-Upload-Session` header with session ID and `X-Upload-Complete: true` header.

    **Resumable Session Ownership:**
    A session created with a user access token remains bound to that user. A session
    created with an anon key remains bound to that exact anon key. Reuse the same
    identity or anon key for part uploads, status, completion, and abort requests;
    an ownership mismatch returns `404`.

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str | Unset):
        x_upload_complete (UploadStorageObjectXUploadComplete | Unset):
        body (UploadStorageObjectFilesBody):
        body (CreateUploadSessionRequest): Request to create a resumable upload session

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error
     """


    return sync_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,
x_upload_session=x_upload_session,
x_upload_complete=x_upload_complete,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body:    UploadStorageObjectFilesBody  |     CreateUploadSessionRequest  | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,
    x_upload_complete: UploadStorageObjectXUploadComplete | Unset = UNSET,

) -> Response[Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error]:
    r""" Upload a file or create resumable session

     Unified endpoint for file uploads. Behavior depends on Content-Type and headers:

    **Simple Upload (multipart/form-data):**
    Upload a complete file in a single request. Best for files under 100MB.

    **Create Resumable Session (application/json):**
    Create a session for chunked uploads. Best for large files or unreliable networks.
    Requires: `Content-Type: application/json` with body `{\"filename\": \"...\", \"content_type\":
    \"...\", \"total_size\": ...}`

    **Complete Resumable Session:**
    Complete a session after all parts are uploaded.
    Requires: `X-Upload-Session` header with session ID and `X-Upload-Complete: true` header.

    **Resumable Session Ownership:**
    A session created with a user access token remains bound to that user. A session
    created with an anon key remains bound to that exact anon key. Reuse the same
    identity or anon key for part uploads, status, completion, and abort requests;
    an ownership mismatch returns `404`.

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str | Unset):
        x_upload_complete (UploadStorageObjectXUploadComplete | Unset):
        body (UploadStorageObjectFilesBody):
        body (CreateUploadSessionRequest): Request to create a resumable upload session

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,
x_upload_session=x_upload_session,
x_upload_complete=x_upload_complete,

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
    body:    UploadStorageObjectFilesBody  |     CreateUploadSessionRequest  | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,
    x_upload_complete: UploadStorageObjectXUploadComplete | Unset = UNSET,

) -> Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error | None:
    r""" Upload a file or create resumable session

     Unified endpoint for file uploads. Behavior depends on Content-Type and headers:

    **Simple Upload (multipart/form-data):**
    Upload a complete file in a single request. Best for files under 100MB.

    **Create Resumable Session (application/json):**
    Create a session for chunked uploads. Best for large files or unreliable networks.
    Requires: `Content-Type: application/json` with body `{\"filename\": \"...\", \"content_type\":
    \"...\", \"total_size\": ...}`

    **Complete Resumable Session:**
    Complete a session after all parts are uploaded.
    Requires: `X-Upload-Session` header with session ID and `X-Upload-Complete: true` header.

    **Resumable Session Ownership:**
    A session created with a user access token remains bound to that user. A session
    created with an anon key remains bound to that exact anon key. Reuse the same
    identity or anon key for part uploads, status, completion, and abort requests;
    an ownership mismatch returns `404`.

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str | Unset):
        x_upload_complete (UploadStorageObjectXUploadComplete | Unset):
        body (UploadStorageObjectFilesBody):
        body (CreateUploadSessionRequest): Request to create a resumable upload session

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | CompleteUploadSessionResponse | CreateUploadSessionResponse | StorageObject | Error
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,
x_upload_session=x_upload_session,
x_upload_complete=x_upload_complete,

    )).parsed
