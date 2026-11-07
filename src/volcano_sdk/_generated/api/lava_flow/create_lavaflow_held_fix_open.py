from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.lavaflow_held_fix_open import LavaflowHeldFixOpen
from ...models.lavaflow_run import LavaflowRun
from typing import cast



def request_kwargs(
    *,
    body: LavaflowHeldFixOpen,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/lavaflow/held-fix-opens",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | LavaflowRun | None:
    if response.status_code == 202:
        response_202 = LavaflowRun.from_dict(response.json())



        return response_202

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


def build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | LavaflowRun]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowHeldFixOpen,

) -> Response[Error | LavaflowRun]:
    """ Open a held LavaFlow fix

     Opens the pull request for a fix LavaFlow held because the
    repository's workflows could run it with the repository's secrets
    before a person approves it (`pull_request_skipped:
    ungated_workflows`). Read the run first: send its `id` as `run_id`,
    with the `diff_sha256` and `held_workflows.jobs_sha256` it served, to
    say you read that diff and that list of jobs. LavaFlow opens the fix it
    saved, exactly as reviewed, past those jobs only. It writes no new
    fix.

    Right before it queues the run, LavaFlow serves the diff again and
    reads the workflows again. A diff served differently since you read
    it, or a job list or a commit the workflows were read at that changed,
    answers `409` with code `run_changed`; read the run again, which lists
    what LavaFlow found. The response is the run, `202` while it is
    `queued`. LavaFlow reads the workflows again before it opens the pull
    request, and once more as it pushes the fix: a job you didn't read, a
    new commit on a branch the workflows were read on, even one that
    changes no job, or a production branch other than the one you read
    them on holds the fix again with a new list.

    Opening a fix lets its pull request open, nothing more. LavaFlow
    starts no CI on it and never merges it, as for every fix opened past
    ungated workflows; a person pushes to the branch or merges it. The
    pull request's description names who opened it and lists the jobs.
    One exception: when LavaFlow's read before the pull request opens
    finds no job that runs the fix before a person approves it, because
    the workflows were gated since you read them, the fix opens as any
    other fix and follows the project's merge settings. A run whose
    `held_workflows` lists no job opens the same way.

    Only the project's owner can open a fix, as a person, while their
    account is active: with a `volcano login` token
    whose sign-in is live, or a platform token that expires. Their GitHub
    account must be able to push to the project's repository. A project
    access token, a request made through MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Opening a fix uses one of the run's attempts: the
    attempt that opens it is one of the run's, so a run held again on its
    last attempt can't be opened again. It starts no new run and counts
    toward no run limit.

    Args:
        body (LavaflowHeldFixOpen): The project, the run, and the diff and jobs of the held fix
            you read, by the digests the run served them with.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
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
    body: LavaflowHeldFixOpen,

) -> Error | LavaflowRun | None:
    """ Open a held LavaFlow fix

     Opens the pull request for a fix LavaFlow held because the
    repository's workflows could run it with the repository's secrets
    before a person approves it (`pull_request_skipped:
    ungated_workflows`). Read the run first: send its `id` as `run_id`,
    with the `diff_sha256` and `held_workflows.jobs_sha256` it served, to
    say you read that diff and that list of jobs. LavaFlow opens the fix it
    saved, exactly as reviewed, past those jobs only. It writes no new
    fix.

    Right before it queues the run, LavaFlow serves the diff again and
    reads the workflows again. A diff served differently since you read
    it, or a job list or a commit the workflows were read at that changed,
    answers `409` with code `run_changed`; read the run again, which lists
    what LavaFlow found. The response is the run, `202` while it is
    `queued`. LavaFlow reads the workflows again before it opens the pull
    request, and once more as it pushes the fix: a job you didn't read, a
    new commit on a branch the workflows were read on, even one that
    changes no job, or a production branch other than the one you read
    them on holds the fix again with a new list.

    Opening a fix lets its pull request open, nothing more. LavaFlow
    starts no CI on it and never merges it, as for every fix opened past
    ungated workflows; a person pushes to the branch or merges it. The
    pull request's description names who opened it and lists the jobs.
    One exception: when LavaFlow's read before the pull request opens
    finds no job that runs the fix before a person approves it, because
    the workflows were gated since you read them, the fix opens as any
    other fix and follows the project's merge settings. A run whose
    `held_workflows` lists no job opens the same way.

    Only the project's owner can open a fix, as a person, while their
    account is active: with a `volcano login` token
    whose sign-in is live, or a platform token that expires. Their GitHub
    account must be able to push to the project's repository. A project
    access token, a request made through MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Opening a fix uses one of the run's attempts: the
    attempt that opens it is one of the run's, so a run held again on its
    last attempt can't be opened again. It starts no new run and counts
    toward no run limit.

    Args:
        body (LavaflowHeldFixOpen): The project, the run, and the diff and jobs of the held fix
            you read, by the digests the run served them with.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: LavaflowHeldFixOpen,

) -> Response[Error | LavaflowRun]:
    """ Open a held LavaFlow fix

     Opens the pull request for a fix LavaFlow held because the
    repository's workflows could run it with the repository's secrets
    before a person approves it (`pull_request_skipped:
    ungated_workflows`). Read the run first: send its `id` as `run_id`,
    with the `diff_sha256` and `held_workflows.jobs_sha256` it served, to
    say you read that diff and that list of jobs. LavaFlow opens the fix it
    saved, exactly as reviewed, past those jobs only. It writes no new
    fix.

    Right before it queues the run, LavaFlow serves the diff again and
    reads the workflows again. A diff served differently since you read
    it, or a job list or a commit the workflows were read at that changed,
    answers `409` with code `run_changed`; read the run again, which lists
    what LavaFlow found. The response is the run, `202` while it is
    `queued`. LavaFlow reads the workflows again before it opens the pull
    request, and once more as it pushes the fix: a job you didn't read, a
    new commit on a branch the workflows were read on, even one that
    changes no job, or a production branch other than the one you read
    them on holds the fix again with a new list.

    Opening a fix lets its pull request open, nothing more. LavaFlow
    starts no CI on it and never merges it, as for every fix opened past
    ungated workflows; a person pushes to the branch or merges it. The
    pull request's description names who opened it and lists the jobs.
    One exception: when LavaFlow's read before the pull request opens
    finds no job that runs the fix before a person approves it, because
    the workflows were gated since you read them, the fix opens as any
    other fix and follows the project's merge settings. A run whose
    `held_workflows` lists no job opens the same way.

    Only the project's owner can open a fix, as a person, while their
    account is active: with a `volcano login` token
    whose sign-in is live, or a platform token that expires. Their GitHub
    account must be able to push to the project's repository. A project
    access token, a request made through MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Opening a fix uses one of the run's attempts: the
    attempt that opens it is one of the run's, so a run held again on its
    last attempt can't be opened again. It starts no new run and counts
    toward no run limit.

    Args:
        body (LavaflowHeldFixOpen): The project, the run, and the diff and jobs of the held fix
            you read, by the digests the run served them with.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | LavaflowRun]
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
    body: LavaflowHeldFixOpen,

) -> Error | LavaflowRun | None:
    """ Open a held LavaFlow fix

     Opens the pull request for a fix LavaFlow held because the
    repository's workflows could run it with the repository's secrets
    before a person approves it (`pull_request_skipped:
    ungated_workflows`). Read the run first: send its `id` as `run_id`,
    with the `diff_sha256` and `held_workflows.jobs_sha256` it served, to
    say you read that diff and that list of jobs. LavaFlow opens the fix it
    saved, exactly as reviewed, past those jobs only. It writes no new
    fix.

    Right before it queues the run, LavaFlow serves the diff again and
    reads the workflows again. A diff served differently since you read
    it, or a job list or a commit the workflows were read at that changed,
    answers `409` with code `run_changed`; read the run again, which lists
    what LavaFlow found. The response is the run, `202` while it is
    `queued`. LavaFlow reads the workflows again before it opens the pull
    request, and once more as it pushes the fix: a job you didn't read, a
    new commit on a branch the workflows were read on, even one that
    changes no job, or a production branch other than the one you read
    them on holds the fix again with a new list.

    Opening a fix lets its pull request open, nothing more. LavaFlow
    starts no CI on it and never merges it, as for every fix opened past
    ungated workflows; a person pushes to the branch or merges it. The
    pull request's description names who opened it and lists the jobs.
    One exception: when LavaFlow's read before the pull request opens
    finds no job that runs the fix before a person approves it, because
    the workflows were gated since you read them, the fix opens as any
    other fix and follows the project's merge settings. A run whose
    `held_workflows` lists no job opens the same way.

    Only the project's owner can open a fix, as a person, while their
    account is active: with a `volcano login` token
    whose sign-in is live, or a platform token that expires. Their GitHub
    account must be able to push to the project's repository. A project
    access token, a request made through MCP, a platform token that never
    expires, and a sign-in that ended get `403` with code
    `person_required`. Opening a fix uses one of the run's attempts: the
    attempt that opens it is one of the run's, so a run held again on its
    last attempt can't be opened again. It starts no new run and counts
    toward no run limit.

    Args:
        body (LavaflowHeldFixOpen): The project, the run, and the diff and jobs of the held fix
            you read, by the digests the run served them with.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | LavaflowRun
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
