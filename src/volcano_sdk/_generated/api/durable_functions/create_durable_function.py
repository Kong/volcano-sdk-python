from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_durable_function_body import CreateDurableFunctionBody
from ...models.durable_function import DurableFunction
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: CreateDurableFunctionBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/durable-functions".format(id=quote(str(id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DurableFunction | Error | None:
    if response.status_code == 200:
        response_200 = DurableFunction.from_dict(response.json())



        return response_200

    if response.status_code == 201:
        response_201 = DurableFunction.from_dict(response.json())



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

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DurableFunction | Error]:
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
    body: CreateDurableFunctionBody,

) -> Response[DurableFunction | Error]:
    """ Create or update a durable function

     Upload a durable function source bundle. Creates the function on the
    first call for a name and redeploys it on every call after that, the
    same create-or-update contract `POST /projects/{id}/functions` has.

    Volcano builds and deploys asynchronously. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`
    or `failed`; a deployment that has to wait for a running one is exposed
    through `pending_deployment_id`. Existing executions keep running
    against the runtime they started on.

    The `durable` configuration is derived from the project's plan rather
    than supplied here, and is fixed once the function exists. A name
    already held by a standard function is rejected with 409: a function
    cannot change kind.

    Args:
        id (UUID):
        body (CreateDurableFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableFunction | Error]
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
    body: CreateDurableFunctionBody,

) -> DurableFunction | Error | None:
    """ Create or update a durable function

     Upload a durable function source bundle. Creates the function on the
    first call for a name and redeploys it on every call after that, the
    same create-or-update contract `POST /projects/{id}/functions` has.

    Volcano builds and deploys asynchronously. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`
    or `failed`; a deployment that has to wait for a running one is exposed
    through `pending_deployment_id`. Existing executions keep running
    against the runtime they started on.

    The `durable` configuration is derived from the project's plan rather
    than supplied here, and is fixed once the function exists. A name
    already held by a standard function is rejected with 409: a function
    cannot change kind.

    Args:
        id (UUID):
        body (CreateDurableFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableFunction | Error
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
    body: CreateDurableFunctionBody,

) -> Response[DurableFunction | Error]:
    """ Create or update a durable function

     Upload a durable function source bundle. Creates the function on the
    first call for a name and redeploys it on every call after that, the
    same create-or-update contract `POST /projects/{id}/functions` has.

    Volcano builds and deploys asynchronously. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`
    or `failed`; a deployment that has to wait for a running one is exposed
    through `pending_deployment_id`. Existing executions keep running
    against the runtime they started on.

    The `durable` configuration is derived from the project's plan rather
    than supplied here, and is fixed once the function exists. A name
    already held by a standard function is rejected with 409: a function
    cannot change kind.

    Args:
        id (UUID):
        body (CreateDurableFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DurableFunction | Error]
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
    body: CreateDurableFunctionBody,

) -> DurableFunction | Error | None:
    """ Create or update a durable function

     Upload a durable function source bundle. Creates the function on the
    first call for a name and redeploys it on every call after that, the
    same create-or-update contract `POST /projects/{id}/functions` has.

    Volcano builds and deploys asynchronously. A deployment that starts
    immediately returns `status: provisioning`, then transitions to `active`
    or `failed`; a deployment that has to wait for a running one is exposed
    through `pending_deployment_id`. Existing executions keep running
    against the runtime they started on.

    The `durable` configuration is derived from the project's plan rather
    than supplied here, and is fixed once the function exists. A name
    already held by a standard function is rejected with 409: a function
    cannot change kind.

    Args:
        id (UUID):
        body (CreateDurableFunctionBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DurableFunction | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
