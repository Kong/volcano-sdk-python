from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.notification_settings import NotificationSettings
from ...models.update_notification_settings_request import UpdateNotificationSettingsRequest
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    body: UpdateNotificationSettingsRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/notifications".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | NotificationSettings | None:
    if response.status_code == 200:
        response_200 = NotificationSettings.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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
    body: UpdateNotificationSettingsRequest,

) -> Response[Error | NotificationSettings]:
    """ Update notification settings

     Changes the project's notification settings. Omitted fields keep their
    current values, so `{"email": {"enabled": false}}` only turns email off.

    Alert emails go only to the project owner's verified account email
    address. `email.recipients` may be empty or name that address; any
    other list is refused with `400`, and so is any non-empty list while
    the owner has no verified address. `email.status` in the response
    says whether alerts are being emailed.

    Setting `webhook.url` on a project without a webhook generates its
    signing secret, returned in `webhook.secret` in this response only.
    Changing the URL keeps the secret. An empty `webhook.url` removes the
    webhook and its secret.

    Outside local mode the webhook must be reachable on the public
    internet; a URL naming a private or loopback address is refused, and
    so is a delivery to a host name that resolves to one.

    Args:
        id (UUID):
        body (UpdateNotificationSettingsRequest): Omitted fields keep their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationSettings]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateNotificationSettingsRequest,

) -> Error | NotificationSettings | None:
    """ Update notification settings

     Changes the project's notification settings. Omitted fields keep their
    current values, so `{"email": {"enabled": false}}` only turns email off.

    Alert emails go only to the project owner's verified account email
    address. `email.recipients` may be empty or name that address; any
    other list is refused with `400`, and so is any non-empty list while
    the owner has no verified address. `email.status` in the response
    says whether alerts are being emailed.

    Setting `webhook.url` on a project without a webhook generates its
    signing secret, returned in `webhook.secret` in this response only.
    Changing the URL keeps the secret. An empty `webhook.url` removes the
    webhook and its secret.

    Outside local mode the webhook must be reachable on the public
    internet; a URL naming a private or loopback address is refused, and
    so is a delivery to a host name that resolves to one.

    Args:
        id (UUID):
        body (UpdateNotificationSettingsRequest): Omitted fields keep their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationSettings
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateNotificationSettingsRequest,

) -> Response[Error | NotificationSettings]:
    """ Update notification settings

     Changes the project's notification settings. Omitted fields keep their
    current values, so `{"email": {"enabled": false}}` only turns email off.

    Alert emails go only to the project owner's verified account email
    address. `email.recipients` may be empty or name that address; any
    other list is refused with `400`, and so is any non-empty list while
    the owner has no verified address. `email.status` in the response
    says whether alerts are being emailed.

    Setting `webhook.url` on a project without a webhook generates its
    signing secret, returned in `webhook.secret` in this response only.
    Changing the URL keeps the secret. An empty `webhook.url` removes the
    webhook and its secret.

    Outside local mode the webhook must be reachable on the public
    internet; a URL naming a private or loopback address is refused, and
    so is a delivery to a host name that resolves to one.

    Args:
        id (UUID):
        body (UpdateNotificationSettingsRequest): Omitted fields keep their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | NotificationSettings]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateNotificationSettingsRequest,

) -> Error | NotificationSettings | None:
    """ Update notification settings

     Changes the project's notification settings. Omitted fields keep their
    current values, so `{"email": {"enabled": false}}` only turns email off.

    Alert emails go only to the project owner's verified account email
    address. `email.recipients` may be empty or name that address; any
    other list is refused with `400`, and so is any non-empty list while
    the owner has no verified address. `email.status` in the response
    says whether alerts are being emailed.

    Setting `webhook.url` on a project without a webhook generates its
    signing secret, returned in `webhook.secret` in this response only.
    Changing the URL keeps the secret. An empty `webhook.url` removes the
    webhook and its secret.

    Outside local mode the webhook must be reachable on the public
    internet; a URL naming a private or loopback address is refused, and
    so is a delivery to a host name that resolves to one.

    Args:
        id (UUID):
        body (UpdateNotificationSettingsRequest): Omitted fields keep their current values.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | NotificationSettings
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
