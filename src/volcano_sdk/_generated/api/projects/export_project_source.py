from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.export_project_source_request import ExportProjectSourceRequest
from ...models.project_source_export import ProjectSourceExport
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: ExportProjectSourceRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/source-export".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectSourceExport | None:
    if response.status_code == 201:
        response_201 = ProjectSourceExport.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectSourceExport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ExportProjectSourceRequest,

) -> Response[Error | ProjectSourceExport]:
    """ Initialize an empty repository with a project's stored source

     Creates the first commit in the connected repository and pushes it
    directly to the configured production branch. The push enters the
    ordinary Git auto-deploy flow. Direct source writes remain frozen until
    that deployment succeeds and the repository becomes the source of truth.

    The caller confirms the production branch shown before export. Starting
    export pins that branch: later GitHub default-branch changes do not
    repoint the project. If the configured branch changed after the caller
    read it, the request fails without exporting so the caller can show and
    confirm the new value.

    The response lists what the export could not carry: resources with no
    successful deployment to take source from (`skipped`), and things no
    export can hand back (`omitted`) — migrations, which Volcano stores no
    copy of, and credential-shaped files, which are left for their owner to
    add.

    Requires a connected repository with no commits or branches, and runs
    once. Volcano never creates the repository. If GitHub did not confirm
    the push, retrying creates the same commit and adopts it when it already
    reached the repository.

    Args:
        id (UUID):
        body (ExportProjectSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectSourceExport]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ExportProjectSourceRequest,

) -> Error | ProjectSourceExport | None:
    """ Initialize an empty repository with a project's stored source

     Creates the first commit in the connected repository and pushes it
    directly to the configured production branch. The push enters the
    ordinary Git auto-deploy flow. Direct source writes remain frozen until
    that deployment succeeds and the repository becomes the source of truth.

    The caller confirms the production branch shown before export. Starting
    export pins that branch: later GitHub default-branch changes do not
    repoint the project. If the configured branch changed after the caller
    read it, the request fails without exporting so the caller can show and
    confirm the new value.

    The response lists what the export could not carry: resources with no
    successful deployment to take source from (`skipped`), and things no
    export can hand back (`omitted`) — migrations, which Volcano stores no
    copy of, and credential-shaped files, which are left for their owner to
    add.

    Requires a connected repository with no commits or branches, and runs
    once. Volcano never creates the repository. If GitHub did not confirm
    the push, retrying creates the same commit and adopts it when it already
    reached the repository.

    Args:
        id (UUID):
        body (ExportProjectSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectSourceExport
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ExportProjectSourceRequest,

) -> Response[Error | ProjectSourceExport]:
    """ Initialize an empty repository with a project's stored source

     Creates the first commit in the connected repository and pushes it
    directly to the configured production branch. The push enters the
    ordinary Git auto-deploy flow. Direct source writes remain frozen until
    that deployment succeeds and the repository becomes the source of truth.

    The caller confirms the production branch shown before export. Starting
    export pins that branch: later GitHub default-branch changes do not
    repoint the project. If the configured branch changed after the caller
    read it, the request fails without exporting so the caller can show and
    confirm the new value.

    The response lists what the export could not carry: resources with no
    successful deployment to take source from (`skipped`), and things no
    export can hand back (`omitted`) — migrations, which Volcano stores no
    copy of, and credential-shaped files, which are left for their owner to
    add.

    Requires a connected repository with no commits or branches, and runs
    once. Volcano never creates the repository. If GitHub did not confirm
    the push, retrying creates the same commit and adopts it when it already
    reached the repository.

    Args:
        id (UUID):
        body (ExportProjectSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectSourceExport]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ExportProjectSourceRequest,

) -> Error | ProjectSourceExport | None:
    """ Initialize an empty repository with a project's stored source

     Creates the first commit in the connected repository and pushes it
    directly to the configured production branch. The push enters the
    ordinary Git auto-deploy flow. Direct source writes remain frozen until
    that deployment succeeds and the repository becomes the source of truth.

    The caller confirms the production branch shown before export. Starting
    export pins that branch: later GitHub default-branch changes do not
    repoint the project. If the configured branch changed after the caller
    read it, the request fails without exporting so the caller can show and
    confirm the new value.

    The response lists what the export could not carry: resources with no
    successful deployment to take source from (`skipped`), and things no
    export can hand back (`omitted`) — migrations, which Volcano stores no
    copy of, and credential-shaped files, which are left for their owner to
    add.

    Requires a connected repository with no commits or branches, and runs
    once. Volcano never creates the repository. If GitHub did not confirm
    the push, retrying creates the same commit and adopts it when it already
    reached the repository.

    Args:
        id (UUID):
        body (ExportProjectSourceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectSourceExport
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
