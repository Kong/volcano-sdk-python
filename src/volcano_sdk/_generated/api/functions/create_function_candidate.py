from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_function_candidate_body import CreateFunctionCandidateBody
from ...models.error import Error
from ...models.function_candidate import FunctionCandidate
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: UUID | str,
    *,
    body: CreateFunctionCandidateBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions/{function_id}/candidates".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),),
    }

    _kwargs["files"] = body.to_multipart()

    headers["Content-Type"] = "multipart/form-data; boundary=+++"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionCandidate | None:
    if response.status_code == 202:
        response_202 = FunctionCandidate.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionCandidate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFunctionCandidateBody,

) -> Response[Error | FunctionCandidate]:
    """ Create a function preview

     Builds the uploaded source with the function's runtime, handler and variables, and deploys it to a
    runtime of its own in every region the function deploys to. The preview is invoked at
    `https://<preview id>.<functions domain>` and is always private, whatever the function's own
    visibility: only the project's service key, with `functions.invoke`, can invoke it, and signed-in
    users, anon keys and access tokens are refused. It gets none of the function's schedules or warmers.
    The response is `202` while the first deployment runs; read the preview for its `status` and `url`.

    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`. Reading and deleting existing previews,
    and rolling the function back to its own build, keep
    working.

    A preview builds like any deploy and spends the project's build minutes. A function has at most 20
    live previews, and each name is unique within the function. Without `ttl_seconds` a preview is kept
    until it is deleted. Durable functions have no previews.

    Args:
        id (UUID):
        function_id (UUID):
        body (CreateFunctionCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCandidate]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFunctionCandidateBody,

) -> Error | FunctionCandidate | None:
    """ Create a function preview

     Builds the uploaded source with the function's runtime, handler and variables, and deploys it to a
    runtime of its own in every region the function deploys to. The preview is invoked at
    `https://<preview id>.<functions domain>` and is always private, whatever the function's own
    visibility: only the project's service key, with `functions.invoke`, can invoke it, and signed-in
    users, anon keys and access tokens are refused. It gets none of the function's schedules or warmers.
    The response is `202` while the first deployment runs; read the preview for its `status` and `url`.

    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`. Reading and deleting existing previews,
    and rolling the function back to its own build, keep
    working.

    A preview builds like any deploy and spends the project's build minutes. A function has at most 20
    live previews, and each name is unique within the function. Without `ttl_seconds` a preview is kept
    until it is deleted. Durable functions have no previews.

    Args:
        id (UUID):
        function_id (UUID):
        body (CreateFunctionCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCandidate
     """


    return sync_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFunctionCandidateBody,

) -> Response[Error | FunctionCandidate]:
    """ Create a function preview

     Builds the uploaded source with the function's runtime, handler and variables, and deploys it to a
    runtime of its own in every region the function deploys to. The preview is invoked at
    `https://<preview id>.<functions domain>` and is always private, whatever the function's own
    visibility: only the project's service key, with `functions.invoke`, can invoke it, and signed-in
    users, anon keys and access tokens are refused. It gets none of the function's schedules or warmers.
    The response is `202` while the first deployment runs; read the preview for its `status` and `url`.

    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`. Reading and deleting existing previews,
    and rolling the function back to its own build, keep
    working.

    A preview builds like any deploy and spends the project's build minutes. A function has at most 20
    live previews, and each name is unique within the function. Without `ttl_seconds` a preview is kept
    until it is deleted. Durable functions have no previews.

    Args:
        id (UUID):
        function_id (UUID):
        body (CreateFunctionCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionCandidate]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    function_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: CreateFunctionCandidateBody,

) -> Error | FunctionCandidate | None:
    """ Create a function preview

     Builds the uploaded source with the function's runtime, handler and variables, and deploys it to a
    runtime of its own in every region the function deploys to. The preview is invoked at
    `https://<preview id>.<functions domain>` and is always private, whatever the function's own
    visibility: only the project's service key, with `functions.invoke`, can invoke it, and signed-in
    users, anon keys and access tokens are refused. It gets none of the function's schedules or warmers.
    The response is `202` while the first deployment runs; read the preview for its `status` and `url`.

    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`. Reading and deleting existing previews,
    and rolling the function back to its own build, keep
    working.

    A preview builds like any deploy and spends the project's build minutes. A function has at most 20
    live previews, and each name is unique within the function. Without `ttl_seconds` a preview is kept
    until it is deleted. Durable functions have no previews.

    Args:
        id (UUID):
        function_id (UUID):
        body (CreateFunctionCandidateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionCandidate
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
client=client,
body=body,

    )).parsed
