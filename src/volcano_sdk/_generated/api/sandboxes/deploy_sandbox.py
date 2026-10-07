from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.deploy_sandbox_body import DeploySandboxBody
from ...models.error import Error
from ...models.sandbox_deployment import SandboxDeployment
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    body: DeploySandboxBody,
    idempotency_key: UUID | str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    headers["Idempotency-Key"] = str(idempotency_key)







    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/sandboxes/{sandbox_id}/deployments".format(id=quote(str(id), safe=""),sandbox_id=quote(str(sandbox_id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SandboxDeployment:
    if response.status_code == 202:
        response_202 = SandboxDeployment.from_dict(response.json())



        return response_202

    response_default = Error.from_dict(response.json())



    return response_default



def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SandboxDeployment]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DeploySandboxBody,
    idempotency_key: UUID | str,

) -> Response[Error | SandboxDeployment]:
    """ Build and deploy a custom sandbox template

     Upload a tar.gz context with a Dockerfile. The template ID may be new. Retries with the same
    Idempotency-Key and content return the same deployment. Existing sessions retain their image while
    the replacement builds and validates.

    Args:
        id (UUID):
        sandbox_id (UUID):
        idempotency_key (UUID):
        body (DeploySandboxBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeployment]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DeploySandboxBody,
    idempotency_key: UUID | str,

) -> Error | SandboxDeployment | None:
    """ Build and deploy a custom sandbox template

     Upload a tar.gz context with a Dockerfile. The template ID may be new. Retries with the same
    Idempotency-Key and content return the same deployment. Existing sessions retain their image while
    the replacement builds and validates.

    Args:
        id (UUID):
        sandbox_id (UUID):
        idempotency_key (UUID):
        body (DeploySandboxBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeployment
     """


    return sync_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DeploySandboxBody,
    idempotency_key: UUID | str,

) -> Response[Error | SandboxDeployment]:
    """ Build and deploy a custom sandbox template

     Upload a tar.gz context with a Dockerfile. The template ID may be new. Retries with the same
    Idempotency-Key and content return the same deployment. Existing sessions retain their image while
    the replacement builds and validates.

    Args:
        id (UUID):
        sandbox_id (UUID):
        idempotency_key (UUID):
        body (DeploySandboxBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SandboxDeployment]
     """


    kwargs = request_kwargs(
        id=id,
sandbox_id=sandbox_id,
body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    sandbox_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: DeploySandboxBody,
    idempotency_key: UUID | str,

) -> Error | SandboxDeployment | None:
    """ Build and deploy a custom sandbox template

     Upload a tar.gz context with a Dockerfile. The template ID may be new. Retries with the same
    Idempotency-Key and content return the same deployment. Existing sessions retain their image while
    the replacement builds and validates.

    Args:
        id (UUID):
        sandbox_id (UUID):
        idempotency_key (UUID):
        body (DeploySandboxBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SandboxDeployment
     """


    return (await asyncio_detailed(
        id=id,
sandbox_id=sandbox_id,
client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
