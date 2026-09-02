from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_source_export_state import ProjectSourceExportState
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/source-export".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectSourceExportState | None:
    if response.status_code == 200:
        response_200 = ProjectSourceExportState.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectSourceExportState]:
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

) -> Response[Error | ProjectSourceExportState]:
    """ Report the project's source-of-truth state

     Volcano stores the source of the functions and frontend it runs for a
    project. This reports whether that source has been written to the
    connected repository, and whether the repository has taken over as the
    project's source of truth.

    `mode` is `platform`, `git_exporting`, `git_pending`, or `git`. Export
    enters `git_exporting` before reading stored source. GitHub's signed
    push event confirms that the initial commit reached the production
    branch. That push or a newer production push changes the mode to
    `git_pending` when it starts a deployment. `exported_at` records that
    transition.

    A successful Git run completes the transition when it matches the
    recorded repository, production branch, and root directory and actually
    dispatches every recorded resource. Ordinary production-branch pushes
    deploy without changing a platform-managed project's source ownership.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectSourceExportState]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectSourceExportState | None:
    """ Report the project's source-of-truth state

     Volcano stores the source of the functions and frontend it runs for a
    project. This reports whether that source has been written to the
    connected repository, and whether the repository has taken over as the
    project's source of truth.

    `mode` is `platform`, `git_exporting`, `git_pending`, or `git`. Export
    enters `git_exporting` before reading stored source. GitHub's signed
    push event confirms that the initial commit reached the production
    branch. That push or a newer production push changes the mode to
    `git_pending` when it starts a deployment. `exported_at` records that
    transition.

    A successful Git run completes the transition when it matches the
    recorded repository, production branch, and root directory and actually
    dispatches every recorded resource. Ordinary production-branch pushes
    deploy without changing a platform-managed project's source ownership.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectSourceExportState
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectSourceExportState]:
    """ Report the project's source-of-truth state

     Volcano stores the source of the functions and frontend it runs for a
    project. This reports whether that source has been written to the
    connected repository, and whether the repository has taken over as the
    project's source of truth.

    `mode` is `platform`, `git_exporting`, `git_pending`, or `git`. Export
    enters `git_exporting` before reading stored source. GitHub's signed
    push event confirms that the initial commit reached the production
    branch. That push or a newer production push changes the mode to
    `git_pending` when it starts a deployment. `exported_at` records that
    transition.

    A successful Git run completes the transition when it matches the
    recorded repository, production branch, and root directory and actually
    dispatches every recorded resource. Ordinary production-branch pushes
    deploy without changing a platform-managed project's source ownership.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectSourceExportState]
     """


    kwargs = _get_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectSourceExportState | None:
    """ Report the project's source-of-truth state

     Volcano stores the source of the functions and frontend it runs for a
    project. This reports whether that source has been written to the
    connected repository, and whether the repository has taken over as the
    project's source of truth.

    `mode` is `platform`, `git_exporting`, `git_pending`, or `git`. Export
    enters `git_exporting` before reading stored source. GitHub's signed
    push event confirms that the initial commit reached the production
    branch. That push or a newer production push changes the mode to
    `git_pending` when it starts a deployment. `exported_at` records that
    transition.

    A successful Git run completes the transition when it matches the
    recorded repository, production branch, and root directory and actually
    dispatches every recorded resource. Ordinary production-branch pushes
    deploy without changing a platform-managed project's source ownership.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectSourceExportState
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
