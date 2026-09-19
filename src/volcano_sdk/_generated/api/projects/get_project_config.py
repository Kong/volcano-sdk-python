from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.get_project_config_format import check_get_project_config_format
from ...models.get_project_config_format import GetProjectConfigFormat
from ...models.project_config import ProjectConfig
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    format_: GetProjectConfigFormat | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_format_: str | Unset = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_

    params["format"] = json_format_


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/projects/{id}/config".format(id=quote(str(id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectConfig | None:
    if response.status_code == 200:
        response_200 = ProjectConfig.from_dict(response.json())



        return response_200

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectConfig]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    format_: GetProjectConfigFormat | Unset = UNSET,

) -> Response[Error | ProjectConfig]:
    """ Export project configuration

     Exports the project's current user-facing configuration as a
    declarative manifest. Returns JSON by default. Request the canonical
    volcano-config.yaml rendering with `Accept: application/yaml` or
    `?format=yaml`; the YAML is returned verbatim as the raw response body
    (`Content-Type: application/yaml`) and is meant to be saved as-is.
    Variable values and write-only secrets (SMTP password, OAuth client secrets, TLS material)
    are omitted from the export; shared_variables contains names only; the YAML rendering adds a header
    comment
    describing how to set them via CLI environment interpolation.

    Args:
        id (UUID):
        format_ (GetProjectConfigFormat | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectConfig]
     """


    kwargs = _get_kwargs(
        id=id,
format_=format_,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    format_: GetProjectConfigFormat | Unset = UNSET,

) -> Error | ProjectConfig | None:
    """ Export project configuration

     Exports the project's current user-facing configuration as a
    declarative manifest. Returns JSON by default. Request the canonical
    volcano-config.yaml rendering with `Accept: application/yaml` or
    `?format=yaml`; the YAML is returned verbatim as the raw response body
    (`Content-Type: application/yaml`) and is meant to be saved as-is.
    Variable values and write-only secrets (SMTP password, OAuth client secrets, TLS material)
    are omitted from the export; shared_variables contains names only; the YAML rendering adds a header
    comment
    describing how to set them via CLI environment interpolation.

    Args:
        id (UUID):
        format_ (GetProjectConfigFormat | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectConfig
     """


    return sync_detailed(
        id=id,
client=client,
format_=format_,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    format_: GetProjectConfigFormat | Unset = UNSET,

) -> Response[Error | ProjectConfig]:
    """ Export project configuration

     Exports the project's current user-facing configuration as a
    declarative manifest. Returns JSON by default. Request the canonical
    volcano-config.yaml rendering with `Accept: application/yaml` or
    `?format=yaml`; the YAML is returned verbatim as the raw response body
    (`Content-Type: application/yaml`) and is meant to be saved as-is.
    Variable values and write-only secrets (SMTP password, OAuth client secrets, TLS material)
    are omitted from the export; shared_variables contains names only; the YAML rendering adds a header
    comment
    describing how to set them via CLI environment interpolation.

    Args:
        id (UUID):
        format_ (GetProjectConfigFormat | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectConfig]
     """


    kwargs = _get_kwargs(
        id=id,
format_=format_,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    format_: GetProjectConfigFormat | Unset = UNSET,

) -> Error | ProjectConfig | None:
    """ Export project configuration

     Exports the project's current user-facing configuration as a
    declarative manifest. Returns JSON by default. Request the canonical
    volcano-config.yaml rendering with `Accept: application/yaml` or
    `?format=yaml`; the YAML is returned verbatim as the raw response body
    (`Content-Type: application/yaml`) and is meant to be saved as-is.
    Variable values and write-only secrets (SMTP password, OAuth client secrets, TLS material)
    are omitted from the export; shared_variables contains names only; the YAML rendering adds a header
    comment
    describing how to set them via CLI environment interpolation.

    Args:
        id (UUID):
        format_ (GetProjectConfigFormat | Unset):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectConfig
     """


    return (await asyncio_detailed(
        id=id,
client=client,
format_=format_,

    )).parsed
