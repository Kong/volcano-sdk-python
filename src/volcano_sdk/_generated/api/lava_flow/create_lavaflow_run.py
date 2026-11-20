from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_run import LavaflowRun
from ...models.lavaflow_run_create import LavaflowRunCreate
from typing import cast



def request_kwargs(
    *,
    body: LavaflowRunCreate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/lavaflow/runs",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowRun | None:
    if response.status_code == 202:
        response_202 = LavaflowRun.from_dict(response.json())



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

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowRun]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowRunCreate,

) -> Response[Error | LavaflowRun]:
    """ Start a LavaFlow run

     Starts a run on one of the project's issues. LavaFlow starts runs on
    its own only for issues with `exception: true`, and only while it is
    on. Start one here for any other issue, or for one recorded before
    LavaFlow was turned on. The run follows the project's settings, as
    one LavaFlow starts on its own does, and answers `202` while it is
    `queued`; read it with `GET /lavaflow/runs/{run_id}`.

    Only the project's owner can start a run, as a person, while their
    account is active: with a platform token that expires, or `volcano
    login`. A platform token that never expires, a `volcano login` token
    whose sign-in ended, a full-scope project access token, and a request
    made through MCP get `403` with code `person_required`; a read-only
    project access token is refused as read-only first, without a code,
    and so is the owner of a read-only account.

    Every start counts toward the run limits: 5 runs per issue and 200 per
    project in any 24 hours. An issue has one run in progress at a time,
    so sending the request again while the first run is in progress
    answers `409` with code `lavaflow_run_in_progress`.

    A run on a Code Quality issue is a Code Quality run. It starts only
    while Code Quality is available to the project, as
    `lavaflow.code_quality` in `GET /capabilities` reports, and on for it.

    Args:
        body (LavaflowRunCreate): The project, and the issue to start a run on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
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
    body: LavaflowRunCreate,

) -> Error | LavaflowRun | None:
    """ Start a LavaFlow run

     Starts a run on one of the project's issues. LavaFlow starts runs on
    its own only for issues with `exception: true`, and only while it is
    on. Start one here for any other issue, or for one recorded before
    LavaFlow was turned on. The run follows the project's settings, as
    one LavaFlow starts on its own does, and answers `202` while it is
    `queued`; read it with `GET /lavaflow/runs/{run_id}`.

    Only the project's owner can start a run, as a person, while their
    account is active: with a platform token that expires, or `volcano
    login`. A platform token that never expires, a `volcano login` token
    whose sign-in ended, a full-scope project access token, and a request
    made through MCP get `403` with code `person_required`; a read-only
    project access token is refused as read-only first, without a code,
    and so is the owner of a read-only account.

    Every start counts toward the run limits: 5 runs per issue and 200 per
    project in any 24 hours. An issue has one run in progress at a time,
    so sending the request again while the first run is in progress
    answers `409` with code `lavaflow_run_in_progress`.

    A run on a Code Quality issue is a Code Quality run. It starts only
    while Code Quality is available to the project, as
    `lavaflow.code_quality` in `GET /capabilities` reports, and on for it.

    Args:
        body (LavaflowRunCreate): The project, and the issue to start a run on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowRunCreate,

) -> Response[Error | LavaflowRun]:
    """ Start a LavaFlow run

     Starts a run on one of the project's issues. LavaFlow starts runs on
    its own only for issues with `exception: true`, and only while it is
    on. Start one here for any other issue, or for one recorded before
    LavaFlow was turned on. The run follows the project's settings, as
    one LavaFlow starts on its own does, and answers `202` while it is
    `queued`; read it with `GET /lavaflow/runs/{run_id}`.

    Only the project's owner can start a run, as a person, while their
    account is active: with a platform token that expires, or `volcano
    login`. A platform token that never expires, a `volcano login` token
    whose sign-in ended, a full-scope project access token, and a request
    made through MCP get `403` with code `person_required`; a read-only
    project access token is refused as read-only first, without a code,
    and so is the owner of a read-only account.

    Every start counts toward the run limits: 5 runs per issue and 200 per
    project in any 24 hours. An issue has one run in progress at a time,
    so sending the request again while the first run is in progress
    answers `409` with code `lavaflow_run_in_progress`.

    A run on a Code Quality issue is a Code Quality run. It starts only
    while Code Quality is available to the project, as
    `lavaflow.code_quality` in `GET /capabilities` reports, and on for it.

    Args:
        body (LavaflowRunCreate): The project, and the issue to start a run on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
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
    body: LavaflowRunCreate,

) -> Error | LavaflowRun | None:
    """ Start a LavaFlow run

     Starts a run on one of the project's issues. LavaFlow starts runs on
    its own only for issues with `exception: true`, and only while it is
    on. Start one here for any other issue, or for one recorded before
    LavaFlow was turned on. The run follows the project's settings, as
    one LavaFlow starts on its own does, and answers `202` while it is
    `queued`; read it with `GET /lavaflow/runs/{run_id}`.

    Only the project's owner can start a run, as a person, while their
    account is active: with a platform token that expires, or `volcano
    login`. A platform token that never expires, a `volcano login` token
    whose sign-in ended, a full-scope project access token, and a request
    made through MCP get `403` with code `person_required`; a read-only
    project access token is refused as read-only first, without a code,
    and so is the owner of a read-only account.

    Every start counts toward the run limits: 5 runs per issue and 200 per
    project in any 24 hours. An issue has one run in progress at a time,
    so sending the request again while the first run is in progress
    answers `409` with code `lavaflow_run_in_progress`.

    A run on a Code Quality issue is a Code Quality run. It starts only
    while Code Quality is available to the project, as
    `lavaflow.code_quality` in `GET /capabilities` reports, and on for it.

    Args:
        body (LavaflowRunCreate): The project, and the issue to start a run on.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
