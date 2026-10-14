from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.issue import Issue
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    issue_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/issues/{issue_id}".format(id=quote(str(id), safe=""),issue_id=quote(str(issue_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Issue | None:
    if response.status_code == 200:
        response_200 = Issue.from_dict(response.json())



        return response_200

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

) -> Response[Error | Issue]:
    """ Get an issue

     Returns one issue: the resource that raised it, how often and when it
    was seen, and its status.

    Project access tokens can read issues, including read-only ones.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
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

) -> Error | Issue | None:
    """ Get an issue

     Returns one issue: the resource that raised it, how often and when it
    was seen, and its status.

    Project access tokens can read issues, including read-only ones.

    Args:
        id (UUID):
        issue_id (UUID):

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

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    issue_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | Issue]:
    """ Get an issue

     Returns one issue: the resource that raised it, how often and when it
    was seen, and its status.

    Project access tokens can read issues, including read-only ones.

    Args:
        id (UUID):
        issue_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Issue]
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

) -> Error | Issue | None:
    """ Get an issue

     Returns one issue: the resource that raised it, how often and when it
    was seen, and its status.

    Project access tokens can read issues, including read-only ones.

    Args:
        id (UUID):
        issue_id (UUID):

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

    )).parsed
