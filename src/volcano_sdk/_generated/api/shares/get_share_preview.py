from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share_preview import SharePreview
from typing import cast



def request_kwargs(
    share_id: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/share-previews/{share_id}".format(share_id=quote(str(share_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SharePreview | None:
    if response.status_code == 200:
        response_200 = SharePreview.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SharePreview]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | SharePreview]:
    """ Preview what a deploy link deploys

     Public: needs no credential, because the link id is the credential. Answers
    the link's current release: when it was published, its digest, the functions
    and frontends installing it creates, the variables the visitor supplies, and
    the functions that receive the new project's service key. Show it to a
    visitor before they confirm, and send its `release.id` when creating the
    project.

    Counts the visit for the link's owner, unless the request comes from a
    crawler or link preview. A link that does not exist, was switched off, or has
    not been published yet all answer the same `404`.

    Args:
        share_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SharePreview]
     """


    kwargs = request_kwargs(
        share_id=share_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    share_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Error | SharePreview | None:
    """ Preview what a deploy link deploys

     Public: needs no credential, because the link id is the credential. Answers
    the link's current release: when it was published, its digest, the functions
    and frontends installing it creates, the variables the visitor supplies, and
    the functions that receive the new project's service key. Show it to a
    visitor before they confirm, and send its `release.id` when creating the
    project.

    Counts the visit for the link's owner, unless the request comes from a
    crawler or link preview. A link that does not exist, was switched off, or has
    not been published yet all answer the same `404`.

    Args:
        share_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SharePreview
     """


    return sync_detailed(
        share_id=share_id,
client=client,

    ).parsed

async def asyncio_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Response[Error | SharePreview]:
    """ Preview what a deploy link deploys

     Public: needs no credential, because the link id is the credential. Answers
    the link's current release: when it was published, its digest, the functions
    and frontends installing it creates, the variables the visitor supplies, and
    the functions that receive the new project's service key. Show it to a
    visitor before they confirm, and send its `release.id` when creating the
    project.

    Counts the visit for the link's owner, unless the request comes from a
    crawler or link preview. A link that does not exist, was switched off, or has
    not been published yet all answer the same `404`.

    Args:
        share_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SharePreview]
     """


    kwargs = request_kwargs(
        share_id=share_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    share_id: str,
    *,
    client: AuthenticatedClient | Client,

) -> Error | SharePreview | None:
    """ Preview what a deploy link deploys

     Public: needs no credential, because the link id is the credential. Answers
    the link's current release: when it was published, its digest, the functions
    and frontends installing it creates, the variables the visitor supplies, and
    the functions that receive the new project's service key. Show it to a
    visitor before they confirm, and send its `release.id` when creating the
    project.

    Counts the visit for the link's owner, unless the request comes from a
    crawler or link preview. A link that does not exist, was switched off, or has
    not been published yet all answer the same `404`.

    Args:
        share_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SharePreview
     """


    return (await asyncio_detailed(
        share_id=share_id,
client=client,

    )).parsed
