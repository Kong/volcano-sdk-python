from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share_draft_changed_error import ShareDraftChangedError
from ...models.share_release import ShareRelease
from ...models.share_release_create_request import ShareReleaseCreateRequest
from typing import cast



def request_kwargs(
    *,
    body: ShareReleaseCreateRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/share-releases",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ShareDraftChangedError | ShareRelease | None:
    if response.status_code == 201:
        response_201 = ShareRelease.from_dict(response.json())



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
        response_409 = ShareDraftChangedError.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ShareDraftChangedError | ShareRelease]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ShareReleaseCreateRequest,

) -> Response[Error | ShareDraftChangedError | ShareRelease]:
    """ Publish a deploy link release

     Snapshots the project's deployed functions and frontends into an immutable
    release and makes it the link's current release in one step, so visitors see
    either the previous release or this one. Visitors install exactly the stored
    release; later deploys to the project change nothing until the owner
    publishes again.

    Send the reviewed draft's `draft_id`, its variables and the functions that
    receive the new project's `VOLCANO_SERVICE_KEY`, as confirmed from the
    draft. Both lists must be exactly the draft's: a release carries every
    variable, since leaving one out would only break the code that reads it. If
    a fresh build is not the reviewed draft, because the project was redeployed
    or changed since, or the lists differ from it, nothing is published and the
    answer is `409` with code `draft_changed` and the new draft. A
    release carries variable names, never values, and no database. A publish is
    a full build and counts against the account's hourly release build budget,
    which it shares with the draft.

    Args:
        body (ShareReleaseCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareDraftChangedError | ShareRelease]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: ShareReleaseCreateRequest,

) -> Error | ShareDraftChangedError | ShareRelease | None:
    """ Publish a deploy link release

     Snapshots the project's deployed functions and frontends into an immutable
    release and makes it the link's current release in one step, so visitors see
    either the previous release or this one. Visitors install exactly the stored
    release; later deploys to the project change nothing until the owner
    publishes again.

    Send the reviewed draft's `draft_id`, its variables and the functions that
    receive the new project's `VOLCANO_SERVICE_KEY`, as confirmed from the
    draft. Both lists must be exactly the draft's: a release carries every
    variable, since leaving one out would only break the code that reads it. If
    a fresh build is not the reviewed draft, because the project was redeployed
    or changed since, or the lists differ from it, nothing is published and the
    answer is `409` with code `draft_changed` and the new draft. A
    release carries variable names, never values, and no database. A publish is
    a full build and counts against the account's hourly release build budget,
    which it shares with the draft.

    Args:
        body (ShareReleaseCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareDraftChangedError | ShareRelease
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ShareReleaseCreateRequest,

) -> Response[Error | ShareDraftChangedError | ShareRelease]:
    """ Publish a deploy link release

     Snapshots the project's deployed functions and frontends into an immutable
    release and makes it the link's current release in one step, so visitors see
    either the previous release or this one. Visitors install exactly the stored
    release; later deploys to the project change nothing until the owner
    publishes again.

    Send the reviewed draft's `draft_id`, its variables and the functions that
    receive the new project's `VOLCANO_SERVICE_KEY`, as confirmed from the
    draft. Both lists must be exactly the draft's: a release carries every
    variable, since leaving one out would only break the code that reads it. If
    a fresh build is not the reviewed draft, because the project was redeployed
    or changed since, or the lists differ from it, nothing is published and the
    answer is `409` with code `draft_changed` and the new draft. A
    release carries variable names, never values, and no database. A publish is
    a full build and counts against the account's hourly release build budget,
    which it shares with the draft.

    Args:
        body (ShareReleaseCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareDraftChangedError | ShareRelease]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ShareReleaseCreateRequest,

) -> Error | ShareDraftChangedError | ShareRelease | None:
    """ Publish a deploy link release

     Snapshots the project's deployed functions and frontends into an immutable
    release and makes it the link's current release in one step, so visitors see
    either the previous release or this one. Visitors install exactly the stored
    release; later deploys to the project change nothing until the owner
    publishes again.

    Send the reviewed draft's `draft_id`, its variables and the functions that
    receive the new project's `VOLCANO_SERVICE_KEY`, as confirmed from the
    draft. Both lists must be exactly the draft's: a release carries every
    variable, since leaving one out would only break the code that reads it. If
    a fresh build is not the reviewed draft, because the project was redeployed
    or changed since, or the lists differ from it, nothing is published and the
    answer is `409` with code `draft_changed` and the new draft. A
    release carries variable names, never values, and no database. A publish is
    a full build and counts against the account's hourly release build budget,
    which it shares with the draft.

    Args:
        body (ShareReleaseCreateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareDraftChangedError | ShareRelease
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
