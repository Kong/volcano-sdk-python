from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.import_provider import check_import_provider
from ...models.import_provider import ImportProvider
from ...models.project_import_run import ProjectImportRun
from typing import cast
from uuid import UUID



def _get_kwargs(
    provider: ImportProvider,
    run_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/imports/{provider}/runs/{run_id}".format(provider=quote(str(provider), safe=""),run_id=quote(str(run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectImportRun | None:
    if response.status_code == 200:
        response_200 = ProjectImportRun.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectImportRun]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: ImportProvider,
    run_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectImportRun]:
    """ Get a project import run

    Args:
        provider (ImportProvider):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportRun]
     """


    kwargs = _get_kwargs(
        provider=provider,
run_id=run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: ImportProvider,
    run_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectImportRun | None:
    """ Get a project import run

    Args:
        provider (ImportProvider):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportRun
     """


    return sync_detailed(
        provider=provider,
run_id=run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    provider: ImportProvider,
    run_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Response[Error | ProjectImportRun]:
    """ Get a project import run

    Args:
        provider (ImportProvider):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportRun]
     """


    kwargs = _get_kwargs(
        provider=provider,
run_id=run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: ImportProvider,
    run_id: UUID,
    *,
    client: AuthenticatedClient,

) -> Error | ProjectImportRun | None:
    """ Get a project import run

    Args:
        provider (ImportProvider):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportRun
     """


    return (await asyncio_detailed(
        provider=provider,
run_id=run_id,
client=client,

    )).parsed
