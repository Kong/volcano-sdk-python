from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_message import DurableMessage
from ...models.error import Error
from ...models.send_durable_message_request import SendDurableMessageRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    function_id: str,
    execution_id: UUID | str,
    *,
    body: SendDurableMessageRequest,
    idempotency_key: str | Unset = UNSET,
    x_volcano_client_token: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key

    if not isinstance(x_volcano_client_token, Unset):
        headers["X-Volcano-Client-Token"] = x_volcano_client_token



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-functions/{function_id}/executions/{execution_id}/messages".format(function_id=quote(str(function_id), safe=""),execution_id=quote(str(execution_id), safe=""),),
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

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableMessage | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SendDurableMessageRequest,
    idempotency_key: str | Unset = UNSET,
    x_volcano_client_token: str | Unset = UNSET,

) -> Response[DurableMessage | Error]:
    """ Send a message to a durable execution from an application

     Sends a named message to a running execution. The workflow receives it
    from `ctx.waitForMessage` with the same name. A message sent before
    anything waits for its name is kept, and each wait takes the oldest
    one, so messages arrive in the order they were sent.

    Messages never decide an approval: a workflow waiting in
    `ctx.waitForApproval` is not resumed by one.

    **With a service key:** any execution in the project.

    **With an auth user token:** an execution the user started, or one
    whose `X-Volcano-Client-Token` the request carries, of a durable
    function whose `visibility` is `authenticated` or `public`.

    **With an anon key:** an execution whose `X-Volcano-Client-Token` the
    request carries, of a function with `visibility: public`.

    Any other execution answers `404`, as a missing one does.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key the
    same sender has used on the execution returns the first message with
    `200` and sends nothing.

    Args:
        function_id (str):
        execution_id (UUID):
        idempotency_key (str | Unset):
        x_volcano_client_token (str | Unset):
        body (SendDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessage | Error]
     """


    kwargs = request_kwargs(
        function_id=function_id,
execution_id=execution_id,
body=body,
idempotency_key=idempotency_key,
x_volcano_client_token=x_volcano_client_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SendDurableMessageRequest,
    idempotency_key: str | Unset = UNSET,
    x_volcano_client_token: str | Unset = UNSET,

) -> DurableMessage | Error | None:
    """ Send a message to a durable execution from an application

     Sends a named message to a running execution. The workflow receives it
    from `ctx.waitForMessage` with the same name. A message sent before
    anything waits for its name is kept, and each wait takes the oldest
    one, so messages arrive in the order they were sent.

    Messages never decide an approval: a workflow waiting in
    `ctx.waitForApproval` is not resumed by one.

    **With a service key:** any execution in the project.

    **With an auth user token:** an execution the user started, or one
    whose `X-Volcano-Client-Token` the request carries, of a durable
    function whose `visibility` is `authenticated` or `public`.

    **With an anon key:** an execution whose `X-Volcano-Client-Token` the
    request carries, of a function with `visibility: public`.

    Any other execution answers `404`, as a missing one does.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key the
    same sender has used on the execution returns the first message with
    `200` and sends nothing.

    Args:
        function_id (str):
        execution_id (UUID):
        idempotency_key (str | Unset):
        x_volcano_client_token (str | Unset):
        body (SendDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessage | Error
     """


    return sync_detailed(
        function_id=function_id,
execution_id=execution_id,
client=client,
body=body,
idempotency_key=idempotency_key,
x_volcano_client_token=x_volcano_client_token,

    ).parsed

async def asyncio_detailed(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SendDurableMessageRequest,
    idempotency_key: str | Unset = UNSET,
    x_volcano_client_token: str | Unset = UNSET,

) -> Response[DurableMessage | Error]:
    """ Send a message to a durable execution from an application

     Sends a named message to a running execution. The workflow receives it
    from `ctx.waitForMessage` with the same name. A message sent before
    anything waits for its name is kept, and each wait takes the oldest
    one, so messages arrive in the order they were sent.

    Messages never decide an approval: a workflow waiting in
    `ctx.waitForApproval` is not resumed by one.

    **With a service key:** any execution in the project.

    **With an auth user token:** an execution the user started, or one
    whose `X-Volcano-Client-Token` the request carries, of a durable
    function whose `visibility` is `authenticated` or `public`.

    **With an anon key:** an execution whose `X-Volcano-Client-Token` the
    request carries, of a function with `visibility: public`.

    Any other execution answers `404`, as a missing one does.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key the
    same sender has used on the execution returns the first message with
    `200` and sends nothing.

    Args:
        function_id (str):
        execution_id (UUID):
        idempotency_key (str | Unset):
        x_volcano_client_token (str | Unset):
        body (SendDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableMessage | Error]
     """


    kwargs = request_kwargs(
        function_id=function_id,
execution_id=execution_id,
body=body,
idempotency_key=idempotency_key,
x_volcano_client_token=x_volcano_client_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    function_id: str,
    execution_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: SendDurableMessageRequest,
    idempotency_key: str | Unset = UNSET,
    x_volcano_client_token: str | Unset = UNSET,

) -> DurableMessage | Error | None:
    """ Send a message to a durable execution from an application

     Sends a named message to a running execution. The workflow receives it
    from `ctx.waitForMessage` with the same name. A message sent before
    anything waits for its name is kept, and each wait takes the oldest
    one, so messages arrive in the order they were sent.

    Messages never decide an approval: a workflow waiting in
    `ctx.waitForApproval` is not resumed by one.

    **With a service key:** any execution in the project.

    **With an auth user token:** an execution the user started, or one
    whose `X-Volcano-Client-Token` the request carries, of a durable
    function whose `visibility` is `authenticated` or `public`.

    **With an anon key:** an execution whose `X-Volcano-Client-Token` the
    request carries, of a function with `visibility: public`.

    Any other execution answers `404`, as a missing one does.

    Send `Idempotency-Key` to make a retry safe: a repeat with a key the
    same sender has used on the execution returns the first message with
    `200` and sends nothing.

    Args:
        function_id (str):
        execution_id (UUID):
        idempotency_key (str | Unset):
        x_volcano_client_token (str | Unset):
        body (SendDurableMessageRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableMessage | Error
     """


    return (await asyncio_detailed(
        function_id=function_id,
execution_id=execution_id,
client=client,
body=body,
idempotency_key=idempotency_key,
x_volcano_client_token=x_volcano_client_token,

    )).parsed
