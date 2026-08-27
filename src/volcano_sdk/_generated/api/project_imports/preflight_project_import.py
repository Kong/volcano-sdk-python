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
from ...models.project_import_preflight_request import ProjectImportPreflightRequest
from ...models.project_import_report import ProjectImportReport
from typing import cast



def _get_kwargs(
    provider: ImportProvider,
    *,
    body: ProjectImportPreflightRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/imports/{provider}/preflight".format(provider=quote(str(provider), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectImportReport | None:
    if response.status_code == 200:
        response_200 = ProjectImportReport.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectImportReport]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportPreflightRequest,

) -> Response[Error | ProjectImportReport]:
    """ Check whether a provider project is ready to import

     Produces a deterministic read-only readiness report for a proposed new Volcano project.

    Args:
        provider (ImportProvider):
        body (ProjectImportPreflightRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportReport]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportPreflightRequest,

) -> Error | ProjectImportReport | None:
    """ Check whether a provider project is ready to import

     Produces a deterministic read-only readiness report for a proposed new Volcano project.

    Args:
        provider (ImportProvider):
        body (ProjectImportPreflightRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportReport
     """


    return sync_detailed(
        provider=provider,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportPreflightRequest,

) -> Response[Error | ProjectImportReport]:
    """ Check whether a provider project is ready to import

     Produces a deterministic read-only readiness report for a proposed new Volcano project.

    Args:
        provider (ImportProvider):
        body (ProjectImportPreflightRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportReport]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportPreflightRequest,

) -> Error | ProjectImportReport | None:
    """ Check whether a provider project is ready to import

     Produces a deterministic read-only readiness report for a proposed new Volcano project.

    Args:
        provider (ImportProvider):
        body (ProjectImportPreflightRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportReport
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
body=body,

    )).parsed
