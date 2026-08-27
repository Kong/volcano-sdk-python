from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.auth_config import AuthConfig
from ...models.error import Error
from ...models.update_auth_config_request import UpdateAuthConfigRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: UpdateAuthConfigRequest | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/auth/config".format(id=quote(str(id), safe=""),),
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AuthConfig | Error | None:
    if response.status_code == 200:
        response_200 = AuthConfig.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AuthConfig | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateAuthConfigRequest | Unset = UNSET,

) -> Response[AuthConfig | Error]:
    """ Update auth configuration

     Updates the project's auth configuration. Only the fields present in
    the body are changed.

    Args:
        id (UUID):
        body (UpdateAuthConfigRequest | Unset): All fields optional - only include fields you want
            to update. Validation rule: require_email_confirmation=true requires email_enabled=true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthConfig | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateAuthConfigRequest | Unset = UNSET,

) -> AuthConfig | Error | None:
    """ Update auth configuration

     Updates the project's auth configuration. Only the fields present in
    the body are changed.

    Args:
        id (UUID):
        body (UpdateAuthConfigRequest | Unset): All fields optional - only include fields you want
            to update. Validation rule: require_email_confirmation=true requires email_enabled=true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthConfig | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateAuthConfigRequest | Unset = UNSET,

) -> Response[AuthConfig | Error]:
    """ Update auth configuration

     Updates the project's auth configuration. Only the fields present in
    the body are changed.

    Args:
        id (UUID):
        body (UpdateAuthConfigRequest | Unset): All fields optional - only include fields you want
            to update. Validation rule: require_email_confirmation=true requires email_enabled=true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AuthConfig | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: UpdateAuthConfigRequest | Unset = UNSET,

) -> AuthConfig | Error | None:
    """ Update auth configuration

     Updates the project's auth configuration. Only the fields present in
    the body are changed.

    Args:
        id (UUID):
        body (UpdateAuthConfigRequest | Unset): All fields optional - only include fields you want
            to update. Validation rule: require_email_confirmation=true requires email_enabled=true.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AuthConfig | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
