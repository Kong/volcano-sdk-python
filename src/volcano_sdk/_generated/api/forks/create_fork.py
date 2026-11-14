from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.fork_create_request import ForkCreateRequest
from ...models.project import Project
from ...types import UNSET, Unset
from typing import cast



def request_kwargs(
    *,
    body: ForkCreateRequest,
    idempotency_key: str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}
    if not isinstance(idempotency_key, Unset):
        headers["Idempotency-Key"] = idempotency_key



    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/forks",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Project | None:
    if response.status_code == 201:
        response_201 = Project.from_dict(response.json())



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

    if response.status_code == 422:
        response_422 = Error.from_dict(response.json())



        return response_422

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 451:
        response_451 = Error.from_dict(response.json())



        return response_451

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Project]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ForkCreateRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[Error | Project]:
    """ Fork a share into a project of your own

     Creates a project in the caller's account from the release a share offers,
    and queues its install: the release's functions and frontends, never the
    owner's data, variable values, keys or sign-in settings. Every variable the
    release declares is created; one the visitor gives no value for is created
    empty. Installation is asynchronous: poll the project until
    `template_installation.status` is `ready`. A `201` without
    `template_installation` means nothing is being installed.

    The fork is checked against what the release recorded when it was published
    (its functions, frontends and variables, and the plan's room for them); the
    release's archive is read and checked by the install. A stored archive that
    fails those checks fails the install with `failure_code` `source_invalid`
    rather than refusing the request.

    Send the `release_id` that `GET /share-previews/{share_id}` returned. If the
    share moved to a new release since, nothing is created and the answer is
    `409` with code `release_changed`.

    Args:
        idempotency_key (str | Unset):
        body (ForkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Project]
     """


    kwargs = request_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: ForkCreateRequest,
    idempotency_key: str | Unset = UNSET,

) -> Error | Project | None:
    """ Fork a share into a project of your own

     Creates a project in the caller's account from the release a share offers,
    and queues its install: the release's functions and frontends, never the
    owner's data, variable values, keys or sign-in settings. Every variable the
    release declares is created; one the visitor gives no value for is created
    empty. Installation is asynchronous: poll the project until
    `template_installation.status` is `ready`. A `201` without
    `template_installation` means nothing is being installed.

    The fork is checked against what the release recorded when it was published
    (its functions, frontends and variables, and the plan's room for them); the
    release's archive is read and checked by the install. A stored archive that
    fails those checks fails the install with `failure_code` `source_invalid`
    rather than refusing the request.

    Send the `release_id` that `GET /share-previews/{share_id}` returned. If the
    share moved to a new release since, nothing is created and the answer is
    `409` with code `release_changed`.

    Args:
        idempotency_key (str | Unset):
        body (ForkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Project
     """


    return sync_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ForkCreateRequest,
    idempotency_key: str | Unset = UNSET,

) -> Response[Error | Project]:
    """ Fork a share into a project of your own

     Creates a project in the caller's account from the release a share offers,
    and queues its install: the release's functions and frontends, never the
    owner's data, variable values, keys or sign-in settings. Every variable the
    release declares is created; one the visitor gives no value for is created
    empty. Installation is asynchronous: poll the project until
    `template_installation.status` is `ready`. A `201` without
    `template_installation` means nothing is being installed.

    The fork is checked against what the release recorded when it was published
    (its functions, frontends and variables, and the plan's room for them); the
    release's archive is read and checked by the install. A stored archive that
    fails those checks fails the install with `failure_code` `source_invalid`
    rather than refusing the request.

    Send the `release_id` that `GET /share-previews/{share_id}` returned. If the
    share moved to a new release since, nothing is created and the answer is
    `409` with code `release_changed`.

    Args:
        idempotency_key (str | Unset):
        body (ForkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Project]
     """


    kwargs = request_kwargs(
        body=body,
idempotency_key=idempotency_key,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ForkCreateRequest,
    idempotency_key: str | Unset = UNSET,

) -> Error | Project | None:
    """ Fork a share into a project of your own

     Creates a project in the caller's account from the release a share offers,
    and queues its install: the release's functions and frontends, never the
    owner's data, variable values, keys or sign-in settings. Every variable the
    release declares is created; one the visitor gives no value for is created
    empty. Installation is asynchronous: poll the project until
    `template_installation.status` is `ready`. A `201` without
    `template_installation` means nothing is being installed.

    The fork is checked against what the release recorded when it was published
    (its functions, frontends and variables, and the plan's room for them); the
    release's archive is read and checked by the install. A stored archive that
    fails those checks fails the install with `failure_code` `source_invalid`
    rather than refusing the request.

    Send the `release_id` that `GET /share-previews/{share_id}` returned. If the
    share moved to a new release since, nothing is created and the answer is
    `409` with code `release_changed`.

    Args:
        idempotency_key (str | Unset):
        body (ForkCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Project
     """


    return (await asyncio_detailed(
        client=client,
body=body,
idempotency_key=idempotency_key,

    )).parsed
