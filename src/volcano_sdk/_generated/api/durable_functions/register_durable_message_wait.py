from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_message_wait_registration import DurableMessageWaitRegistration
from ...models.error import Error
from ...models.register_durable_message_wait_request import RegisterDurableMessageWaitRequest
from typing import cast



def request_kwargs(
    *,
    body: RegisterDurableMessageWaitRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-messages/waits",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableMessageWaitRegistration | Error | None:
    if response.status_code == 200:
        response_200 = DurableMessageWaitRegistration.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = DurableMessageWaitRegistration.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableMessageWaitRegistration | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterDurableMessageWaitRequest,

) -> Response[DurableMessageWaitRegistration | Error]:
    """ Wait for a message from inside a workflow

     Registers a wait for a named message. The Volcano SDK calls this from
    `ctx.waitForMessage`; applications do not call it directly.

    `execution_ref` and `callback_id` are opaque values the SDK reads from
    the running workflow. Together they are the request's credential, so
    the operation takes no other authentication. When a message for the
    name is already queued, the wait takes the oldest one at once.

    Retrying is safe: a request for a wait that is already registered
    returns it with `200`.

    Args:
        body (RegisterDurableMessageWaitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageWaitRegistration | Error]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterDurableMessageWaitRequest,

) -> DurableMessageWaitRegistration | Error | None:
    """ Wait for a message from inside a workflow

     Registers a wait for a named message. The Volcano SDK calls this from
    `ctx.waitForMessage`; applications do not call it directly.

    `execution_ref` and `callback_id` are opaque values the SDK reads from
    the running workflow. Together they are the request's credential, so
    the operation takes no other authentication. When a message for the
    name is already queued, the wait takes the oldest one at once.

    Retrying is safe: a request for a wait that is already registered
    returns it with `200`.

    Args:
        body (RegisterDurableMessageWaitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageWaitRegistration | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterDurableMessageWaitRequest,

) -> Response[DurableMessageWaitRegistration | Error]:
    """ Wait for a message from inside a workflow

     Registers a wait for a named message. The Volcano SDK calls this from
    `ctx.waitForMessage`; applications do not call it directly.

    `execution_ref` and `callback_id` are opaque values the SDK reads from
    the running workflow. Together they are the request's credential, so
    the operation takes no other authentication. When a message for the
    name is already queued, the wait takes the oldest one at once.

    Retrying is safe: a request for a wait that is already registered
    returns it with `200`.

    Args:
        body (RegisterDurableMessageWaitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessageWaitRegistration | Error]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: RegisterDurableMessageWaitRequest,

) -> DurableMessageWaitRegistration | Error | None:
    """ Wait for a message from inside a workflow

     Registers a wait for a named message. The Volcano SDK calls this from
    `ctx.waitForMessage`; applications do not call it directly.

    `execution_ref` and `callback_id` are opaque values the SDK reads from
    the running workflow. Together they are the request's credential, so
    the operation takes no other authentication. When a message for the
    name is already queued, the wait takes the oldest one at once.

    Retrying is safe: a request for a wait that is already registered
    returns it with `200`.

    Args:
        body (RegisterDurableMessageWaitRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessageWaitRegistration | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
