from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_insights_interval import AuthInsightsInterval
from ...models.auth_insights_interval import check_auth_insights_interval
from ...models.auth_insights_response import AuthInsightsResponse
from ...models.error import Error
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    id: UUID,
    *,
    from_: datetime.date | Unset = UNSET,
    to: datetime.date | Unset = UNSET,
    interval: AuthInsightsInterval | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_from_: str | Unset = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: str | Unset = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_interval: str | Unset = UNSET
    if not isinstance(interval, Unset):
        json_interval = interval

    params["interval"] = json_interval


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/insights".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthInsightsResponse | Error | None:
    if response.status_code == 200:
        response_200 = AuthInsightsResponse.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthInsightsResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    from_: datetime.date | Unset = UNSET,
    to: datetime.date | Unset = UNSET,
    interval: AuthInsightsInterval | Unset = UNSET,

) -> Response[AuthInsightsResponse | Error]:
    """ Get auth user insights

     Returns current auth-user totals, rolling 30-day active users, and
    zero-filled signup and successful sign-in counts for an inclusive UTC
    date range. Weeks start on Monday. Sign-in counts and active-user
    activity begin when collection is deployed. Historical signup counts
    are backfilled from users present at deployment. Token refreshes affect
    active users but not the sign-in series.

    Args:
        id (UUID):
        from_ (datetime.date | Unset):
        to (datetime.date | Unset):
        interval (AuthInsightsInterval | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthInsightsResponse | Error]
     """


    kwargs = _get_kwargs(
        id=id,
from_=from_,
to=to,
interval=interval,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    from_: datetime.date | Unset = UNSET,
    to: datetime.date | Unset = UNSET,
    interval: AuthInsightsInterval | Unset = UNSET,

) -> AuthInsightsResponse | Error | None:
    """ Get auth user insights

     Returns current auth-user totals, rolling 30-day active users, and
    zero-filled signup and successful sign-in counts for an inclusive UTC
    date range. Weeks start on Monday. Sign-in counts and active-user
    activity begin when collection is deployed. Historical signup counts
    are backfilled from users present at deployment. Token refreshes affect
    active users but not the sign-in series.

    Args:
        id (UUID):
        from_ (datetime.date | Unset):
        to (datetime.date | Unset):
        interval (AuthInsightsInterval | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthInsightsResponse | Error
     """


    return sync_detailed(
        id=id,
client=client,
from_=from_,
to=to,
interval=interval,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    from_: datetime.date | Unset = UNSET,
    to: datetime.date | Unset = UNSET,
    interval: AuthInsightsInterval | Unset = UNSET,

) -> Response[AuthInsightsResponse | Error]:
    """ Get auth user insights

     Returns current auth-user totals, rolling 30-day active users, and
    zero-filled signup and successful sign-in counts for an inclusive UTC
    date range. Weeks start on Monday. Sign-in counts and active-user
    activity begin when collection is deployed. Historical signup counts
    are backfilled from users present at deployment. Token refreshes affect
    active users but not the sign-in series.

    Args:
        id (UUID):
        from_ (datetime.date | Unset):
        to (datetime.date | Unset):
        interval (AuthInsightsInterval | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthInsightsResponse | Error]
     """


    kwargs = _get_kwargs(
        id=id,
from_=from_,
to=to,
interval=interval,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    from_: datetime.date | Unset = UNSET,
    to: datetime.date | Unset = UNSET,
    interval: AuthInsightsInterval | Unset = UNSET,

) -> AuthInsightsResponse | Error | None:
    """ Get auth user insights

     Returns current auth-user totals, rolling 30-day active users, and
    zero-filled signup and successful sign-in counts for an inclusive UTC
    date range. Weeks start on Monday. Sign-in counts and active-user
    activity begin when collection is deployed. Historical signup counts
    are backfilled from users present at deployment. Token refreshes affect
    active users but not the sign-in series.

    Args:
        id (UUID):
        from_ (datetime.date | Unset):
        to (datetime.date | Unset):
        interval (AuthInsightsInterval | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthInsightsResponse | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
from_=from_,
to=to,
interval=interval,

    )).parsed
