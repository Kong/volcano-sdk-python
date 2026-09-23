from __future__ import annotations

import asyncio
import os
import secrets
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, TypeVar

from volcano_sdk import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    Session,
    TransportError,
    ValidationError,
    VolcanoClient,
    VolcanoError,
)
from volcano_sdk.realtime import CENTRIFUGE_ERROR

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from contract_fixture import ContractFixture

    from volcano_sdk.models import (
        AuthChangeEvent,
        DurableExecution,
        DurableExecutionPage,
        LockLease,
    )
    from volcano_sdk.realtime import Channel

HTTP_NOT_FOUND = 404
HTTP_CONFLICT = 409
HTTP_RATE_LIMITED = 429
HTTP_SERVER_ERROR_MIN = 500
HTTP_SERVER_ERROR_MAX = 599

# A durable execution is started asynchronously and observed through a status
# read, so it settles in seconds. Bounded, so a scenario reports a timeout
# instead of hanging the lane.
DURABLE_POLL_INTERVAL_SECONDS = 5
DURABLE_POLL_TIMEOUT_SECONDS = 300

# The platform token is not an auth session: it cannot be refreshed and belongs
# to no auth user. The SDK carries a credential as a session and requires a
# complete one, so the rest of the owner's session is a placeholder.
OWNER_SESSION_PLACEHOLDER = "sdk-contract-platform-token-has-no-auth-session"

CONTRACT_EXCEPTIONS = (
    CENTRIFUGE_ERROR,
    KeyError,
    OSError,
    RuntimeError,
    TypeError,
    ValueError,
    VolcanoError,
)

_ResultT = TypeVar("_ResultT")


@dataclass(frozen=True, slots=True)
class Outcome:
    ok: bool
    value: object = None
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
        return classify_status(error.status)
    return "transport error"


def classify_status(status: int | None) -> str:
    category_by_status = {
        401: "authentication error",
        403: "authentication error",
        400: "validation error",
        422: "validation error",
        HTTP_NOT_FOUND: "not found",
        HTTP_CONFLICT: "conflict",
        HTTP_RATE_LIMITED: "rate limited",
    }
    if status is None:
        return "transport error"
    if HTTP_SERVER_ERROR_MIN <= status <= HTTP_SERVER_ERROR_MAX:
        return "server error"
    return category_by_status.get(status, "transport error")


class ContractWorld:
    def __init__(self, fixture: ContractFixture) -> None:
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
        # Reading or stopping an execution is owner-scoped, so its client
        # carries the project's own token as its session. Neither key above can
        # reach those routes.
        self.owner_client = VolcanoClient(
            api_url=fixture["api_url"],
            anon_key=fixture["anon_key"],
        )
        self.owner_client.auth.set_session(
            Session(
                access_token=fixture["platform_token"],
                refresh_token=OWNER_SESSION_PLACEHOLDER,
                user_id=OWNER_SESSION_PLACEHOLDER,
            )
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
        self.durable_execution_name = f"{fixture['durable_function_name']}-{suffix}"
        self.durable_payload = {"value": f"volcano-sdk-contract-{suffix}"}
        self.started_execution: DurableExecution | None = None
        self.last_outcome: Outcome | None = None
        self.previous_session: Session | None = None
        self.signed_out_session: Session | None = None
        self.bootstrap_cleanup: Callable[[], None] | None = None
        self.auth_state_events: list[tuple[AuthChangeEvent, Session | None]] = []
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

    def run(self, operation: Awaitable[_ResultT]) -> _ResultT:
        return self.loop.run_until_complete(operation)

    def start_durable_execution(self) -> DurableExecution:
        execution = self.service_client.durable.start(
            self.fixture["durable_function_name"],
            self.durable_payload,
            execution_name=self.durable_execution_name,
        )
        self.started_execution = execution
        return execution

    def follow_durable_execution(self, execution_id: str) -> DurableExecution:
        """Poll an execution to a terminal status under the owner's credential.

        That read is also what reconciles the stored status against the
        platform's, so it is the path a client waiting for a result takes.

        Returns:
            The execution in a terminal state.

        Raises:
            TimeoutError: If the execution stays active past the polling deadline.
        """
        deadline = time.monotonic() + DURABLE_POLL_TIMEOUT_SECONDS
        while True:
            execution = self.owner_client.durable.get(
                self.fixture["project_id"],
                self.fixture["durable_function_name"],
                execution_id,
            )
            if execution.is_terminal:
                return execution
            if time.monotonic() >= deadline:
                message = (
                    f"durable execution {execution_id} was still "
                    f"{execution.status} after {DURABLE_POLL_TIMEOUT_SECONDS}s"
                )
                raise TimeoutError(message)
            time.sleep(DURABLE_POLL_INTERVAL_SECONDS)

    def list_durable_executions(self) -> DurableExecutionPage:
        return self.owner_client.durable.list(
            self.fixture["project_id"],
            self.fixture["durable_function_name"],
        )

    def record(self, operation: Callable[[], object]) -> Outcome:
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
        failures.extend(self.disconnect_realtime_clients())
        self.cleanup_callbacks.clear()
        self.realtime_clients.clear()
        self.loop.close()
        if failures:
            message = "Python contract cleanup failed"
            raise ExceptionGroup(message, failures)

    def disconnect_realtime_clients(self) -> list[Exception]:
        failures: list[Exception] = []
        for client in self.realtime_clients:
            try:
                self.run(client.realtime.disconnect())
            except CONTRACT_EXCEPTIONS as error:
                failures.append(error)
        return failures
