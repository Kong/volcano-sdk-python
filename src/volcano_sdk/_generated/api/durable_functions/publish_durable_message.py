from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_message import DurableMessage
from ...models.error import Error
from ...models.publish_durable_message_request import PublishDurableMessageRequest
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    body: PublishDurableMessageRequest,
    x_volcano_durable_session: str,
    idempotency_key: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["X-Volcano-Durable-Session"] = x_volcano_durable_session

    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-messages/publish",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableMessage | Error | None:
    if response.status_code == 200:
        response_200 = DurableMessage.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = DurableMessage.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableMessage | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PublishDurableMessageRequest,
    x_volcano_durable_session: str,
    idempotency_key: str | Unset = UNSET,

) -> Response[DurableMessage | Error]:
    """ Publish a message from inside a workflow

     Publishes a named message from a running workflow. The Volcano SDK
    calls this from `ctx.publish`; applications do not call it directly.

    The message is stored, listed with the execution's messages, and
    delivered live to clients subscribed to the execution. Live delivery
    counts against the project's Realtime messages.

    The SDK sends an `Idempotency-Key` that a rerun of the publishing step
    repeats, so a step that runs again returns the first message with
    `200` and publishes nothing.

    Args:
        x_volcano_durable_session (str):
        idempotency_key (str | Unset):
        body (PublishDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessage | Error]
     """


    kwargs = request_kwargs(
        body=body,
x_volcano_durable_session=x_volcano_durable_session,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: PublishDurableMessageRequest,
    x_volcano_durable_session: str,
    idempotency_key: str | Unset = UNSET,

) -> DurableMessage | Error | None:
    """ Publish a message from inside a workflow

     Publishes a named message from a running workflow. The Volcano SDK
    calls this from `ctx.publish`; applications do not call it directly.

    The message is stored, listed with the execution's messages, and
    delivered live to clients subscribed to the execution. Live delivery
    counts against the project's Realtime messages.

    The SDK sends an `Idempotency-Key` that a rerun of the publishing step
    repeats, so a step that runs again returns the first message with
    `200` and publishes nothing.

    Args:
        x_volcano_durable_session (str):
        idempotency_key (str | Unset):
        body (PublishDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessage | Error
     """


    return sync_detailed(
        client=client,
body=body,
x_volcano_durable_session=x_volcano_durable_session,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: PublishDurableMessageRequest,
    x_volcano_durable_session: str,
    idempotency_key: str | Unset = UNSET,

) -> Response[DurableMessage | Error]:
    """ Publish a message from inside a workflow

     Publishes a named message from a running workflow. The Volcano SDK
    calls this from `ctx.publish`; applications do not call it directly.

    The message is stored, listed with the execution's messages, and
    delivered live to clients subscribed to the execution. Live delivery
    counts against the project's Realtime messages.

    The SDK sends an `Idempotency-Key` that a rerun of the publishing step
    repeats, so a step that runs again returns the first message with
    `200` and publishes nothing.

    Args:
        x_volcano_durable_session (str):
        idempotency_key (str | Unset):
        body (PublishDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessage | Error]
     """


    kwargs = request_kwargs(
        body=body,
x_volcano_durable_session=x_volcano_durable_session,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: PublishDurableMessageRequest,
    x_volcano_durable_session: str,
    idempotency_key: str | Unset = UNSET,

) -> DurableMessage | Error | None:
    """ Publish a message from inside a workflow

     Publishes a named message from a running workflow. The Volcano SDK
    calls this from `ctx.publish`; applications do not call it directly.

    The message is stored, listed with the execution's messages, and
    delivered live to clients subscribed to the execution. Live delivery
    counts against the project's Realtime messages.

    The SDK sends an `Idempotency-Key` that a rerun of the publishing step
    repeats, so a step that runs again returns the first message with
    `200` and publishes nothing.

    Args:
        x_volcano_durable_session (str):
        idempotency_key (str | Unset):
        body (PublishDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessage | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,
x_volcano_durable_session=x_volcano_durable_session,
idempotency_key=idempotency_key,

    )).parsed
