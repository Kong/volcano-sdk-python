from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend_serving import FrontendServing
from ...models.rollback_frontend_serving_body import RollbackFrontendServingBody
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    body: RollbackFrontendServingBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/serving/rollback".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendServing | None:
    if response.status_code == 200:
        response_200 = FrontendServing.from_dict(response.json())



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

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendServing]:
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
    body: RollbackFrontendServingBody,

) -> Response[Error | FrontendServing]:
    """ Roll a frontend back to the runtime it served before

     Returns the frontend's traffic to the runtime it served before the last activation, or to its
    own runtime with `to_production`. A rollback is a new activation, so what it leaves becomes the
    runtime a further rollback returns to, and it can itself be undone. It names the revision the
    caller read; a competing activation makes it fail with `409`.

    Rolling back to a Candidate promotes it again and is refused with `409` when promoting it would
    be. Rolling back to the frontend's own runtime is not.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (RollbackFrontendServingBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendServing]
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
    body: RollbackFrontendServingBody,

) -> Error | FrontendServing | None:
    """ Roll a frontend back to the runtime it served before

     Returns the frontend's traffic to the runtime it served before the last activation, or to its
    own runtime with `to_production`. A rollback is a new activation, so what it leaves becomes the
    runtime a further rollback returns to, and it can itself be undone. It names the revision the
    caller read; a competing activation makes it fail with `409`.

    Rolling back to a Candidate promotes it again and is refused with `409` when promoting it would
    be. Rolling back to the frontend's own runtime is not.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (RollbackFrontendServingBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendServing
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
    body: RollbackFrontendServingBody,

) -> Response[Error | FrontendServing]:
    """ Roll a frontend back to the runtime it served before

     Returns the frontend's traffic to the runtime it served before the last activation, or to its
    own runtime with `to_production`. A rollback is a new activation, so what it leaves becomes the
    runtime a further rollback returns to, and it can itself be undone. It names the revision the
    caller read; a competing activation makes it fail with `409`.

    Rolling back to a Candidate promotes it again and is refused with `409` when promoting it would
    be. Rolling back to the frontend's own runtime is not.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (RollbackFrontendServingBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendServing]
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
    body: RollbackFrontendServingBody,

) -> Error | FrontendServing | None:
    """ Roll a frontend back to the runtime it served before

     Returns the frontend's traffic to the runtime it served before the last activation, or to its
    own runtime with `to_production`. A rollback is a new activation, so what it leaves becomes the
    runtime a further rollback returns to, and it can itself be undone. It names the revision the
    caller read; a competing activation makes it fail with `409`.

    Rolling back to a Candidate promotes it again and is refused with `409` when promoting it would
    be. Rolling back to the frontend's own runtime is not.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (RollbackFrontendServingBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendServing
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed
