from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_password_policy import AuthPasswordPolicy
from ...models.error import Error
from typing import cast



def _get_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/auth/password-policy",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthPasswordPolicy | Error | None:
    if response.status_code == 200:
        response_200 = AuthPasswordPolicy.from_dict(response.json())



        return response_200

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthPasswordPolicy | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AuthPasswordPolicy | Error]:
    """ Get the effective password policy

     Returns the backend-enforced password bounds and compromised-password
    screening status for the project identified by the anon key. A valid
    anon key is required, but no route-specific auth permission is needed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthPasswordPolicy | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,

) -> AuthPasswordPolicy | Error | None:
    """ Get the effective password policy

     Returns the backend-enforced password bounds and compromised-password
    screening status for the project identified by the anon key. A valid
    anon key is required, but no route-specific auth permission is needed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthPasswordPolicy | Error
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,

) -> Response[AuthPasswordPolicy | Error]:
    """ Get the effective password policy

     Returns the backend-enforced password bounds and compromised-password
    screening status for the project identified by the anon key. A valid
    anon key is required, but no route-specific auth permission is needed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthPasswordPolicy | Error]
     """


    kwargs = _get_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,

) -> AuthPasswordPolicy | Error | None:
    """ Get the effective password policy

     Returns the backend-enforced password bounds and compromised-password
    screening status for the project identified by the anon key. A valid
    anon key is required, but no route-specific auth permission is needed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthPasswordPolicy | Error
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
