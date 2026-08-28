from __future__ import annotations

import asyncio
import os
import secrets
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

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

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from volcano_sdk.models import LockLease
    from volcano_sdk.realtime import Channel

HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_RATE_LIMITED = 429
HTTP_SERVER_ERROR_MIN = 500
HTTP_SERVER_ERROR_MAX = 599

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
    matched_category = next(
        (
            category
            for error_type, category in categories
            if isinstance(error, error_type)
        ),
        None,
    )
    if matched_category is not None:
        return matched_category
    if isinstance(error, VolcanoError):
        status = error.status
        if status in (401, 403):
            return "authentication error"
        if status in (400, 422):
            return "validation error"
        category_by_status = {
            HTTP_NOT_FOUND: "not found",
            HTTP_CONFLICT: "conflict",
            HTTP_RATE_LIMITED: "rate limited",
        }
        if status in category_by_status:
            return category_by_status[status]
        if (
            status is not None
            and HTTP_SERVER_ERROR_MIN <= status <= HTTP_SERVER_ERROR_MAX
        ):
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
        self.unique_email = f"{suffix}@example.com"
        self.unique_password = f"Sdk-{suffix}!123"
        self.metadata_marker = f"updated-{suffix}"
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
        self.secondary_client: VolcanoClient | None = None
        self.listener_events: list[str | None] = []
        self.listener_event_count = 0
        self.unsubscribe_auth: Callable[[], None] | None = None
        self.previous_access_token: str | None = None
        self.previous_refresh_token: str | None = None
        self.anonymous_user_id: str | None = None
        self.deleted_session_id: str | None = None
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
            message = "Python contract cleanup failed"
            raise ExceptionGroup(message, failures)
