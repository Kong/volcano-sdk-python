from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.function_promotion_request import FunctionPromotionRequest
from ...models.function_serving import FunctionServing
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    body: FunctionPromotionRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/functions/{function_id}/candidates/{candidate_id}/promote".format(id=quote(str(id), safe=""),function_id=quote(str(function_id), safe=""),candidate_id=quote(str(candidate_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | FunctionServing | None:
    if response.status_code == 200:
        response_200 = FunctionServing.from_dict(response.json())



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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | FunctionServing]:
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
    body: FunctionPromotionRequest,

) -> Response[Error | FunctionServing]:
    """ Promote a function preview

     Points the function's traffic at the preview's runtime. Nothing is deployed or rebuilt, so it
    takes effect at once: every call to the function, through its own URL, the invoke route, a
    schedule or a frontend route, runs the preview's code, while the function keeps its ID, URL,
    visibility, schedules, metering and logs. The function's own build is kept as it is for a
    rollback, and what the function ran becomes what a rollback returns to.

    The preview must be serving a successful deployment built with the variables, runtime and handler
    the function has now, in every region the function deploys to, and the function must have a
    successful deployment of its own. It is refused while a deployment of the function, or a
    synchronization of its variables, runs. Promotion names the `revision` the caller read from
    `serving`; a competing promotion or rollback makes it fail with `409`. Once the project's
    repository is the source of truth, promotion is refused with `409`, as a direct deploy is.
    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):
        body (FunctionPromotionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionServing]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
body=body,

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
    body: FunctionPromotionRequest,

) -> Error | FunctionServing | None:
    """ Promote a function preview

     Points the function's traffic at the preview's runtime. Nothing is deployed or rebuilt, so it
    takes effect at once: every call to the function, through its own URL, the invoke route, a
    schedule or a frontend route, runs the preview's code, while the function keeps its ID, URL,
    visibility, schedules, metering and logs. The function's own build is kept as it is for a
    rollback, and what the function ran becomes what a rollback returns to.

    The preview must be serving a successful deployment built with the variables, runtime and handler
    the function has now, in every region the function deploys to, and the function must have a
    successful deployment of its own. It is refused while a deployment of the function, or a
    synchronization of its variables, runs. Promotion names the `revision` the caller read from
    `serving`; a competing promotion or rollback makes it fail with `409`. Once the project's
    repository is the source of truth, promotion is refused with `409`, as a direct deploy is.
    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):
        body (FunctionPromotionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionServing
     """


    return sync_detailed(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    function_id: UUID | str,
    candidate_id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: FunctionPromotionRequest,

) -> Response[Error | FunctionServing]:
    """ Promote a function preview

     Points the function's traffic at the preview's runtime. Nothing is deployed or rebuilt, so it
    takes effect at once: every call to the function, through its own URL, the invoke route, a
    schedule or a frontend route, runs the preview's code, while the function keeps its ID, URL,
    visibility, schedules, metering and logs. The function's own build is kept as it is for a
    rollback, and what the function ran becomes what a rollback returns to.

    The preview must be serving a successful deployment built with the variables, runtime and handler
    the function has now, in every region the function deploys to, and the function must have a
    successful deployment of its own. It is refused while a deployment of the function, or a
    synchronization of its variables, runs. Promotion names the `revision` the caller read from
    `serving`; a competing promotion or rollback makes it fail with `409`. Once the project's
    repository is the source of truth, promotion is refused with `409`, as a direct deploy is.
    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):
        body (FunctionPromotionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | FunctionServing]
     """


    kwargs = request_kwargs(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
body=body,

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
    body: FunctionPromotionRequest,

) -> Error | FunctionServing | None:
    """ Promote a function preview

     Points the function's traffic at the preview's runtime. Nothing is deployed or rebuilt, so it
    takes effect at once: every call to the function, through its own URL, the invoke route, a
    schedule or a frontend route, runs the preview's code, while the function keeps its ID, URL,
    visibility, schedules, metering and logs. The function's own build is kept as it is for a
    rollback, and what the function ran becomes what a rollback returns to.

    The preview must be serving a successful deployment built with the variables, runtime and handler
    the function has now, in every region the function deploys to, and the function must have a
    successful deployment of its own. It is refused while a deployment of the function, or a
    synchronization of its variables, runs. Promotion names the `revision` the caller read from
    `serving`; a competing promotion or rollback makes it fail with `409`. Once the project's
    repository is the source of truth, promotion is refused with `409`, as a direct deploy is.
    While the `functions.candidates` capability is unavailable, including on the local development
    server, it answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        function_id (UUID):
        candidate_id (UUID):
        body (FunctionPromotionRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | FunctionServing
     """


    return (await asyncio_detailed(
        id=id,
function_id=function_id,
candidate_id=candidate_id,
client=client,
body=body,

    )).parsed
