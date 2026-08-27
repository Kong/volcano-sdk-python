from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_stats import DatabaseStats
from ...models.error import Error
from ...models.get_database_stats_granularity import check_get_database_stats_granularity
from ...models.get_database_stats_granularity import GetDatabaseStatsGranularity
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    id: UUID,
    database_name: str,
    *,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    granularity: GetDatabaseStatsGranularity | Unset = 'hourly',

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

    json_granularity: str | Unset = UNSET
    if not isinstance(granularity, Unset):
        json_granularity = granularity

    params["granularity"] = json_granularity


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/databases/{database_name}/stats".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseStats | Error | None:
    if response.status_code == 200:
        response_200 = DatabaseStats.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseStats | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    granularity: GetDatabaseStatsGranularity | Unset = 'hourly',

) -> Response[DatabaseStats | Error]:
    """ Get database consumption metrics

     Retrieve consumption metrics including storage, compute time, and data transfer.
    Metrics are aggregated at the project level. Defaults to last 24 hours.

    **Note:** Advanced metrics require an upgraded plan.

    Args:
        id (UUID):
        database_name (str):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):
        granularity (GetDatabaseStatsGranularity | Unset):  Default: 'hourly'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseStats | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
from_=from_,
to=to,
granularity=granularity,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    granularity: GetDatabaseStatsGranularity | Unset = 'hourly',

) -> DatabaseStats | Error | None:
    """ Get database consumption metrics

     Retrieve consumption metrics including storage, compute time, and data transfer.
    Metrics are aggregated at the project level. Defaults to last 24 hours.

    **Note:** Advanced metrics require an upgraded plan.

    Args:
        id (UUID):
        database_name (str):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):
        granularity (GetDatabaseStatsGranularity | Unset):  Default: 'hourly'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseStats | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
client=client,
from_=from_,
to=to,
granularity=granularity,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    granularity: GetDatabaseStatsGranularity | Unset = 'hourly',

) -> Response[DatabaseStats | Error]:
    """ Get database consumption metrics

     Retrieve consumption metrics including storage, compute time, and data transfer.
    Metrics are aggregated at the project level. Defaults to last 24 hours.

    **Note:** Advanced metrics require an upgraded plan.

    Args:
        id (UUID):
        database_name (str):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):
        granularity (GetDatabaseStatsGranularity | Unset):  Default: 'hourly'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseStats | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
from_=from_,
to=to,
granularity=granularity,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    *,
    client: AuthenticatedClient,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    granularity: GetDatabaseStatsGranularity | Unset = 'hourly',

) -> DatabaseStats | Error | None:
    """ Get database consumption metrics

     Retrieve consumption metrics including storage, compute time, and data transfer.
    Metrics are aggregated at the project level. Defaults to last 24 hours.

    **Note:** Advanced metrics require an upgraded plan.

    Args:
        id (UUID):
        database_name (str):
        from_ (datetime.datetime | Unset):
        to (datetime.datetime | Unset):
        granularity (GetDatabaseStatsGranularity | Unset):  Default: 'hourly'.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseStats | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
client=client,
from_=from_,
to=to,
granularity=granularity,

    )).parsed
