from __future__ import annotations

import asyncio
import os
import secrets
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from centrifuge import CentrifugeError

from volcano_sdk import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    TransportError,
    ValidationError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk.models import LockLease
from volcano_sdk.realtime import Channel

CONTRACT_EXCEPTIONS = (
    CentrifugeError,
    KeyError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
    VolcanoError,
)


@dataclass(frozen=True, slots=True)
class Outcome:
    ok: bool
    value: Any = None
    category: str | None = None
    error: Exception | None = None


def classify_error(error: Exception) -> str:
    categories = (
        (AuthenticationError, "authentication error"),
        (ValidationError, "validation error"),
        (NotFoundError, "not found"),
        (ConflictError, "conflict"),
        (RateLimitedError, "rate limited"),
        (ServerError, "server error"),
        (TransportError, "transport error"),
    )
    for error_type, category in categories:
        if isinstance(error, error_type):
            return category
    if isinstance(error, VolcanoError):
        status = error.status
        if status in (401, 403):
            return "authentication error"
        if status in (400, 422):
            return "validation error"
        if status == 404:
            return "not found"
        if status == 409:
            return "conflict"
        if status == 429:
            return "rate limited"
        if status is not None and 500 <= status <= 599:
            return "server error"
    return "transport error"


class ContractWorld:
    def __init__(self, fixture: dict[str, Any]) -> None:
        self.fixture = fixture
        self.client = VolcanoClient(
            api_url=fixture["api_url"],
            anon_key=fixture["anon_key"],
        )
        self.service_client = VolcanoClient(
            api_url=fixture["api_url"],
            anon_key=fixture["anon_key"],
            service_key=fixture["service_key"],
        )
        suffix = f"py-{os.getpid()}-{secrets.token_hex(5)}"
        self.storage_path = f"{fixture['storage_path']}.{suffix}"
        self.realtime_channel = f"{fixture['realtime_channel']}-{suffix}"
        self.lock_key = f"{fixture['lock_key']}-{suffix}"
        self.storage_bytes = f"volcano-sdk-contract-{suffix}".encode()
        self.realtime_message = {
            "event": "message",
            "value": f"volcano-sdk-contract-{suffix}",
        }
        self.last_outcome: Outcome | None = None
        self.subscriber: Channel | None = None
        self.publisher: Channel | None = None
        self.realtime_clients: list[VolcanoClient] = []
        self.cleanup_callbacks: list[Callable[[], None]] = []
        self.loop = asyncio.new_event_loop()

    def authenticate(self) -> None:
        self.client.auth.sign_in(
            email=self.fixture["user_email"],
            password=self.fixture["user_password"],
        )

    def run(self, operation: Awaitable[Any]) -> Any:
        return self.loop.run_until_complete(operation)

    def record(self, operation: Callable[[], Any]) -> Outcome:
        try:
            self.last_outcome = Outcome(ok=True, value=operation())
        except CONTRACT_EXCEPTIONS as error:
            self.last_outcome = Outcome(
                ok=False,
                category=classify_error(error),
                error=error,
            )
        return self.last_outcome

    def register_lock_cleanup(self, key: str, lease: LockLease) -> Callable[[], None]:
        def release() -> None:
            self.service_client.locks.release(key, lease)

        self.cleanup_callbacks.append(release)
        return release

    def cleanup(self) -> None:
        failures: list[Exception] = []
        for callback in reversed(self.cleanup_callbacks):
            try:
                callback()
            except CONTRACT_EXCEPTIONS as error:
                failures.append(error)
        for client in self.realtime_clients:
            try:
                self.run(client.realtime.disconnect())
            except CONTRACT_EXCEPTIONS as error:
                failures.append(error)
        self.cleanup_callbacks.clear()
        self.realtime_clients.clear()
        self.loop.close()
        if failures:
            raise ExceptionGroup("Python contract cleanup failed", failures)
