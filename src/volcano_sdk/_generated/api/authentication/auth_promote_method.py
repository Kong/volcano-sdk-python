from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_method_summary import AuthMethodSummary
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    method_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/auth/user/methods/{method_id}/promote".format(method_id=quote(str(method_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthMethodSummary | Error | None:
    if response.status_code == 200:
        response_200 = AuthMethodSummary.from_dict(response.json())



        return response_200

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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthMethodSummary | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    method_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AuthMethodSummary | Error]:
    """ Set a method as the account's primary

     Promotes the given method to the account's primary sign-in method. The
    account's canonical email is re-derived from the promoted method's identity.
    Refused for password stubs and converted anonymous methods, and for an
    identity whose domain is outside the project's `allowed_email_domains`.

    Args:
        method_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthMethodSummary | Error]
     """


    kwargs = _get_kwargs(
        method_id=method_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    method_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AuthMethodSummary | Error | None:
    """ Set a method as the account's primary

     Promotes the given method to the account's primary sign-in method. The
    account's canonical email is re-derived from the promoted method's identity.
    Refused for password stubs and converted anonymous methods, and for an
    identity whose domain is outside the project's `allowed_email_domains`.

    Args:
        method_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthMethodSummary | Error
     """


    return sync_detailed(
        method_id=method_id,
client=client,

    ).parsed

async def asyncio_detailed(
    method_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[AuthMethodSummary | Error]:
    """ Set a method as the account's primary

     Promotes the given method to the account's primary sign-in method. The
    account's canonical email is re-derived from the promoted method's identity.
    Refused for password stubs and converted anonymous methods, and for an
    identity whose domain is outside the project's `allowed_email_domains`.

    Args:
        method_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthMethodSummary | Error]
     """


    kwargs = _get_kwargs(
        method_id=method_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    method_id: UUID,
    *,
    client: AuthenticatedClient,

) -> AuthMethodSummary | Error | None:
    """ Set a method as the account's primary

     Promotes the given method to the account's primary sign-in method. The
    account's canonical email is re-derived from the promoted method's identity.
    Refused for password stubs and converted anonymous methods, and for an
    identity whose domain is outside the project's `allowed_email_domains`.

    Args:
        method_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthMethodSummary | Error
     """


    return (await asyncio_detailed(
        method_id=method_id,
client=client,

    )).parsed
