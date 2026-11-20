from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.capability_list import CapabilityList
from ...models.error import Error
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/capabilities".format(id=quote(str(id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CapabilityList | Error | None:
    if response.status_code == 200:
        response_200 = CapabilityList.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CapabilityList | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[CapabilityList | Error]:
    """ List a project's capabilities

     Lists which product capabilities accept new work for this project. It
    has the same entries as `GET /capabilities`, and answers each one as it
    does, except for capabilities a project can have when another can't:

    | ID | Available for this project when |
    | --- | --- |
    | `lavaflow` | LavaFlow is released, offered to the project's owner, and included in the owner's
    plan |
    | `lavaflow.merge` | `lavaflow` is, and LavaFlow's merging is released in this environment |
    | `lavaflow.lineage` | `lavaflow` is, and fix lineage is released in this environment |
    | `lavaflow.code_quality` | `lavaflow` is, Code Quality is released in this environment, and the
    owner's plan allows Code Quality findings; with an allowance of 0 it is `unavailable` with `code`
    `plan_required` |
    | `lavaflow.slack` | `lavaflow` is, the Volcano Slack app is set up in this environment, and Slack
    reports have launched in it |

    Where `lavaflow` isn't available, a project with LavaFlow settings or
    runs lists it `read_only`: its LavaFlow reads answer, and its owner can
    turn LavaFlow off. A project without them lists it `unavailable`, with
    `code` `plan_required` when the owner's plan leaves LavaFlow out.

    Check it to decide what to offer for a project, instead of calling a
    route to see whether it fails. Project access tokens can read it,
    including read-only ones.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilityList | Error]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> CapabilityList | Error | None:
    """ List a project's capabilities

     Lists which product capabilities accept new work for this project. It
    has the same entries as `GET /capabilities`, and answers each one as it
    does, except for capabilities a project can have when another can't:

    | ID | Available for this project when |
    | --- | --- |
    | `lavaflow` | LavaFlow is released, offered to the project's owner, and included in the owner's
    plan |
    | `lavaflow.merge` | `lavaflow` is, and LavaFlow's merging is released in this environment |
    | `lavaflow.lineage` | `lavaflow` is, and fix lineage is released in this environment |
    | `lavaflow.code_quality` | `lavaflow` is, Code Quality is released in this environment, and the
    owner's plan allows Code Quality findings; with an allowance of 0 it is `unavailable` with `code`
    `plan_required` |
    | `lavaflow.slack` | `lavaflow` is, the Volcano Slack app is set up in this environment, and Slack
    reports have launched in it |

    Where `lavaflow` isn't available, a project with LavaFlow settings or
    runs lists it `read_only`: its LavaFlow reads answer, and its owner can
    turn LavaFlow off. A project without them lists it `unavailable`, with
    `code` `plan_required` when the owner's plan leaves LavaFlow out.

    Check it to decide what to offer for a project, instead of calling a
    route to see whether it fails. Project access tokens can read it,
    including read-only ones.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilityList | Error
     """


    return sync_detailed(
        id=id,
client=client,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> Response[CapabilityList | Error]:
    """ List a project's capabilities

     Lists which product capabilities accept new work for this project. It
    has the same entries as `GET /capabilities`, and answers each one as it
    does, except for capabilities a project can have when another can't:

    | ID | Available for this project when |
    | --- | --- |
    | `lavaflow` | LavaFlow is released, offered to the project's owner, and included in the owner's
    plan |
    | `lavaflow.merge` | `lavaflow` is, and LavaFlow's merging is released in this environment |
    | `lavaflow.lineage` | `lavaflow` is, and fix lineage is released in this environment |
    | `lavaflow.code_quality` | `lavaflow` is, Code Quality is released in this environment, and the
    owner's plan allows Code Quality findings; with an allowance of 0 it is `unavailable` with `code`
    `plan_required` |
    | `lavaflow.slack` | `lavaflow` is, the Volcano Slack app is set up in this environment, and Slack
    reports have launched in it |

    Where `lavaflow` isn't available, a project with LavaFlow settings or
    runs lists it `read_only`: its LavaFlow reads answer, and its owner can
    turn LavaFlow off. A project without them lists it `unavailable`, with
    `code` `plan_required` when the owner's plan leaves LavaFlow out.

    Check it to decide what to offer for a project, instead of calling a
    route to see whether it fails. Project access tokens can read it,
    including read-only ones.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilityList | Error]
     """


    kwargs = request_kwargs(
        id=id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,

) -> CapabilityList | Error | None:
    """ List a project's capabilities

     Lists which product capabilities accept new work for this project. It
    has the same entries as `GET /capabilities`, and answers each one as it
    does, except for capabilities a project can have when another can't:

    | ID | Available for this project when |
    | --- | --- |
    | `lavaflow` | LavaFlow is released, offered to the project's owner, and included in the owner's
    plan |
    | `lavaflow.merge` | `lavaflow` is, and LavaFlow's merging is released in this environment |
    | `lavaflow.lineage` | `lavaflow` is, and fix lineage is released in this environment |
    | `lavaflow.code_quality` | `lavaflow` is, Code Quality is released in this environment, and the
    owner's plan allows Code Quality findings; with an allowance of 0 it is `unavailable` with `code`
    `plan_required` |
    | `lavaflow.slack` | `lavaflow` is, the Volcano Slack app is set up in this environment, and Slack
    reports have launched in it |

    Where `lavaflow` isn't available, a project with LavaFlow settings or
    runs lists it `read_only`: its LavaFlow reads answer, and its owner can
    turn LavaFlow off. A project without them lists it `unavailable`, with
    `code` `plan_required` when the owner's plan leaves LavaFlow out.

    Check it to decide what to offer for a project, instead of calling a
    route to see whether it fails. Project access tokens can read it,
    including read-only ones.

    Args:
        id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilityList | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,

    )).parsed
