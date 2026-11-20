from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_file_part import SandboxFilePart
from ...models.sandbox_file_part_request import SandboxFilePartRequest
from typing import cast



def request_kwargs(
    *,
    body: SandboxFilePartRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}






    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandbox-file-parts",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxFilePart:
    if response.status_code == 201:
        response_201 = SandboxFilePart.from_dict(response.json())



        return response_201

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxFilePart]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SandboxFilePartRequest,

) -> Response[Error | SandboxFilePart]:
    """ Write one part of a large workspace file

     Writes a file of up to 1 GiB into a session's workspace in parts of at most 8 MiB. Each part
    names its `offset` in the file, the whole file's `size`, and the whole file's lowercase hex
    `sha256`. Parts collect in a hidden staging file beside `path`; nothing appears at `path` until
    the part that ends at `size` arrives. That part checks the whole file's size and SHA-256, then
    moves the file into place in one step, so a partial file is never visible at `path`. The
    response's `complete` says which part finished the file. Missing parent directories are created,
    and a symbolic link among them is never followed. The finished file is readable and writable
    only by the session user.

    A part may start anywhere up to the bytes already received, so a failed part can be resent. A
    part at offset 0 starts the file again. Resending the part that finished the file answers the
    same completion while the file at `path` still matches `size` and `sha256`. Code
    `sandbox_file_part_out_of_order` (409) means the
    part starts past the bytes received; resend from the last part that succeeded. Code
    `sandbox_file_part_mismatch` (409) means the finished file differs from `size` or `sha256`; its
    parts are discarded, so start again at offset 0. Code `sandbox_path_conflict` (409) means a
    directory is at `path`, a file or symbolic link is where a parent directory belongs, or the
    session user cannot write the parent directory, or, when parents are missing, the nearest
    one that exists. Read-only directories the session user owns still take new entries and
    keep their modes. Code
    `sandbox_disk_full` (409) means the session's disk has no room; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates parted
    writes. A staging file stays until its file completes, a part at offset 0 restarts it, or the
    session ends. A session outside `project_id`, or a project the caller cannot reach, answers 404
    like an unknown session.

    Args:
        body (SandboxFilePartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFilePart]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: SandboxFilePartRequest,

) -> Error | SandboxFilePart | None:
    """ Write one part of a large workspace file

     Writes a file of up to 1 GiB into a session's workspace in parts of at most 8 MiB. Each part
    names its `offset` in the file, the whole file's `size`, and the whole file's lowercase hex
    `sha256`. Parts collect in a hidden staging file beside `path`; nothing appears at `path` until
    the part that ends at `size` arrives. That part checks the whole file's size and SHA-256, then
    moves the file into place in one step, so a partial file is never visible at `path`. The
    response's `complete` says which part finished the file. Missing parent directories are created,
    and a symbolic link among them is never followed. The finished file is readable and writable
    only by the session user.

    A part may start anywhere up to the bytes already received, so a failed part can be resent. A
    part at offset 0 starts the file again. Resending the part that finished the file answers the
    same completion while the file at `path` still matches `size` and `sha256`. Code
    `sandbox_file_part_out_of_order` (409) means the
    part starts past the bytes received; resend from the last part that succeeded. Code
    `sandbox_file_part_mismatch` (409) means the finished file differs from `size` or `sha256`; its
    parts are discarded, so start again at offset 0. Code `sandbox_path_conflict` (409) means a
    directory is at `path`, a file or symbolic link is where a parent directory belongs, or the
    session user cannot write the parent directory, or, when parents are missing, the nearest
    one that exists. Read-only directories the session user owns still take new entries and
    keep their modes. Code
    `sandbox_disk_full` (409) means the session's disk has no room; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates parted
    writes. A staging file stays until its file completes, a part at offset 0 restarts it, or the
    session ends. A session outside `project_id`, or a project the caller cannot reach, answers 404
    like an unknown session.

    Args:
        body (SandboxFilePartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFilePart
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SandboxFilePartRequest,

) -> Response[Error | SandboxFilePart]:
    """ Write one part of a large workspace file

     Writes a file of up to 1 GiB into a session's workspace in parts of at most 8 MiB. Each part
    names its `offset` in the file, the whole file's `size`, and the whole file's lowercase hex
    `sha256`. Parts collect in a hidden staging file beside `path`; nothing appears at `path` until
    the part that ends at `size` arrives. That part checks the whole file's size and SHA-256, then
    moves the file into place in one step, so a partial file is never visible at `path`. The
    response's `complete` says which part finished the file. Missing parent directories are created,
    and a symbolic link among them is never followed. The finished file is readable and writable
    only by the session user.

    A part may start anywhere up to the bytes already received, so a failed part can be resent. A
    part at offset 0 starts the file again. Resending the part that finished the file answers the
    same completion while the file at `path` still matches `size` and `sha256`. Code
    `sandbox_file_part_out_of_order` (409) means the
    part starts past the bytes received; resend from the last part that succeeded. Code
    `sandbox_file_part_mismatch` (409) means the finished file differs from `size` or `sha256`; its
    parts are discarded, so start again at offset 0. Code `sandbox_path_conflict` (409) means a
    directory is at `path`, a file or symbolic link is where a parent directory belongs, or the
    session user cannot write the parent directory, or, when parents are missing, the nearest
    one that exists. Read-only directories the session user owns still take new entries and
    keep their modes. Code
    `sandbox_disk_full` (409) means the session's disk has no room; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates parted
    writes. A staging file stays until its file completes, a part at offset 0 restarts it, or the
    session ends. A session outside `project_id`, or a project the caller cannot reach, answers 404
    like an unknown session.

    Args:
        body (SandboxFilePartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFilePart]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SandboxFilePartRequest,

) -> Error | SandboxFilePart | None:
    """ Write one part of a large workspace file

     Writes a file of up to 1 GiB into a session's workspace in parts of at most 8 MiB. Each part
    names its `offset` in the file, the whole file's `size`, and the whole file's lowercase hex
    `sha256`. Parts collect in a hidden staging file beside `path`; nothing appears at `path` until
    the part that ends at `size` arrives. That part checks the whole file's size and SHA-256, then
    moves the file into place in one step, so a partial file is never visible at `path`. The
    response's `complete` says which part finished the file. Missing parent directories are created,
    and a symbolic link among them is never followed. The finished file is readable and writable
    only by the session user.

    A part may start anywhere up to the bytes already received, so a failed part can be resent. A
    part at offset 0 starts the file again. Resending the part that finished the file answers the
    same completion while the file at `path` still matches `size` and `sha256`. Code
    `sandbox_file_part_out_of_order` (409) means the
    part starts past the bytes received; resend from the last part that succeeded. Code
    `sandbox_file_part_mismatch` (409) means the finished file differs from `size` or `sha256`; its
    parts are discarded, so start again at offset 0. Code `sandbox_path_conflict` (409) means a
    directory is at `path`, a file or symbolic link is where a parent directory belongs, or the
    session user cannot write the parent directory, or, when parents are missing, the nearest
    one that exists. Read-only directories the session user owns still take new entries and
    keep their modes. Code
    `sandbox_disk_full` (409) means the session's disk has no room; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates parted
    writes. A staging file stays until its file completes, a part at offset 0 restarts it, or the
    session ends. A session outside `project_id`, or a project the caller cannot reach, answers 404
    like an unknown session.

    Args:
        body (SandboxFilePartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFilePart
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
