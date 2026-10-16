"""Durable message authoring tests against a recording runtime context.

The handler tests that run on the local runner are in test_durable_authoring.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from aws_durable_execution_sdk_python.config import (
    StepConfig,
    StepSemantics,
    WaitForCallbackConfig,
)
from aws_durable_execution_sdk_python.exceptions import (
    CallbackError,
    CallbackTimeoutError,
)

from volcano_sdk._durable_engine import Engine
from volcano_sdk.durable_authoring import DurableContext, ReceivedMessage
from volcano_sdk.models import DurableMessageSender

from .fixtures.durable_context import RecordingContext
from .fixtures.durable_messages import SESSION, message_payload, session_answer
from .fixtures.invalid_arguments import non_json_message_data, non_string_message_name
from .test_durable_authoring import PLATFORM_API_URL

if TYPE_CHECKING:
    from volcano_sdk.durable_authoring import Duration
    from volcano_sdk.models import JSONValue


class Waits:
    """Record what wait_for_message registers, in place of the HTTP request."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str, str]] = []

    def register(
        self, api_url: str, execution_ref: str, callback: str, name: str
    ) -> None:
        self.calls.append((api_url, execution_ref, callback, name))


@pytest.fixture
def waits(monkeypatch: pytest.MonkeyPatch) -> Waits:
    recorder = Waits()
    monkeypatch.setattr(
        "volcano_sdk.durable_authoring.register_wait", recorder.register
    )
    monkeypatch.setenv("VOLCANO_PLATFORM_API_URL", PLATFORM_API_URL)
    return recorder


def test_wait_for_message_forwards_its_name_timeout_and_submitter(
    waits: Waits,
) -> None:
    runtime = RecordingContext()
    runtime.callback_result = json.dumps(message_payload("approve", [1]))
    context = DurableContext(runtime, Engine())

    approval = context.wait_for_message("approve", timeout="2h")

    assert approval == ReceivedMessage(
        id="message-for-approve",
        name="approve",
        data=[1],
        sender=DurableMessageSender(type="user", user_id="user-7"),
        sent_at="2026-10-12T09:00:00Z",
    )
    assert runtime.name == "approve"
    assert isinstance(runtime.config, WaitForCallbackConfig)
    assert runtime.config.timeout.to_seconds() == 7200
    retry = runtime.config.retry_strategy
    assert retry is not None
    assert retry(RuntimeError("failed"), 1).should_retry is False
    assert runtime.submitter is not None
    assert waits.calls == []
    runtime.submitter("callback-9", None)
    assert waits.calls == [(PLATFORM_API_URL, "arn:execution", "callback-9", "approve")]


@pytest.mark.usefixtures("waits")
def test_a_message_wait_without_a_timeout_lasts_as_long_as_the_execution() -> None:
    runtime = RecordingContext()
    runtime.callback_result = message_payload("approve")
    context = DurableContext(runtime, Engine())

    approval = context.wait_for_message("approve")

    assert approval is not None
    assert approval.data is None
    assert isinstance(runtime.config, WaitForCallbackConfig)
    assert runtime.config.timeout.to_seconds() == 0


@pytest.mark.usefixtures("waits")
def test_only_a_callback_timeout_ends_a_message_wait_with_none() -> None:
    runtime = RecordingContext()
    runtime.callback_error = CallbackTimeoutError("timed out")
    context = DurableContext(runtime, Engine())

    assert context.wait_for_message("approve", timeout=60) is None
    runtime.callback_error = CallbackError("callback failed")
    with pytest.raises(CallbackError, match="callback failed"):
        _ = context.wait_for_message("approve")


@pytest.mark.usefixtures("waits")
def test_an_unreadable_message_fails_the_wait() -> None:
    runtime = RecordingContext()
    runtime.callback_result = {"id": "message-1"}
    context = DurableContext(runtime, Engine())

    with pytest.raises(TypeError, match="cannot read"):
        _ = context.wait_for_message("approve")


