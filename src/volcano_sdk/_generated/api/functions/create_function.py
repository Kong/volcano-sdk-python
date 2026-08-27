from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_function_body import CreateFunctionBody
from ...models.error import Error
from ...models.function import Function
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateFunctionBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions".format(id=quote(str(id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Function | None:
    if response.status_code == 200:
        response_200 = Function.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = Function.from_dict(response.json())



        return response_201

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Function]:
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
    body: CreateFunctionBody,

) -> Response[Error | Function]:
    """ Create or update function code

     Upload a serverless function source bundle. Direct API clients may send the function code
    as a ZIP or tar.gz archive via multipart/form-data. The API stores a normalized tar.gz
    source archive.
    Cloud deploys should include source files and dependency manifests/lockfiles, not installed
    dependency directories. Volcano installs Node.js, Python, and Ruby dependencies during the
    function compile build.
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container image is
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    Uploaded source archives cannot contain symlink entries. Safe symlinks created during
    the cloud build are materialized before publish.
    Volcano builds and deploys the function asynchronously after upload. A deployment that starts
    immediately returns a Function resource with `status: provisioning`, then transitions to
    `active` or `failed`. If another deployment is running, the response preserves the resource's
    current status and exposes the queued deployment through `pending_deployment_id`.
    Existing function traffic continues to use the last known-good runtime during an update. A failed
    update keeps that runtime available and records the attempted deployment as failed.
    Only one deployment runs for a given function. A newer request supersedes any queued request
    and starts after the running deployment. Different functions and projects deploy concurrently.
    If a function with the same name already exists in the project, this operation updates that
    function's runtime, handler, and source bundle and returns `200 OK`.
    Each project can contain up to 10,000 functions. Creating a new function over this cap returns 403.

    Args:
        id (UUID):
        body (CreateFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Function]
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
    body: CreateFunctionBody,

) -> Error | Function | None:
    """ Create or update function code

     Upload a serverless function source bundle. Direct API clients may send the function code
    as a ZIP or tar.gz archive via multipart/form-data. The API stores a normalized tar.gz
    source archive.
    Cloud deploys should include source files and dependency manifests/lockfiles, not installed
    dependency directories. Volcano installs Node.js, Python, and Ruby dependencies during the
    function compile build.
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container image is
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    Uploaded source archives cannot contain symlink entries. Safe symlinks created during
    the cloud build are materialized before publish.
    Volcano builds and deploys the function asynchronously after upload. A deployment that starts
    immediately returns a Function resource with `status: provisioning`, then transitions to
    `active` or `failed`. If another deployment is running, the response preserves the resource's
    current status and exposes the queued deployment through `pending_deployment_id`.
    Existing function traffic continues to use the last known-good runtime during an update. A failed
    update keeps that runtime available and records the attempted deployment as failed.
    Only one deployment runs for a given function. A newer request supersedes any queued request
    and starts after the running deployment. Different functions and projects deploy concurrently.
    If a function with the same name already exists in the project, this operation updates that
    function's runtime, handler, and source bundle and returns `200 OK`.
    Each project can contain up to 10,000 functions. Creating a new function over this cap returns 403.

    Args:
        id (UUID):
        body (CreateFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Function
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
    body: CreateFunctionBody,

) -> Response[Error | Function]:
    """ Create or update function code

     Upload a serverless function source bundle. Direct API clients may send the function code
    as a ZIP or tar.gz archive via multipart/form-data. The API stores a normalized tar.gz
    source archive.
    Cloud deploys should include source files and dependency manifests/lockfiles, not installed
    dependency directories. Volcano installs Node.js, Python, and Ruby dependencies during the
    function compile build.
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container image is
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    Uploaded source archives cannot contain symlink entries. Safe symlinks created during
    the cloud build are materialized before publish.
    Volcano builds and deploys the function asynchronously after upload. A deployment that starts
    immediately returns a Function resource with `status: provisioning`, then transitions to
    `active` or `failed`. If another deployment is running, the response preserves the resource's
    current status and exposes the queued deployment through `pending_deployment_id`.
    Existing function traffic continues to use the last known-good runtime during an update. A failed
    update keeps that runtime available and records the attempted deployment as failed.
    Only one deployment runs for a given function. A newer request supersedes any queued request
    and starts after the running deployment. Different functions and projects deploy concurrently.
    If a function with the same name already exists in the project, this operation updates that
    function's runtime, handler, and source bundle and returns `200 OK`.
    Each project can contain up to 10,000 functions. Creating a new function over this cap returns 403.

    Args:
        id (UUID):
        body (CreateFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Function]
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
    body: CreateFunctionBody,

) -> Error | Function | None:
    """ Create or update function code

     Upload a serverless function source bundle. Direct API clients may send the function code
    as a ZIP or tar.gz archive via multipart/form-data. The API stores a normalized tar.gz
    source archive.
    Cloud deploys should include source files and dependency manifests/lockfiles, not installed
    dependency directories. Volcano installs Node.js, Python, and Ruby dependencies during the
    function compile build.
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container image is
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    Uploaded source archives cannot contain symlink entries. Safe symlinks created during
    the cloud build are materialized before publish.
    Volcano builds and deploys the function asynchronously after upload. A deployment that starts
    immediately returns a Function resource with `status: provisioning`, then transitions to
    `active` or `failed`. If another deployment is running, the response preserves the resource's
    current status and exposes the queued deployment through `pending_deployment_id`.
    Existing function traffic continues to use the last known-good runtime during an update. A failed
    update keeps that runtime available and records the attempted deployment as failed.
    Only one deployment runs for a given function. A newer request supersedes any queued request
    and starts after the running deployment. Different functions and projects deploy concurrently.
    If a function with the same name already exists in the project, this operation updates that
    function's runtime, handler, and source bundle and returns `200 OK`.
    Each project can contain up to 10,000 functions. Creating a new function over this cap returns 403.

    Args:
        id (UUID):
        body (CreateFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Function
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
