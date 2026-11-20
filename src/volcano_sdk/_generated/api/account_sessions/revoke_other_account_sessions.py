from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from typing import cast



def request_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/user/sessions",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Sign out every other session

     Ends every session of the account except the one the calling token
    was exchanged from, and revokes the platform tokens exchanged from
    them. When the calling token has no session, every session ends.

    Platform tokens that were never linked to a session, such as one
    created in the dashboard or through the management API, keep working.
    Revoke each with `DELETE /user/tokens/current`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Sign out every other session

     Ends every session of the account except the one the calling token
    was exchanged from, and revokes the platform tokens exchanged from
    them. When the calling token has no session, every session ends.

    Platform tokens that were never linked to a session, such as one
    created in the dashboard or through the management API, keep working.
    Revoke each with `DELETE /user/tokens/current`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[Any | Error]:
    """ Sign out every other session

     Ends every session of the account except the one the calling token
    was exchanged from, and revokes the platform tokens exchanged from
    them. When the calling token has no session, every session ends.

    Platform tokens that were never linked to a session, such as one
    created in the dashboard or through the management API, keep working.
    Revoke each with `DELETE /user/tokens/current`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = request_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> Any | Error | None:
    """ Sign out every other session

     Ends every session of the account except the one the calling token
    was exchanged from, and revokes the platform tokens exchanged from
    them. When the calling token has no session, every session ends.

    Platform tokens that were never linked to a session, such as one
    created in the dashboard or through the management API, keep working.
    Revoke each with `DELETE /user/tokens/current`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
