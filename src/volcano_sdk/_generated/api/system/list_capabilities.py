from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.capability_list import CapabilityList
from typing import cast



def request_kwargs(
    
) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/capabilities",
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> CapabilityList | None:
    if response.status_code == 200:
        response_200 = CapabilityList.from_dict(response.json())



        return response_200

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[CapabilityList]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[CapabilityList]:
    """ List capabilities

     Lists which product capabilities accept new work in this environment. Check it
    to decide what to offer, instead of calling a route to see whether it fails.

    | ID | Covers |
    | --- | --- |
    | `sandboxes` | The Sandbox API: presets, templates, sessions, and executions |
    | `sandboxes.sessions` | Starting and resuming sessions, and one-shot executions |
    | `sandboxes.custom_templates` | Deploying a custom template; its validation waits while
    `sandboxes.sessions` is unavailable |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilityList]
     """


    kwargs = request_kwargs(
        
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,

) -> CapabilityList | None:
    """ List capabilities

     Lists which product capabilities accept new work in this environment. Check it
    to decide what to offer, instead of calling a route to see whether it fails.

    | ID | Covers |
    | --- | --- |
    | `sandboxes` | The Sandbox API: presets, templates, sessions, and executions |
    | `sandboxes.sessions` | Starting and resuming sessions, and one-shot executions |
    | `sandboxes.custom_templates` | Deploying a custom template; its validation waits while
    `sandboxes.sessions` is unavailable |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilityList
     """


    return sync_detailed(
        client=client,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,

) -> Response[CapabilityList]:
    """ List capabilities

     Lists which product capabilities accept new work in this environment. Check it
    to decide what to offer, instead of calling a route to see whether it fails.

    | ID | Covers |
    | --- | --- |
    | `sandboxes` | The Sandbox API: presets, templates, sessions, and executions |
    | `sandboxes.sessions` | Starting and resuming sessions, and one-shot executions |
    | `sandboxes.custom_templates` | Deploying a custom template; its validation waits while
    `sandboxes.sessions` is unavailable |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CapabilityList]
     """


    kwargs = request_kwargs(
        
    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,

) -> CapabilityList | None:
    """ List capabilities

     Lists which product capabilities accept new work in this environment. Check it
    to decide what to offer, instead of calling a route to see whether it fails.

    | ID | Covers |
    | --- | --- |
    | `sandboxes` | The Sandbox API: presets, templates, sessions, and executions |
    | `sandboxes.sessions` | Starting and resuming sessions, and one-shot executions |
    | `sandboxes.custom_templates` | Deploying a custom template; its validation waits while
    `sandboxes.sessions` is unavailable |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilityList
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
