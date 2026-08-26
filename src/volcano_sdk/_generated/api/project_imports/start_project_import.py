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
from ...models.project_import_start_request import ProjectImportStartRequest
from typing import cast



def _get_kwargs(
    provider: ImportProvider,
    *,
    body: ProjectImportStartRequest,
    idempotency_key: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/imports/{provider}/runs".format(provider=quote(str(provider), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectImportRun | None:
    if response.status_code == 202:
        response_202 = ProjectImportRun.from_dict(response.json())



        return response_202

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

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())



        return response_422

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectImportRun]:
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
    body: ProjectImportStartRequest,
    idempotency_key: str,

) -> Response[Error | ProjectImportRun]:
    """ Start a Vercel project import

     Creates a Volcano project from an importable production preflight report. Retrying the same request
    with the same Idempotency-Key returns the existing run.

    Args:
        provider (ImportProvider):
        idempotency_key (str):
        body (ProjectImportStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportRun]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportStartRequest,
    idempotency_key: str,

) -> Error | ProjectImportRun | None:
    """ Start a Vercel project import

     Creates a Volcano project from an importable production preflight report. Retrying the same request
    with the same Idempotency-Key returns the existing run.

    Args:
        provider (ImportProvider):
        idempotency_key (str):
        body (ProjectImportStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportRun
     """


    return sync_detailed(
        provider=provider,
client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportStartRequest,
    idempotency_key: str,

) -> Response[Error | ProjectImportRun]:
    """ Start a Vercel project import

     Creates a Volcano project from an importable production preflight report. Retrying the same request
    with the same Idempotency-Key returns the existing run.

    Args:
        provider (ImportProvider):
        idempotency_key (str):
        body (ProjectImportStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectImportRun]
     """


    kwargs = _get_kwargs(
        provider=provider,
body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient,
    body: ProjectImportStartRequest,
    idempotency_key: str,

) -> Error | ProjectImportRun | None:
    """ Start a Vercel project import

     Creates a Volcano project from an importable production preflight report. Retrying the same request
    with the same Idempotency-Key returns the existing run.

    Args:
        provider (ImportProvider):
        idempotency_key (str):
        body (ProjectImportStartRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectImportRun
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
