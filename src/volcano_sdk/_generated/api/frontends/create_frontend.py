from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_body import CreateFrontendBody
from ...models.error import Error
from ...models.frontend import Frontend
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateFrontendBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends".format(id=quote(str(id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Frontend | None:
    if response.status_code == 200:
        response_200 = Frontend.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = Frontend.from_dict(response.json())



        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Frontend]:
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
    body: CreateFrontendBody,

) -> Response[Error | Frontend]:
    """ Create a new frontend deployment

     Creates and deploys a frontend for the project.
    If a frontend with the same name already exists in the project, this operation updates that
    frontend using the uploaded archive and starts a new deployment. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. If another deployment is running, the response preserves the frontend's current status
    and exposes the queued deployment through `pending_deployment_id`.
    Existing frontend traffic continues to use an available runtime while the new deployment builds
    and provisions. Each deployment publishes its own static assets before the runtimes switch to its
    build, and the live build's assets keep serving until the new deployment is live, so a page loaded
    mid-deployment resolves its assets whichever build served it. A failed redeploy puts the runtimes
    back on the build they were running, leaves the frontend `active` on the previous deployment, and
    records the attempted deployment as failed. `degraded` means the runtime remains available but
    edge synchronization requires recovery; Volcano retries the edge step without rebuilding. Only one
    deployment may run for a
    given frontend, while independent frontends and projects can deploy concurrently.
    For monorepos, provide `app_root` as a relative path from the uploaded archive root
    to the Next.js app that should be built. Omit it for single-app archives.
    Supported frontend environments are Next.js 15.x and 16.x with Node.js
    22.x or 24.x. The Node.js runtime is inferred from
    `package.json` `engines.node`; if omitted, Volcano uses Node.js 22.x.
    The selected Node.js family must also satisfy the installed Next.js package's
    `engines.node` constraint. Volcano tests Next 15.5.24 (`^18.18.0 || ^19.8.0 || >=20.0.0`) and Next
    16.3.3 (`>=20.9.0`).
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container images are
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    This operation is limited by plan-based frontend deployment quotas (`FREE_FRONTEND_DEPLOYMENTS`,
    `PRO_FRONTEND_DEPLOYMENTS`).
    Each project can contain up to 10,000 frontends regardless of plan.

    Args:
        id (UUID):
        body (CreateFrontendBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
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
    body: CreateFrontendBody,

) -> Error | Frontend | None:
    """ Create a new frontend deployment

     Creates and deploys a frontend for the project.
    If a frontend with the same name already exists in the project, this operation updates that
    frontend using the uploaded archive and starts a new deployment. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. If another deployment is running, the response preserves the frontend's current status
    and exposes the queued deployment through `pending_deployment_id`.
    Existing frontend traffic continues to use an available runtime while the new deployment builds
    and provisions. Each deployment publishes its own static assets before the runtimes switch to its
    build, and the live build's assets keep serving until the new deployment is live, so a page loaded
    mid-deployment resolves its assets whichever build served it. A failed redeploy puts the runtimes
    back on the build they were running, leaves the frontend `active` on the previous deployment, and
    records the attempted deployment as failed. `degraded` means the runtime remains available but
    edge synchronization requires recovery; Volcano retries the edge step without rebuilding. Only one
    deployment may run for a
    given frontend, while independent frontends and projects can deploy concurrently.
    For monorepos, provide `app_root` as a relative path from the uploaded archive root
    to the Next.js app that should be built. Omit it for single-app archives.
    Supported frontend environments are Next.js 15.x and 16.x with Node.js
    22.x or 24.x. The Node.js runtime is inferred from
    `package.json` `engines.node`; if omitted, Volcano uses Node.js 22.x.
    The selected Node.js family must also satisfy the installed Next.js package's
    `engines.node` constraint. Volcano tests Next 15.5.24 (`^18.18.0 || ^19.8.0 || >=20.0.0`) and Next
    16.3.3 (`>=20.9.0`).
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container images are
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    This operation is limited by plan-based frontend deployment quotas (`FREE_FRONTEND_DEPLOYMENTS`,
    `PRO_FRONTEND_DEPLOYMENTS`).
    Each project can contain up to 10,000 frontends regardless of plan.

    Args:
        id (UUID):
        body (CreateFrontendBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
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
    body: CreateFrontendBody,

) -> Response[Error | Frontend]:
    """ Create a new frontend deployment

     Creates and deploys a frontend for the project.
    If a frontend with the same name already exists in the project, this operation updates that
    frontend using the uploaded archive and starts a new deployment. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. If another deployment is running, the response preserves the frontend's current status
    and exposes the queued deployment through `pending_deployment_id`.
    Existing frontend traffic continues to use an available runtime while the new deployment builds
    and provisions. Each deployment publishes its own static assets before the runtimes switch to its
    build, and the live build's assets keep serving until the new deployment is live, so a page loaded
    mid-deployment resolves its assets whichever build served it. A failed redeploy puts the runtimes
    back on the build they were running, leaves the frontend `active` on the previous deployment, and
    records the attempted deployment as failed. `degraded` means the runtime remains available but
    edge synchronization requires recovery; Volcano retries the edge step without rebuilding. Only one
    deployment may run for a
    given frontend, while independent frontends and projects can deploy concurrently.
    For monorepos, provide `app_root` as a relative path from the uploaded archive root
    to the Next.js app that should be built. Omit it for single-app archives.
    Supported frontend environments are Next.js 15.x and 16.x with Node.js
    22.x or 24.x. The Node.js runtime is inferred from
    `package.json` `engines.node`; if omitted, Volcano uses Node.js 22.x.
    The selected Node.js family must also satisfy the installed Next.js package's
    `engines.node` constraint. Volcano tests Next 15.5.24 (`^18.18.0 || ^19.8.0 || >=20.0.0`) and Next
    16.3.3 (`>=20.9.0`).
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container images are
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    This operation is limited by plan-based frontend deployment quotas (`FREE_FRONTEND_DEPLOYMENTS`,
    `PRO_FRONTEND_DEPLOYMENTS`).
    Each project can contain up to 10,000 frontends regardless of plan.

    Args:
        id (UUID):
        body (CreateFrontendBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
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
    body: CreateFrontendBody,

) -> Error | Frontend | None:
    """ Create a new frontend deployment

     Creates and deploys a frontend for the project.
    If a frontend with the same name already exists in the project, this operation updates that
    frontend using the uploaded archive and starts a new deployment. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`, `degraded`, or
    `failed`. If another deployment is running, the response preserves the frontend's current status
    and exposes the queued deployment through `pending_deployment_id`.
    Existing frontend traffic continues to use an available runtime while the new deployment builds
    and provisions. Each deployment publishes its own static assets before the runtimes switch to its
    build, and the live build's assets keep serving until the new deployment is live, so a page loaded
    mid-deployment resolves its assets whichever build served it. A failed redeploy puts the runtimes
    back on the build they were running, leaves the frontend `active` on the previous deployment, and
    records the attempted deployment as failed. `degraded` means the runtime remains available but
    edge synchronization requires recovery; Volcano retries the edge step without rebuilding. Only one
    deployment may run for a
    given frontend, while independent frontends and projects can deploy concurrently.
    For monorepos, provide `app_root` as a relative path from the uploaded archive root
    to the Next.js app that should be built. Omit it for single-app archives.
    Supported frontend environments are Next.js 15.x and 16.x with Node.js
    22.x or 24.x. The Node.js runtime is inferred from
    `package.json` `engines.node`; if omitted, Volcano uses Node.js 22.x.
    The selected Node.js family must also satisfy the installed Next.js package's
    `engines.node` constraint. Volcano tests Next 15.5.24 (`^18.18.0 || ^19.8.0 || >=20.0.0`) and Next
    16.3.3 (`>=20.9.0`).
    Source archive size is enforced by the API with `SOURCE_ARCHIVE_SIZE_LIMIT_MB`; the CLI
    does not apply its own source archive size limit. After the final container images are
    built, the publish build enforces `LAMBDA_TARGET_CONTAINER_SIZE_LIMIT_MB` before pushing.
    This operation is limited by plan-based frontend deployment quotas (`FREE_FRONTEND_DEPLOYMENTS`,
    `PRO_FRONTEND_DEPLOYMENTS`).
    Each project can contain up to 10,000 frontends regardless of plan.

    Args:
        id (UUID):
        body (CreateFrontendBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
