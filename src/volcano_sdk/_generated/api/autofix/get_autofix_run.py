from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.autofix_run import AutofixRun
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    run_id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/autofix-runs/{run_id}".format(id=quote(str(id), safe=""),run_id=quote(str(run_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AutofixRun | Error | None:
    if response.status_code == 200:
        response_200 = AutofixRun.from_dict(response.json())



        return response_200

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AutofixRun | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixRun | Error]:
    """ Get an autofix run

     Returns one run: its status, the diagnosis once it succeeds, and why it
    failed or was canceled. Runs stay readable where autofix is not
    available.

    Project access tokens can read runs, including read-only ones.

    Args:
        id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
run_id=run_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixRun | Error | None:
    """ Get an autofix run

     Returns one run: its status, the diagnosis once it succeeds, and why it
    failed or was canceled. Runs stay readable where autofix is not
    available.

    Project access tokens can read runs, including read-only ones.

    Args:
        id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixRun | Error
     """


    return sync_detailed(
        id=id,
run_id=run_id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[AutofixRun | Error]:
    """ Get an autofix run

     Returns one run: its status, the diagnosis once it succeeds, and why it
    failed or was canceled. Runs stay readable where autofix is not
    available.

    Project access tokens can read runs, including read-only ones.

    Args:
        id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixRun | Error]
     """


    kwargs = request_kwargs(
        id=id,
run_id=run_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    run_id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> AutofixRun | Error | None:
    """ Get an autofix run

     Returns one run: its status, the diagnosis once it succeeds, and why it
    failed or was canceled. Runs stay readable where autofix is not
    available.

    Project access tokens can read runs, including read-only ones.

    Args:
        id (UUID):
        run_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixRun | Error
     """


    return (await asyncio_detailed(
        id=id,
run_id=run_id,
client=client,

    )).parsed