@pytest.mark.usefixtures("waits")
@pytest.mark.parametrize(
    ("name", "timeout", "error", "match"),
    [
        ("", None, ValueError, "^name must not be empty$"),
        ("ap\tprove", None, ValueError, "^name must be printable ASCII$"),
        ("n" * 238, None, ValueError, "^name must be at most 237 characters$"),
        ("approve", "0s", TypeError, "^timeout must be at least 1 second$"),
        ("approve", "soon", ValueError, "^timeout must be a duration"),
    ],
)
def test_a_message_wait_is_checked_before_its_callback_opens(
    name: str, timeout: Duration | None, error: type[Exception], match: str
) -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(error, match=match):
        _ = context.wait_for_message(name, timeout=timeout)
    assert runtime.submitter is None


@pytest.mark.usefixtures("waits")
def test_a_message_name_must_be_a_string() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(TypeError, match=r"^name must be a string$"):
        non_string_message_name(context)
    assert runtime.submitter is None


def test_waiting_for_a_message_needs_the_platform_api_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("VOLCANO_PLATFORM_API_URL", raising=False)
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(RuntimeError, match=r"^wait_for_message\(\) needs VOLCANO"):
        _ = context.wait_for_message("approve")
    assert runtime.submitter is None


class Sessions:
    """Record the sessions publish opens, in place of the HTTP request."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, str]] = []

    def open(self, api_url: str, execution_ref: str, callback: str) -> None:
        self.calls.append((api_url, execution_ref, callback))


@pytest.fixture
def sessions(monkeypatch: pytest.MonkeyPatch) -> Sessions:
    recorder = Sessions()
    monkeypatch.setattr("volcano_sdk.durable_authoring.open_session", recorder.open)
    monkeypatch.setenv("VOLCANO_PLATFORM_API_URL", PLATFORM_API_URL)
    return recorder


def test_publish_opens_its_session_then_runs_a_step_that_is_never_retried(
    sessions: Sessions,
) -> None:
    runtime = RecordingContext()
    runtime.callback_result = session_answer(1).decode()
    context = DurableContext(runtime, Engine())

    with pytest.raises(AssertionError, match="unexpected runtime operation"):
        _ = context.publish("progress", {"done": 1})

    assert runtime.name == SESSION
    assert isinstance(runtime.config, StepConfig)
    assert runtime.config.step_semantics is StepSemantics.AT_LEAST_ONCE_PER_RETRY
    retry = runtime.config.retry_strategy
    assert retry is not None
    assert retry(RuntimeError("failed"), 1).should_retry is False
    assert runtime.submitter is not None
    runtime.submitter("callback-3", None)
    assert sessions.calls == [(PLATFORM_API_URL, "arn:execution", "callback-3")]


@pytest.mark.usefixtures("sessions")
def test_a_session_without_a_token_fails_the_publish() -> None:
    runtime = RecordingContext()
    runtime.callback_result = {"token": ""}
    context = DurableContext(runtime, Engine())

    with pytest.raises(TypeError, match="token this SDK cannot read"):
        _ = context.publish("progress")
    assert isinstance(runtime.config, WaitForCallbackConfig)
    assert runtime.config.timeout.to_seconds() == 0


@pytest.mark.usefixtures("sessions")
@pytest.mark.parametrize(
    ("name", "data", "error", "match"),
    [
        ("", None, ValueError, "^name must not be empty$"),
        ("pro\ngress", None, ValueError, "^name must be printable ASCII$"),
        ("progress", "\0", ValueError, "^data must not contain NUL characters$"),
        ("progress", "x" * 65535, ValueError, "^data must be at most 64 KiB"),
    ],
)
def test_a_publish_is_checked_before_its_session_opens(
    name: str, data: JSONValue, error: type[Exception], match: str
) -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(error, match=match):
        _ = context.publish(name, data)
    assert runtime.submitter is None


@pytest.mark.usefixtures("sessions")
def test_published_data_must_be_json() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(TypeError, match=r"^data must be JSON-serializable"):
        non_json_message_data(context)
    assert runtime.submitter is None


def test_publishing_needs_the_platform_api_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("VOLCANO_PLATFORM_API_URL", raising=False)
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(RuntimeError, match=r"^publish\(\) needs VOLCANO"):
        _ = context.publish("progress")
    assert runtime.submitter is None
