from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.frontend_candidate_deployment import FrontendCandidateDeployment
from ...models.redeploy_frontend_candidate_body import RedeployFrontendCandidateBody
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    body: RedeployFrontendCandidateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/frontends/{frontend_id}/candidates/{candidate_id}/deployments".format(id=quote(str(id), safe=""),frontend_id=quote(str(frontend_id), safe=""),candidate_id=quote(str(candidate_id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FrontendCandidateDeployment | None:
    if response.status_code == 202:
        response_202 = FrontendCandidateDeployment.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FrontendCandidateDeployment]:
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
    body: RedeployFrontendCandidateBody,

) -> Response[Error | FrontendCandidateDeployment]:
    """ Deploy a new archive to a frontend Candidate

     Builds the uploaded archive with the frontend's own variable selection and deploys it to the
    Candidate. The Candidate keeps serving its previous deployment until this one succeeds, and a
    failed deployment leaves it on the previous one. A Candidate takes one deployment at a time.
    While the `frontends.candidates` capability is unavailable, it answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):
        body (RedeployFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidateDeployment]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
body=body,

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
    body: RedeployFrontendCandidateBody,

) -> Error | FrontendCandidateDeployment | None:
    """ Deploy a new archive to a frontend Candidate

     Builds the uploaded archive with the frontend's own variable selection and deploys it to the
    Candidate. The Candidate keeps serving its previous deployment until this one succeeds, and a
    failed deployment leaves it on the previous one. A Candidate takes one deployment at a time.
    While the `frontends.candidates` capability is unavailable, it answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):
        body (RedeployFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidateDeployment
     """


    return sync_detailed(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    frontend_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: RedeployFrontendCandidateBody,

) -> Response[Error | FrontendCandidateDeployment]:
    """ Deploy a new archive to a frontend Candidate

     Builds the uploaded archive with the frontend's own variable selection and deploys it to the
    Candidate. The Candidate keeps serving its previous deployment until this one succeeds, and a
    failed deployment leaves it on the previous one. A Candidate takes one deployment at a time.
    While the `frontends.candidates` capability is unavailable, it answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):
        body (RedeployFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FrontendCandidateDeployment]
     """


    kwargs = request_kwargs(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
body=body,

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
    body: RedeployFrontendCandidateBody,

) -> Error | FrontendCandidateDeployment | None:
    """ Deploy a new archive to a frontend Candidate

     Builds the uploaded archive with the frontend's own variable selection and deploys it to the
    Candidate. The Candidate keeps serving its previous deployment until this one succeeds, and a
    failed deployment leaves it on the previous one. A Candidate takes one deployment at a time.
    While the `frontends.candidates` capability is unavailable, it answers `404` with code
    `feature_unavailable`.

    Args:
        id (UUID):
        frontend_id (UUID):
        candidate_id (UUID):
        body (RedeployFrontendCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FrontendCandidateDeployment
     """


    return (await asyncio_detailed(
        id=id,
frontend_id=frontend_id,
candidate_id=candidate_id,
client=client,
body=body,

    )).parsed
