from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_resend_confirmation_body import AuthResendConfirmationBody
from ...models.auth_resend_confirmation_response_200 import AuthResendConfirmationResponse200
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: AuthResendConfirmationBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/resend-confirmation",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthResendConfirmationResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthResendConfirmationResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthResendConfirmationResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResendConfirmationBody,

) -> Response[AuthResendConfirmationResponse200 | Error]:
    """ Resend confirmation email

     Resend email confirmation link.
    Returns generic message to prevent email enumeration.
    No email is sent when the account does not exist or is already confirmed.
    If the account exists and is unconfirmed, a new token is generated and
    any previous confirmation token is invalidated.

    Args:
        body (AuthResendConfirmationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthResendConfirmationResponse200 | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: AuthResendConfirmationBody,

) -> AuthResendConfirmationResponse200 | Error | None:
    """ Resend confirmation email

     Resend email confirmation link.
    Returns generic message to prevent email enumeration.
    No email is sent when the account does not exist or is already confirmed.
    If the account exists and is unconfirmed, a new token is generated and
    any previous confirmation token is invalidated.

    Args:
        body (AuthResendConfirmationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthResendConfirmationResponse200 | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthResendConfirmationBody,

) -> Response[AuthResendConfirmationResponse200 | Error]:
    """ Resend confirmation email

     Resend email confirmation link.
    Returns generic message to prevent email enumeration.
    No email is sent when the account does not exist or is already confirmed.
    If the account exists and is unconfirmed, a new token is generated and
    any previous confirmation token is invalidated.

    Args:
        body (AuthResendConfirmationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthResendConfirmationResponse200 | Error]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: AuthResendConfirmationBody,

) -> AuthResendConfirmationResponse200 | Error | None:
    """ Resend confirmation email

     Resend email confirmation link.
    Returns generic message to prevent email enumeration.
    No email is sent when the account does not exist or is already confirmed.
    If the account exists and is unconfirmed, a new token is generated and
    any previous confirmation token is invalidated.

    Args:
        body (AuthResendConfirmationBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthResendConfirmationResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
