from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_run import LavaflowRun
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    run_id: UUID | str,
    *,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/lavaflow/runs/{run_id}".format(run_id=quote(str(run_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowRun | None:
    if response.status_code == 200:
        response_200 = LavaflowRun.from_dict(response.json())



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
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowRun]:
    """ Get a LavaFlow run

     Returns a run, with its diagnosis, the log lines it cites, its diff and
    its review, including the findings the review left open and what it
    asks a person to decide. The run's project authorizes the read, so
    `project_id` is optional. The text holds the project's logs and source
    code, so this endpoint takes the same access as the project's log
    endpoints.

    A run held because the repository's workflows could run its fix with
    the repository's secrets before a person approves it
    (`pull_request_skipped: ungated_workflows`) lists every such job in
    `held_workflows`, beside the fix's `diff` and `diff_sha256`.

    Args:
        run_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
     """


    kwargs = request_kwargs(
        run_id=run_id,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowRun | None:
    """ Get a LavaFlow run

     Returns a run, with its diagnosis, the log lines it cites, its diff and
    its review, including the findings the review left open and what it
    asks a person to decide. The run's project authorizes the read, so
    `project_id` is optional. The text holds the project's logs and source
    code, so this endpoint takes the same access as the project's log
    endpoints.

    A run held because the repository's workflows could run its fix with
    the repository's secrets before a person approves it
    (`pull_request_skipped: ungated_workflows`) lists every such job in
    `held_workflows`, beside the fix's `diff` and `diff_sha256`.

    Args:
        run_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return sync_detailed(
        run_id=run_id,
client=client,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | LavaflowRun]:
    """ Get a LavaFlow run

     Returns a run, with its diagnosis, the log lines it cites, its diff and
    its review, including the findings the review left open and what it
    asks a person to decide. The run's project authorizes the read, so
    `project_id` is optional. The text holds the project's logs and source
    code, so this endpoint takes the same access as the project's log
    endpoints.

    A run held because the repository's workflows could run its fix with
    the repository's secrets before a person approves it
    (`pull_request_skipped: ungated_workflows`) lists every such job in
    `held_workflows`, beside the fix's `diff` and `diff_sha256`.

    Args:
        run_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
     """


    kwargs = request_kwargs(
        run_id=run_id,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,
    project_id: UUID | str | Unset = UNSET,

) -> Error | LavaflowRun | None:
    """ Get a LavaFlow run

     Returns a run, with its diagnosis, the log lines it cites, its diff and
    its review, including the findings the review left open and what it
    asks a person to decide. The run's project authorizes the read, so
    `project_id` is optional. The text holds the project's logs and source
    code, so this endpoint takes the same access as the project's log
    endpoints.

    A run held because the repository's workflows could run its fix with
    the repository's secrets before a person approves it
    (`pull_request_skipped: ungated_workflows`) lists every such job in
    `held_workflows`, beside the fix's `diff` and `diff_sha256`.

    Args:
        run_id (UUID):
        project_id (UUID | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return (await asyncio_detailed(
        run_id=run_id,
client=client,
project_id=project_id,

    )).parsed
