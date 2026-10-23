from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.durable_callback_outcome import DurableCallbackOutcome
from ...models.error import Error
from ...models.succeed_durable_callback_request import SucceedDurableCallbackRequest
from typing import cast



def request_kwargs(
    *,
    body: SucceedDurableCallbackRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/durable-callbacks/succeed",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableCallbackOutcome | Error | None:
    if response.status_code == 200:
        response_200 = DurableCallbackOutcome.from_dict(response.json())



        return response_200

    if response.status_code == 202:
        response_202 = DurableCallbackOutcome.from_dict(response.json())



        return response_202

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 410:
        response_410 = Error.from_dict(response.json())



        return response_410

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableCallbackOutcome | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SucceedDurableCallbackRequest,

) -> Response[DurableCallbackOutcome | Error]:
    """ Complete a waiting step with a result

     Resumes the workflow step waiting on the token with `result`. Call it
    from the system the workflow handed the token to.

    The token is the only credential. A token takes one outcome: once it
    has succeeded or failed, every later request is refused with
    `409 callback_completed`, including a retry of the request that
    succeeded it.

    Args:
        body (SucceedDurableCallbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableCallbackOutcome | Error]
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
    body: SucceedDurableCallbackRequest,

) -> DurableCallbackOutcome | Error | None:
    """ Complete a waiting step with a result

     Resumes the workflow step waiting on the token with `result`. Call it
    from the system the workflow handed the token to.

    The token is the only credential. A token takes one outcome: once it
    has succeeded or failed, every later request is refused with
    `409 callback_completed`, including a retry of the request that
    succeeded it.

    Args:
        body (SucceedDurableCallbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableCallbackOutcome | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: SucceedDurableCallbackRequest,

) -> Response[DurableCallbackOutcome | Error]:
    """ Complete a waiting step with a result

     Resumes the workflow step waiting on the token with `result`. Call it
    from the system the workflow handed the token to.

    The token is the only credential. A token takes one outcome: once it
    has succeeded or failed, every later request is refused with
    `409 callback_completed`, including a retry of the request that
    succeeded it.

    Args:
        body (SucceedDurableCallbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableCallbackOutcome | Error]
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
    body: SucceedDurableCallbackRequest,

) -> DurableCallbackOutcome | Error | None:
    """ Complete a waiting step with a result

     Resumes the workflow step waiting on the token with `result`. Call it
    from the system the workflow handed the token to.

    The token is the only credential. A token takes one outcome: once it
    has succeeded or failed, every later request is refused with
    `409 callback_completed`, including a retry of the request that
    succeeded it.

    Args:
        body (SucceedDurableCallbackRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableCallbackOutcome | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
