from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    key: str,
    *,
    x_volcano_request_id: UUID,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Volcano-Request-Id"] = x_volcano_request_id



    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/locks/{key}".format(key=quote(str(key), safe=""),),
    }


    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    x_volcano_request_id: UUID,

) -> Response[Any | Error]:
    """ Force release a project lock

     Drops the lease whatever token holds it, for recovering a lock whose holder
    died without releasing. Use `DELETE /locks/{key}/lease` for normal release.

    This breaks mutual exclusion by itself: the previous holder keeps working
    until its own renewal fails. Guard the protected resource with the lease's
    `fencing_token`, which the next acquisition raises, so a write from the
    displaced holder can be rejected. Succeeds when the lock is already absent.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        key=key,
x_volcano_request_id=x_volcano_request_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    key: str,
    *,
    client: AuthenticatedClient,
    x_volcano_request_id: UUID,

) -> Any | Error | None:
    """ Force release a project lock

     Drops the lease whatever token holds it, for recovering a lock whose holder
    died without releasing. Use `DELETE /locks/{key}/lease` for normal release.

    This breaks mutual exclusion by itself: the previous holder keeps working
    until its own renewal fails. Guard the protected resource with the lease's
    `fencing_token`, which the next acquisition raises, so a write from the
    displaced holder can be rejected. Succeeds when the lock is already absent.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        key=key,
client=client,
x_volcano_request_id=x_volcano_request_id,

    ).parsed

async def asyncio_detailed(
    key: str,
    *,
    client: AuthenticatedClient,
    x_volcano_request_id: UUID,

) -> Response[Any | Error]:
    """ Force release a project lock

     Drops the lease whatever token holds it, for recovering a lock whose holder
    died without releasing. Use `DELETE /locks/{key}/lease` for normal release.

    This breaks mutual exclusion by itself: the previous holder keeps working
    until its own renewal fails. Guard the protected resource with the lease's
    `fencing_token`, which the next acquisition raises, so a write from the
    displaced holder can be rejected. Succeeds when the lock is already absent.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        key=key,
x_volcano_request_id=x_volcano_request_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    key: str,
    *,
    client: AuthenticatedClient,
    x_volcano_request_id: UUID,

) -> Any | Error | None:
    """ Force release a project lock

     Drops the lease whatever token holds it, for recovering a lock whose holder
    died without releasing. Use `DELETE /locks/{key}/lease` for normal release.

    This breaks mutual exclusion by itself: the previous holder keeps working
    until its own renewal fails. Guard the protected resource with the lease's
    `fencing_token`, which the next acquisition raises, so a write from the
    displaced holder can be rejected. Succeeds when the lock is already absent.

    Args:
        key (str):
        x_volcano_request_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        key=key,
client=client,
x_volcano_request_id=x_volcano_request_id,

    )).parsed
