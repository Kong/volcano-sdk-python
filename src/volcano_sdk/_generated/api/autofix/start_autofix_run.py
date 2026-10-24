from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.autofix_run import AutofixRun
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    issue_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/issues/{issue_id}/autofix-runs".format(id=quote(str(id), safe=""),issue_id=quote(str(issue_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AutofixRun | Error | None:
    if response.status_code == 202:
        response_202 = AutofixRun.from_dict(response.json())



        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AutofixRun | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixRun | Error]:
    """ Diagnose an issue

     Queues a run that diagnoses the issue with AI. The run reads the
    issue's runtime logs and, when a push to the project's connected
    repository built the deployment that was live when the issue was
    last seen, its source at that commit. Poll the run until its status is
    `succeeded`, `failed`, or `canceled`.

    Autofix must be on for the project. An issue has at most one queued or
    running run, a project runs one at a time, and a project starts at most
    25 runs, manual and automatic, in any 24 hours.

    Project access tokens are refused. A run can open a pull request in
    the project's repository, so a person starts it with a platform token
    or in the dashboard.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
issue_id=issue_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixRun | Error | None:
    """ Diagnose an issue

     Queues a run that diagnoses the issue with AI. The run reads the
    issue's runtime logs and, when a push to the project's connected
    repository built the deployment that was live when the issue was
    last seen, its source at that commit. Poll the run until its status is
    `succeeded`, `failed`, or `canceled`.

    Autofix must be on for the project. An issue has at most one queued or
    running run, a project runs one at a time, and a project starts at most
    25 runs, manual and automatic, in any 24 hours.

    Project access tokens are refused. A run can open a pull request in
    the project's repository, so a person starts it with a platform token
    or in the dashboard.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixRun | Error
     """


    return sync_detailed(
        id=id,
issue_id=issue_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixRun | Error]:
    """ Diagnose an issue

     Queues a run that diagnoses the issue with AI. The run reads the
    issue's runtime logs and, when a push to the project's connected
    repository built the deployment that was live when the issue was
    last seen, its source at that commit. Poll the run until its status is
    `succeeded`, `failed`, or `canceled`.

    Autofix must be on for the project. An issue has at most one queued or
    running run, a project runs one at a time, and a project starts at most
    25 runs, manual and automatic, in any 24 hours.

    Project access tokens are refused. A run can open a pull request in
    the project's repository, so a person starts it with a platform token
    or in the dashboard.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
issue_id=issue_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixRun | Error | None:
    """ Diagnose an issue

     Queues a run that diagnoses the issue with AI. The run reads the
    issue's runtime logs and, when a push to the project's connected
    repository built the deployment that was live when the issue was
    last seen, its source at that commit. Poll the run until its status is
    `succeeded`, `failed`, or `canceled`.

    Autofix must be on for the project. An issue has at most one queued or
    running run, a project runs one at a time, and a project starts at most
    25 runs, manual and automatic, in any 24 hours.

    Project access tokens are refused. A run can open a pull request in
    the project's repository, so a person starts it with a platform token
    or in the dashboard.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixRun | Error
     """


    return (await asyncio_detailed(
        id=id,
issue_id=issue_id,
client=client,

    )).parsed
