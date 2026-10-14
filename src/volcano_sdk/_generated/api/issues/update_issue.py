from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.issue import Issue
from ...models.update_issue_request import UpdateIssueRequest
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    body: UpdateIssueRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/projects/{id}/issues/{issue_id}".format(id=quote(str(id), safe=""),issue_id=quote(str(issue_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Issue | None:
    if response.status_code == 200:
        response_200 = Issue.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateIssueRequest,

) -> Response[Error | Issue]:
    """ Update an issue

     Sets an issue's status. A resolved issue that is seen again after it
    was resolved reopens, and `regressed_at` records when. An ignored issue
    stays ignored while it keeps being counted.

    Setting the status an issue already has is safe to repeat.

    Args:
        id (UUID):
        issue_id (UUID):
        body (UpdateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
     """


    kwargs = request_kwargs(
        id=id,
issue_id=issue_id,
body=body,

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
    body: UpdateIssueRequest,

) -> Error | Issue | None:
    """ Update an issue

     Sets an issue's status. A resolved issue that is seen again after it
    was resolved reopens, and `regressed_at` records when. An ignored issue
    stays ignored while it keeps being counted.

    Setting the status an issue already has is safe to repeat.

    Args:
        id (UUID):
        issue_id (UUID):
        body (UpdateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Issue
     """


    return sync_detailed(
        id=id,
issue_id=issue_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateIssueRequest,

) -> Response[Error | Issue]:
    """ Update an issue

     Sets an issue's status. A resolved issue that is seen again after it
    was resolved reopens, and `regressed_at` records when. An ignored issue
    stays ignored while it keeps being counted.

    Setting the status an issue already has is safe to repeat.

    Args:
        id (UUID):
        issue_id (UUID):
        body (UpdateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
     """


    kwargs = request_kwargs(
        id=id,
issue_id=issue_id,
body=body,

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
    body: UpdateIssueRequest,

) -> Error | Issue | None:
    """ Update an issue

     Sets an issue's status. A resolved issue that is seen again after it
    was resolved reopens, and `regressed_at` records when. An ignored issue
    stays ignored while it keeps being counted.

    Setting the status an issue already has is safe to repeat.

    Args:
        id (UUID):
        issue_id (UUID):
        body (UpdateIssueRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Issue
     """


    return (await asyncio_detailed(
        id=id,
issue_id=issue_id,
client=client,
body=body,

    )).parsed
