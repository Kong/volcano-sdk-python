from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.autofix_settings import AutofixSettings
from ...models.error import Error
from ...models.update_autofix_settings_request import UpdateAutofixSettingsRequest
from typing import cast
from uuid import UUID



def request_kwargs(
    id: UUID | str,
    *,
    body: UpdateAutofixSettingsRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/projects/{id}/autofix".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> AutofixSettings | Error | None:
    if response.status_code == 200:
        response_200 = AutofixSettings.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 403:
        response_403 = Error.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

    if response.status_code == 501:
        response_501 = Error.from_dict(response.json())



        return response_501

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[AutofixSettings | Error]:
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
    body: UpdateAutofixSettingsRequest,

) -> Response[AutofixSettings | Error]:
    """ Save autofix settings

     Saves the project's autofix settings. An omitted `max_stage` or
    `auto_trigger` keeps its saved value, or takes its default when the
    project has no saved settings, so `{"enabled": true}` on a new project
    diagnoses every new or regressed issue and opens a draft pull request
    with each fix. Set `max_stage` and `auto_trigger` to stop at a diagnosis
    or to start runs only on request. Volcano picks the models a run uses.

    Project access tokens are refused. Autofix opens pull requests in the
    project's repository, so a person turns it on with a platform token.

    During the preview, turning autofix on needs the SUPERAGENT plan, and
    nothing is charged yet. Settings that are already on stay stored after
    a downgrade, and saving them again is not refused, but no run starts
    until the plan allows autofix again. Other saves need no plan.

    Where autofix is not available, a project with saved settings can
    still change them with `enabled: false`. Saving `enabled: true`
    answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        body (UpdateAutofixSettingsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixSettings | Error]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateAutofixSettingsRequest,

) -> AutofixSettings | Error | None:
    """ Save autofix settings

     Saves the project's autofix settings. An omitted `max_stage` or
    `auto_trigger` keeps its saved value, or takes its default when the
    project has no saved settings, so `{"enabled": true}` on a new project
    diagnoses every new or regressed issue and opens a draft pull request
    with each fix. Set `max_stage` and `auto_trigger` to stop at a diagnosis
    or to start runs only on request. Volcano picks the models a run uses.

    Project access tokens are refused. Autofix opens pull requests in the
    project's repository, so a person turns it on with a platform token.

    During the preview, turning autofix on needs the SUPERAGENT plan, and
    nothing is charged yet. Settings that are already on stay stored after
    a downgrade, and saving them again is not refused, but no run starts
    until the plan allows autofix again. Other saves need no plan.

    Where autofix is not available, a project with saved settings can
    still change them with `enabled: false`. Saving `enabled: true`
    answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        body (UpdateAutofixSettingsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixSettings | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateAutofixSettingsRequest,

) -> Response[AutofixSettings | Error]:
    """ Save autofix settings

     Saves the project's autofix settings. An omitted `max_stage` or
    `auto_trigger` keeps its saved value, or takes its default when the
    project has no saved settings, so `{"enabled": true}` on a new project
    diagnoses every new or regressed issue and opens a draft pull request
    with each fix. Set `max_stage` and `auto_trigger` to stop at a diagnosis
    or to start runs only on request. Volcano picks the models a run uses.

    Project access tokens are refused. Autofix opens pull requests in the
    project's repository, so a person turns it on with a platform token.

    During the preview, turning autofix on needs the SUPERAGENT plan, and
    nothing is charged yet. Settings that are already on stay stored after
    a downgrade, and saving them again is not refused, but no run starts
    until the plan allows autofix again. Other saves need no plan.

    Where autofix is not available, a project with saved settings can
    still change them with `enabled: false`. Saving `enabled: true`
    answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        body (UpdateAutofixSettingsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AutofixSettings | Error]
     """


    kwargs = request_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    id: UUID | str,
    *,
    client: AuthenticatedClient,
    body: UpdateAutofixSettingsRequest,

) -> AutofixSettings | Error | None:
    """ Save autofix settings

     Saves the project's autofix settings. An omitted `max_stage` or
    `auto_trigger` keeps its saved value, or takes its default when the
    project has no saved settings, so `{"enabled": true}` on a new project
    diagnoses every new or regressed issue and opens a draft pull request
    with each fix. Set `max_stage` and `auto_trigger` to stop at a diagnosis
    or to start runs only on request. Volcano picks the models a run uses.

    Project access tokens are refused. Autofix opens pull requests in the
    project's repository, so a person turns it on with a platform token.

    During the preview, turning autofix on needs the SUPERAGENT plan, and
    nothing is charged yet. Settings that are already on stay stored after
    a downgrade, and saving them again is not refused, but no run starts
    until the plan allows autofix again. Other saves need no plan.

    Where autofix is not available, a project with saved settings can
    still change them with `enabled: false`. Saving `enabled: true`
    answers `404` with code `feature_unavailable`.

    Args:
        id (UUID):
        body (UpdateAutofixSettingsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AutofixSettings | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
