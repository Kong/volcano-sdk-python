from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.list_deployments_operation import check_list_deployments_operation
from ...models.list_deployments_operation import ListDeploymentsOperation
from ...models.list_deployments_order import check_list_deployments_order
from ...models.list_deployments_order import ListDeploymentsOrder
from ...models.list_deployments_resource_type import check_list_deployments_resource_type
from ...models.list_deployments_resource_type import ListDeploymentsResourceType
from ...models.list_deployments_status import check_list_deployments_status
from ...models.list_deployments_status import ListDeploymentsStatus
from ...models.paginated_project_deployments import PaginatedProjectDeployments
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    owner_id: str | Unset = UNSET,
    project_id: UUID | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListDeploymentsResourceType | Unset = UNSET,
    status: ListDeploymentsStatus | Unset = UNSET,
    operation: ListDeploymentsOperation | Unset = UNSET,
    order: ListDeploymentsOrder | Unset = 'created_at.desc',

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["cursor"] = cursor

    params["ending_before"] = ending_before

    params["offset"] = offset

    params["owner_id"] = owner_id

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id

    json_created_after: str | Unset = UNSET
    if not isinstance(created_after, Unset):
        json_created_after = created_after.isoformat()
    params["created_after"] = json_created_after

    json_resource_type: str | Unset = UNSET
    if not isinstance(resource_type, Unset):
        json_resource_type = resource_type

    params["resource_type"] = json_resource_type

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status

    json_operation: str | Unset = UNSET
    if not isinstance(operation, Unset):
        json_operation = operation

    params["operation"] = json_operation

    json_order: str | Unset = UNSET
    if not isinstance(order, Unset):
        json_order = order

    params["order"] = json_order


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/deployments",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedProjectDeployments | None:
    if response.status_code == 200:
        response_200 = PaginatedProjectDeployments.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedProjectDeployments]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    owner_id: str | Unset = UNSET,
    project_id: UUID | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListDeploymentsResourceType | Unset = UNSET,
    status: ListDeploymentsStatus | Unset = UNSET,
    operation: ListDeploymentsOperation | Unset = UNSET,
    order: ListDeploymentsOrder | Unset = 'created_at.desc',

) -> Response[Error | PaginatedProjectDeployments]:
    r""" List deployments across a user's projects

     Lists Function and Frontend deployment attempts across every project the
    user owns, newest first. Pass `project_id` to narrow the feed to a single
    project.

    Scope is project **ownership** (`projects.user_id`). `owner_id` names
    whose deployments to return, not who started them — the actor is
    `initiated_by_user_id`, which this endpoint does not filter on.

    With a user token the scope is always the authenticated user: `owner_id`
    may be omitted, or set to that same user, but naming anyone else is
    refused with 403. Service callers on the management API must pass it,
    since they have no authenticated user.

    The owner is not checked for existence: an id with no projects returns an
    empty page rather than `404`. Unlike `/users/{id}/usage`, this endpoint is
    polled to detect an event, so a caller needs `404` to keep meaning \"this
    route is not served here\" — which is how a consumer notices it is running
    against an older release. A mistyped owner therefore reads as \"nothing
    deployed\"; callers that need to tell those apart should verify the user
    through `GET /users/{id}` first.

    Ordering is selectable. The default is the feed order — most recent
    attempt first. `completed_at.asc` orders by completion, oldest first, and
    considers only attempts that finished; combined with `limit=1` and a
    `status` filter it answers \"when did this user first succeed\" in one
    bounded query.

    Both pagination modes are supported, selected exactly as
    `/projects/{id}/deployments` selects them: `cursor`/`ending_before` (or a
    `limit` with no `page`) uses keyset pagination; otherwise `page`/`limit`
    offset pagination. `page` with a cursor, and `cursor` with
    `ending_before`, are rejected.

    A cursor is bound to every filter *and* to `order`, so changing any of
    them mid-pagination rejects the cursor rather than silently skipping or
    repeating rows. The keyset position is `(created_at, id)` for
    `created_at.desc` and `(completed_at, id)` for `completed_at.asc`.

    Args:
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        owner_id (str | Unset):
        project_id (UUID | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListDeploymentsResourceType | Unset):
        status (ListDeploymentsStatus | Unset):
        operation (ListDeploymentsOperation | Unset):
        order (ListDeploymentsOrder | Unset):  Default: 'created_at.desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectDeployments]
     """


    kwargs = _get_kwargs(
        page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
owner_id=owner_id,
project_id=project_id,
created_after=created_after,
resource_type=resource_type,
status=status,
operation=operation,
order=order,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    owner_id: str | Unset = UNSET,
    project_id: UUID | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListDeploymentsResourceType | Unset = UNSET,
    status: ListDeploymentsStatus | Unset = UNSET,
    operation: ListDeploymentsOperation | Unset = UNSET,
    order: ListDeploymentsOrder | Unset = 'created_at.desc',

) -> Error | PaginatedProjectDeployments | None:
    r""" List deployments across a user's projects

     Lists Function and Frontend deployment attempts across every project the
    user owns, newest first. Pass `project_id` to narrow the feed to a single
    project.

    Scope is project **ownership** (`projects.user_id`). `owner_id` names
    whose deployments to return, not who started them — the actor is
    `initiated_by_user_id`, which this endpoint does not filter on.

    With a user token the scope is always the authenticated user: `owner_id`
    may be omitted, or set to that same user, but naming anyone else is
    refused with 403. Service callers on the management API must pass it,
    since they have no authenticated user.

    The owner is not checked for existence: an id with no projects returns an
    empty page rather than `404`. Unlike `/users/{id}/usage`, this endpoint is
    polled to detect an event, so a caller needs `404` to keep meaning \"this
    route is not served here\" — which is how a consumer notices it is running
    against an older release. A mistyped owner therefore reads as \"nothing
    deployed\"; callers that need to tell those apart should verify the user
    through `GET /users/{id}` first.

    Ordering is selectable. The default is the feed order — most recent
    attempt first. `completed_at.asc` orders by completion, oldest first, and
    considers only attempts that finished; combined with `limit=1` and a
    `status` filter it answers \"when did this user first succeed\" in one
    bounded query.

    Both pagination modes are supported, selected exactly as
    `/projects/{id}/deployments` selects them: `cursor`/`ending_before` (or a
    `limit` with no `page`) uses keyset pagination; otherwise `page`/`limit`
    offset pagination. `page` with a cursor, and `cursor` with
    `ending_before`, are rejected.

    A cursor is bound to every filter *and* to `order`, so changing any of
    them mid-pagination rejects the cursor rather than silently skipping or
    repeating rows. The keyset position is `(created_at, id)` for
    `created_at.desc` and `(completed_at, id)` for `completed_at.asc`.

    Args:
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        owner_id (str | Unset):
        project_id (UUID | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListDeploymentsResourceType | Unset):
        status (ListDeploymentsStatus | Unset):
        operation (ListDeploymentsOperation | Unset):
        order (ListDeploymentsOrder | Unset):  Default: 'created_at.desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectDeployments
     """


    return sync_detailed(
        client=client,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
owner_id=owner_id,
project_id=project_id,
created_after=created_after,
resource_type=resource_type,
status=status,
operation=operation,
order=order,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    owner_id: str | Unset = UNSET,
    project_id: UUID | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListDeploymentsResourceType | Unset = UNSET,
    status: ListDeploymentsStatus | Unset = UNSET,
    operation: ListDeploymentsOperation | Unset = UNSET,
    order: ListDeploymentsOrder | Unset = 'created_at.desc',

) -> Response[Error | PaginatedProjectDeployments]:
    r""" List deployments across a user's projects

     Lists Function and Frontend deployment attempts across every project the
    user owns, newest first. Pass `project_id` to narrow the feed to a single
    project.

    Scope is project **ownership** (`projects.user_id`). `owner_id` names
    whose deployments to return, not who started them — the actor is
    `initiated_by_user_id`, which this endpoint does not filter on.

    With a user token the scope is always the authenticated user: `owner_id`
    may be omitted, or set to that same user, but naming anyone else is
    refused with 403. Service callers on the management API must pass it,
    since they have no authenticated user.

    The owner is not checked for existence: an id with no projects returns an
    empty page rather than `404`. Unlike `/users/{id}/usage`, this endpoint is
    polled to detect an event, so a caller needs `404` to keep meaning \"this
    route is not served here\" — which is how a consumer notices it is running
    against an older release. A mistyped owner therefore reads as \"nothing
    deployed\"; callers that need to tell those apart should verify the user
    through `GET /users/{id}` first.

    Ordering is selectable. The default is the feed order — most recent
    attempt first. `completed_at.asc` orders by completion, oldest first, and
    considers only attempts that finished; combined with `limit=1` and a
    `status` filter it answers \"when did this user first succeed\" in one
    bounded query.

    Both pagination modes are supported, selected exactly as
    `/projects/{id}/deployments` selects them: `cursor`/`ending_before` (or a
    `limit` with no `page`) uses keyset pagination; otherwise `page`/`limit`
    offset pagination. `page` with a cursor, and `cursor` with
    `ending_before`, are rejected.

    A cursor is bound to every filter *and* to `order`, so changing any of
    them mid-pagination rejects the cursor rather than silently skipping or
    repeating rows. The keyset position is `(created_at, id)` for
    `created_at.desc` and `(completed_at, id)` for `completed_at.asc`.

    Args:
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        owner_id (str | Unset):
        project_id (UUID | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListDeploymentsResourceType | Unset):
        status (ListDeploymentsStatus | Unset):
        operation (ListDeploymentsOperation | Unset):
        order (ListDeploymentsOrder | Unset):  Default: 'created_at.desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedProjectDeployments]
     """


    kwargs = _get_kwargs(
        page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
owner_id=owner_id,
project_id=project_id,
created_after=created_after,
resource_type=resource_type,
status=status,
operation=operation,
order=order,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    ending_before: str | Unset = UNSET,
    offset: int | Unset = 0,
    owner_id: str | Unset = UNSET,
    project_id: UUID | Unset = UNSET,
    created_after: datetime.datetime | Unset = UNSET,
    resource_type: ListDeploymentsResourceType | Unset = UNSET,
    status: ListDeploymentsStatus | Unset = UNSET,
    operation: ListDeploymentsOperation | Unset = UNSET,
    order: ListDeploymentsOrder | Unset = 'created_at.desc',

) -> Error | PaginatedProjectDeployments | None:
    r""" List deployments across a user's projects

     Lists Function and Frontend deployment attempts across every project the
    user owns, newest first. Pass `project_id` to narrow the feed to a single
    project.

    Scope is project **ownership** (`projects.user_id`). `owner_id` names
    whose deployments to return, not who started them — the actor is
    `initiated_by_user_id`, which this endpoint does not filter on.

    With a user token the scope is always the authenticated user: `owner_id`
    may be omitted, or set to that same user, but naming anyone else is
    refused with 403. Service callers on the management API must pass it,
    since they have no authenticated user.

    The owner is not checked for existence: an id with no projects returns an
    empty page rather than `404`. Unlike `/users/{id}/usage`, this endpoint is
    polled to detect an event, so a caller needs `404` to keep meaning \"this
    route is not served here\" — which is how a consumer notices it is running
    against an older release. A mistyped owner therefore reads as \"nothing
    deployed\"; callers that need to tell those apart should verify the user
    through `GET /users/{id}` first.

    Ordering is selectable. The default is the feed order — most recent
    attempt first. `completed_at.asc` orders by completion, oldest first, and
    considers only attempts that finished; combined with `limit=1` and a
    `status` filter it answers \"when did this user first succeed\" in one
    bounded query.

    Both pagination modes are supported, selected exactly as
    `/projects/{id}/deployments` selects them: `cursor`/`ending_before` (or a
    `limit` with no `page`) uses keyset pagination; otherwise `page`/`limit`
    offset pagination. `page` with a cursor, and `cursor` with
    `ending_before`, are rejected.

    A cursor is bound to every filter *and* to `order`, so changing any of
    them mid-pagination rejects the cursor rather than silently skipping or
    repeating rows. The keyset position is `(created_at, id)` for
    `created_at.desc` and `(completed_at, id)` for `completed_at.asc`.

    Args:
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        cursor (str | Unset):
        ending_before (str | Unset):
        offset (int | Unset):  Default: 0.
        owner_id (str | Unset):
        project_id (UUID | Unset):
        created_after (datetime.datetime | Unset):
        resource_type (ListDeploymentsResourceType | Unset):
        status (ListDeploymentsStatus | Unset):
        operation (ListDeploymentsOperation | Unset):
        order (ListDeploymentsOrder | Unset):  Default: 'created_at.desc'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedProjectDeployments
     """


    return (await asyncio_detailed(
        client=client,
page=page,
limit=limit,
cursor=cursor,
ending_before=ending_before,
offset=offset,
owner_id=owner_id,
project_id=project_id,
created_after=created_after,
resource_type=resource_type,
status=status,
operation=operation,
order=order,

    )).parsed
