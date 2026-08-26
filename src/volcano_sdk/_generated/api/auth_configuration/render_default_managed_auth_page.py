from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.render_default_managed_auth_page_action import check_render_default_managed_auth_page_action
from ...models.render_default_managed_auth_page_action import RenderDefaultManagedAuthPageAction
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    action: RenderDefaultManagedAuthPageAction | Unset = UNSET,
    user_code: str | Unset = UNSET,
    anon_key: str | Unset = UNSET,
    state: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_action: str | Unset = UNSET
    if not isinstance(action, Unset):
        json_action = action

    params["action"] = json_action

    params["user_code"] = user_code

    params["anon_key"] = anon_key

    params["state"] = state


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/auth/hosted".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | str | None:
    if response.status_code == 200:
        response_200 = response.text
        return response_200

    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400

    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    action: RenderDefaultManagedAuthPageAction | Unset = UNSET,
    user_code: str | Unset = UNSET,
    anon_key: str | Unset = UNSET,
    state: str | Unset = UNSET,

) -> Response[Any | str]:
    """ Render default managed auth page

     Public HTML endpoint for the managed login page.
    Requires `Accept: text/html`.

    Args:
        id (UUID):
        action (RenderDefaultManagedAuthPageAction | Unset):
        user_code (str | Unset):
        anon_key (str | Unset):
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | str]
     """


    kwargs = _get_kwargs(
        id=id,
action=action,
user_code=user_code,
anon_key=anon_key,
state=state,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    action: RenderDefaultManagedAuthPageAction | Unset = UNSET,
    user_code: str | Unset = UNSET,
    anon_key: str | Unset = UNSET,
    state: str | Unset = UNSET,

) -> Any | str | None:
    """ Render default managed auth page

     Public HTML endpoint for the managed login page.
    Requires `Accept: text/html`.

    Args:
        id (UUID):
        action (RenderDefaultManagedAuthPageAction | Unset):
        user_code (str | Unset):
        anon_key (str | Unset):
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | str
     """


    return sync_detailed(
        id=id,
client=client,
action=action,
user_code=user_code,
anon_key=anon_key,
state=state,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    action: RenderDefaultManagedAuthPageAction | Unset = UNSET,
    user_code: str | Unset = UNSET,
    anon_key: str | Unset = UNSET,
    state: str | Unset = UNSET,

) -> Response[Any | str]:
    """ Render default managed auth page

     Public HTML endpoint for the managed login page.
    Requires `Accept: text/html`.

    Args:
        id (UUID):
        action (RenderDefaultManagedAuthPageAction | Unset):
        user_code (str | Unset):
        anon_key (str | Unset):
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | str]
     """


    kwargs = _get_kwargs(
        id=id,
action=action,
user_code=user_code,
anon_key=anon_key,
state=state,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient | Client,
    action: RenderDefaultManagedAuthPageAction | Unset = UNSET,
    user_code: str | Unset = UNSET,
    anon_key: str | Unset = UNSET,
    state: str | Unset = UNSET,

) -> Any | str | None:
    """ Render default managed auth page

     Public HTML endpoint for the managed login page.
    Requires `Accept: text/html`.

    Args:
        id (UUID):
        action (RenderDefaultManagedAuthPageAction | Unset):
        user_code (str | Unset):
        anon_key (str | Unset):
        state (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | str
     """


    return (await asyncio_detailed(
        id=id,
client=client,
action=action,
user_code=user_code,
anon_key=anon_key,
state=state,

    )).parsed
