from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.autofix_run_status import AutofixRunStatus
from ...models.autofix_run_status import check_autofix_run_status
from ...models.error import Error
from ...models.paginated_autofix_runs import PaginatedAutofixRuns
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    status: AutofixRunStatus | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    json_issue_id: str | Unset = UNSET
    if not isinstance(issue_id, Unset):
        json_issue_id = str(issue_id)
    params["issue_id"] = json_issue_id

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/autofix-runs".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedAutofixRuns | None:
    if response.status_code == 200:
        response_200 = PaginatedAutofixRuns.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedAutofixRuns]:
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
    issue_id: UUID | str | Unset = UNSET,
    status: AutofixRunStatus | Unset = UNSET,

) -> Response[Error | PaginatedAutofixRuns]:
    """ List autofix runs

     Lists the project's autofix runs, newest first. Runs stay readable after
    autofix is turned off, and where autofix is not available.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        issue_id (UUID | Unset):
        status (AutofixRunStatus | Unset): Where a run is. `canceled` means the project's settings
            or plan stopped allowing the run before it finished; `failure_code` says which.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedAutofixRuns]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
issue_id=issue_id,
status=status,

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
    issue_id: UUID | str | Unset = UNSET,
    status: AutofixRunStatus | Unset = UNSET,

) -> Error | PaginatedAutofixRuns | None:
    """ List autofix runs

     Lists the project's autofix runs, newest first. Runs stay readable after
    autofix is turned off, and where autofix is not available.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        issue_id (UUID | Unset):
        status (AutofixRunStatus | Unset): Where a run is. `canceled` means the project's settings
            or plan stopped allowing the run before it finished; `failure_code` says which.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedAutofixRuns
     """


    return sync_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
issue_id=issue_id,
status=status,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    status: AutofixRunStatus | Unset = UNSET,

) -> Response[Error | PaginatedAutofixRuns]:
    """ List autofix runs

     Lists the project's autofix runs, newest first. Runs stay readable after
    autofix is turned off, and where autofix is not available.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        issue_id (UUID | Unset):
        status (AutofixRunStatus | Unset): Where a run is. `canceled` means the project's settings
            or plan stopped allowing the run before it finished; `failure_code` says which.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedAutofixRuns]
     """


    kwargs = request_kwargs(
        id=id,
limit=limit,
cursor=cursor,
issue_id=issue_id,
status=status,

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
    issue_id: UUID | str | Unset = UNSET,
    status: AutofixRunStatus | Unset = UNSET,

) -> Error | PaginatedAutofixRuns | None:
    """ List autofix runs

     Lists the project's autofix runs, newest first. Runs stay readable after
    autofix is turned off, and where autofix is not available.

    Project access tokens can list runs, including read-only ones.

    Args:
        id (UUID):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        issue_id (UUID | Unset):
        status (AutofixRunStatus | Unset): Where a run is. `canceled` means the project's settings
            or plan stopped allowing the run before it finished; `failure_code` says which.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedAutofixRuns
     """


    return (await asyncio_detailed(
        id=id,
client=client,
limit=limit,
cursor=cursor,
issue_id=issue_id,
status=status,

    )).parsed
