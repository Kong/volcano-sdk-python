from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_signup_anonymous_body import AuthSignupAnonymousBody
from ...models.auth_token_response import AuthTokenResponse
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    body: AuthSignupAnonymousBody | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/signup-anonymous",
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthTokenResponse | None:
    if response.status_code == 201:
        response_201 = AuthTokenResponse.from_dict(response.json())



        return response_201

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthTokenResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSignupAnonymousBody | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
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
    body: AuthSignupAnonymousBody | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSignupAnonymousBody | Unset = UNSET,

) -> Response[Any | AuthTokenResponse]:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthTokenResponse]
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
    body: AuthSignupAnonymousBody | Unset = UNSET,

) -> Any | AuthTokenResponse | None:
    """ Create anonymous user

     Create guest user without email/password.

    User metadata (like display_name) can be included and will appear in realtime presence events.
    Requires enable_anonymous_signins to be true.

    Args:
        body (AuthSignupAnonymousBody | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthTokenResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
