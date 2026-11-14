from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_run_status import check_lavaflow_run_status
from ...models.lavaflow_run_status import LavaflowRunStatus
from ...models.list_lavaflow_runs_category import check_list_lavaflow_runs_category
from ...models.list_lavaflow_runs_category import ListLavaflowRunsCategory
from ...models.list_lavaflow_runs_include_item import check_list_lavaflow_runs_include_item
from ...models.list_lavaflow_runs_include_item import ListLavaflowRunsIncludeItem
from ...models.list_lavaflow_runs_order import check_list_lavaflow_runs_order
from ...models.list_lavaflow_runs_order import ListLavaflowRunsOrder
from ...models.list_lavaflow_runs_pull_request_state import check_list_lavaflow_runs_pull_request_state
from ...models.list_lavaflow_runs_pull_request_state import ListLavaflowRunsPullRequestState
from ...models.paginated_lavaflow_runs import PaginatedLavaflowRuns
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,
    status: LavaflowRunStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,
    category: ListLavaflowRunsCategory | Unset = UNSET,
    involved_resource_id: UUID | str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    pull_request_state: ListLavaflowRunsPullRequestState | Unset = UNSET,
    days: int | Unset = UNSET,
    order: ListLavaflowRunsOrder | Unset = 'created_at.desc',
    include: list[ListLavaflowRunsIncludeItem] | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id

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

    json_category: str | Unset = UNSET
    if not isinstance(category, Unset):
        json_category = category

    params["category"] = json_category

    json_involved_resource_id: str | Unset = UNSET
    if not isinstance(involved_resource_id, Unset):
        json_involved_resource_id = str(involved_resource_id)
    params["involved_resource_id"] = json_involved_resource_id

    json_issue_id: str | Unset = UNSET
    if not isinstance(issue_id, Unset):
        json_issue_id = str(issue_id)
    params["issue_id"] = json_issue_id

    json_pull_request_state: str | Unset = UNSET
    if not isinstance(pull_request_state, Unset):
        json_pull_request_state = pull_request_state

    params["pull_request_state"] = json_pull_request_state

    params["days"] = days

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order

    params["order"] = json_order

    json_include: list[str] | Unset = UNSET
    if not isinstance(include, Unset):
        json_include = []
        for include_item_data in include:
            include_item: str = include_item_data
            json_include.append(include_item)


    params["include"] = json_include


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/runs",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedLavaflowRuns | None:
    if response.status_code == 200:
        response_200 = PaginatedLavaflowRuns.from_dict(response.json())



        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedLavaflowRuns]:
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
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,
    status: LavaflowRunStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,
    category: ListLavaflowRunsCategory | Unset = UNSET,
    involved_resource_id: UUID | str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    pull_request_state: ListLavaflowRunsPullRequestState | Unset = UNSET,
    days: int | Unset = UNSET,
    order: ListLavaflowRunsOrder | Unset = 'created_at.desc',
    include: list[ListLavaflowRunsIncludeItem] | Unset = UNSET,

) -> Response[Error | PaginatedLavaflowRuns]:
    """ List LavaFlow runs

     Pages the project's LavaFlow runs, newest first unless `order` says
    otherwise. A page carries bounded display text, including the saved
    proposed fix's optional `fix_summary`; read a run for its diagnosis,
    log lines and diff. Each run names its category, the resources it
    involves and its issue. A confirmed Code Quality finding can supply
    `issue.severity`, and a recorded pull request can supply `branch`.
    Unknown or withheld optional fields are omitted.

    Every filter narrows the list, and filters combine. `include=counts`
    adds `counts`, computed from the same filters: ask for them on the
    first page, since they don't depend on the cursor. Keep the filters
    and `order` while paging.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):
        status (LavaflowRunStatus | Unset): Where a run is. `diagnosing`, `fixing` and `reviewing`
            are the stages of a running run. `pr_open` means its pull request is open; `completed`
            means it finished, with no pull request or one that was merged or closed.
        resource_id (UUID | Unset):
        category (ListLavaflowRunsCategory | Unset):
        involved_resource_id (UUID | Unset):
        issue_id (UUID | Unset):
        pull_request_state (ListLavaflowRunsPullRequestState | Unset):
        days (int | Unset):
        order (ListLavaflowRunsOrder | Unset):  Default: 'created_at.desc'.
        include (list[ListLavaflowRunsIncludeItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedLavaflowRuns]
     """


    kwargs = request_kwargs(
        project_id=project_id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,
category=category,
involved_resource_id=involved_resource_id,
issue_id=issue_id,
pull_request_state=pull_request_state,
days=days,
order=order,
include=include,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,
    status: LavaflowRunStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,
    category: ListLavaflowRunsCategory | Unset = UNSET,
    involved_resource_id: UUID | str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    pull_request_state: ListLavaflowRunsPullRequestState | Unset = UNSET,
    days: int | Unset = UNSET,
    order: ListLavaflowRunsOrder | Unset = 'created_at.desc',
    include: list[ListLavaflowRunsIncludeItem] | Unset = UNSET,

) -> Error | PaginatedLavaflowRuns | None:
    """ List LavaFlow runs

     Pages the project's LavaFlow runs, newest first unless `order` says
    otherwise. A page carries bounded display text, including the saved
    proposed fix's optional `fix_summary`; read a run for its diagnosis,
    log lines and diff. Each run names its category, the resources it
    involves and its issue. A confirmed Code Quality finding can supply
    `issue.severity`, and a recorded pull request can supply `branch`.
    Unknown or withheld optional fields are omitted.

    Every filter narrows the list, and filters combine. `include=counts`
    adds `counts`, computed from the same filters: ask for them on the
    first page, since they don't depend on the cursor. Keep the filters
    and `order` while paging.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):
        status (LavaflowRunStatus | Unset): Where a run is. `diagnosing`, `fixing` and `reviewing`
            are the stages of a running run. `pr_open` means its pull request is open; `completed`
            means it finished, with no pull request or one that was merged or closed.
        resource_id (UUID | Unset):
        category (ListLavaflowRunsCategory | Unset):
        involved_resource_id (UUID | Unset):
        issue_id (UUID | Unset):
        pull_request_state (ListLavaflowRunsPullRequestState | Unset):
        days (int | Unset):
        order (ListLavaflowRunsOrder | Unset):  Default: 'created_at.desc'.
        include (list[ListLavaflowRunsIncludeItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedLavaflowRuns
     """


    return sync_detailed(
        client=client,
project_id=project_id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,
category=category,
involved_resource_id=involved_resource_id,
issue_id=issue_id,
pull_request_state=pull_request_state,
days=days,
order=order,
include=include,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,
    status: LavaflowRunStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,
    category: ListLavaflowRunsCategory | Unset = UNSET,
    involved_resource_id: UUID | str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    pull_request_state: ListLavaflowRunsPullRequestState | Unset = UNSET,
    days: int | Unset = UNSET,
    order: ListLavaflowRunsOrder | Unset = 'created_at.desc',
    include: list[ListLavaflowRunsIncludeItem] | Unset = UNSET,

) -> Response[Error | PaginatedLavaflowRuns]:
    """ List LavaFlow runs

     Pages the project's LavaFlow runs, newest first unless `order` says
    otherwise. A page carries bounded display text, including the saved
    proposed fix's optional `fix_summary`; read a run for its diagnosis,
    log lines and diff. Each run names its category, the resources it
    involves and its issue. A confirmed Code Quality finding can supply
    `issue.severity`, and a recorded pull request can supply `branch`.
    Unknown or withheld optional fields are omitted.

    Every filter narrows the list, and filters combine. `include=counts`
    adds `counts`, computed from the same filters: ask for them on the
    first page, since they don't depend on the cursor. Keep the filters
    and `order` while paging.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):
        status (LavaflowRunStatus | Unset): Where a run is. `diagnosing`, `fixing` and `reviewing`
            are the stages of a running run. `pr_open` means its pull request is open; `completed`
            means it finished, with no pull request or one that was merged or closed.
        resource_id (UUID | Unset):
        category (ListLavaflowRunsCategory | Unset):
        involved_resource_id (UUID | Unset):
        issue_id (UUID | Unset):
        pull_request_state (ListLavaflowRunsPullRequestState | Unset):
        days (int | Unset):
        order (ListLavaflowRunsOrder | Unset):  Default: 'created_at.desc'.
        include (list[ListLavaflowRunsIncludeItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedLavaflowRuns]
     """


    kwargs = request_kwargs(
        project_id=project_id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,
category=category,
involved_resource_id=involved_resource_id,
issue_id=issue_id,
pull_request_state=pull_request_state,
days=days,
order=order,
include=include,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,
    limit: int | Unset = 25,
    cursor: str | Unset = UNSET,
    status: LavaflowRunStatus | Unset = UNSET,
    resource_id: UUID | str | Unset = UNSET,
    category: ListLavaflowRunsCategory | Unset = UNSET,
    involved_resource_id: UUID | str | Unset = UNSET,
    issue_id: UUID | str | Unset = UNSET,
    pull_request_state: ListLavaflowRunsPullRequestState | Unset = UNSET,
    days: int | Unset = UNSET,
    order: ListLavaflowRunsOrder | Unset = 'created_at.desc',
    include: list[ListLavaflowRunsIncludeItem] | Unset = UNSET,

) -> Error | PaginatedLavaflowRuns | None:
    """ List LavaFlow runs

     Pages the project's LavaFlow runs, newest first unless `order` says
    otherwise. A page carries bounded display text, including the saved
    proposed fix's optional `fix_summary`; read a run for its diagnosis,
    log lines and diff. Each run names its category, the resources it
    involves and its issue. A confirmed Code Quality finding can supply
    `issue.severity`, and a recorded pull request can supply `branch`.
    Unknown or withheld optional fields are omitted.

    Every filter narrows the list, and filters combine. `include=counts`
    adds `counts`, computed from the same filters: ask for them on the
    first page, since they don't depend on the cursor. Keep the filters
    and `order` while paging.

    Args:
        project_id (UUID):
        limit (int | Unset):  Default: 25.
        cursor (str | Unset):
        status (LavaflowRunStatus | Unset): Where a run is. `diagnosing`, `fixing` and `reviewing`
            are the stages of a running run. `pr_open` means its pull request is open; `completed`
            means it finished, with no pull request or one that was merged or closed.
        resource_id (UUID | Unset):
        category (ListLavaflowRunsCategory | Unset):
        involved_resource_id (UUID | Unset):
        issue_id (UUID | Unset):
        pull_request_state (ListLavaflowRunsPullRequestState | Unset):
        days (int | Unset):
        order (ListLavaflowRunsOrder | Unset):  Default: 'created_at.desc'.
        include (list[ListLavaflowRunsIncludeItem] | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedLavaflowRuns
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,
limit=limit,
cursor=cursor,
status=status,
resource_id=resource_id,
category=category,
involved_resource_id=involved_resource_id,
issue_id=issue_id,
pull_request_state=pull_request_state,
days=days,
order=order,
include=include,

    )).parsed
