from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_convert_anonymous_body import AuthConvertAnonymousBody
from ...models.auth_convert_anonymous_response_200 import AuthConvertAnonymousResponse200
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: AuthConvertAnonymousBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/user/convert-anonymous",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthConvertAnonymousResponse200 | Error | None:
    if response.status_code == 200:
        response_200 = AuthConvertAnonymousResponse200.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthConvertAnonymousResponse200 | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthConvertAnonymousBody,

) -> Response[Any | AuthConvertAnonymousResponse200 | Error]:
    """ Convert anonymous user to authenticated

     Add email and password to anonymous user.
    Requires auth user access token.
    If require_email_confirmation is enabled for the project, the converted
    user remains unconfirmed until /auth/confirm succeeds. When email
    sending is enabled, a confirmation email is sent during conversion.

    Args:
        body (AuthConvertAnonymousBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthConvertAnonymousResponse200 | Error]
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
    body: AuthConvertAnonymousBody,

) -> Any | AuthConvertAnonymousResponse200 | Error | None:
    """ Convert anonymous user to authenticated

     Add email and password to anonymous user.
    Requires auth user access token.
    If require_email_confirmation is enabled for the project, the converted
    user remains unconfirmed until /auth/confirm succeeds. When email
    sending is enabled, a confirmation email is sent during conversion.

    Args:
        body (AuthConvertAnonymousBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthConvertAnonymousResponse200 | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthConvertAnonymousBody,

) -> Response[Any | AuthConvertAnonymousResponse200 | Error]:
    """ Convert anonymous user to authenticated

     Add email and password to anonymous user.
    Requires auth user access token.
    If require_email_confirmation is enabled for the project, the converted
    user remains unconfirmed until /auth/confirm succeeds. When email
    sending is enabled, a confirmation email is sent during conversion.

    Args:
        body (AuthConvertAnonymousBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthConvertAnonymousResponse200 | Error]
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
    body: AuthConvertAnonymousBody,

) -> Any | AuthConvertAnonymousResponse200 | Error | None:
    """ Convert anonymous user to authenticated

     Add email and password to anonymous user.
    Requires auth user access token.
    If require_email_confirmation is enabled for the project, the converted
    user remains unconfirmed until /auth/confirm succeeds. When email
    sending is enabled, a confirmation email is sent during conversion.

    Args:
        body (AuthConvertAnonymousBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthConvertAnonymousResponse200 | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
