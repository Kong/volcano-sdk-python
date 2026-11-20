from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend_candidate import FrontendCandidate
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/frontends/{frontend_id}/candidates/{candidate_id}".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),candidate_id=quote(str(candidate_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendCandidate | None:
    if response.status_code == 200:
        response_200 = FrontendCandidate.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendCandidate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | FrontendCandidate]:
    """ Get a frontend Candidate

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidate]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | FrontendCandidate | None:
    """ Get a frontend Candidate

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidate
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | FrontendCandidate]:
    """ Get a frontend Candidate

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidate]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | FrontendCandidate | None:
    """ Get a frontend Candidate

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidate
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
client=client,

    )).parsed
