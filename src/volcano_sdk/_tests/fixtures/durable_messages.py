"""Volcano's durable message routes, faked for handlers on the local runner."""

from __future__ import annotations

import hashlib
import json
import threading
from typing import TYPE_CHECKING

import httpx

from volcano_sdk._durable_response import json_value
from volcano_sdk._transport_types import decode_json

from .durable_platform import REAL_CLIENT

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from volcano_sdk.durable_authoring import FunctionHandler
    from volcano_sdk.models import JSONValue

WAITS = "/durable-messages/waits"
SESSIONS = "/durable-messages/sessions"
PUBLISH = "/durable-messages/publish"
SESSION = "volcano:messages-session"
# Keys hash "token-1", the first token the fake hands out.
FIRST_TOKEN_DIGEST = hashlib.sha256(b"token-1").hexdigest()
_INVOCATION_TIMEOUT_SECONDS = 30

Answer = tuple[str, bytes]


def callback_id(body: Mapping[str, JSONValue]) -> str:
    value = body["callback_id"]
    assert isinstance(value, str)
    assert value
    return value


def session_answer(index: int) -> bytes:
    return json.dumps({"token": f"token-{index}"}).encode()


def message_payload(name: str, data: JSONValue = None) -> dict[str, JSONValue]:
    return {
        "id": f"message-for-{name}",
        "name": name,
        "data": data,
        "sender": {"type": "user", "user_id": "user-7"},
        "sent_at": "2026-10-12T09:00:00Z",
    }


class MessagePlatform:
    """Stand in for Volcano's message routes, from the runtime's threads."""

    def __init__(self) -> None:
        self.waits: list[dict[str, JSONValue]] = []
        self.sessions: list[dict[str, JSONValue]] = []
        self.publishes: list[httpx.Request] = []
        # What a wait for each name is completed with; a name missing here is
        # left for its timeout.
        self.messages: dict[str, dict[str, JSONValue]] = {}
        self.refusals: dict[str, httpx.Response] = {}
        self._published: dict[str, dict[str, JSONValue]] = {}
        self._answered: set[str] = set()
        self._lock: threading.Lock = threading.Lock()

    def handle(self, request: httpx.Request) -> httpx.Response:
        body = json_value(decode_json(request.content), "expected a JSON body")
        assert isinstance(body, dict)
        with self._lock:
            path = request.url.path
            if path == PUBLISH:
                self.publishes.append(request)
            else:
                (self.waits if path == WAITS else self.sessions).append(body)
            if path in self.refusals:
                return self.refusals[path]
            if path == PUBLISH:
                return self._publish(request.headers["Idempotency-Key"], body)
            registered = len(self.waits) + len(self.sessions)
            return httpx.Response(201, json={"id": f"registration-{registered}"})

    def _publish(self, key: str, body: Mapping[str, JSONValue]) -> httpx.Response:
        if key in self._published:
            return httpx.Response(200, json=self._published[key])
        message: dict[str, JSONValue] = {
            "id": f"message-{len(self._published) + 1}",
            "execution_id": "execution-1",
            "direction": "out",
            "seq": len(self._published) + 1,
            "name": body["name"],
            "data": body.get("data"),
            "sender": {"type": "execution", "user_id": None},
            "status": "published",
            "delivered_at": None,
            "sent_at": "2026-10-12T09:00:00Z",
        }
        self._published[key] = message
        return httpx.Response(201, json=message)

    def client(self, *, timeout: float) -> httpx.AsyncClient:
        return REAL_CLIENT(transport=httpx.MockTransport(self.handle), timeout=timeout)

    def unanswered(self) -> list[Answer]:
        """Claim the sessions and waits that can be completed now.

        Returns:
            Each callback id with what to complete it with.

        """
        with self._lock:
            answers = [
                (callback_id(body), session_answer(index))
                for index, body in enumerate(self.sessions, start=1)
            ]
            answers += [
                (
                    callback_id(body),
                    json.dumps(self.messages[str(body["name"])]).encode(),
                )
                for body in self.waits
                if body["name"] in self.messages
            ]
            fresh = [answer for answer in answers if answer[0] not in self._answered]
            self._answered.update(answer[0] for answer in fresh)
            return fresh

    def idempotency_keys(self) -> list[str]:
        return [request.headers["Idempotency-Key"] for request in self.publishes]

    def sessions_used(self) -> list[str]:
        return [
            request.headers["X-Volcano-Durable-Session"] for request in self.publishes
        ]


class Suspensions:
    """Track a handler's invocations, to answer what each suspended on.

    The local runner invalidates an invocation's checkpoints when a callback
    completes under it, so callbacks are completed only once no invocation
    is running.
    """

    def __init__(self, handler: FunctionHandler) -> None:
        self._handler: FunctionHandler = handler
        self._running: int = 0
        self._finished: bool = False
        self._changed: threading.Condition = threading.Condition()

    def __call__(self, event: object, function_context: object) -> object:
        with self._changed:
            self._running += 1
        output: object = None
        try:
            output = self._handler(event, function_context)
        finally:
            with self._changed:
                self._running -= 1
                match output:
                    case {"Status": "PENDING"}:
                        self._finished = False
                    case _:
                        self._finished = True
                self._changed.notify_all()
        return output

    def next(self, unanswered: Callable[[], list[Answer]]) -> list[Answer]:
        """Wait for the handler to stop, then return what it waits on.

        Returns:
            The callbacks to complete, or none once the handler finished.

        Raises:
            AssertionError: The handler neither suspends nor finishes.

        """
        answers: list[Answer] = []

        def stopped() -> bool:
            nonlocal answers
            if self._running:
                return False
            answers = unanswered()
            return bool(answers) or self._finished

        with self._changed:
            if not self._changed.wait_for(stopped, timeout=_INVOCATION_TIMEOUT_SECONDS):
                message = "expected the invocation to suspend or finish"
                raise AssertionError(message)
        return answers
