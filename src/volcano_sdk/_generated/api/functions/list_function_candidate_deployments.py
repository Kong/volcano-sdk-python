from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_candidate_deployment_list import FunctionCandidateDeploymentList
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/functions/{function_id}/candidates/{candidate_id}/deployments".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),candidate_id=quote(str(candidate_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionCandidateDeploymentList | None:
    if response.status_code == 200:
        response_200 = FunctionCandidateDeploymentList.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionCandidateDeploymentList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | FunctionCandidateDeploymentList]:
    """ List a function preview's deployments

     Returns the preview's deployments, newest first, at most 100. Never depends on the
    `functions.candidates` capability.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCandidateDeploymentList]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
candidate_id=candidate_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | FunctionCandidateDeploymentList | None:
    """ List a function preview's deployments

     Returns the preview's deployments, newest first, at most 100. Never depends on the
    `functions.candidates` capability.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCandidateDeploymentList
     """


    return sync_detailed(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[Error | FunctionCandidateDeploymentList]:
    """ List a function preview's deployments

     Returns the preview's deployments, newest first, at most 100. Never depends on the
    `functions.candidates` capability.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCandidateDeploymentList]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
candidate_id=candidate_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Error | FunctionCandidateDeploymentList | None:
    """ List a function preview's deployments

     Returns the preview's deployments, newest first, at most 100. Never depends on the
    `functions.candidates` capability.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCandidateDeploymentList
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
client=client,

    )).parsed
