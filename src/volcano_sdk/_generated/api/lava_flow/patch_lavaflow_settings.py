from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_settings import LavaflowSettings
from ...models.lavaflow_settings_update import LavaflowSettingsUpdate
from typing import cast



def request_kwargs(
    *,
    body: LavaflowSettingsUpdate,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/lavaflow/settings",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowSettings | None:
    if response.status_code == 200:
        response_200 = LavaflowSettings.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())



        return response_409

    if response.status_code == 413:
        response_413 = Error.from_dict(response.json())



        return response_413

    if response.status_code == 429:
        response_429 = Error.from_dict(response.json())



        return response_429

    if response.status_code == 503:
        response_503 = Error.from_dict(response.json())



        return response_503

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowSettings]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowSettingsUpdate,

) -> Response[Error | LavaflowSettings]:
    """ Update LavaFlow settings

     Changes the fields the request names for the project `project_id`
    names; an omitted field keeps its saved value, or its default when
    nothing is saved. `{"project_id": "…", "enabled": true}` turns LavaFlow
    on for every function, frontend and durable function in the project,
    and records the repository the project points at as the one LavaFlow
    works in. A request carrying `"enabled": true` is a turn-on, even while
    LavaFlow is on. When the project points at no repository at a turn-on,
    the first repository it connects afterwards is recorded. A request
    that omits `enabled` never changes which repository is recorded.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    Turning LavaFlow on, from off, also starts runs for up to 5 open issues
    with `exception: true` and an `event_count` of at least 2, last seen in
    the past 7 days, most recently seen first, leaving out any issue
    LavaFlow already ran; runs LavaFlow queued on its own and hasn't
    started count toward the 5. They start like any run LavaFlow starts on
    its own, up to 3 at once per project. Only the owner's save with a
    `volcano login` token whose sign-in is live, a live Volcano dashboard
    sign-in, or a platform token that expires, starts them; any other save turns LavaFlow on without
    them. A save while LavaFlow is on starts none, and neither
    does LavaFlow becoming available to the project.

    Only the project's owner can save, with a platform token or a live
    Volcano dashboard sign-in, while their account is active. A full-scope project access token can only
    turn
    settings off: a body with `project_id` and
    `"code_quality": {"enabled": false}`, each field spelled exactly and
    sent once, and nothing else. Any other
    body from a project access token, including one that turns a setting
    on, adds a field, sends `null`, or names a field the schema doesn't
    have, gets `403` with code `person_required`, as does a request made
    through MCP. A read-only project access token is refused as read-only
    first, without a code,
    and so is the owner of a read-only account.

    `code_quality.enabled: true` turns on LavaFlow Code Quality, which
    reviews the lines each production deploy of a frontend changes and
    turns what it confirms into issues and pull requests. Function deploys
    ask for no scan yet. It needs the project's `lavaflow.code_quality`
    capability: while Code Quality isn't released here the save answers
    `400` with code `feature_unavailable`, and while the owner's plan
    allows no Code Quality findings it answers `403` with code
    `plan_required`. Only the owner can turn it on, with the check below.
    Turning it off always works, and drops the deploys waiting to be
    scanned.

    `autonomy: merge` needs the project's `lavaflow.merge` capability.
    Without it, a save that sets `autonomy` to `merge`, or changes
    `merge_policy`, answers `400` with code `feature_unavailable`. A save
    that sends the saved values again passes this check, though it can
    still need the owner's check below, and a project at `merge` can
    still change to another autonomy. The save doesn't read the
    repository's branch rules: LavaFlow merges only into a base branch
    that requires at least one status check, and holds every fix with
    `no_required_checks` on any other.

    Changing `autonomy` to `merge` lets LavaFlow merge with no one else
    looking. So does turning `enabled` on while `autonomy` stays `merge`,
    and changing `merge_policy`, to any value, while `autonomy` is, or
    becomes, `merge`. Turning `allow_ungated_workflows` on lets LavaFlow
    open a fix where a workflow could run it with the repository's
    secrets before a person approves it. Turning `code_quality` on starts
    work on every frontend production deploy with no incident behind it.
    Only the owner can make these changes, with a credential of
    their own that expires: a `volcano login` token
    whose sign-in is live, a live Volcano dashboard sign-in, or a
    platform token with an expiry. The owner's
    GitHub account must also be able to push to the project's repository.
    A project access token, MCP, a platform token that never expires, a
    sign-in that ended, an owner who can't push, and a project with no
    repository get `403` with code `person_required`, and nothing is
    saved. Turning LavaFlow, `allow_ungated_workflows` or `code_quality`
    off needs no check.
    Nothing is saved either when the push check can't be answered (`429`
    or `503`, with `Retry-After`). When the project points at another
    repository, reaches its repository through another Volcano GitHub App
    installation, or points at none, `autonomy` changes from `merge` to
    `open_pr`; pointing back doesn't change it back. Reconnecting after a
    reinstall of the App counts as another installation.

    Turning LavaFlow on needs a plan that includes it (`403`, code
    `plan_required`). LavaFlow is available where the project's
    `lavaflow` capability is, which includes the owner's plan. Where it is
    not, a project with LavaFlow records can still turn LavaFlow, Code
    Quality or both off: a save that sends `enabled: false`,
    `code_quality: {enabled: false}` or both, and otherwise only
    `allow_ungated_workflows: false` sent with `enabled`. Any other save,
    and any save for a project without records, answers `404` with code
    `feature_unavailable` while LavaFlow is not offered to the project, and
    `403` with code `plan_required` when it is but the owner's plan does
    not include it.

    Args:
        body (LavaflowSettingsUpdate): The project, and at least one field to change. An omitted
            field keeps its saved value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSettings]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: LavaflowSettingsUpdate,

) -> Error | LavaflowSettings | None:
    """ Update LavaFlow settings

     Changes the fields the request names for the project `project_id`
    names; an omitted field keeps its saved value, or its default when
    nothing is saved. `{"project_id": "…", "enabled": true}` turns LavaFlow
    on for every function, frontend and durable function in the project,
    and records the repository the project points at as the one LavaFlow
    works in. A request carrying `"enabled": true` is a turn-on, even while
    LavaFlow is on. When the project points at no repository at a turn-on,
    the first repository it connects afterwards is recorded. A request
    that omits `enabled` never changes which repository is recorded.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    Turning LavaFlow on, from off, also starts runs for up to 5 open issues
    with `exception: true` and an `event_count` of at least 2, last seen in
    the past 7 days, most recently seen first, leaving out any issue
    LavaFlow already ran; runs LavaFlow queued on its own and hasn't
    started count toward the 5. They start like any run LavaFlow starts on
    its own, up to 3 at once per project. Only the owner's save with a
    `volcano login` token whose sign-in is live, a live Volcano dashboard
    sign-in, or a platform token that expires, starts them; any other save turns LavaFlow on without
    them. A save while LavaFlow is on starts none, and neither
    does LavaFlow becoming available to the project.

    Only the project's owner can save, with a platform token or a live
    Volcano dashboard sign-in, while their account is active. A full-scope project access token can only
    turn
    settings off: a body with `project_id` and
    `"code_quality": {"enabled": false}`, each field spelled exactly and
    sent once, and nothing else. Any other
    body from a project access token, including one that turns a setting
    on, adds a field, sends `null`, or names a field the schema doesn't
    have, gets `403` with code `person_required`, as does a request made
    through MCP. A read-only project access token is refused as read-only
    first, without a code,
    and so is the owner of a read-only account.

    `code_quality.enabled: true` turns on LavaFlow Code Quality, which
    reviews the lines each production deploy of a frontend changes and
    turns what it confirms into issues and pull requests. Function deploys
    ask for no scan yet. It needs the project's `lavaflow.code_quality`
    capability: while Code Quality isn't released here the save answers
    `400` with code `feature_unavailable`, and while the owner's plan
    allows no Code Quality findings it answers `403` with code
    `plan_required`. Only the owner can turn it on, with the check below.
    Turning it off always works, and drops the deploys waiting to be
    scanned.

    `autonomy: merge` needs the project's `lavaflow.merge` capability.
    Without it, a save that sets `autonomy` to `merge`, or changes
    `merge_policy`, answers `400` with code `feature_unavailable`. A save
    that sends the saved values again passes this check, though it can
    still need the owner's check below, and a project at `merge` can
    still change to another autonomy. The save doesn't read the
    repository's branch rules: LavaFlow merges only into a base branch
    that requires at least one status check, and holds every fix with
    `no_required_checks` on any other.

    Changing `autonomy` to `merge` lets LavaFlow merge with no one else
    looking. So does turning `enabled` on while `autonomy` stays `merge`,
    and changing `merge_policy`, to any value, while `autonomy` is, or
    becomes, `merge`. Turning `allow_ungated_workflows` on lets LavaFlow
    open a fix where a workflow could run it with the repository's
    secrets before a person approves it. Turning `code_quality` on starts
    work on every frontend production deploy with no incident behind it.
    Only the owner can make these changes, with a credential of
    their own that expires: a `volcano login` token
    whose sign-in is live, a live Volcano dashboard sign-in, or a
    platform token with an expiry. The owner's
    GitHub account must also be able to push to the project's repository.
    A project access token, MCP, a platform token that never expires, a
    sign-in that ended, an owner who can't push, and a project with no
    repository get `403` with code `person_required`, and nothing is
    saved. Turning LavaFlow, `allow_ungated_workflows` or `code_quality`
    off needs no check.
    Nothing is saved either when the push check can't be answered (`429`
    or `503`, with `Retry-After`). When the project points at another
    repository, reaches its repository through another Volcano GitHub App
    installation, or points at none, `autonomy` changes from `merge` to
    `open_pr`; pointing back doesn't change it back. Reconnecting after a
    reinstall of the App counts as another installation.

    Turning LavaFlow on needs a plan that includes it (`403`, code
    `plan_required`). LavaFlow is available where the project's
    `lavaflow` capability is, which includes the owner's plan. Where it is
    not, a project with LavaFlow records can still turn LavaFlow, Code
    Quality or both off: a save that sends `enabled: false`,
    `code_quality: {enabled: false}` or both, and otherwise only
    `allow_ungated_workflows: false` sent with `enabled`. Any other save,
    and any save for a project without records, answers `404` with code
    `feature_unavailable` while LavaFlow is not offered to the project, and
    `403` with code `plan_required` when it is but the owner's plan does
    not include it.

    Args:
        body (LavaflowSettingsUpdate): The project, and at least one field to change. An omitted
            field keeps its saved value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSettings
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowSettingsUpdate,

) -> Response[Error | LavaflowSettings]:
    """ Update LavaFlow settings

     Changes the fields the request names for the project `project_id`
    names; an omitted field keeps its saved value, or its default when
    nothing is saved. `{"project_id": "…", "enabled": true}` turns LavaFlow
    on for every function, frontend and durable function in the project,
    and records the repository the project points at as the one LavaFlow
    works in. A request carrying `"enabled": true` is a turn-on, even while
    LavaFlow is on. When the project points at no repository at a turn-on,
    the first repository it connects afterwards is recorded. A request
    that omits `enabled` never changes which repository is recorded.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    Turning LavaFlow on, from off, also starts runs for up to 5 open issues
    with `exception: true` and an `event_count` of at least 2, last seen in
    the past 7 days, most recently seen first, leaving out any issue
    LavaFlow already ran; runs LavaFlow queued on its own and hasn't
    started count toward the 5. They start like any run LavaFlow starts on
    its own, up to 3 at once per project. Only the owner's save with a
    `volcano login` token whose sign-in is live, a live Volcano dashboard
    sign-in, or a platform token that expires, starts them; any other save turns LavaFlow on without
    them. A save while LavaFlow is on starts none, and neither
    does LavaFlow becoming available to the project.

    Only the project's owner can save, with a platform token or a live
    Volcano dashboard sign-in, while their account is active. A full-scope project access token can only
    turn
    settings off: a body with `project_id` and
    `"code_quality": {"enabled": false}`, each field spelled exactly and
    sent once, and nothing else. Any other
    body from a project access token, including one that turns a setting
    on, adds a field, sends `null`, or names a field the schema doesn't
    have, gets `403` with code `person_required`, as does a request made
    through MCP. A read-only project access token is refused as read-only
    first, without a code,
    and so is the owner of a read-only account.

    `code_quality.enabled: true` turns on LavaFlow Code Quality, which
    reviews the lines each production deploy of a frontend changes and
    turns what it confirms into issues and pull requests. Function deploys
    ask for no scan yet. It needs the project's `lavaflow.code_quality`
    capability: while Code Quality isn't released here the save answers
    `400` with code `feature_unavailable`, and while the owner's plan
    allows no Code Quality findings it answers `403` with code
    `plan_required`. Only the owner can turn it on, with the check below.
    Turning it off always works, and drops the deploys waiting to be
    scanned.

    `autonomy: merge` needs the project's `lavaflow.merge` capability.
    Without it, a save that sets `autonomy` to `merge`, or changes
    `merge_policy`, answers `400` with code `feature_unavailable`. A save
    that sends the saved values again passes this check, though it can
    still need the owner's check below, and a project at `merge` can
    still change to another autonomy. The save doesn't read the
    repository's branch rules: LavaFlow merges only into a base branch
    that requires at least one status check, and holds every fix with
    `no_required_checks` on any other.

    Changing `autonomy` to `merge` lets LavaFlow merge with no one else
    looking. So does turning `enabled` on while `autonomy` stays `merge`,
    and changing `merge_policy`, to any value, while `autonomy` is, or
    becomes, `merge`. Turning `allow_ungated_workflows` on lets LavaFlow
    open a fix where a workflow could run it with the repository's
    secrets before a person approves it. Turning `code_quality` on starts
    work on every frontend production deploy with no incident behind it.
    Only the owner can make these changes, with a credential of
    their own that expires: a `volcano login` token
    whose sign-in is live, a live Volcano dashboard sign-in, or a
    platform token with an expiry. The owner's
    GitHub account must also be able to push to the project's repository.
    A project access token, MCP, a platform token that never expires, a
    sign-in that ended, an owner who can't push, and a project with no
    repository get `403` with code `person_required`, and nothing is
    saved. Turning LavaFlow, `allow_ungated_workflows` or `code_quality`
    off needs no check.
    Nothing is saved either when the push check can't be answered (`429`
    or `503`, with `Retry-After`). When the project points at another
    repository, reaches its repository through another Volcano GitHub App
    installation, or points at none, `autonomy` changes from `merge` to
    `open_pr`; pointing back doesn't change it back. Reconnecting after a
    reinstall of the App counts as another installation.

    Turning LavaFlow on needs a plan that includes it (`403`, code
    `plan_required`). LavaFlow is available where the project's
    `lavaflow` capability is, which includes the owner's plan. Where it is
    not, a project with LavaFlow records can still turn LavaFlow, Code
    Quality or both off: a save that sends `enabled: false`,
    `code_quality: {enabled: false}` or both, and otherwise only
    `allow_ungated_workflows: false` sent with `enabled`. Any other save,
    and any save for a project without records, answers `404` with code
    `feature_unavailable` while LavaFlow is not offered to the project, and
    `403` with code `plan_required` when it is but the owner's plan does
    not include it.

    Args:
        body (LavaflowSettingsUpdate): The project, and at least one field to change. An omitted
            field keeps its saved value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowSettings]
     """


    kwargs = request_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: LavaflowSettingsUpdate,

) -> Error | LavaflowSettings | None:
    """ Update LavaFlow settings

     Changes the fields the request names for the project `project_id`
    names; an omitted field keeps its saved value, or its default when
    nothing is saved. `{"project_id": "…", "enabled": true}` turns LavaFlow
    on for every function, frontend and durable function in the project,
    and records the repository the project points at as the one LavaFlow
    works in. A request carrying `"enabled": true` is a turn-on, even while
    LavaFlow is on. When the project points at no repository at a turn-on,
    the first repository it connects afterwards is recorded. A request
    that omits `enabled` never changes which repository is recorded.
    LavaFlow sends this project's logs and source code to an AI service
    that Volcano operates.

    Turning LavaFlow on, from off, also starts runs for up to 5 open issues
    with `exception: true` and an `event_count` of at least 2, last seen in
    the past 7 days, most recently seen first, leaving out any issue
    LavaFlow already ran; runs LavaFlow queued on its own and hasn't
    started count toward the 5. They start like any run LavaFlow starts on
    its own, up to 3 at once per project. Only the owner's save with a
    `volcano login` token whose sign-in is live, a live Volcano dashboard
    sign-in, or a platform token that expires, starts them; any other save turns LavaFlow on without
    them. A save while LavaFlow is on starts none, and neither
    does LavaFlow becoming available to the project.

    Only the project's owner can save, with a platform token or a live
    Volcano dashboard sign-in, while their account is active. A full-scope project access token can only
    turn
    settings off: a body with `project_id` and
    `"code_quality": {"enabled": false}`, each field spelled exactly and
    sent once, and nothing else. Any other
    body from a project access token, including one that turns a setting
    on, adds a field, sends `null`, or names a field the schema doesn't
    have, gets `403` with code `person_required`, as does a request made
    through MCP. A read-only project access token is refused as read-only
    first, without a code,
    and so is the owner of a read-only account.

    `code_quality.enabled: true` turns on LavaFlow Code Quality, which
    reviews the lines each production deploy of a frontend changes and
    turns what it confirms into issues and pull requests. Function deploys
    ask for no scan yet. It needs the project's `lavaflow.code_quality`
    capability: while Code Quality isn't released here the save answers
    `400` with code `feature_unavailable`, and while the owner's plan
    allows no Code Quality findings it answers `403` with code
    `plan_required`. Only the owner can turn it on, with the check below.
    Turning it off always works, and drops the deploys waiting to be
    scanned.

    `autonomy: merge` needs the project's `lavaflow.merge` capability.
    Without it, a save that sets `autonomy` to `merge`, or changes
    `merge_policy`, answers `400` with code `feature_unavailable`. A save
    that sends the saved values again passes this check, though it can
    still need the owner's check below, and a project at `merge` can
    still change to another autonomy. The save doesn't read the
    repository's branch rules: LavaFlow merges only into a base branch
    that requires at least one status check, and holds every fix with
    `no_required_checks` on any other.

    Changing `autonomy` to `merge` lets LavaFlow merge with no one else
    looking. So does turning `enabled` on while `autonomy` stays `merge`,
    and changing `merge_policy`, to any value, while `autonomy` is, or
    becomes, `merge`. Turning `allow_ungated_workflows` on lets LavaFlow
    open a fix where a workflow could run it with the repository's
    secrets before a person approves it. Turning `code_quality` on starts
    work on every frontend production deploy with no incident behind it.
    Only the owner can make these changes, with a credential of
    their own that expires: a `volcano login` token
    whose sign-in is live, a live Volcano dashboard sign-in, or a
    platform token with an expiry. The owner's
    GitHub account must also be able to push to the project's repository.
    A project access token, MCP, a platform token that never expires, a
    sign-in that ended, an owner who can't push, and a project with no
    repository get `403` with code `person_required`, and nothing is
    saved. Turning LavaFlow, `allow_ungated_workflows` or `code_quality`
    off needs no check.
    Nothing is saved either when the push check can't be answered (`429`
    or `503`, with `Retry-After`). When the project points at another
    repository, reaches its repository through another Volcano GitHub App
    installation, or points at none, `autonomy` changes from `merge` to
    `open_pr`; pointing back doesn't change it back. Reconnecting after a
    reinstall of the App counts as another installation.

    Turning LavaFlow on needs a plan that includes it (`403`, code
    `plan_required`). LavaFlow is available where the project's
    `lavaflow` capability is, which includes the owner's plan. Where it is
    not, a project with LavaFlow records can still turn LavaFlow, Code
    Quality or both off: a save that sends `enabled: false`,
    `code_quality: {enabled: false}` or both, and otherwise only
    `allow_ungated_workflows: false` sent with `enabled`. Any other save,
    and any save for a project without records, answers `404` with code
    `feature_unavailable` while LavaFlow is not offered to the project, and
    `403` with code `plan_required` when it is but the owner's plan does
    not include it.

    Args:
        body (LavaflowSettingsUpdate): The project, and at least one field to change. An omitted
            field keeps its saved value.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowSettings
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
