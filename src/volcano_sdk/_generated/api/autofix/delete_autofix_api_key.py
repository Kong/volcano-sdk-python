from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.autofix_settings import AutofixSettings
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": "/projects/{id}/autofix/api-key".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AutofixSettings | Error | None:
    if response.status_code == 200:
        response_200 = AutofixSettings.from_dict(response.json())



        return response_200

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AutofixSettings | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixSettings | Error]:
    """ Delete the API key

     Deletes the project's stored API key and returns the settings. Autofix
    on the key's provider runs on that key, so it turns off; on another
    provider it stays as it is. Deleting when no key is stored succeeds.

    Turning autofix off or switching providers never deletes the key, and
    neither does applying a project configuration. This works where
    autofix is not available, for a project that saved settings.

    Project access tokens are refused.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixSettings | Error]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixSettings | Error | None:
    """ Delete the API key

     Deletes the project's stored API key and returns the settings. Autofix
    on the key's provider runs on that key, so it turns off; on another
    provider it stays as it is. Deleting when no key is stored succeeds.

    Turning autofix off or switching providers never deletes the key, and
    neither does applying a project configuration. This works where
    autofix is not available, for a project that saved settings.

    Project access tokens are refused.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixSettings | Error
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixSettings | Error]:
    """ Delete the API key

     Deletes the project's stored API key and returns the settings. Autofix
    on the key's provider runs on that key, so it turns off; on another
    provider it stays as it is. Deleting when no key is stored succeeds.

    Turning autofix off or switching providers never deletes the key, and
    neither does applying a project configuration. This works where
    autofix is not available, for a project that saved settings.

    Project access tokens are refused.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixSettings | Error]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixSettings | Error | None:
    """ Delete the API key

     Deletes the project's stored API key and returns the settings. Autofix
    on the key's provider runs on that key, so it turns off; on another
    provider it stays as it is. Deleting when no key is stored succeeds.

    Turning autofix off or switching providers never deletes the key, and
    neither does applying a project configuration. This works where
    autofix is not available, for a project that saved settings.

    Project access tokens are refused.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixSettings | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
