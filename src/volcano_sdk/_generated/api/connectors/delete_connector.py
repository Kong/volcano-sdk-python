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



def request_kwargs(
    connector_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/connectors/{connector_id}".format(connector_id=quote(str(connector_id), safe=""),),
    }


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

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 502:
        response_502 = Error.from_dict(response.json())



        return response_502

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Remove a connector

     Removes a connector. Removing a `slack` connector uninstalls the
    Volcano app from the Slack workspace, for every Volcano account that
    uses it. Only the person who installed the app there can remove it
    (`removable` is `true` for them); anyone else can uninstall the app in
    Slack. The workspace's channels stop reporting problems at their next
    check, which also cancels reports still queued. The channel bindings
    stay, and report again if the app is installed in the workspace again.

    Removing an `aikido` connector deletes its credentials and its project
    bindings, and cancels its queued reports at their next check. Remove
    the webhook in Aikido too: Volcano refuses its deliveries from then on.

    Removing works whether or not reporting problems from either service
    is available in this environment.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        connector_id=connector_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Remove a connector

     Removes a connector. Removing a `slack` connector uninstalls the
    Volcano app from the Slack workspace, for every Volcano account that
    uses it. Only the person who installed the app there can remove it
    (`removable` is `true` for them); anyone else can uninstall the app in
    Slack. The workspace's channels stop reporting problems at their next
    check, which also cancels reports still queued. The channel bindings
    stay, and report again if the app is installed in the workspace again.

    Removing an `aikido` connector deletes its credentials and its project
    bindings, and cancels its queued reports at their next check. Remove
    the webhook in Aikido too: Volcano refuses its deliveries from then on.

    Removing works whether or not reporting problems from either service
    is available in this environment.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        connector_id=connector_id,
client=client,

    ).parsed

async def asyncio_detailed(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Remove a connector

     Removes a connector. Removing a `slack` connector uninstalls the
    Volcano app from the Slack workspace, for every Volcano account that
    uses it. Only the person who installed the app there can remove it
    (`removable` is `true` for them); anyone else can uninstall the app in
    Slack. The workspace's channels stop reporting problems at their next
    check, which also cancels reports still queued. The channel bindings
    stay, and report again if the app is installed in the workspace again.

    Removing an `aikido` connector deletes its credentials and its project
    bindings, and cancels its queued reports at their next check. Remove
    the webhook in Aikido too: Volcano refuses its deliveries from then on.

    Removing works whether or not reporting problems from either service
    is available in this environment.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        connector_id=connector_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    connector_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Remove a connector

     Removes a connector. Removing a `slack` connector uninstalls the
    Volcano app from the Slack workspace, for every Volcano account that
    uses it. Only the person who installed the app there can remove it
    (`removable` is `true` for them); anyone else can uninstall the app in
    Slack. The workspace's channels stop reporting problems at their next
    check, which also cancels reports still queued. The channel bindings
    stay, and report again if the app is installed in the workspace again.

    Removing an `aikido` connector deletes its credentials and its project
    bindings, and cancels its queued reports at their next check. Remove
    the webhook in Aikido too: Volcano refuses its deliveries from then on.

    Removing works whether or not reporting problems from either service
    is available in this environment.

    Args:
        connector_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        connector_id=connector_id,
client=client,

    )).parsed
