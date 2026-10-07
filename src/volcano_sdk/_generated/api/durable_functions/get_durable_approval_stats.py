from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_approval_stats import DurableApprovalStats
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def request_kwargs(
    id: UUID | str,
    *,
    function: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["function"] = function

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
        "url": "/projects/{id}/durable-approvals/stats".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableApprovalStats | Error | None:
    if response.status_code == 200:
        response_200 = DurableApprovalStats.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableApprovalStats | Error]:
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
    function: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[DurableApprovalStats | Error]:
    """ Get durable approval statistics

     Counts the project's approvals by outcome over a time window, overall,
    per workflow, and per day. The window defaults to the last 30 days and
    can cover up to a year. An approval is counted on the day it was
    requested.

    Project access tokens can read statistics, including read-only ones.

    Args:
        id (UUID):
        function (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableApprovalStats | Error]
     """


    kwargs = request_kwargs(
        id=id,
function=function,
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
    function: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> DurableApprovalStats | Error | None:
    """ Get durable approval statistics

     Counts the project's approvals by outcome over a time window, overall,
    per workflow, and per day. The window defaults to the last 30 days and
    can cover up to a year. An approval is counted on the day it was
    requested.

    Project access tokens can read statistics, including read-only ones.

    Args:
        id (UUID):
        function (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableApprovalStats | Error
     """


    return sync_detailed(
        id=id,
client=client,
function=function,
from_=from_,
to=to,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    function: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> Response[DurableApprovalStats | Error]:
    """ Get durable approval statistics

     Counts the project's approvals by outcome over a time window, overall,
    per workflow, and per day. The window defaults to the last 30 days and
    can cover up to a year. An approval is counted on the day it was
    requested.

    Project access tokens can read statistics, including read-only ones.

    Args:
        id (UUID):
        function (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableApprovalStats | Error]
     """


    kwargs = request_kwargs(
        id=id,
function=function,
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
    function: str | Unset = UNSET,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,

) -> DurableApprovalStats | Error | None:
    """ Get durable approval statistics

     Counts the project's approvals by outcome over a time window, overall,
    per workflow, and per day. The window defaults to the last 30 days and
    can cover up to a year. An approval is counted on the day it was
    requested.

    Project access tokens can read statistics, including read-only ones.

    Args:
        id (UUID):
        function (str | Unset):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableApprovalStats | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
function=function,
from_=from_,
to=to,

    )).parsed
