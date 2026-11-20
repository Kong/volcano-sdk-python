from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_file_archive import SandboxFileArchive
from ...models.sandbox_file_archive_form import SandboxFileArchiveForm
from typing import cast



def request_kwargs(
    *,
    body: SandboxFileArchiveForm,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}






    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sandbox-file-archives",
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxFileArchive:
    if response.status_code == 201:
        response_201 = SandboxFileArchive.from_dict(response.json())



        return response_201

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxFileArchive]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SandboxFileArchiveForm,

) -> Response[Error | SandboxFileArchive]:
    """ Extract a tar archive into a session's workspace

     Extracts a tar archive into a directory of a session's workspace. Send `multipart/form-data`
    with `project_id`, `session_id` and `path`, in any order, then the archive as the file part
    `archive`. The archive may be gzip-compressed; Volcano detects compression from its first bytes.
    The request streams to the session, so the archive is never held whole in memory.

    Each call accepts at most 32 MiB of archive, 10,000 files and directories, and 256 MiB of
    uncompressed archive, counting tar headers, and has 2 minutes to send its archive; a slower
    call fails and writes nothing. Split larger trees into several archives and create one after
    another. For a single file larger than 8 MiB, use `POST /sandbox-file-parts`.

    `path` must name a directory below the workspace root; a path that resolves to the root or to
    `/`, such as `.`, `./`, `/`, `/workspace` or `/workspace/.`, is refused with
    `sandbox_archive_invalid`. The archive may contain only regular files and directories. Entry
    names are relative to `path`, which is created when missing; an absolute name, a `..`
    component, a symbolic link, a
    hard link, a sparse file, or a device refuses the whole archive. File and directory modes keep their
    permission bits; setuid, setgid and sticky bits are dropped. A file replaces an existing file or
    symbolic link at its path. Existing directories keep their modes. A symbolic link in the
    destination is never followed.

    The archive is checked and staged before the workspace changes, so a refused archive writes
    nothing, and one that fails part way is undone. If a session process moves or removes a
    directory while the archive is written, the call answers `409`, a file the archive replaced
    there is kept in a `.sandbox-archive-*` directory at the workspace root, and files the
    archive already placed can stay. Read-only directories the session user
    owns still take new entries and keep their modes. Code `sandbox_archive_invalid` (400) means the
    archive or form is malformed or holds an
    entry that is not allowed. Code `sandbox_archive_too_large` (413) means it exceeds a limit
    above. Code `sandbox_path_conflict` (409) means the destination has a symbolic link or a file
    where the archive needs a directory, a directory where it has a file, or a directory the
    session user cannot write. Code
    `sandbox_disk_full` (409) means the session's disk has no room for it; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates archive
    writes; start a new session from a current preset, or redeploy the template. A session outside
    `project_id`, or a project the caller cannot reach, answers 404 like an unknown session.

    Args:
        body (SandboxFileArchiveForm): Send `project_id`, `session_id` and `path`, in any order,
            then the `archive` part.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFileArchive]
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
    body: SandboxFileArchiveForm,

) -> Error | SandboxFileArchive | None:
    """ Extract a tar archive into a session's workspace

     Extracts a tar archive into a directory of a session's workspace. Send `multipart/form-data`
    with `project_id`, `session_id` and `path`, in any order, then the archive as the file part
    `archive`. The archive may be gzip-compressed; Volcano detects compression from its first bytes.
    The request streams to the session, so the archive is never held whole in memory.

    Each call accepts at most 32 MiB of archive, 10,000 files and directories, and 256 MiB of
    uncompressed archive, counting tar headers, and has 2 minutes to send its archive; a slower
    call fails and writes nothing. Split larger trees into several archives and create one after
    another. For a single file larger than 8 MiB, use `POST /sandbox-file-parts`.

    `path` must name a directory below the workspace root; a path that resolves to the root or to
    `/`, such as `.`, `./`, `/`, `/workspace` or `/workspace/.`, is refused with
    `sandbox_archive_invalid`. The archive may contain only regular files and directories. Entry
    names are relative to `path`, which is created when missing; an absolute name, a `..`
    component, a symbolic link, a
    hard link, a sparse file, or a device refuses the whole archive. File and directory modes keep their
    permission bits; setuid, setgid and sticky bits are dropped. A file replaces an existing file or
    symbolic link at its path. Existing directories keep their modes. A symbolic link in the
    destination is never followed.

    The archive is checked and staged before the workspace changes, so a refused archive writes
    nothing, and one that fails part way is undone. If a session process moves or removes a
    directory while the archive is written, the call answers `409`, a file the archive replaced
    there is kept in a `.sandbox-archive-*` directory at the workspace root, and files the
    archive already placed can stay. Read-only directories the session user
    owns still take new entries and keep their modes. Code `sandbox_archive_invalid` (400) means the
    archive or form is malformed or holds an
    entry that is not allowed. Code `sandbox_archive_too_large` (413) means it exceeds a limit
    above. Code `sandbox_path_conflict` (409) means the destination has a symbolic link or a file
    where the archive needs a directory, a directory where it has a file, or a directory the
    session user cannot write. Code
    `sandbox_disk_full` (409) means the session's disk has no room for it; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates archive
    writes; start a new session from a current preset, or redeploy the template. A session outside
    `project_id`, or a project the caller cannot reach, answers 404 like an unknown session.

    Args:
        body (SandboxFileArchiveForm): Send `project_id`, `session_id` and `path`, in any order,
            then the `archive` part.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFileArchive
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SandboxFileArchiveForm,

) -> Response[Error | SandboxFileArchive]:
    """ Extract a tar archive into a session's workspace

     Extracts a tar archive into a directory of a session's workspace. Send `multipart/form-data`
    with `project_id`, `session_id` and `path`, in any order, then the archive as the file part
    `archive`. The archive may be gzip-compressed; Volcano detects compression from its first bytes.
    The request streams to the session, so the archive is never held whole in memory.

    Each call accepts at most 32 MiB of archive, 10,000 files and directories, and 256 MiB of
    uncompressed archive, counting tar headers, and has 2 minutes to send its archive; a slower
    call fails and writes nothing. Split larger trees into several archives and create one after
    another. For a single file larger than 8 MiB, use `POST /sandbox-file-parts`.

    `path` must name a directory below the workspace root; a path that resolves to the root or to
    `/`, such as `.`, `./`, `/`, `/workspace` or `/workspace/.`, is refused with
    `sandbox_archive_invalid`. The archive may contain only regular files and directories. Entry
    names are relative to `path`, which is created when missing; an absolute name, a `..`
    component, a symbolic link, a
    hard link, a sparse file, or a device refuses the whole archive. File and directory modes keep their
    permission bits; setuid, setgid and sticky bits are dropped. A file replaces an existing file or
    symbolic link at its path. Existing directories keep their modes. A symbolic link in the
    destination is never followed.

    The archive is checked and staged before the workspace changes, so a refused archive writes
    nothing, and one that fails part way is undone. If a session process moves or removes a
    directory while the archive is written, the call answers `409`, a file the archive replaced
    there is kept in a `.sandbox-archive-*` directory at the workspace root, and files the
    archive already placed can stay. Read-only directories the session user
    owns still take new entries and keep their modes. Code `sandbox_archive_invalid` (400) means the
    archive or form is malformed or holds an
    entry that is not allowed. Code `sandbox_archive_too_large` (413) means it exceeds a limit
    above. Code `sandbox_path_conflict` (409) means the destination has a symbolic link or a file
    where the archive needs a directory, a directory where it has a file, or a directory the
    session user cannot write. Code
    `sandbox_disk_full` (409) means the session's disk has no room for it; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates archive
    writes; start a new session from a current preset, or redeploy the template. A session outside
    `project_id`, or a project the caller cannot reach, answers 404 like an unknown session.

    Args:
        body (SandboxFileArchiveForm): Send `project_id`, `session_id` and `path`, in any order,
            then the `archive` part.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFileArchive]
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
    body: SandboxFileArchiveForm,

) -> Error | SandboxFileArchive | None:
    """ Extract a tar archive into a session's workspace

     Extracts a tar archive into a directory of a session's workspace. Send `multipart/form-data`
    with `project_id`, `session_id` and `path`, in any order, then the archive as the file part
    `archive`. The archive may be gzip-compressed; Volcano detects compression from its first bytes.
    The request streams to the session, so the archive is never held whole in memory.

    Each call accepts at most 32 MiB of archive, 10,000 files and directories, and 256 MiB of
    uncompressed archive, counting tar headers, and has 2 minutes to send its archive; a slower
    call fails and writes nothing. Split larger trees into several archives and create one after
    another. For a single file larger than 8 MiB, use `POST /sandbox-file-parts`.

    `path` must name a directory below the workspace root; a path that resolves to the root or to
    `/`, such as `.`, `./`, `/`, `/workspace` or `/workspace/.`, is refused with
    `sandbox_archive_invalid`. The archive may contain only regular files and directories. Entry
    names are relative to `path`, which is created when missing; an absolute name, a `..`
    component, a symbolic link, a
    hard link, a sparse file, or a device refuses the whole archive. File and directory modes keep their
    permission bits; setuid, setgid and sticky bits are dropped. A file replaces an existing file or
    symbolic link at its path. Existing directories keep their modes. A symbolic link in the
    destination is never followed.

    The archive is checked and staged before the workspace changes, so a refused archive writes
    nothing, and one that fails part way is undone. If a session process moves or removes a
    directory while the archive is written, the call answers `409`, a file the archive replaced
    there is kept in a `.sandbox-archive-*` directory at the workspace root, and files the
    archive already placed can stay. Read-only directories the session user
    owns still take new entries and keep their modes. Code `sandbox_archive_invalid` (400) means the
    archive or form is malformed or holds an
    entry that is not allowed. Code `sandbox_archive_too_large` (413) means it exceeds a limit
    above. Code `sandbox_path_conflict` (409) means the destination has a symbolic link or a file
    where the archive needs a directory, a directory where it has a file, or a directory the
    session user cannot write. Code
    `sandbox_disk_full` (409) means the session's disk has no room for it; free space and retry. Code
    `sandbox_image_outdated` (409) means the session started from an image that predates archive
    writes; start a new session from a current preset, or redeploy the template. A session outside
    `project_id`, or a project the caller cannot reach, answers 404 like an unknown session.

    Args:
        body (SandboxFileArchiveForm): Send `project_id`, `session_id` and `path`, in any order,
            then the `archive` part.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFileArchive
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
