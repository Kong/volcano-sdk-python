from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_signup_body import AuthSignupBody
from ...models.auth_signup_response import AuthSignupResponse
from ...models.error import Error
from typing import cast



def _get_kwargs(
    *,
    body: AuthSignupBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/signup",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | AuthSignupResponse | Error | None:
    if response.status_code == 201:
        response_201 = AuthSignupResponse.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401

    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403

    if response.status_code == 429:
        response_429 = cast(Any, None)
        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | AuthSignupResponse | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSignupBody,

) -> Response[Any | AuthSignupResponse | Error]:
    """ Sign up a new auth user

     Create a new end-user account. The project is determined from the anon key.
    Requires project-specific anon key in Authorization header.

    **Session-less**: signup never issues a session. On success it returns a
    uniform acknowledgement (`AuthSignupResponse`) with no tokens; the client
    obtains a session with a subsequent `POST /auth/signin`. If email confirmation
    is enabled for the project, a confirmation email is sent and
    `confirmation_required` is `true`.

    **Anti-enumeration**: a signup for an already-registered email returns the
    exact same `201` response as a fresh signup — it never returns `409` — so the
    response cannot be used to discover which emails are registered.

    Args:
        body (AuthSignupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthSignupResponse | Error]
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
    body: AuthSignupBody,

) -> Any | AuthSignupResponse | Error | None:
    """ Sign up a new auth user

     Create a new end-user account. The project is determined from the anon key.
    Requires project-specific anon key in Authorization header.

    **Session-less**: signup never issues a session. On success it returns a
    uniform acknowledgement (`AuthSignupResponse`) with no tokens; the client
    obtains a session with a subsequent `POST /auth/signin`. If email confirmation
    is enabled for the project, a confirmation email is sent and
    `confirmation_required` is `true`.

    **Anti-enumeration**: a signup for an already-registered email returns the
    exact same `201` response as a fresh signup — it never returns `409` — so the
    response cannot be used to discover which emails are registered.

    Args:
        body (AuthSignupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthSignupResponse | Error
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: AuthSignupBody,

) -> Response[Any | AuthSignupResponse | Error]:
    """ Sign up a new auth user

     Create a new end-user account. The project is determined from the anon key.
    Requires project-specific anon key in Authorization header.

    **Session-less**: signup never issues a session. On success it returns a
    uniform acknowledgement (`AuthSignupResponse`) with no tokens; the client
    obtains a session with a subsequent `POST /auth/signin`. If email confirmation
    is enabled for the project, a confirmation email is sent and
    `confirmation_required` is `true`.

    **Anti-enumeration**: a signup for an already-registered email returns the
    exact same `201` response as a fresh signup — it never returns `409` — so the
    response cannot be used to discover which emails are registered.

    Args:
        body (AuthSignupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | AuthSignupResponse | Error]
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
    body: AuthSignupBody,

) -> Any | AuthSignupResponse | Error | None:
    """ Sign up a new auth user

     Create a new end-user account. The project is determined from the anon key.
    Requires project-specific anon key in Authorization header.

    **Session-less**: signup never issues a session. On success it returns a
    uniform acknowledgement (`AuthSignupResponse`) with no tokens; the client
    obtains a session with a subsequent `POST /auth/signin`. If email confirmation
    is enabled for the project, a confirmation email is sent and
    `confirmation_required` is `true`.

    **Anti-enumeration**: a signup for an already-registered email returns the
    exact same `201` response as a fresh signup — it never returns `409` — so the
    response cannot be used to discover which emails are registered.

    Args:
        body (AuthSignupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | AuthSignupResponse | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
