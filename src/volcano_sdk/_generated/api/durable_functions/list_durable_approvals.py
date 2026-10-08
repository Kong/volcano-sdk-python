from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_approval_status import check_durable_approval_status
from ...models.durable_approval_status import DurableApprovalStatus
from ...models.error import Error
from ...models.paginated_durable_approvals import PaginatedDurableApprovals
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def request_kwargs(
    id: UUID | str,
    *,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableApprovalStatus | Unset = UNSET,
    function: str | Unset = UNSET,
    execution_id: UUID | str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    json_status: str | Unset = UNSET
    if not isinstance(status, Unset):
        json_status = status

    params["status"] = json_status

    params["function"] = function

    json_execution_id: str | Unset = UNSET
    if not isinstance(execution_id, Unset):
        json_execution_id = str(execution_id)
    params["execution_id"] = json_execution_id

    json_from_: str | Unset = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: str | Unset = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/durable-approvals".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | PaginatedDurableApprovals | None:
    if response.status_code == 200:
        response_200 = PaginatedDurableApprovals.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | PaginatedDurableApprovals]:
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
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableApprovalStatus | Unset = UNSET,
    function: str | Unset = UNSET,
    execution_id: UUID | str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[Error | PaginatedDurableApprovals]:
    """ List durable approvals

     Lists the approvals durable workflows in the project have requested,
    newest first. Pending approvals are the ones a workflow is waiting on;
    decided, expired, and cancelled ones are kept for a year.

    Project access tokens can list approvals, including read-only ones.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableApprovalStatus | Unset): `pending` means the workflow is waiting for a
            decision. `approved` and
            `denied` are decisions a person made. `expired` means the workflow's
            approval timeout passed first, and `cancelled` means the execution
            ended while the approval was still pending. Every status but `pending`
            is final.
        function (str | Unset):
        execution_id (UUID | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableApprovals]
     """


    kwargs = request_kwargs(
        id=id,
page=page,
limit=limit,
status=status,
function=function,
execution_id=execution_id,
from_=from_,
to=to,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableApprovalStatus | Unset = UNSET,
    function: str | Unset = UNSET,
    execution_id: UUID | str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Error | PaginatedDurableApprovals | None:
    """ List durable approvals

     Lists the approvals durable workflows in the project have requested,
    newest first. Pending approvals are the ones a workflow is waiting on;
    decided, expired, and cancelled ones are kept for a year.

    Project access tokens can list approvals, including read-only ones.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableApprovalStatus | Unset): `pending` means the workflow is waiting for a
            decision. `approved` and
            `denied` are decisions a person made. `expired` means the workflow's
            approval timeout passed first, and `cancelled` means the execution
            ended while the approval was still pending. Every status but `pending`
            is final.
        function (str | Unset):
        execution_id (UUID | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableApprovals
     """


    return sync_detailed(
        id=id,
client=client,
page=page,
limit=limit,
status=status,
function=function,
execution_id=execution_id,
from_=from_,
to=to,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableApprovalStatus | Unset = UNSET,
    function: str | Unset = UNSET,
    execution_id: UUID | str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[Error | PaginatedDurableApprovals]:
    """ List durable approvals

     Lists the approvals durable workflows in the project have requested,
    newest first. Pending approvals are the ones a workflow is waiting on;
    decided, expired, and cancelled ones are kept for a year.

    Project access tokens can list approvals, including read-only ones.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableApprovalStatus | Unset): `pending` means the workflow is waiting for a
            decision. `approved` and
            `denied` are decisions a person made. `expired` means the workflow's
            approval timeout passed first, and `cancelled` means the execution
            ended while the approval was still pending. Every status but `pending`
            is final.
        function (str | Unset):
        execution_id (UUID | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | PaginatedDurableApprovals]
     """


    kwargs = request_kwargs(
        id=id,
page=page,
limit=limit,
status=status,
function=function,
execution_id=execution_id,
from_=from_,
to=to,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    page: int | Unset = UNSET,
    limit: int | Unset = 10,
    status: DurableApprovalStatus | Unset = UNSET,
    function: str | Unset = UNSET,
    execution_id: UUID | str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Error | PaginatedDurableApprovals | None:
    """ List durable approvals

     Lists the approvals durable workflows in the project have requested,
    newest first. Pending approvals are the ones a workflow is waiting on;
    decided, expired, and cancelled ones are kept for a year.

    Project access tokens can list approvals, including read-only ones.

    Args:
        id (UUID):
        page (int | Unset):
        limit (int | Unset):  Default: 10.
        status (DurableApprovalStatus | Unset): `pending` means the workflow is waiting for a
            decision. `approved` and
            `denied` are decisions a person made. `expired` means the workflow's
            approval timeout passed first, and `cancelled` means the execution
            ended while the approval was still pending. Every status but `pending`
            is final.
        function (str | Unset):
        execution_id (UUID | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | PaginatedDurableApprovals
     """


    return (await asyncio_detailed(
        id=id,
client=client,
page=page,
limit=limit,
status=status,
function=function,
execution_id=execution_id,
from_=from_,
to=to,

    )).parsed
