from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...types import File, FileTypes
from ...types import UNSET, Unset
from io import BytesIO
from typing import cast



def _get_kwargs(
    bucket_name: str,
    path: str,
    *,
    range_: str | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(range_, Unset):
        headers["Range"] = range_

    if not isinstance(x_upload_session, Unset):
        headers["X-Upload-Session"] = x_upload_session



    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/storage/{bucket_name}/{path}".format(bucket_name=quote(str(bucket_name), safe=""),path=quote(str(path), safe=""),),
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | File | None:
    if response.status_code == 200:
        response_200 = File(
             payload = BytesIO(response.content)
        )



        return response_200

    if response.status_code == 206:
        response_206 = cast(Any, None)
        return response_206

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error | File]:
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
    range_: str | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,

) -> Response[Any | Error | File]:
    """ Download a file or get upload session status

     Download a file, or get the status of a resumable upload session.

    **File Download (default):**
    Downloads the file at the specified path.

    **Session Status (with X-Upload-Session header):**
    Returns the status of a resumable upload session, including which parts have been uploaded.

    Args:
        bucket_name (str):
        path (str):
        range_ (str | Unset):
        x_upload_session (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | File]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
range_=range_,
x_upload_session=x_upload_session,

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
    range_: str | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,

) -> Any | Error | File | None:
    """ Download a file or get upload session status

     Download a file, or get the status of a resumable upload session.

    **File Download (default):**
    Downloads the file at the specified path.

    **Session Status (with X-Upload-Session header):**
    Returns the status of a resumable upload session, including which parts have been uploaded.

    Args:
        bucket_name (str):
        path (str):
        range_ (str | Unset):
        x_upload_session (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | File
     """


    return sync_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
range_=range_,
x_upload_session=x_upload_session,

    ).parsed

async def asyncio_detailed(
    bucket_name: str,
    path: str,
    *,
    client: AuthenticatedClient,
    range_: str | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,

) -> Response[Any | Error | File]:
    """ Download a file or get upload session status

     Download a file, or get the status of a resumable upload session.

    **File Download (default):**
    Downloads the file at the specified path.

    **Session Status (with X-Upload-Session header):**
    Returns the status of a resumable upload session, including which parts have been uploaded.

    Args:
        bucket_name (str):
        path (str):
        range_ (str | Unset):
        x_upload_session (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error | File]
     """


    kwargs = _get_kwargs(
        bucket_name=bucket_name,
path=path,
range_=range_,
x_upload_session=x_upload_session,

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
    range_: str | Unset = UNSET,
    x_upload_session: str | Unset = UNSET,

) -> Any | Error | File | None:
    """ Download a file or get upload session status

     Download a file, or get the status of a resumable upload session.

    **File Download (default):**
    Downloads the file at the specified path.

    **Session Status (with X-Upload-Session header):**
    Returns the status of a resumable upload session, including which parts have been uploaded.

    Args:
        bucket_name (str):
        path (str):
        range_ (str | Unset):
        x_upload_session (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error | File
     """


    return (await asyncio_detailed(
        bucket_name=bucket_name,
path=path,
client=client,
range_=range_,
x_upload_session=x_upload_session,

    )).parsed
