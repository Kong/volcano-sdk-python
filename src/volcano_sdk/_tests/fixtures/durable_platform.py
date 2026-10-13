"""A stand-in for the routes Volcano serves running workflows."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, NoReturn, TypeAlias

import httpx

if TYPE_CHECKING:
    import pytest

# Replaced for the module under test, which is the same attribute everywhere.
REAL_CLIENT = httpx.AsyncClient
PLATFORM_REQUEST = "volcano_sdk._durable_platform_request"
# Long past any attempt's deadline: a slow answer still running by then was
# never cut off, and ends rather than hang the suite.
GIVE_UP_SECONDS = 10.0
_NEVER_CANCELLED = "the attempt outlived its deadline"


class Stall:
    """Accept the request and never answer it."""

    def __init__(self) -> None:
        self.released: bool = False

    async def hold(self) -> NoReturn:
        try:
            await asyncio.sleep(GIVE_UP_SECONDS)
        finally:
            self.released = True
        raise AssertionError(_NEVER_CANCELLED)


Answer: TypeAlias = "httpx.Response | Exception | Stall"


class Platform:
    """Answer requests in order and record what was sent.

    Time is the platform's own: it passes while a request sleeps to retry and
    while one runs into its timeout, and nowhere else. An attempt that is
    cancelled at its deadline takes real time, not platform time.
    """

    def __init__(self, *answers: Answer) -> None:
        self.answers: list[Answer] = list(answers)
        self.requests: list[httpx.Request] = []
        self.timeouts: list[float] = []
        self.sleeps: list[float] = []
        self.now: float = 0.0
        # How much longer than asked each sleep takes.
        self.oversleep: float = 0.0
        self.clock_runs: bool = True

    async def handle(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        match request.extensions:
            case {"timeout": {"read": float(timeout)}}:
                self.timeouts.append(timeout)
            case _:
                message = f"expected a read timeout, got {request.extensions}"
                raise AssertionError(message)
        answer = self.answers[0] if len(self.answers) == 1 else self.answers.pop(0)
        if isinstance(answer, Stall):
            await answer.hold()
        if isinstance(answer, httpx.TimeoutException):
            self.advance(timeout)
        if isinstance(answer, Exception):
            raise answer
        return answer

    def client(self, *, timeout: float) -> httpx.AsyncClient:
        return REAL_CLIENT(transport=httpx.MockTransport(self.handle), timeout=timeout)

    def monotonic(self) -> float:
        return self.now

    def sleep(self, delay: float) -> None:
        self.sleeps.append(delay)
        self.advance(delay + self.oversleep)

    def advance(self, seconds: float) -> None:
        if self.clock_runs:
            self.now += seconds


def install_platform(monkeypatch: pytest.MonkeyPatch, *answers: Answer) -> Platform:
    """Route the platform requests, and their clock, to a fake.

    Returns:
        The fake, to inspect what was sent.

    """
    fake = Platform(*answers)
    monkeypatch.setattr(f"{PLATFORM_REQUEST}.httpx.AsyncClient", fake.client)
    monkeypatch.setattr(f"{PLATFORM_REQUEST}.monotonic", fake.monotonic)
    monkeypatch.setattr(f"{PLATFORM_REQUEST}.sleep", fake.sleep)
    return fake


def refused(status: int, code: str | None = None) -> httpx.Response:
    """Answer the way Volcano refuses a request.

    Returns:
        An error response with the status, and the code when given.

    """
    body = {"error": f"refused with {status}"}
    if code is not None:
        body["code"] = code
    return httpx.Response(status, json=body)
