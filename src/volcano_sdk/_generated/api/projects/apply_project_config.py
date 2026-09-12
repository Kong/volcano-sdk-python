from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.project_config import ProjectConfig
from ...models.project_config_apply_result import ProjectConfigApplyResult
from ...models.project_config_validation_error_response import ProjectConfigValidationErrorResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    id: UUID,
    *,
    body: ProjectConfig,
    dry_run: bool | Unset = False,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["dry_run"] = dry_run


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/config".format(id=quote(str(id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse | None:
    if response.status_code == 200:
        response_200 = ProjectConfigApplyResult.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 422:
        response_422 = ProjectConfigValidationErrorResponse.from_dict(response.json())



        return response_422

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse]:
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
    body: ProjectConfig,
    dry_run: bool | Unset = False,

) -> Response[Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse]:
    """ Apply project configuration

     Validates and applies a declarative configuration manifest to the
    project, reconciling each declared section and returning a per-resource
    report. Omitted sections are untouched. Declared collection keys
    (`variables`, `buckets[].policies`, `auth.providers.oauth`,
    `auth.email.templates`, `functions[].schedulers`) are fully synced:
    resources absent from the manifest are deleted. Functions, frontends,
    databases, and buckets are never created or deleted; manifest entries
    for resources that do not exist are skipped and reported in `skipped`,
    and existing resources missing from a declared section are reported in
    `missing`. Validation failures (including plan-gate violations) return
    422 and nothing is applied. Set `dry_run=true` to get the projected
    report without applying changes. Applies are serialized per project;
    a concurrent apply returns 409.

    Args:
        id (UUID):
        dry_run (bool | Unset):  Default: False.
        body (ProjectConfig): Declarative project configuration manifest (the JSON form of
            volcano-config.yaml). Omitted sections are left untouched. Within
            declared entries, omitted optional fields keep their current server
            values (patch semantics). Declared collection keys are fully synced to
            the manifest: `variables`, `buckets[].policies`, `auth.providers.oauth`,
            `auth.email.templates`, and `functions[].schedulers` are reconciled to
            exactly match, deleting resources absent from the manifest. Functions,
            frontends, databases, and buckets are never created or deleted through
            this manifest; entries referencing resources that do not exist are
            skipped and reported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,
dry_run=dry_run,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectConfig,
    dry_run: bool | Unset = False,

) -> Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse | None:
    """ Apply project configuration

     Validates and applies a declarative configuration manifest to the
    project, reconciling each declared section and returning a per-resource
    report. Omitted sections are untouched. Declared collection keys
    (`variables`, `buckets[].policies`, `auth.providers.oauth`,
    `auth.email.templates`, `functions[].schedulers`) are fully synced:
    resources absent from the manifest are deleted. Functions, frontends,
    databases, and buckets are never created or deleted; manifest entries
    for resources that do not exist are skipped and reported in `skipped`,
    and existing resources missing from a declared section are reported in
    `missing`. Validation failures (including plan-gate violations) return
    422 and nothing is applied. Set `dry_run=true` to get the projected
    report without applying changes. Applies are serialized per project;
    a concurrent apply returns 409.

    Args:
        id (UUID):
        dry_run (bool | Unset):  Default: False.
        body (ProjectConfig): Declarative project configuration manifest (the JSON form of
            volcano-config.yaml). Omitted sections are left untouched. Within
            declared entries, omitted optional fields keep their current server
            values (patch semantics). Declared collection keys are fully synced to
            the manifest: `variables`, `buckets[].policies`, `auth.providers.oauth`,
            `auth.email.templates`, and `functions[].schedulers` are reconciled to
            exactly match, deleting resources absent from the manifest. Functions,
            frontends, databases, and buckets are never created or deleted through
            this manifest; entries referencing resources that do not exist are
            skipped and reported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse
     """


    return sync_detailed(
        id=id,
client=client,
body=body,
dry_run=dry_run,

    ).parsed

async def asyncio_detailed(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectConfig,
    dry_run: bool | Unset = False,

) -> Response[Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse]:
    """ Apply project configuration

     Validates and applies a declarative configuration manifest to the
    project, reconciling each declared section and returning a per-resource
    report. Omitted sections are untouched. Declared collection keys
    (`variables`, `buckets[].policies`, `auth.providers.oauth`,
    `auth.email.templates`, `functions[].schedulers`) are fully synced:
    resources absent from the manifest are deleted. Functions, frontends,
    databases, and buckets are never created or deleted; manifest entries
    for resources that do not exist are skipped and reported in `skipped`,
    and existing resources missing from a declared section are reported in
    `missing`. Validation failures (including plan-gate violations) return
    422 and nothing is applied. Set `dry_run=true` to get the projected
    report without applying changes. Applies are serialized per project;
    a concurrent apply returns 409.

    Args:
        id (UUID):
        dry_run (bool | Unset):  Default: False.
        body (ProjectConfig): Declarative project configuration manifest (the JSON form of
            volcano-config.yaml). Omitted sections are left untouched. Within
            declared entries, omitted optional fields keep their current server
            values (patch semantics). Declared collection keys are fully synced to
            the manifest: `variables`, `buckets[].policies`, `auth.providers.oauth`,
            `auth.email.templates`, and `functions[].schedulers` are reconciled to
            exactly match, deleting resources absent from the manifest. Functions,
            frontends, databases, and buckets are never created or deleted through
            this manifest; entries referencing resources that do not exist are
            skipped and reported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,
dry_run=dry_run,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: UUID,
    *,
    client: AuthenticatedClient,
    body: ProjectConfig,
    dry_run: bool | Unset = False,

) -> Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse | None:
    """ Apply project configuration

     Validates and applies a declarative configuration manifest to the
    project, reconciling each declared section and returning a per-resource
    report. Omitted sections are untouched. Declared collection keys
    (`variables`, `buckets[].policies`, `auth.providers.oauth`,
    `auth.email.templates`, `functions[].schedulers`) are fully synced:
    resources absent from the manifest are deleted. Functions, frontends,
    databases, and buckets are never created or deleted; manifest entries
    for resources that do not exist are skipped and reported in `skipped`,
    and existing resources missing from a declared section are reported in
    `missing`. Validation failures (including plan-gate violations) return
    422 and nothing is applied. Set `dry_run=true` to get the projected
    report without applying changes. Applies are serialized per project;
    a concurrent apply returns 409.

    Args:
        id (UUID):
        dry_run (bool | Unset):  Default: False.
        body (ProjectConfig): Declarative project configuration manifest (the JSON form of
            volcano-config.yaml). Omitted sections are left untouched. Within
            declared entries, omitted optional fields keep their current server
            values (patch semantics). Declared collection keys are fully synced to
            the manifest: `variables`, `buckets[].policies`, `auth.providers.oauth`,
            `auth.email.templates`, and `functions[].schedulers` are reconciled to
            exactly match, deleting resources absent from the manifest. Functions,
            frontends, databases, and buckets are never created or deleted through
            this manifest; entries referencing resources that do not exist are
            skipped and reported.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ProjectConfigApplyResult | ProjectConfigValidationErrorResponse
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,
dry_run=dry_run,

    )).parsed
