from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.slack_authorization_response import SlackAuthorizationResponse
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    redirect: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["redirect"] = redirect


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/user/slack/connections",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SlackAuthorizationResponse | None:
    if response.status_code == 200:
        response_200 = SlackAuthorizationResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SlackAuthorizationResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    redirect: str | Unset = UNSET,

) -> Response[Error | SlackAuthorizationResponse]:
    """ Start connecting a Slack identity

     Starts connecting the caller's Slack identity to their Volcano account
    and returns its Sign in with Slack URL. LavaFlow acts on a person's
    Slack mention only for projects owned by an account their identity is
    connected to. The callback finishes only in the browser that started
    the connection, so a link forwarded to anyone else connects no one.
    One Slack identity may connect to several accounts, and one account may
    have several identities connected. The identity is also tied to the
    caller's sign-in session: the channel picker and binding act only as
    the identities this session signed in as, so on an account several
    people share, nobody picks or binds as another person's identity. An
    API token has no session, so it can connect an identity that reports,
    but not pick or bind channels with it. Volcano stores the workspace and
    user IDs, and no Slack token.

    The response also sets a short-lived HttpOnly cookie that binds the
    callback to this browser. Installing and connecting each set their
    own, so starting one leaves the other's callback working.

    Args:
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackAuthorizationResponse]
     """


    kwargs = request_kwargs(
        redirect=redirect,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    redirect: str | Unset = UNSET,

) -> Error | SlackAuthorizationResponse | None:
    """ Start connecting a Slack identity

     Starts connecting the caller's Slack identity to their Volcano account
    and returns its Sign in with Slack URL. LavaFlow acts on a person's
    Slack mention only for projects owned by an account their identity is
    connected to. The callback finishes only in the browser that started
    the connection, so a link forwarded to anyone else connects no one.
    One Slack identity may connect to several accounts, and one account may
    have several identities connected. The identity is also tied to the
    caller's sign-in session: the channel picker and binding act only as
    the identities this session signed in as, so on an account several
    people share, nobody picks or binds as another person's identity. An
    API token has no session, so it can connect an identity that reports,
    but not pick or bind channels with it. Volcano stores the workspace and
    user IDs, and no Slack token.

    The response also sets a short-lived HttpOnly cookie that binds the
    callback to this browser. Installing and connecting each set their
    own, so starting one leaves the other's callback working.

    Args:
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackAuthorizationResponse
     """


    return sync_detailed(
        client=client,
redirect=redirect,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    redirect: str | Unset = UNSET,

) -> Response[Error | SlackAuthorizationResponse]:
    """ Start connecting a Slack identity

     Starts connecting the caller's Slack identity to their Volcano account
    and returns its Sign in with Slack URL. LavaFlow acts on a person's
    Slack mention only for projects owned by an account their identity is
    connected to. The callback finishes only in the browser that started
    the connection, so a link forwarded to anyone else connects no one.
    One Slack identity may connect to several accounts, and one account may
    have several identities connected. The identity is also tied to the
    caller's sign-in session: the channel picker and binding act only as
    the identities this session signed in as, so on an account several
    people share, nobody picks or binds as another person's identity. An
    API token has no session, so it can connect an identity that reports,
    but not pick or bind channels with it. Volcano stores the workspace and
    user IDs, and no Slack token.

    The response also sets a short-lived HttpOnly cookie that binds the
    callback to this browser. Installing and connecting each set their
    own, so starting one leaves the other's callback working.

    Args:
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SlackAuthorizationResponse]
     """


    kwargs = request_kwargs(
        redirect=redirect,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    redirect: str | Unset = UNSET,

) -> Error | SlackAuthorizationResponse | None:
    """ Start connecting a Slack identity

     Starts connecting the caller's Slack identity to their Volcano account
    and returns its Sign in with Slack URL. LavaFlow acts on a person's
    Slack mention only for projects owned by an account their identity is
    connected to. The callback finishes only in the browser that started
    the connection, so a link forwarded to anyone else connects no one.
    One Slack identity may connect to several accounts, and one account may
    have several identities connected. The identity is also tied to the
    caller's sign-in session: the channel picker and binding act only as
    the identities this session signed in as, so on an account several
    people share, nobody picks or binds as another person's identity. An
    API token has no session, so it can connect an identity that reports,
    but not pick or bind channels with it. Volcano stores the workspace and
    user IDs, and no Slack token.

    The response also sets a short-lived HttpOnly cookie that binds the
    callback to this browser. Installing and connecting each set their
    own, so starting one leaves the other's callback working.

    Args:
        redirect (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SlackAuthorizationResponse
     """


    return (await asyncio_detailed(
        client=client,
redirect=redirect,

    )).parsed
