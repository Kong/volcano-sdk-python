"""Requests a durable function makes to Volcano's runtime routes."""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass, field
from http import HTTPMethod
from time import monotonic, sleep
from typing import TYPE_CHECKING

import httpx

from ._transport_response import (
    invoke_async,
    plain_json,
    response_payload,
    unparsed_response,
)
from ._transport_types import HTTP_CREATED, HTTP_OK
from .errors import (
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    VolcanoError,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from ._transport_types import TransportResponse
    from .models import JSONValue

# 0.5 s doubling to a 5 s cap, within the deadline: long enough to outlast the
# moment the platform has not yet seen the execution start or the callback open.
_RETRY_DELAYS = (0.5, 1.0, 2.0, 4.0, 5.0, 5.0, 5.0, 5.0)
_DEADLINE_SECONDS = 30.0
_REQUEST_TIMEOUT_SECONDS = 10.0
_JSON = {"Content-Type": "application/json"}
# Volcano answers in a few hundred bytes, or with one published message: up to
# 64 KiB of data, which escaping `<`, `>`, and `&` can grow sixfold. More is not
# an answer worth reading.
_MAX_ANSWER_BYTES = 524288
_API_URL_VARIABLE = "VOLCANO_PLATFORM_API_URL"


@dataclass(frozen=True, slots=True)
class PlatformRequest:
    """A POST to one of the routes Volcano serves running workflows."""

    path: str
    body: Mapping[str, JSONValue]
    headers: Mapping[str, str] = field(default_factory=dict[str, str])
    # The conflict code for a callback Volcano cannot see waiting yet.
    not_ready: str | None = None
    # The conflict code for a callback that stopped waiting before the request
    # landed, normally because its timeout passed. The runtime resumes the
    # callback with that outcome, so there is nothing left to do.
    closed: str | None = None


def platform_api_url(operation: str) -> str:
    """Read the Volcano API address the platform gives durable functions.

    Returns:
        The API base URL.

    Raises:
        RuntimeError: The variable is unset or empty.

    """
    url = os.environ.get(_API_URL_VARIABLE, "").strip()
    if not url:
        message = (
            f"{operation} needs {_API_URL_VARIABLE}. Volcano sets it on deployed "
            "durable functions; set it yourself to run the handler elsewhere."
        )
        raise RuntimeError(message)
    return url


def encode(value: JSONValue) -> bytes:
    """Encode a value the way a request sends it, to size it.

    Returns:
        The compact UTF-8 JSON document.

    """
    return json.dumps(
        plain_json(value), ensure_ascii=False, separators=(",", ":"), allow_nan=False
    ).encode()


def post_to_platform(api_url: str, request: PlatformRequest) -> object:
    """Send the request and return the payload Volcano answered with.

    The routes take no platform credential: what the body or headers carry is
    what Volcano checks against the running execution.

    What can clear on its own is retried until a 30 second deadline: no
    answer, an execution or callback Volcano cannot see yet, throttling, and
    server failures. Each attempt, from connecting to the last byte of the
    answer, ends within 10 seconds or what is left of the deadline, whichever
    is sooner.

    Returns:
        The decoded answer to a 200 or 201, or None when the request's closed
        code says the callback no longer waits.

    Raises:
        VolcanoError: Volcano refused the request, or kept failing until the
            deadline passed or the retries ran out.

    """
    url = f"{api_url.removesuffix('/')}{request.path}"
    content = encode(request.body)
    headers = {**_JSON, **request.headers}
    deadline = monotonic() + _DEADLINE_SECONDS
    timeout = _REQUEST_TIMEOUT_SECONDS
    for delay in _RETRY_DELAYS:
        try:
            return _attempt(url, content, headers, request, timeout)
        except VolcanoError as error:
            next_timeout = _next_timeout(error, request, delay, deadline)
            if next_timeout is None:
                raise
            timeout = next_timeout
    return _attempt(url, content, headers, request, timeout)


def _attempt(
    url: str,
    content: bytes,
    headers: Mapping[str, str],
    request: PlatformRequest,
    timeout: float,
) -> object:
    response = _send(url, content, headers, timeout)
    expected = HTTP_CREATED if response.status_code == HTTP_CREATED else HTTP_OK
    try:
        return response_payload(response, expected)
    except ConflictError as error:
        # A request without the code expects none, so an uncoded conflict is
        # not it.
        if request.closed is None or error.code != request.closed:
            raise
    return None


def _send(
    url: str, content: bytes, headers: Mapping[str, str], timeout: float
) -> TransportResponse:
    # httpx times each network read on its own, restarting with every chunk,
    # so only cancelling the request bounds the attempt as a whole; its own
    # timeouts still keep any one phase within it. The runtime calls the
    # submitter on a thread without an event loop. asyncio.run() would wait on
    # its way out for a host lookup that cancelling leaves running in the
    # loop's executor; closing the loop leaves it behind instead.
    client = httpx.AsyncClient(timeout=timeout)
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(
            asyncio.wait_for(
                invoke_async(_exchange, client, url, content, headers), timeout
            )
        )
    except TimeoutError as error:
        raise _no_answer(timeout) from error
    except TransportError as error:
        # The client's timeouts spend the same budget. When a stalled loop
        # fires both at once, Python 3.11's wait_for reports the client's.
        if isinstance(error.__cause__, httpx.TimeoutException):
            raise _no_answer(timeout) from error.__cause__
        raise
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


def _no_answer(timeout: float) -> TransportError:
    return TransportError(f"Volcano did not answer within {timeout:g} seconds")


async def _exchange(
    client: httpx.AsyncClient, url: str, content: bytes, headers: Mapping[str, str]
) -> TransportResponse:
    async with (
        client,
        client.stream(
            HTTPMethod.POST, url, content=content, headers=headers
        ) as response,
    ):
        answer = await _answer(response)
    return unparsed_response(_Answer(response.status_code, answer, response.headers))


async def _answer(response: httpx.Response) -> bytes:
    """Read the answer, unless it runs past what Volcano would send.

    Returns:
        The body, or nothing when it is too large to be one of Volcano's.

    """
    answer = bytearray()
    async for chunk in response.aiter_bytes():
        answer += chunk
        if len(answer) > _MAX_ANSWER_BYTES:
            answer.clear()
            break
    return bytes(answer)


@dataclass(frozen=True, slots=True)
class _Answer:
    status_code: int
    content: bytes
    headers: Mapping[str, str]


def _retryable(error: VolcanoError, request: PlatformRequest) -> bool:
    # NotFoundError included: Volcano records an execution only once it has
    # started, so a request made first thing can arrive first.
    if isinstance(
        error, (TransportError, NotFoundError, RateLimitedError, ServerError)
    ):
        return True
    return (
        isinstance(error, ConflictError)
        and request.not_ready is not None
        and error.code == request.not_ready
    )


def _next_timeout(
    error: VolcanoError, request: PlatformRequest, delay: float, deadline: float
) -> float | None:
    """Wait to retry a failed attempt, if it is worth retrying in the time left.

    Returns:
        The next attempt's timeout, or None when the failure is final.

    """
    if not _retryable(error, request) or monotonic() + delay >= deadline:
        return None
    sleep(delay)
    remaining = deadline - monotonic()
    if remaining <= 0:
        return None
    return min(_REQUEST_TIMEOUT_SECONDS, remaining)
