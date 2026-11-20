from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.shares_response import SharesResponse
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    project_id: UUID | str,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/shares",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SharesResponse | None:
    if response.status_code == 200:
        response_200 = SharesResponse.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SharesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | SharesResponse]:
    """ List a project's deploy links

     Deploy links let anyone deploy a release the project's owner published as
    their own new project. A link's public address is
    `https://volcano.dev/deploy/<id>`; the address carries no release, so it
    cannot be edited to point at other code.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SharesResponse]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | SharesResponse | None:
    """ List a project's deploy links

     Deploy links let anyone deploy a release the project's owner published as
    their own new project. A link's public address is
    `https://volcano.dev/deploy/<id>`; the address carries no release, so it
    cannot be edited to point at other code.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SharesResponse
     """


    return sync_detailed(
        client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Response[Error | SharesResponse]:
    """ List a project's deploy links

     Deploy links let anyone deploy a release the project's owner published as
    their own new project. A link's public address is
    `https://volcano.dev/deploy/<id>`; the address carries no release, so it
    cannot be edited to point at other code.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SharesResponse]
     """


    kwargs = request_kwargs(
        project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    project_id: UUID | str,

) -> Error | SharesResponse | None:
    """ List a project's deploy links

     Deploy links let anyone deploy a release the project's owner published as
    their own new project. A link's public address is
    `https://volcano.dev/deploy/<id>`; the address carries no release, so it
    cannot be edited to point at other code.

    Args:
        project_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SharesResponse
     """


    return (await asyncio_detailed(
        client=client,
project_id=project_id,

    )).parsed
