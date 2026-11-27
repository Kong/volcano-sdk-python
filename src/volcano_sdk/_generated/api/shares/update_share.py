from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.share import Share
from ...models.share_update_request import ShareUpdateRequest
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def request_kwargs(
    share_id: str,
    *,
    body: ShareUpdateRequest,
    project_id: UUID | str | Unset = UNSET,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    json_project_id: str | Unset = UNSET
    if not isinstance(project_id, Unset):
        json_project_id = str(project_id)
    params["project_id"] = json_project_id


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/shares/{share_id}".format(share_id=quote(str(share_id), safe=""),),
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | Share | None:
    if response.status_code == 200:
        response_200 = Share.from_dict(response.json())



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

    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())



        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | Share]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient,
    body: ShareUpdateRequest,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | Share]:
    """ Edit or switch a deploy link on or off

     Changes the suggested name, the status, or both. An owner can always switch a
    link off: it works even while deploy links are not available in this
    environment, and while the owner's account is read-only. Setting
    `allow_reshare` to false also works in both cases, alone or with a
    switch-off, since like a switch-off it only shares less; for a read-only
    account these are the only changes allowed. While deploy links are not
    available, a request that sends back the values the link already has,
    including `status` `active` on an active link, changes nothing and answers
    `200`.

    Switching a link off also stops the installs it started that have not
    finished, including ones still queued: each fails at its next step. The
    visitor keeps the project, with its installation failed. Switching the link
    back on lets only installs that have not failed yet go ahead.

    A link Volcano took down (`disabled_reason` `operator`) cannot be switched
    back on; other edits still work, and it stays down. While any of the
    project's links is taken down, no link of the project can be switched on or
    allowed to be re-shared.

    A request that switches the link off together with an edit while deploy links
    are not available, or that also allows re-sharing on a copy whose source does
    not allow it, still switches the link off, but answers `400` with code
    `edit_dropped`: the link is off and the edit was not applied. While the
    account is read-only, a request that switches the link off or sets
    `allow_reshare` to false together with another edit is answered the same way:
    the switch-off and the re-sharing change are saved, and the other edit is not.
    A `status` the link already has is no edit, so sending the fetched link back
    with `allow_reshare` false answers `200`; a switch-on is such another edit.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        body (ShareUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Share]
     """


    kwargs = request_kwargs(
        share_id=share_id,
body=body,
project_id=project_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    share_id: str,
    *,
    client: AuthenticatedClient,
    body: ShareUpdateRequest,
    project_id: UUID | str | Unset = UNSET,

) -> Error | Share | None:
    """ Edit or switch a deploy link on or off

     Changes the suggested name, the status, or both. An owner can always switch a
    link off: it works even while deploy links are not available in this
    environment, and while the owner's account is read-only. Setting
    `allow_reshare` to false also works in both cases, alone or with a
    switch-off, since like a switch-off it only shares less; for a read-only
    account these are the only changes allowed. While deploy links are not
    available, a request that sends back the values the link already has,
    including `status` `active` on an active link, changes nothing and answers
    `200`.

    Switching a link off also stops the installs it started that have not
    finished, including ones still queued: each fails at its next step. The
    visitor keeps the project, with its installation failed. Switching the link
    back on lets only installs that have not failed yet go ahead.

    A link Volcano took down (`disabled_reason` `operator`) cannot be switched
    back on; other edits still work, and it stays down. While any of the
    project's links is taken down, no link of the project can be switched on or
    allowed to be re-shared.

    A request that switches the link off together with an edit while deploy links
    are not available, or that also allows re-sharing on a copy whose source does
    not allow it, still switches the link off, but answers `400` with code
    `edit_dropped`: the link is off and the edit was not applied. While the
    account is read-only, a request that switches the link off or sets
    `allow_reshare` to false together with another edit is answered the same way:
    the switch-off and the re-sharing change are saved, and the other edit is not.
    A `status` the link already has is no edit, so sending the fetched link back
    with `allow_reshare` false answers `200`; a switch-on is such another edit.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        body (ShareUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Share
     """


    return sync_detailed(
        share_id=share_id,
client=client,
body=body,
project_id=project_id,

    ).parsed

