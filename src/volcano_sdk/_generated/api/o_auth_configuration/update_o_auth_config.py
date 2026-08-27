from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.o_auth_config import OAuthConfig
from ...models.update_o_auth_config_provider import check_update_o_auth_config_provider
from ...models.update_o_auth_config_provider import UpdateOAuthConfigProvider
from ...models.update_o_auth_config_request import UpdateOAuthConfigRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    provider: UpdateOAuthConfigProvider,
    *,
    body: UpdateOAuthConfigRequest | Unset = UNSET,
    client_id: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["client_id"] = client_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/oauth/configs/{provider}".format(id=quote(str(id), safe=""),provider=quote(str(provider), safe=""),),
        "params": params,
    }

    
    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> OAuthConfig | None:
    if response.status_code == 200:
        response_200 = OAuthConfig.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[OAuthConfig]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    provider: UpdateOAuthConfigProvider,
    *,
    client: AuthenticatedClient,
    body: UpdateOAuthConfigRequest | Unset = UNSET,
    client_id: str | Unset = UNSET,

) -> Response[OAuthConfig]:
    """ Update OAuth configuration

    Args:
        id (UUID):
        provider (UpdateOAuthConfigProvider):
        client_id (str | Unset):
        body (UpdateOAuthConfigRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OAuthConfig]
     """


    kwargs = _get_kwargs(
        id=id,
provider=provider,
body=body,
client_id=client_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    provider: UpdateOAuthConfigProvider,
    *,
    client: AuthenticatedClient,
    body: UpdateOAuthConfigRequest | Unset = UNSET,
    client_id: str | Unset = UNSET,

) -> OAuthConfig | None:
    """ Update OAuth configuration

    Args:
        id (UUID):
        provider (UpdateOAuthConfigProvider):
        client_id (str | Unset):
        body (UpdateOAuthConfigRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OAuthConfig
     """


    return sync_detailed(
        id=id,
provider=provider,
client=client,
body=body,
client_id=client_id,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    provider: UpdateOAuthConfigProvider,
    *,
    client: AuthenticatedClient,
    body: UpdateOAuthConfigRequest | Unset = UNSET,
    client_id: str | Unset = UNSET,

) -> Response[OAuthConfig]:
    """ Update OAuth configuration

    Args:
        id (UUID):
        provider (UpdateOAuthConfigProvider):
        client_id (str | Unset):
        body (UpdateOAuthConfigRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OAuthConfig]
     """


    kwargs = _get_kwargs(
        id=id,
provider=provider,
body=body,
client_id=client_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    provider: UpdateOAuthConfigProvider,
    *,
    client: AuthenticatedClient,
    body: UpdateOAuthConfigRequest | Unset = UNSET,
    client_id: str | Unset = UNSET,

) -> OAuthConfig | None:
    """ Update OAuth configuration

    Args:
        id (UUID):
        provider (UpdateOAuthConfigProvider):
        client_id (str | Unset):
        body (UpdateOAuthConfigRequest | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OAuthConfig
     """


    return (await asyncio_detailed(
        id=id,
provider=provider,
client=client,
body=body,
client_id=client_id,

    )).parsed
