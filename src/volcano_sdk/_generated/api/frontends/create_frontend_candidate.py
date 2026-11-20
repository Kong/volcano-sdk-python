from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_frontend_candidate_body import CreateFrontendCandidateBody
from ...models.error import Error
from ...models.frontend_candidate import FrontendCandidate
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    *,
    body: CreateFrontendCandidateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/candidates".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendCandidate | None:
    if response.status_code == 202:
        response_202 = FrontendCandidate.from_dict(response.json())



        return response_202

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
    *,
    client: AuthenticatedClient,
    body: CreateFrontendCandidateBody,

) -> Response[Error | FrontendCandidate]:
    """ Create a frontend Candidate

     Builds a copy of the frontend from the uploaded archive, with the frontend's own variable
    selection, and deploys it to one region: the first region the frontend deploys to, or the
    project's first region by name if it has not deployed yet. The Candidate is served at its own
    URL, so it can be checked without changing what the frontend serves. The URL is reachable by
    anyone who holds it and is not indexed; a Candidate is never public and does not claim to be
    private. The response is `202` while the first deployment runs; read the Candidate for its
    `status` and `url`.

    Creating a Candidate is available while the `frontends.candidates` capability is. While it is
    not, this operation, redeploying, promoting and rolling back to a Candidate answer `404` with
    code `feature_unavailable`; reading and deleting existing Candidates, and rolling back to the
    frontend's own runtime, keep working.

    A Candidate builds like any deploy and spends the project's build minutes. A frontend has at
    most 20 live Candidates, and each name is unique within the frontend. Without `ttl_seconds` a
    Candidate is kept until it is deleted.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidate]
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
    body: CreateFrontendCandidateBody,

) -> Error | FrontendCandidate | None:
    """ Create a frontend Candidate

     Builds a copy of the frontend from the uploaded archive, with the frontend's own variable
    selection, and deploys it to one region: the first region the frontend deploys to, or the
    project's first region by name if it has not deployed yet. The Candidate is served at its own
    URL, so it can be checked without changing what the frontend serves. The URL is reachable by
    anyone who holds it and is not indexed; a Candidate is never public and does not claim to be
    private. The response is `202` while the first deployment runs; read the Candidate for its
    `status` and `url`.

    Creating a Candidate is available while the `frontends.candidates` capability is. While it is
    not, this operation, redeploying, promoting and rolling back to a Candidate answer `404` with
    code `feature_unavailable`; reading and deleting existing Candidates, and rolling back to the
    frontend's own runtime, keep working.

    A Candidate builds like any deploy and spends the project's build minutes. A frontend has at
    most 20 live Candidates, and each name is unique within the frontend. Without `ttl_seconds` a
    Candidate is kept until it is deleted.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidate
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
    body: CreateFrontendCandidateBody,

) -> Response[Error | FrontendCandidate]:
    """ Create a frontend Candidate

     Builds a copy of the frontend from the uploaded archive, with the frontend's own variable
    selection, and deploys it to one region: the first region the frontend deploys to, or the
    project's first region by name if it has not deployed yet. The Candidate is served at its own
    URL, so it can be checked without changing what the frontend serves. The URL is reachable by
    anyone who holds it and is not indexed; a Candidate is never public and does not claim to be
    private. The response is `202` while the first deployment runs; read the Candidate for its
    `status` and `url`.

    Creating a Candidate is available while the `frontends.candidates` capability is. While it is
    not, this operation, redeploying, promoting and rolling back to a Candidate answer `404` with
    code `feature_unavailable`; reading and deleting existing Candidates, and rolling back to the
    frontend's own runtime, keep working.

    A Candidate builds like any deploy and spends the project's build minutes. A frontend has at
    most 20 live Candidates, and each name is unique within the frontend. Without `ttl_seconds` a
    Candidate is kept until it is deleted.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidate]
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
    body: CreateFrontendCandidateBody,

) -> Error | FrontendCandidate | None:
    """ Create a frontend Candidate

     Builds a copy of the frontend from the uploaded archive, with the frontend's own variable
    selection, and deploys it to one region: the first region the frontend deploys to, or the
    project's first region by name if it has not deployed yet. The Candidate is served at its own
    URL, so it can be checked without changing what the frontend serves. The URL is reachable by
    anyone who holds it and is not indexed; a Candidate is never public and does not claim to be
    private. The response is `202` while the first deployment runs; read the Candidate for its
    `status` and `url`.

    Creating a Candidate is available while the `frontends.candidates` capability is. While it is
    not, this operation, redeploying, promoting and rolling back to a Candidate answer `404` with
    code `feature_unavailable`; reading and deleting existing Candidates, and rolling back to the
    frontend's own runtime, keep working.

    A Candidate builds like any deploy and spends the project's build minutes. A frontend has at
    most 20 live Candidates, and each name is unique within the frontend. Without `ttl_seconds` a
    Candidate is kept until it is deleted.

    Args:
        id (UUID):
        frontend_id (UUID):
        body (CreateFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidate
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
client=client,
body=body,

    )).parsed
