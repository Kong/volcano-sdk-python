from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share import Share
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    share_id: str,
    *,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/shares/{share_id}".format(share_id=quote(str(share_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Share | None:
    if response.status_code == 200:
        response_200 = Share.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Share]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | Share]:
    """ Get a deploy link

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Share]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    share_id: str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | Share | None:
    """ Get a deploy link

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Share
     """


    return sync_detailed(
        share_id=share_id,
client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | Share]:
    """ Get a deploy link

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Share]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    share_id: str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | Share | None:
    """ Get a deploy link

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Share
     """


    return (await asyncio_detailed(
        share_id=share_id,
client=client,
project_id=project_id,

    )).parsed
