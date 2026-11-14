from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_issue_request import CreateIssueRequest
from ...models.error import Error
from ...models.issue import Issue
from typing import cast



def request_kwargs(
    *,
    body: CreateIssueRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/issues",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Issue | None:
    if response.status_code == 201:
        response_201 = Issue.from_dict(response.json())



        return response_201

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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Issue]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateIssueRequest,

) -> Response[Error | Issue]:
    """ Create an issue

     Records an issue you write on the project `project_id` names: a
    description of what to fix, in your words, and optionally a title. The
    issue has `source` `request`, the
    project as its resource, and status `open`. With LavaFlow on, LavaFlow
    starts a run on it by itself, as on a new error: the run follows the
    project's LavaFlow settings and counts toward the run limits. Follow
    it with `GET /lavaflow/runs?project_id=…&issue_id=…`. Where none
    starts, as with LavaFlow off, start one with `POST /lavaflow/runs`.

    The issue counts toward the project's 1,000 open issues, with runtime,
    build and reported issues; at that limit it is refused with code
    `open_issue_limit_reached`. Resolve or ignore issues to make room.

    Only the project's owner can create an issue, as a person: with
    `volcano login`, a live Volcano dashboard sign-in, or a platform token
    that expires. A full-scope project access
    token, MCP and a never-expiring platform token are refused with code
    `person_required`, as starting a run is, and a read-only project access
    token or account with an uncoded `403`, because creating one starts a
    run, which sends the description to an AI service with the project's
    source. A project access token is refused before its `project_id` is
    looked up. List, read and update the issue under
    `/projects/{id}/issues`.

    Args:
        body (CreateIssueRequest): The project, and an issue a person writes on it, describing
            what to fix.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
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
    body: CreateIssueRequest,

) -> Error | Issue | None:
    """ Create an issue

     Records an issue you write on the project `project_id` names: a
    description of what to fix, in your words, and optionally a title. The
    issue has `source` `request`, the
    project as its resource, and status `open`. With LavaFlow on, LavaFlow
    starts a run on it by itself, as on a new error: the run follows the
    project's LavaFlow settings and counts toward the run limits. Follow
    it with `GET /lavaflow/runs?project_id=…&issue_id=…`. Where none
    starts, as with LavaFlow off, start one with `POST /lavaflow/runs`.

    The issue counts toward the project's 1,000 open issues, with runtime,
    build and reported issues; at that limit it is refused with code
    `open_issue_limit_reached`. Resolve or ignore issues to make room.

    Only the project's owner can create an issue, as a person: with
    `volcano login`, a live Volcano dashboard sign-in, or a platform token
    that expires. A full-scope project access
    token, MCP and a never-expiring platform token are refused with code
    `person_required`, as starting a run is, and a read-only project access
    token or account with an uncoded `403`, because creating one starts a
    run, which sends the description to an AI service with the project's
    source. A project access token is refused before its `project_id` is
    looked up. List, read and update the issue under
    `/projects/{id}/issues`.

    Args:
        body (CreateIssueRequest): The project, and an issue a person writes on it, describing
            what to fix.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Issue
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateIssueRequest,

) -> Response[Error | Issue]:
    """ Create an issue

     Records an issue you write on the project `project_id` names: a
    description of what to fix, in your words, and optionally a title. The
    issue has `source` `request`, the
    project as its resource, and status `open`. With LavaFlow on, LavaFlow
    starts a run on it by itself, as on a new error: the run follows the
    project's LavaFlow settings and counts toward the run limits. Follow
    it with `GET /lavaflow/runs?project_id=…&issue_id=…`. Where none
    starts, as with LavaFlow off, start one with `POST /lavaflow/runs`.

    The issue counts toward the project's 1,000 open issues, with runtime,
    build and reported issues; at that limit it is refused with code
    `open_issue_limit_reached`. Resolve or ignore issues to make room.

    Only the project's owner can create an issue, as a person: with
    `volcano login`, a live Volcano dashboard sign-in, or a platform token
    that expires. A full-scope project access
    token, MCP and a never-expiring platform token are refused with code
    `person_required`, as starting a run is, and a read-only project access
    token or account with an uncoded `403`, because creating one starts a
    run, which sends the description to an AI service with the project's
    source. A project access token is refused before its `project_id` is
    looked up. List, read and update the issue under
    `/projects/{id}/issues`.

    Args:
        body (CreateIssueRequest): The project, and an issue a person writes on it, describing
            what to fix.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
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
    body: CreateIssueRequest,

) -> Error | Issue | None:
    """ Create an issue

     Records an issue you write on the project `project_id` names: a
    description of what to fix, in your words, and optionally a title. The
    issue has `source` `request`, the
    project as its resource, and status `open`. With LavaFlow on, LavaFlow
    starts a run on it by itself, as on a new error: the run follows the
    project's LavaFlow settings and counts toward the run limits. Follow
    it with `GET /lavaflow/runs?project_id=…&issue_id=…`. Where none
    starts, as with LavaFlow off, start one with `POST /lavaflow/runs`.

    The issue counts toward the project's 1,000 open issues, with runtime,
    build and reported issues; at that limit it is refused with code
    `open_issue_limit_reached`. Resolve or ignore issues to make room.

    Only the project's owner can create an issue, as a person: with
    `volcano login`, a live Volcano dashboard sign-in, or a platform token
    that expires. A full-scope project access
    token, MCP and a never-expiring platform token are refused with code
    `person_required`, as starting a run is, and a read-only project access
    token or account with an uncoded `403`, because creating one starts a
    run, which sends the description to an AI service with the project's
    source. A project access token is refused before its `project_id` is
    looked up. List, read and update the issue under
    `/projects/{id}/issues`.

    Args:
        body (CreateIssueRequest): The project, and an issue a person writes on it, describing
            what to fix.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Issue
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
