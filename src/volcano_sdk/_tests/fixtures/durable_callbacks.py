"""Stand-ins for the callback-token route and the systems tokens go to."""

from __future__ import annotations

import json
import threading

REGISTER = "volcano_sdk._durable_callback_token.register_callback"
FAILURE_DATA = json.dumps({"type": "CardDeclined", "message": "Insufficient funds"})


class CallbackRegistrations:
    """Stand in for Volcano's token route, from the runtime's thread."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str, str]] = []
        self.closed: bool = False
        self._lock: threading.Lock = threading.Lock()

    def register(
        self, api_url: str, execution_ref: str, callback_id: str, name: str
    ) -> str | None:
        with self._lock:
            self.calls.append((api_url, execution_ref, callback_id, name))
        return None if self.closed else f"vcb_{callback_id}"

    def callback_ids(self) -> list[str]:
        with self._lock:
            return [callback_id for _, _, callback_id, _ in self.calls]


class Handoffs:
    """Record the tokens a submitter is handed."""

    def __init__(self) -> None:
        self.tokens: list[str] = []
        self._lock: threading.Lock = threading.Lock()

    def __call__(self, token: str) -> None:
        with self._lock:
            self.tokens.append(token)
