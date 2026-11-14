from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.sandbox_file_list_result import SandboxFileListResult
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    session_id: UUID | str,
    path: str | Unset = UNSET,
    recursive: bool | Unset = True,
    include_sha256: bool | Unset = False,
    limit: int | Unset = 10000,
    cursor: str | Unset = UNSET,

) -> dict[str, Any]:




    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

    json_session_id = str(session_id)
    params["session_id"] = json_session_id

    params["path"] = path

    params["recursive"] = recursive

    params["include_sha256"] = include_sha256

    params["limit"] = limit

    params["cursor"] = cursor


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/sandbox-session-files",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxFileListResult:
    if response.status_code == 200:
        response_200 = SandboxFileListResult.from_dict(response.json())



        return response_200

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxFileListResult]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    session_id: UUID | str,
    path: str | Unset = UNSET,
    recursive: bool | Unset = True,
    include_sha256: bool | Unset = False,
    limit: int | Unset = 10000,
    cursor: str | Unset = UNSET,

) -> Response[Error | SandboxFileListResult]:
    """ List workspace files

     Lists a directory in a Sandbox session's workspace, one page at a time. The listing never follows a
    symlink and never leaves the workspace. It is not a snapshot: a file that changes while it runs can
    appear before or after the change. Sessions started on an image built before file listing answer 409
    with code `sandbox_image_outdated`; start a new session, after redeploying a custom template.

    Args:
        project_id (UUID):
        session_id (UUID):
        path (str | Unset):
        recursive (bool | Unset):  Default: True.
        include_sha256 (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 10000.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFileListResult]
     """


    kwargs = request_kwargs(
        project_id=project_id,
session_id=session_id,
path=path,
recursive=recursive,
include_sha256=include_sha256,
limit=limit,
cursor=cursor,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    session_id: UUID | str,
    path: str | Unset = UNSET,
    recursive: bool | Unset = True,
    include_sha256: bool | Unset = False,
    limit: int | Unset = 10000,
    cursor: str | Unset = UNSET,

) -> Error | SandboxFileListResult | None:
    """ List workspace files

     Lists a directory in a Sandbox session's workspace, one page at a time. The listing never follows a
    symlink and never leaves the workspace. It is not a snapshot: a file that changes while it runs can
    appear before or after the change. Sessions started on an image built before file listing answer 409
    with code `sandbox_image_outdated`; start a new session, after redeploying a custom template.

    Args:
        project_id (UUID):
        session_id (UUID):
        path (str | Unset):
        recursive (bool | Unset):  Default: True.
        include_sha256 (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 10000.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFileListResult
     """


    return sync_detailed(
        client=client,
project_id=project_id,
session_id=session_id,
path=path,
recursive=recursive,
include_sha256=include_sha256,
limit=limit,
cursor=cursor,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    session_id: UUID | str,
    path: str | Unset = UNSET,
    recursive: bool | Unset = True,
    include_sha256: bool | Unset = False,
    limit: int | Unset = 10000,
    cursor: str | Unset = UNSET,

) -> Response[Error | SandboxFileListResult]:
    """ List workspace files

     Lists a directory in a Sandbox session's workspace, one page at a time. The listing never follows a
    symlink and never leaves the workspace. It is not a snapshot: a file that changes while it runs can
    appear before or after the change. Sessions started on an image built before file listing answer 409
    with code `sandbox_image_outdated`; start a new session, after redeploying a custom template.

    Args:
        project_id (UUID):
        session_id (UUID):
        path (str | Unset):
        recursive (bool | Unset):  Default: True.
        include_sha256 (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 10000.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxFileListResult]
     """


    kwargs = request_kwargs(
        project_id=project_id,
session_id=session_id,
path=path,
recursive=recursive,
include_sha256=include_sha256,
limit=limit,
cursor=cursor,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    session_id: UUID | str,
    path: str | Unset = UNSET,
    recursive: bool | Unset = True,
    include_sha256: bool | Unset = False,
    limit: int | Unset = 10000,
    cursor: str | Unset = UNSET,

) -> Error | SandboxFileListResult | None:
    """ List workspace files

     Lists a directory in a Sandbox session's workspace, one page at a time. The listing never follows a
    symlink and never leaves the workspace. It is not a snapshot: a file that changes while it runs can
    appear before or after the change. Sessions started on an image built before file listing answer 409
    with code `sandbox_image_outdated`; start a new session, after redeploying a custom template.

    Args:
        project_id (UUID):
        session_id (UUID):
        path (str | Unset):
        recursive (bool | Unset):  Default: True.
        include_sha256 (bool | Unset):  Default: False.
        limit (int | Unset):  Default: 10000.
        cursor (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxFileListResult
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
session_id=session_id,
path=path,
recursive=recursive,
include_sha256=include_sha256,
limit=limit,
cursor=cursor,

    )).parsed
