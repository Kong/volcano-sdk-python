from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.upload_session_part import UploadSessionPart
from ...types import File, FileTypes
from io import BytesIO
from typing import cast



def _get_kwargs(
    bucket_name: str,
    path: str,
    *,
    body: File,
    x_upload_session: str,
    x_part_number: int,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Upload-Session"] = x_upload_session

    headers["X-Part-Number"] = str(x_part_number)




    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/storage/{bucket_name}/{path}".format(bucket_name=quote(str(bucket_name), safe=""),path=quote(str(path), safe=""),),
    }

    _kwargs["content"] = body.payload
    headers["Content-Type"] = "application/octet-stream"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | UploadSessionPart | None:
    if response.status_code == 200:
        response_200 = UploadSessionPart.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | UploadSessionPart]:
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
    body: File,
    x_upload_session: str,
    x_part_number: int,

) -> Response[Any | UploadSessionPart]:
    """ Upload a part of a resumable upload

     Upload a single part of a resumable upload session.

    **Requirements:**
    - Part numbers start at 1
    - All parts except the last must be at least 5MB
    - Maximum part size is 25MB
    - Parts can be uploaded in any order
    - Re-uploading a part overwrites the previous upload
    - Anonymous sessions must reuse the exact anon key that created the session

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str):
        x_part_number (int):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UploadSessionPart]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,
x_upload_session=x_upload_session,
x_part_number=x_part_number,

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
    body: File,
    x_upload_session: str,
    x_part_number: int,

) -> Any | UploadSessionPart | None:
    """ Upload a part of a resumable upload

     Upload a single part of a resumable upload session.

    **Requirements:**
    - Part numbers start at 1
    - All parts except the last must be at least 5MB
    - Maximum part size is 25MB
    - Parts can be uploaded in any order
    - Re-uploading a part overwrites the previous upload
    - Anonymous sessions must reuse the exact anon key that created the session

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str):
        x_part_number (int):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | UploadSessionPart
     """


    return sync_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,
x_upload_session=x_upload_session,
x_part_number=x_part_number,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    body: File,
    x_upload_session: str,
    x_part_number: int,

) -> Response[Any | UploadSessionPart]:
    """ Upload a part of a resumable upload

     Upload a single part of a resumable upload session.

    **Requirements:**
    - Part numbers start at 1
    - All parts except the last must be at least 5MB
    - Maximum part size is 25MB
    - Parts can be uploaded in any order
    - Re-uploading a part overwrites the previous upload
    - Anonymous sessions must reuse the exact anon key that created the session

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str):
        x_part_number (int):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | UploadSessionPart]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
body=body,
x_upload_session=x_upload_session,
x_part_number=x_part_number,

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
    body: File,
    x_upload_session: str,
    x_part_number: int,

) -> Any | UploadSessionPart | None:
    """ Upload a part of a resumable upload

     Upload a single part of a resumable upload session.

    **Requirements:**
    - Part numbers start at 1
    - All parts except the last must be at least 5MB
    - Maximum part size is 25MB
    - Parts can be uploaded in any order
    - Re-uploading a part overwrites the previous upload
    - Anonymous sessions must reuse the exact anon key that created the session

    Args:
        bucket_name (str):
        path (str):
        x_upload_session (str):
        x_part_number (int):
        body (File):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | UploadSessionPart
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
body=body,
x_upload_session=x_upload_session,
x_part_number=x_part_number,

    )).parsed
