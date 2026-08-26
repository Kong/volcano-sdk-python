from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.batch_function_deploy_response import BatchFunctionDeployResponse
from ...models.create_functions_batch_body import CreateFunctionsBatchBody
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateFunctionsBatchBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions/batch".format(id=quote(str(id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> BatchFunctionDeployResponse | Error | None:
    if response.status_code == 202:
        response_202 = BatchFunctionDeployResponse.from_dict(response.json())



        return response_202

    if response.status_code == 207:
        response_207 = BatchFunctionDeployResponse.from_dict(response.json())



        return response_207

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[BatchFunctionDeployResponse | Error]:
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
    body: CreateFunctionsBatchBody,

) -> Response[BatchFunctionDeployResponse | Error]:
    """ Deploy multiple functions in one request

     Upload multiple function source archives in one multipart request. Each archive should contain
    source files
    plus dependency manifests/lockfiles, not installed dependency directories. ZIP and tar.gz uploads
    are
    accepted and normalized to tar.gz before storage. The API enforces `SOURCE_ARCHIVE_SIZE_LIMIT_MB`
    for each uploaded and normalized source archive. The server records a shared
    deployment batch ID for the resulting function deployments. Each function deployment runs its own
    compile/publish workflow concurrently, and each publish build enforces
    `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB`
    for the final container image.
    One batch request can include up to 100 functions. Submit multiple batch requests for larger
    projects.
    If one function fails before its workflow starts, already-started function deployments are left
    running and the failed function is reported in the `failed` array. Failed new functions are deleted;
    failed updates are rolled back to their previous metadata/status where possible.

    Args:
        id (UUID):
        body (CreateFunctionsBatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchFunctionDeployResponse | Error]
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
    body: CreateFunctionsBatchBody,

) -> BatchFunctionDeployResponse | Error | None:
    """ Deploy multiple functions in one request

     Upload multiple function source archives in one multipart request. Each archive should contain
    source files
    plus dependency manifests/lockfiles, not installed dependency directories. ZIP and tar.gz uploads
    are
    accepted and normalized to tar.gz before storage. The API enforces `SOURCE_ARCHIVE_SIZE_LIMIT_MB`
    for each uploaded and normalized source archive. The server records a shared
    deployment batch ID for the resulting function deployments. Each function deployment runs its own
    compile/publish workflow concurrently, and each publish build enforces
    `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB`
    for the final container image.
    One batch request can include up to 100 functions. Submit multiple batch requests for larger
    projects.
    If one function fails before its workflow starts, already-started function deployments are left
    running and the failed function is reported in the `failed` array. Failed new functions are deleted;
    failed updates are rolled back to their previous metadata/status where possible.

    Args:
        id (UUID):
        body (CreateFunctionsBatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchFunctionDeployResponse | Error
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
    body: CreateFunctionsBatchBody,

) -> Response[BatchFunctionDeployResponse | Error]:
    """ Deploy multiple functions in one request

     Upload multiple function source archives in one multipart request. Each archive should contain
    source files
    plus dependency manifests/lockfiles, not installed dependency directories. ZIP and tar.gz uploads
    are
    accepted and normalized to tar.gz before storage. The API enforces `SOURCE_ARCHIVE_SIZE_LIMIT_MB`
    for each uploaded and normalized source archive. The server records a shared
    deployment batch ID for the resulting function deployments. Each function deployment runs its own
    compile/publish workflow concurrently, and each publish build enforces
    `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB`
    for the final container image.
    One batch request can include up to 100 functions. Submit multiple batch requests for larger
    projects.
    If one function fails before its workflow starts, already-started function deployments are left
    running and the failed function is reported in the `failed` array. Failed new functions are deleted;
    failed updates are rolled back to their previous metadata/status where possible.

    Args:
        id (UUID):
        body (CreateFunctionsBatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[BatchFunctionDeployResponse | Error]
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
    body: CreateFunctionsBatchBody,

) -> BatchFunctionDeployResponse | Error | None:
    """ Deploy multiple functions in one request

     Upload multiple function source archives in one multipart request. Each archive should contain
    source files
    plus dependency manifests/lockfiles, not installed dependency directories. ZIP and tar.gz uploads
    are
    accepted and normalized to tar.gz before storage. The API enforces `SOURCE_ARCHIVE_SIZE_LIMIT_MB`
    for each uploaded and normalized source archive. The server records a shared
    deployment batch ID for the resulting function deployments. Each function deployment runs its own
    compile/publish workflow concurrently, and each publish build enforces
    `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB`
    for the final container image.
    One batch request can include up to 100 functions. Submit multiple batch requests for larger
    projects.
    If one function fails before its workflow starts, already-started function deployments are left
    running and the failed function is reported in the `failed` array. Failed new functions are deleted;
    failed updates are rolled back to their previous metadata/status where possible.

    Args:
        id (UUID):
        body (CreateFunctionsBatchBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        BatchFunctionDeployResponse | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
