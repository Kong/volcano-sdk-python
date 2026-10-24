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
        "method": "get",
        "url": "/projects/{id}/autofix".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AutofixSettings | Error | None:
    if response.status_code == 200:
        response_200 = AutofixSettings.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

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
    """ Get autofix settings

     Returns whether Volcano diagnoses the project's issues with AI and how
    far a run may go. A project that never saved settings returns the
    defaults, with autofix off.

    Where autofix is not available, saved settings stay readable. A project
    that never saved any answers `404` with code `feature_unavailable`.

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
    """ Get autofix settings

     Returns whether Volcano diagnoses the project's issues with AI and how
    far a run may go. A project that never saved settings returns the
    defaults, with autofix off.

    Where autofix is not available, saved settings stay readable. A project
    that never saved any answers `404` with code `feature_unavailable`.

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
    """ Get autofix settings

     Returns whether Volcano diagnoses the project's issues with AI and how
    far a run may go. A project that never saved settings returns the
    defaults, with autofix off.

    Where autofix is not available, saved settings stay readable. A project
    that never saved any answers `404` with code `feature_unavailable`.

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
    """ Get autofix settings

     Returns whether Volcano diagnoses the project's issues with AI and how
    far a run may go. A project that never saved settings returns the
    defaults, with autofix off.

    Where autofix is not available, saved settings stay readable. A project
    that never saved any answers `404` with code `feature_unavailable`.

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
