from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.notification_settings import NotificationSettings
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/notifications".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | NotificationSettings | None:
    if response.status_code == 200:
        response_200 = NotificationSettings.from_dict(response.json())



        return response_200

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | NotificationSettings]:
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

) -> Response[Error | NotificationSettings]:
    """ Get notification settings

     Returns where the project's alerts go and when a failing scheduler is
    announced. A project that never saved settings returns the defaults:
    email to the project owner, no webhook, and an alert after 3 failed
    runs in a row, followed by one when the scheduler recovers.

    The webhook signing secret is never returned here; `secret_configured`
    shows whether one is set. A read-only project access token is refused
    with `403`, because the webhook URL can carry the receiver's token.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationSettings]
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

) -> Error | NotificationSettings | None:
    """ Get notification settings

     Returns where the project's alerts go and when a failing scheduler is
    announced. A project that never saved settings returns the defaults:
    email to the project owner, no webhook, and an alert after 3 failed
    runs in a row, followed by one when the scheduler recovers.

    The webhook signing secret is never returned here; `secret_configured`
    shows whether one is set. A read-only project access token is refused
    with `403`, because the webhook URL can carry the receiver's token.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationSettings
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | NotificationSettings]:
    """ Get notification settings

     Returns where the project's alerts go and when a failing scheduler is
    announced. A project that never saved settings returns the defaults:
    email to the project owner, no webhook, and an alert after 3 failed
    runs in a row, followed by one when the scheduler recovers.

    The webhook signing secret is never returned here; `secret_configured`
    shows whether one is set. A read-only project access token is refused
    with `403`, because the webhook URL can carry the receiver's token.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationSettings]
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

) -> Error | NotificationSettings | None:
    """ Get notification settings

     Returns where the project's alerts go and when a failing scheduler is
    announced. A project that never saved settings returns the defaults:
    email to the project owner, no webhook, and an alert after 3 failed
    runs in a row, followed by one when the scheduler recovers.

    The webhook signing secret is never returned here; `secret_configured`
    shows whether one is set. A read-only project access token is refused
    with `403`, because the webhook URL can carry the receiver's token.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationSettings
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
