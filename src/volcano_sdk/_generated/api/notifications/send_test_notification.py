from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.notification_test_result import NotificationTestResult
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/notifications/test".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | NotificationTestResult | None:
    if response.status_code == 200:
        response_200 = NotificationTestResult.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | NotificationTestResult]:
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

) -> Response[Error | NotificationTestResult]:
    """ Send a test notification

     Sends a `notification.test` event on every channel that delivers
    right away and reports how each delivery went. A webhook delivery is
    signed like an alert. Enabled email is reported undelivered, without
    sending, while the project owner has no verified account email
    address. One test per project per minute.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationTestResult]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | NotificationTestResult | None:
    """ Send a test notification

     Sends a `notification.test` event on every channel that delivers
    right away and reports how each delivery went. A webhook delivery is
    signed like an alert. Enabled email is reported undelivered, without
    sending, while the project owner has no verified account email
    address. One test per project per minute.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationTestResult
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | NotificationTestResult]:
    """ Send a test notification

     Sends a `notification.test` event on every channel that delivers
    right away and reports how each delivery went. A webhook delivery is
    signed like an alert. Enabled email is reported undelivered, without
    sending, while the project owner has no verified account email
    address. One test per project per minute.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationTestResult]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | NotificationTestResult | None:
    """ Send a test notification

     Sends a `notification.test` event on every channel that delivers
    right away and reports how each delivery went. A webhook delivery is
    signed like an alert. Enabled email is reported undelivered, without
    sending, while the project owner has no verified account email
    address. One test per project per minute.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationTestResult
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
