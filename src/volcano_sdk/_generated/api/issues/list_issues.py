from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.issue_status import check_issue_status
from ...models.issue_status import IssueStatus
from ...models.paginated_issues import PaginatedIssues
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: IssueStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status

    json_resource_id: str | Unset = UNSET
    if not isinstance(resource_id, Unset):
        json_resource_id = str(resource_id)
    params["resource_id"] = json_resource_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/issues".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedIssues | None:
    if response.status_code == 200:
        response_200 = PaginatedIssues.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedIssues]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: IssueStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,

) -> Response[Error | PaginatedIssues]:
    """ List issues

     Lists the project's issues, most recently seen first. An issue groups
    the runtime errors one function or frontend raised with the same error
    type and stack, or the same message when there is no stack.

    Project access tokens can list issues, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (IssueStatus | Unset): `open` until someone resolves or ignores the issue. A
            resolved issue
            seen again reopens.
        resource_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedIssues]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: IssueStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,

) -> Error | PaginatedIssues | None:
    """ List issues

     Lists the project's issues, most recently seen first. An issue groups
    the runtime errors one function or frontend raised with the same error
    type and stack, or the same message when there is no stack.

    Project access tokens can list issues, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (IssueStatus | Unset): `open` until someone resolves or ignores the issue. A
            resolved issue
            seen again reopens.
        resource_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedIssues
     """


    return sync_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: IssueStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,

) -> Response[Error | PaginatedIssues]:
    """ List issues

     Lists the project's issues, most recently seen first. An issue groups
    the runtime errors one function or frontend raised with the same error
    type and stack, or the same message when there is no stack.

    Project access tokens can list issues, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (IssueStatus | Unset): `open` until someone resolves or ignores the issue. A
            resolved issue
            seen again reopens.
        resource_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedIssues]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    status: IssueStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,

) -> Error | PaginatedIssues | None:
    """ List issues

     Lists the project's issues, most recently seen first. An issue groups
    the runtime errors one function or frontend raised with the same error
    type and stack, or the same message when there is no stack.

    Project access tokens can list issues, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        status (IssueStatus | Unset): `open` until someone resolves or ignores the issue. A
            resolved issue
            seen again reopens.
        resource_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedIssues
     """


    return (await asyncio_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,

    )).parsed
