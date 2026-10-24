from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_deployment_request import CreateFrontendDeploymentRequest
from ...models.error import Error
from ...models.frontend import Frontend
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    body: CreateFrontendDeploymentRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/deployments".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Frontend | None:
    if response.status_code == 200:
        response_200 = Frontend.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Frontend]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendDeploymentRequest,

) -> Response[Error | Frontend]:
    """ Deploy an existing build to a frontend

     Deploys the build of another frontend's deployment in the same project to this frontend, without
    compiling it again. Use it to serve one build from several frontends, such as one per region or
    brand. This frontend gets its own copy of the source archive and the build, so later changes to the
    source frontend do not reach it, and a later redeploy of this frontend compiles that copied source.

    The build-time variables this frontend would build with must equal those the source build read,
    compared by name and value. Volcano records a keyed digest of each value, unique to the build, and
    never stores the values. A mismatch returns `409` with `code: build_variables_differ` and the
    differing
    names in `error`. The source deployment must be `active` or `degraded`, and both frontends must use
    the same framework and app root.

    Admission is the redeploy's: the deployment starts with `status: provisioning`, or, while another
    deployment is in progress, is exposed through `pending_deployment_id` and supersedes any older
    queued deployment. Nothing is compiled: the deployment's build minutes cover publishing the build
    alone. The checks run again when a queued deployment starts. A refusal then fails the deployment
    without a retry, its `error_message` starting with the refusal's code.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendDeploymentRequest): Deploys the build of an existing deployment
            instead of compiling the frontend's source.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendDeploymentRequest,

) -> Error | Frontend | None:
    """ Deploy an existing build to a frontend

     Deploys the build of another frontend's deployment in the same project to this frontend, without
    compiling it again. Use it to serve one build from several frontends, such as one per region or
    brand. This frontend gets its own copy of the source archive and the build, so later changes to the
    source frontend do not reach it, and a later redeploy of this frontend compiles that copied source.

    The build-time variables this frontend would build with must equal those the source build read,
    compared by name and value. Volcano records a keyed digest of each value, unique to the build, and
    never stores the values. A mismatch returns `409` with `code: build_variables_differ` and the
    differing
    names in `error`. The source deployment must be `active` or `degraded`, and both frontends must use
    the same framework and app root.

    Admission is the redeploy's: the deployment starts with `status: provisioning`, or, while another
    deployment is in progress, is exposed through `pending_deployment_id` and supersedes any older
    queued deployment. Nothing is compiled: the deployment's build minutes cover publishing the build
    alone. The checks run again when a queued deployment starts. A refusal then fails the deployment
    without a retry, its `error_message` starting with the refusal's code.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendDeploymentRequest): Deploys the build of an existing deployment
            instead of compiling the frontend's source.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendDeploymentRequest,

) -> Response[Error | Frontend]:
    """ Deploy an existing build to a frontend

     Deploys the build of another frontend's deployment in the same project to this frontend, without
    compiling it again. Use it to serve one build from several frontends, such as one per region or
    brand. This frontend gets its own copy of the source archive and the build, so later changes to the
    source frontend do not reach it, and a later redeploy of this frontend compiles that copied source.

    The build-time variables this frontend would build with must equal those the source build read,
    compared by name and value. Volcano records a keyed digest of each value, unique to the build, and
    never stores the values. A mismatch returns `409` with `code: build_variables_differ` and the
    differing
    names in `error`. The source deployment must be `active` or `degraded`, and both frontends must use
    the same framework and app root.

    Admission is the redeploy's: the deployment starts with `status: provisioning`, or, while another
    deployment is in progress, is exposed through `pending_deployment_id` and supersedes any older
    queued deployment. Nothing is compiled: the deployment's build minutes cover publishing the build
    alone. The checks run again when a queued deployment starts. A refusal then fails the deployment
    without a retry, its `error_message` starting with the refusal's code.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendDeploymentRequest): Deploys the build of an existing deployment
            instead of compiling the frontend's source.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Frontend]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFrontendDeploymentRequest,

) -> Error | Frontend | None:
    """ Deploy an existing build to a frontend

     Deploys the build of another frontend's deployment in the same project to this frontend, without
    compiling it again. Use it to serve one build from several frontends, such as one per region or
    brand. This frontend gets its own copy of the source archive and the build, so later changes to the
    source frontend do not reach it, and a later redeploy of this frontend compiles that copied source.

    The build-time variables this frontend would build with must equal those the source build read,
    compared by name and value. Volcano records a keyed digest of each value, unique to the build, and
    never stores the values. A mismatch returns `409` with `code: build_variables_differ` and the
    differing
    names in `error`. The source deployment must be `active` or `degraded`, and both frontends must use
    the same framework and app root.

    Admission is the redeploy's: the deployment starts with `status: provisioning`, or, while another
    deployment is in progress, is exposed through `pending_deployment_id` and supersedes any older
    queued deployment. Nothing is compiled: the deployment's build minutes cover publishing the build
    alone. The checks run again when a queued deployment starts. A refusal then fails the deployment
    without a retry, its `error_message` starting with the refusal's code.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendDeploymentRequest): Deploys the build of an existing deployment
            instead of compiling the frontend's source.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Frontend
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed
