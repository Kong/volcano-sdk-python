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
    | `sandboxes.network_isolation` | Creating sessions and one-shot executions with `network.egress`
    `deny_all`; existing `deny_all` sessions work either way |
    | `sandboxes.output_not_kept` | Commands that keep no output: `keep_output: false` on a command, and
    `executions.keep_output: false` on a session; commands that keep output work either way |
    | `issues` | The Issues API: listing, reading, and updating grouped runtime errors |
    | `issues.create` | Writing an issue with `POST /issues`; written issues already recorded read and
    update either way |
    | `lavaflow` | LavaFlow, which diagnoses a project's issues and opens pull requests that fix them.
    Here it reports only whether LavaFlow is released in this environment; whether a project has it
    comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.merge` | LavaFlow merging its fixes, with `autonomy: merge`. Here it reports only
    whether merging is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.lineage` | LavaFlow following up its fixes: linking a fix's recurrence or a new issue
    its deploy caused to the fix, the follow-up runs, and the lineage holds. Here it reports only
    whether fix lineage is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.open_pr_ci_start` | A fix a person merges, as under `autonomy: open_pr`, opening ready
    for review with LavaFlow running its CI once, unless the repository may run CI outside GitHub
    Actions; unavailable, such a fix opens as a draft whose commit skips CI. Here it reports only
    whether this is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.code_quality` | LavaFlow Code Quality, which reviews the code each frontend production
    deploy changes. Here it reports only whether Code Quality is released in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.slack` | Reporting problems to LavaFlow from Slack: installing the Volcano Slack app,
    connecting Slack identities, and binding channels to projects. Here it reports whether LavaFlow is
    released, the Slack app is set up, and Slack reports have launched in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.aikido` | LavaFlow fixing the security issues Aikido finds: connecting an Aikido
    workspace and binding projects to it. Here it reports whether LavaFlow is released and Aikido
    reports have launched in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `functions.response_streaming` | Streaming an HTTP-mode function's response on its own URL as the
    function writes it |
    | `frontend_routes` | Creating and changing Frontend routes; listing, deleting, and serving existing
    ones work either way |
    | `frontends.candidates` | Creating, redeploying, promoting and rolling back to a frontend
    Candidate; reading, deleting and rolling back to the frontend's own runtime always work |
    | `databases.migrations` | Starting migration runs and recording a baseline; reading history and
    runs works either way |
    | `shares` | Creating, switching on and publishing shares, and forking one |
    | `ai_gateway` | The Volcano AI gateway: creating a key that holds `ai.invoke` with `POST
    /projects/{id}/service-keys`, and minting the first run token of a run; reading, regenerating and
    deleting existing keys, and reading, extending, revoking and minting again for a run already minted
    for, work either way |
    | `realtime.http_publish` | Publishing a message with `POST /realtime/v1/publish`; while Realtime is
    paused it stays available, and the route answers `503` `feature_paused` |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer; `GET /projects/{id}/capabilities`
    answers for one project.

    `functions.response_streaming` refuses nothing: while it is unavailable, a
    function's own URL still answers and sends a streamed response whole, once
    the function finishes, up to 6 MiB with headers; a larger one fails the
    invocation. Frontend Function routes stream either way.

    After these, the list names each first-party app Volcano runs in this
    environment, such as `builder`, by its own ID. Such an app is available
    while it accepts new work. When only the app's own release is off, work
    it already accepted continues; when first-party app mounts are off, its
    mount refuses every request with 404 `feature_unavailable`.

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
    | `sandboxes.network_isolation` | Creating sessions and one-shot executions with `network.egress`
    `deny_all`; existing `deny_all` sessions work either way |
    | `sandboxes.output_not_kept` | Commands that keep no output: `keep_output: false` on a command, and
    `executions.keep_output: false` on a session; commands that keep output work either way |
    | `issues` | The Issues API: listing, reading, and updating grouped runtime errors |
    | `issues.create` | Writing an issue with `POST /issues`; written issues already recorded read and
    update either way |
    | `lavaflow` | LavaFlow, which diagnoses a project's issues and opens pull requests that fix them.
    Here it reports only whether LavaFlow is released in this environment; whether a project has it
    comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.merge` | LavaFlow merging its fixes, with `autonomy: merge`. Here it reports only
    whether merging is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.lineage` | LavaFlow following up its fixes: linking a fix's recurrence or a new issue
    its deploy caused to the fix, the follow-up runs, and the lineage holds. Here it reports only
    whether fix lineage is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.open_pr_ci_start` | A fix a person merges, as under `autonomy: open_pr`, opening ready
    for review with LavaFlow running its CI once, unless the repository may run CI outside GitHub
    Actions; unavailable, such a fix opens as a draft whose commit skips CI. Here it reports only
    whether this is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.code_quality` | LavaFlow Code Quality, which reviews the code each frontend production
    deploy changes. Here it reports only whether Code Quality is released in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.slack` | Reporting problems to LavaFlow from Slack: installing the Volcano Slack app,
    connecting Slack identities, and binding channels to projects. Here it reports whether LavaFlow is
    released, the Slack app is set up, and Slack reports have launched in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.aikido` | LavaFlow fixing the security issues Aikido finds: connecting an Aikido
    workspace and binding projects to it. Here it reports whether LavaFlow is released and Aikido
    reports have launched in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `functions.response_streaming` | Streaming an HTTP-mode function's response on its own URL as the
    function writes it |
    | `frontend_routes` | Creating and changing Frontend routes; listing, deleting, and serving existing
    ones work either way |
    | `frontends.candidates` | Creating, redeploying, promoting and rolling back to a frontend
    Candidate; reading, deleting and rolling back to the frontend's own runtime always work |
    | `databases.migrations` | Starting migration runs and recording a baseline; reading history and
    runs works either way |
    | `shares` | Creating, switching on and publishing shares, and forking one |
    | `ai_gateway` | The Volcano AI gateway: creating a key that holds `ai.invoke` with `POST
    /projects/{id}/service-keys`, and minting the first run token of a run; reading, regenerating and
    deleting existing keys, and reading, extending, revoking and minting again for a run already minted
    for, work either way |
    | `realtime.http_publish` | Publishing a message with `POST /realtime/v1/publish`; while Realtime is
    paused it stays available, and the route answers `503` `feature_paused` |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer; `GET /projects/{id}/capabilities`
    answers for one project.

    `functions.response_streaming` refuses nothing: while it is unavailable, a
    function's own URL still answers and sends a streamed response whole, once
    the function finishes, up to 6 MiB with headers; a larger one fails the
    invocation. Frontend Function routes stream either way.

    After these, the list names each first-party app Volcano runs in this
    environment, such as `builder`, by its own ID. Such an app is available
    while it accepts new work. When only the app's own release is off, work
    it already accepted continues; when first-party app mounts are off, its
    mount refuses every request with 404 `feature_unavailable`.

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
    | `sandboxes.network_isolation` | Creating sessions and one-shot executions with `network.egress`
    `deny_all`; existing `deny_all` sessions work either way |
    | `sandboxes.output_not_kept` | Commands that keep no output: `keep_output: false` on a command, and
    `executions.keep_output: false` on a session; commands that keep output work either way |
    | `issues` | The Issues API: listing, reading, and updating grouped runtime errors |
    | `issues.create` | Writing an issue with `POST /issues`; written issues already recorded read and
    update either way |
    | `lavaflow` | LavaFlow, which diagnoses a project's issues and opens pull requests that fix them.
    Here it reports only whether LavaFlow is released in this environment; whether a project has it
    comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.merge` | LavaFlow merging its fixes, with `autonomy: merge`. Here it reports only
    whether merging is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.lineage` | LavaFlow following up its fixes: linking a fix's recurrence or a new issue
    its deploy caused to the fix, the follow-up runs, and the lineage holds. Here it reports only
    whether fix lineage is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.open_pr_ci_start` | A fix a person merges, as under `autonomy: open_pr`, opening ready
    for review with LavaFlow running its CI once, unless the repository may run CI outside GitHub
    Actions; unavailable, such a fix opens as a draft whose commit skips CI. Here it reports only
    whether this is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.code_quality` | LavaFlow Code Quality, which reviews the code each frontend production
    deploy changes. Here it reports only whether Code Quality is released in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.slack` | Reporting problems to LavaFlow from Slack: installing the Volcano Slack app,
    connecting Slack identities, and binding channels to projects. Here it reports whether LavaFlow is
    released, the Slack app is set up, and Slack reports have launched in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.aikido` | LavaFlow fixing the security issues Aikido finds: connecting an Aikido
    workspace and binding projects to it. Here it reports whether LavaFlow is released and Aikido
    reports have launched in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `functions.response_streaming` | Streaming an HTTP-mode function's response on its own URL as the
    function writes it |
    | `frontend_routes` | Creating and changing Frontend routes; listing, deleting, and serving existing
    ones work either way |
    | `frontends.candidates` | Creating, redeploying, promoting and rolling back to a frontend
    Candidate; reading, deleting and rolling back to the frontend's own runtime always work |
    | `databases.migrations` | Starting migration runs and recording a baseline; reading history and
    runs works either way |
    | `shares` | Creating, switching on and publishing shares, and forking one |
    | `ai_gateway` | The Volcano AI gateway: creating a key that holds `ai.invoke` with `POST
    /projects/{id}/service-keys`, and minting the first run token of a run; reading, regenerating and
    deleting existing keys, and reading, extending, revoking and minting again for a run already minted
    for, work either way |
    | `realtime.http_publish` | Publishing a message with `POST /realtime/v1/publish`; while Realtime is
    paused it stays available, and the route answers `503` `feature_paused` |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer; `GET /projects/{id}/capabilities`
    answers for one project.

    `functions.response_streaming` refuses nothing: while it is unavailable, a
    function's own URL still answers and sends a streamed response whole, once
    the function finishes, up to 6 MiB with headers; a larger one fails the
    invocation. Frontend Function routes stream either way.

    After these, the list names each first-party app Volcano runs in this
    environment, such as `builder`, by its own ID. Such an app is available
    while it accepts new work. When only the app's own release is off, work
    it already accepted continues; when first-party app mounts are off, its
    mount refuses every request with 404 `feature_unavailable`.

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
    | `sandboxes.network_isolation` | Creating sessions and one-shot executions with `network.egress`
    `deny_all`; existing `deny_all` sessions work either way |
    | `sandboxes.output_not_kept` | Commands that keep no output: `keep_output: false` on a command, and
    `executions.keep_output: false` on a session; commands that keep output work either way |
    | `issues` | The Issues API: listing, reading, and updating grouped runtime errors |
    | `issues.create` | Writing an issue with `POST /issues`; written issues already recorded read and
    update either way |
    | `lavaflow` | LavaFlow, which diagnoses a project's issues and opens pull requests that fix them.
    Here it reports only whether LavaFlow is released in this environment; whether a project has it
    comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.merge` | LavaFlow merging its fixes, with `autonomy: merge`. Here it reports only
    whether merging is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.lineage` | LavaFlow following up its fixes: linking a fix's recurrence or a new issue
    its deploy caused to the fix, the follow-up runs, and the lineage holds. Here it reports only
    whether fix lineage is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.open_pr_ci_start` | A fix a person merges, as under `autonomy: open_pr`, opening ready
    for review with LavaFlow running its CI once, unless the repository may run CI outside GitHub
    Actions; unavailable, such a fix opens as a draft whose commit skips CI. Here it reports only
    whether this is released in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `lavaflow.code_quality` | LavaFlow Code Quality, which reviews the code each frontend production
    deploy changes. Here it reports only whether Code Quality is released in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.slack` | Reporting problems to LavaFlow from Slack: installing the Volcano Slack app,
    connecting Slack identities, and binding channels to projects. Here it reports whether LavaFlow is
    released, the Slack app is set up, and Slack reports have launched in this environment; whether a
    project has it comes from `GET /projects/{id}/capabilities` |
    | `lavaflow.aikido` | LavaFlow fixing the security issues Aikido finds: connecting an Aikido
    workspace and binding projects to it. Here it reports whether LavaFlow is released and Aikido
    reports have launched in this environment; whether a project has it comes from `GET
    /projects/{id}/capabilities` |
    | `functions.response_streaming` | Streaming an HTTP-mode function's response on its own URL as the
    function writes it |
    | `frontend_routes` | Creating and changing Frontend routes; listing, deleting, and serving existing
    ones work either way |
    | `frontends.candidates` | Creating, redeploying, promoting and rolling back to a frontend
    Candidate; reading, deleting and rolling back to the frontend's own runtime always work |
    | `databases.migrations` | Starting migration runs and recording a baseline; reading history and
    runs works either way |
    | `shares` | Creating, switching on and publishing shares, and forking one |
    | `ai_gateway` | The Volcano AI gateway: creating a key that holds `ai.invoke` with `POST
    /projects/{id}/service-keys`, and minting the first run token of a run; reading, regenerating and
    deleting existing keys, and reading, extending, revoking and minting again for a run already minted
    for, work either way |
    | `realtime.http_publish` | Publishing a message with `POST /realtime/v1/publish`; while Realtime is
    paused it stays available, and the route answers `503` `feature_paused` |

    A capability missing from the list is unavailable, and a capability under
    another, such as `sandboxes.sessions`, is unavailable whenever its parent is.
    While a capability is unavailable, requests that start new work answer `404`
    or `400` with code `feature_unavailable`; refresh this list when you receive
    that code. Reading, deleting, and terminating what already exists keep
    working unless the whole feature is absent from the environment. Every caller
    in an environment gets the same answer; `GET /projects/{id}/capabilities`
    answers for one project.

    `functions.response_streaming` refuses nothing: while it is unavailable, a
    function's own URL still answers and sends a streamed response whole, once
    the function finishes, up to 6 MiB with headers; a larger one fails the
    invocation. Frontend Function routes stream either way.

    After these, the list names each first-party app Volcano runs in this
    environment, such as `builder`, by its own ID. Such an app is available
    while it accepts new work. When only the app's own release is off, work
    it already accepted continues; when first-party app mounts are off, its
    mount refuses every request with 404 `feature_unavailable`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CapabilityList
     """


    return (await asyncio_detailed(
        client=client,

    )).parsed