async def asyncio_detailed(
    share_id: str,
    *,
    client: AuthenticatedClient,
    body: ShareUpdateRequest,
    project_id: UUID | str | Unset = UNSET,

) -> Response[Error | Share]:
    """ Edit or switch a deploy link on or off

     Changes the suggested name, the status, or both. An owner can always switch a
    link off: it works even while deploy links are not available in this
    environment, and while the owner's account is read-only. Setting
    `allow_reshare` to false also works in both cases, alone or with a
    switch-off, since like a switch-off it only shares less; for a read-only
    account these are the only changes allowed. While deploy links are not
    available, a request that sends back the values the link already has,
    including `status` `active` on an active link, changes nothing and answers
    `200`.

    Switching a link off also stops the installs it started that have not
    finished, including ones still queued: each fails at its next step. The
    visitor keeps the project, with its installation failed. Switching the link
    back on lets only installs that have not failed yet go ahead.

    A link Volcano took down (`disabled_reason` `operator`) cannot be switched
    back on; other edits still work, and it stays down. While any of the
    project's links is taken down, no link of the project can be switched on or
    allowed to be re-shared.

    A request that switches the link off together with an edit while deploy links
    are not available, or that also allows re-sharing on a copy whose source does
    not allow it, still switches the link off, but answers `400` with code
    `edit_dropped`: the link is off and the edit was not applied. While the
    account is read-only, a request that switches the link off or sets
    `allow_reshare` to false together with another edit is answered the same way:
    the switch-off and the re-sharing change are saved, and the other edit is not.
    A `status` the link already has is no edit, so sending the fetched link back
    with `allow_reshare` false answers `200`; a switch-on is such another edit.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        body (ShareUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | Share]
     """


    kwargs = request_kwargs(
        share_id=share_id,
body=body,
project_id=project_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    share_id: str,
    *,
    client: AuthenticatedClient,
    body: ShareUpdateRequest,
    project_id: UUID | str | Unset = UNSET,

) -> Error | Share | None:
    """ Edit or switch a deploy link on or off

     Changes the suggested name, the status, or both. An owner can always switch a
    link off: it works even while deploy links are not available in this
    environment, and while the owner's account is read-only. Setting
    `allow_reshare` to false also works in both cases, alone or with a
    switch-off, since like a switch-off it only shares less; for a read-only
    account these are the only changes allowed. While deploy links are not
    available, a request that sends back the values the link already has,
    including `status` `active` on an active link, changes nothing and answers
    `200`.

    Switching a link off also stops the installs it started that have not
    finished, including ones still queued: each fails at its next step. The
    visitor keeps the project, with its installation failed. Switching the link
    back on lets only installs that have not failed yet go ahead.

    A link Volcano took down (`disabled_reason` `operator`) cannot be switched
    back on; other edits still work, and it stays down. While any of the
    project's links is taken down, no link of the project can be switched on or
    allowed to be re-shared.

    A request that switches the link off together with an edit while deploy links
    are not available, or that also allows re-sharing on a copy whose source does
    not allow it, still switches the link off, but answers `400` with code
    `edit_dropped`: the link is off and the edit was not applied. While the
    account is read-only, a request that switches the link off or sets
    `allow_reshare` to false together with another edit is answered the same way:
    the switch-off and the re-sharing change are saved, and the other edit is not.
    A `status` the link already has is no edit, so sending the fetched link back
    with `allow_reshare` false answers `200`; a switch-on is such another edit.

    Args:
        share_id (str):
        project_id (UUID | Unset):
        body (ShareUpdateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | Share
     """


    return (await asyncio_detailed(
        share_id=share_id,
client=client,
body=body,
project_id=project_id,

    )).parsed
