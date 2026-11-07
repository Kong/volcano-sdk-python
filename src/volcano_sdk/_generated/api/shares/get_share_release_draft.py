from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share_release_draft import ShareReleaseDraft
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    *,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["share_id"] = share_id

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/share-release-drafts",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ShareReleaseDraft | None:
    if response.status_code == 200:
        response_200 = ShareReleaseDraft.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ShareReleaseDraft]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | ShareReleaseDraft]:
    """ Show what publishing a deploy link would release

     Builds the project's deployed functions and frontends the way a release
    would, without storing anything, and reports what it would carry: the
    functions and frontends, the project variables every project created from
    the release gets (empty unless the visitor gives a value), the functions
    whose code reads `VOLCANO_SERVICE_KEY`, and what is left out (resources with
    no stored source, databases, sandboxes, dotenv and key files). Review it,
    then publish with its `draft_id`, and its variables and service key
    functions confirmed.

    Every call runs a full build and counts against the account's hourly
    release build budget, which drafts and publishes share. Fetch it when the
    owner opens the publish step, not on every focus or poll.

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareReleaseDraft]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,

) -> Error | ShareReleaseDraft | None:
    """ Show what publishing a deploy link would release

     Builds the project's deployed functions and frontends the way a release
    would, without storing anything, and reports what it would carry: the
    functions and frontends, the project variables every project created from
    the release gets (empty unless the visitor gives a value), the functions
    whose code reads `VOLCANO_SERVICE_KEY`, and what is left out (resources with
    no stored source, databases, sandboxes, dotenv and key files). Review it,
    then publish with its `draft_id`, and its variables and service key
    functions confirmed.

    Every call runs a full build and counts against the account's hourly
    release build budget, which drafts and publishes share. Fetch it when the
    owner opens the publish step, not on every focus or poll.

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareReleaseDraft
     """


    return sync_detailed(
        client=client,
share_id=share_id,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | ShareReleaseDraft]:
    """ Show what publishing a deploy link would release

     Builds the project's deployed functions and frontends the way a release
    would, without storing anything, and reports what it would carry: the
    functions and frontends, the project variables every project created from
    the release gets (empty unless the visitor gives a value), the functions
    whose code reads `VOLCANO_SERVICE_KEY`, and what is left out (resources with
    no stored source, databases, sandboxes, dotenv and key files). Review it,
    then publish with its `draft_id`, and its variables and service key
    functions confirmed.

    Every call runs a full build and counts against the account's hourly
    release build budget, which drafts and publishes share. Fetch it when the
    owner opens the publish step, not on every focus or poll.

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ShareReleaseDraft]
     """


    kwargs = request_kwargs(
        share_id=share_id,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    share_id: str,
    project_id: UUID | str | Unset = UNSET,

) -> Error | ShareReleaseDraft | None:
    """ Show what publishing a deploy link would release

     Builds the project's deployed functions and frontends the way a release
    would, without storing anything, and reports what it would carry: the
    functions and frontends, the project variables every project created from
    the release gets (empty unless the visitor gives a value), the functions
    whose code reads `VOLCANO_SERVICE_KEY`, and what is left out (resources with
    no stored source, databases, sandboxes, dotenv and key files). Review it,
    then publish with its `draft_id`, and its variables and service key
    functions confirmed.

    Every call runs a full build and counts against the account's hourly
    release build budget, which drafts and publishes share. Fetch it when the
    owner opens the publish step, not on every focus or poll.

    Args:
        share_id (str):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ShareReleaseDraft
     """


    return (await asyncio_detailed(
        client=client,
share_id=share_id,
project_id=project_id,

    )).parsed
