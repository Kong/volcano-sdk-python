from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.import_provider import check_import_provider
from ...models.import_provider import ImportProvider
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    provider: ImportProvider,
    *,
    state: str,
    code: str | Unset = UNSET,
    error: str | Unset = UNSET,
    team_id: str | Unset = UNSET,
    configuration_id: str | Unset = UNSET,
    next_: str | Unset = UNSET,
    source: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["state"] = state

    params["code"] = code

    params["error"] = error

    params["teamId"] = team_id

    params["configurationId"] = configuration_id

    params["next"] = next_

    params["source"] = source


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/imports/{provider}/callback".format(provider=quote(str(provider), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 303:
        response_303 = cast(Any, None)
        return response_303

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient | Client,
    state: str,
    code: str | Unset = UNSET,
    error: str | Unset = UNSET,
    team_id: str | Unset = UNSET,
    configuration_id: str | Unset = UNSET,
    next_: str | Unset = UNSET,
    source: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ Complete a project import provider connection

     Public provider callback protected by signed state and the browser-binding
    cookie created by startImportConnect.

    Args:
        provider (ImportProvider):
        state (str):
        code (str | Unset):
        error (str | Unset):
        team_id (str | Unset):
        configuration_id (str | Unset):
        next_ (str | Unset):
        source (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
state=state,
code=code,
error=error,
team_id=team_id,
configuration_id=configuration_id,
next_=next_,
source=source,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient | Client,
    state: str,
    code: str | Unset = UNSET,
    error: str | Unset = UNSET,
    team_id: str | Unset = UNSET,
    configuration_id: str | Unset = UNSET,
    next_: str | Unset = UNSET,
    source: str | Unset = UNSET,

) -> Any | Error | None:
    """ Complete a project import provider connection

     Public provider callback protected by signed state and the browser-binding
    cookie created by startImportConnect.

    Args:
        provider (ImportProvider):
        state (str):
        code (str | Unset):
        error (str | Unset):
        team_id (str | Unset):
        configuration_id (str | Unset):
        next_ (str | Unset):
        source (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        provider=provider,
client=client,
state=state,
code=code,
error=error,
team_id=team_id,
configuration_id=configuration_id,
next_=next_,
source=source,

    ).parsed

async def asyncio_detailed(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient | Client,
    state: str,
    code: str | Unset = UNSET,
    error: str | Unset = UNSET,
    team_id: str | Unset = UNSET,
    configuration_id: str | Unset = UNSET,
    next_: str | Unset = UNSET,
    source: str | Unset = UNSET,

) -> Response[Any | Error]:
    """ Complete a project import provider connection

     Public provider callback protected by signed state and the browser-binding
    cookie created by startImportConnect.

    Args:
        provider (ImportProvider):
        state (str):
        code (str | Unset):
        error (str | Unset):
        team_id (str | Unset):
        configuration_id (str | Unset):
        next_ (str | Unset):
        source (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        provider=provider,
state=state,
code=code,
error=error,
team_id=team_id,
configuration_id=configuration_id,
next_=next_,
source=source,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    provider: ImportProvider,
    *,
    client: AuthenticatedClient | Client,
    state: str,
    code: str | Unset = UNSET,
    error: str | Unset = UNSET,
    team_id: str | Unset = UNSET,
    configuration_id: str | Unset = UNSET,
    next_: str | Unset = UNSET,
    source: str | Unset = UNSET,

) -> Any | Error | None:
    """ Complete a project import provider connection

     Public provider callback protected by signed state and the browser-binding
    cookie created by startImportConnect.

    Args:
        provider (ImportProvider):
        state (str):
        code (str | Unset):
        error (str | Unset):
        team_id (str | Unset):
        configuration_id (str | Unset):
        next_ (str | Unset):
        source (str | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        provider=provider,
client=client,
state=state,
code=code,
error=error,
team_id=team_id,
configuration_id=configuration_id,
next_=next_,
source=source,

    )).parsed
