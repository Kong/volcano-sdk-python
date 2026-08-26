from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.database_branch import DatabaseBranch
from ...models.error import Error
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    database_name: str,
    branch_name: str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/projects/{id}/databases/{database_name}/branches/{branch_name}/reset".format(id=quote(str(id), safe=""),database_name=quote(str(database_name), safe=""),branch_name=quote(str(branch_name), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> DatabaseBranch | Error | None:
    if response.status_code == 202:
        response_202 = DatabaseBranch.from_dict(response.json())



        return response_202

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[DatabaseBranch | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseBranch | Error]:
    """ Reset a branch to its parent's current state

     Discards everything written on the branch and re-forks it from the
    parent as it is now.

    Returns immediately with the branch in `provisioning`. The rewind runs in
    the background; poll the branch until it reports `active` before
    connecting again.

    The branch keeps its name and its connection string, so anything holding
    that string keeps working once it is active again, and its lifetime is
    re-armed to the duration it was created with. The branch does not serve
    connections for the duration of the reset.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseBranch | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
branch_name=branch_name,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> DatabaseBranch | Error | None:
    """ Reset a branch to its parent's current state

     Discards everything written on the branch and re-forks it from the
    parent as it is now.

    Returns immediately with the branch in `provisioning`. The rewind runs in
    the background; poll the branch until it reports `active` before
    connecting again.

    The branch keeps its name and its connection string, so anything holding
    that string keeps working once it is active again, and its lifetime is
    re-armed to the duration it was created with. The branch does not serve
    connections for the duration of the reset.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseBranch | Error
     """


    return sync_detailed(
        id=id,
database_name=database_name,
branch_name=branch_name,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> Response[DatabaseBranch | Error]:
    """ Reset a branch to its parent's current state

     Discards everything written on the branch and re-forks it from the
    parent as it is now.

    Returns immediately with the branch in `provisioning`. The rewind runs in
    the background; poll the branch until it reports `active` before
    connecting again.

    The branch keeps its name and its connection string, so anything holding
    that string keeps working once it is active again, and its lifetime is
    re-armed to the duration it was created with. The branch does not serve
    connections for the duration of the reset.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DatabaseBranch | Error]
     """


    kwargs = _get_kwargs(
        id=id,
database_name=database_name,
branch_name=branch_name,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    database_name: str,
    branch_name: str,
    *,
    client: AuthenticatedClient,

) -> DatabaseBranch | Error | None:
    """ Reset a branch to its parent's current state

     Discards everything written on the branch and re-forks it from the
    parent as it is now.

    Returns immediately with the branch in `provisioning`. The rewind runs in
    the background; poll the branch until it reports `active` before
    connecting again.

    The branch keeps its name and its connection string, so anything holding
    that string keeps working once it is active again, and its lifetime is
    re-armed to the duration it was created with. The branch does not serve
    connections for the duration of the reset.

    Args:
        id (UUID):
        database_name (str):
        branch_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DatabaseBranch | Error
     """


    return (await asyncio_detailed(
        id=id,
database_name=database_name,
branch_name=branch_name,
client=client,

    )).parsed
