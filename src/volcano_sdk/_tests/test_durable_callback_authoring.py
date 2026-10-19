"""Callback-token authoring tests against a recording runtime context.

The handler tests that run on the local runner are in test_durable_authoring.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

import pytest
from aws_durable_execution_sdk_python.config import WaitForCallbackConfig
from aws_durable_execution_sdk_python.exceptions import (
    CallbackError,
    CallbackExternalError,
    CallbackTimeoutError,
)

from volcano_sdk._durable_engine import Engine
from volcano_sdk.durable_authoring import CallbackFailedError, DurableContext

from .fixtures.durable_callbacks import (
    FAILURE_DATA,
    REGISTER,
    CallbackRegistrations,
    Handoffs,
)
from .fixtures.durable_context import RecordingContext
from .fixtures.invalid_callbacks import wait_for_callback_without_submitter
from .test_durable_authoring import PLATFORM_API_URL

if TYPE_CHECKING:
    from volcano_sdk.durable_authoring import Duration


@pytest.fixture
def registrations(monkeypatch: pytest.MonkeyPatch) -> CallbackRegistrations:
    recorder = CallbackRegistrations()
    monkeypatch.setattr(REGISTER, recorder.register)
    monkeypatch.setenv("VOLCANO_PLATFORM_API_URL", PLATFORM_API_URL)
    return recorder


def test_wait_for_callback_forwards_its_name_timeouts_and_submitter(
    registrations: CallbackRegistrations,
) -> None:
    runtime = RecordingContext()
    runtime.callback_result = json.dumps({"charge": "ch_1"})
    context = DurableContext(runtime, Engine())
    handoffs = Handoffs()

    result = context.wait_for_callback(
        "payment", handoffs, timeout="2h", heartbeat_timeout="5m"
    )

    assert result == {"charge": "ch_1"}
    assert runtime.name == "payment"
    assert isinstance(runtime.config, WaitForCallbackConfig)
    assert runtime.config.timeout.to_seconds() == 7200
    assert runtime.config.heartbeat_timeout.to_seconds() == 300
    retry = runtime.config.retry_strategy
    assert retry is not None
    assert retry(RuntimeError("failed"), 1).should_retry is False
    assert runtime.submitter is not None
    assert registrations.calls == []
    runtime.submitter("callback-9", None)
    assert registrations.calls == [
        (PLATFORM_API_URL, "arn:execution", "callback-9", "payment")
    ]
    assert handoffs.tokens == ["vcb_callback-9"]


@pytest.mark.usefixtures("registrations")
def test_a_callback_wait_without_timeouts_lasts_as_long_as_the_execution() -> None:
    runtime = RecordingContext()
    runtime.callback_result = '"done"'
    context = DurableContext(runtime, Engine())

    assert context.wait_for_callback("payment", Handoffs()) == "done"
    assert isinstance(runtime.config, WaitForCallbackConfig)
    assert runtime.config.timeout.to_seconds() == 0
    assert runtime.config.heartbeat_timeout.to_seconds() == 0


def test_a_callback_that_already_closed_is_not_handed_on(
    registrations: CallbackRegistrations,
) -> None:
    registrations.closed = True
    runtime = RecordingContext()
    runtime.callback_result = '"unused"'
    context = DurableContext(runtime, Engine())
    handoffs = Handoffs()
    _ = context.wait_for_callback("payment", handoffs)
    assert runtime.submitter is not None

    runtime.submitter("callback-9", None)

    assert len(registrations.calls) == 1
    assert handoffs.tokens == []


@pytest.mark.usefixtures("registrations")
def test_only_a_callback_timeout_ends_the_wait_with_none() -> None:
    runtime = RecordingContext()
    runtime.callback_error = CallbackTimeoutError("timed out")
    context = DurableContext(runtime, Engine())

    assert context.wait_for_callback("payment", Handoffs(), timeout=60) is None
    runtime.callback_error = CallbackError("callback failed")
    with pytest.raises(CallbackError, match="callback failed"):
        _ = context.wait_for_callback("payment", Handoffs())


@pytest.mark.usefixtures("registrations")
def test_a_failure_raises_its_type_and_message() -> None:
    runtime = RecordingContext()
    failure = CallbackExternalError("Insufficient funds", data=FAILURE_DATA)
    runtime.callback_error = failure
    context = DurableContext(runtime, Engine())

    with pytest.raises(CallbackFailedError, match=r"^Insufficient funds$") as caught:
        _ = context.wait_for_callback("payment", Handoffs())

    assert caught.value.type == "CardDeclined"
    assert caught.value.message == "Insufficient funds"
    assert caught.value.__cause__ is failure


@pytest.mark.usefixtures("registrations")
@pytest.mark.parametrize("data", [None, "not json", json.dumps({"message": "x"})])
def test_a_failure_volcano_did_not_send_is_raised_as_the_runtime_raised_it(
    data: str | None,
) -> None:
    runtime = RecordingContext()
    failure = CallbackExternalError("Callback failed", data=data)
    runtime.callback_error = failure
    context = DurableContext(runtime, Engine())

    with pytest.raises(CallbackExternalError) as caught:
        _ = context.wait_for_callback("payment", Handoffs())

    assert caught.value is failure


@pytest.mark.usefixtures("registrations")
def test_an_unreadable_result_fails_the_wait() -> None:
    runtime = RecordingContext()
    runtime.callback_result = "{not json"
    context = DurableContext(runtime, Engine())

    with pytest.raises(TypeError, match="result this SDK cannot read"):
        _ = context.wait_for_callback("payment", Handoffs())


@pytest.mark.usefixtures("registrations")
@pytest.mark.parametrize(
    ("name", "timeout", "heartbeat_timeout", "error", "match"),
    [
        ("", None, None, ValueError, "^name must not be empty$"),
        ("pay\tment", None, None, ValueError, "^name must be printable ASCII$"),
        ("n" * 238, None, None, ValueError, "^name must be at most 237 characters$"),
        ("payment", "0s", None, TypeError, "^timeout must be at least 1 second$"),
        ("payment", "367d", None, TypeError, "^timeout must be at most 31622400"),
        (
            "payment",
            None,
            "0s",
            TypeError,
            "^heartbeat_timeout must be at least 1 second$",
        ),
        ("payment", None, "soon", ValueError, "^heartbeat_timeout must be a duration"),
    ],
)
def test_a_callback_wait_is_checked_before_its_callback_opens(
    name: str,
    timeout: Duration | None,
    heartbeat_timeout: Duration | None,
    error: type[Exception],
    match: str,
) -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(error, match=match):
        _ = context.wait_for_callback(
            name, Handoffs(), timeout=timeout, heartbeat_timeout=heartbeat_timeout
        )
    assert runtime.submitter is None


@pytest.mark.usefixtures("registrations")
def test_a_callback_wait_requires_a_submitter() -> None:
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(
        TypeError,
        match=r"^wait_for_callback\(\) requires a submitter function that receives",
    ):
        wait_for_callback_without_submitter(context)
    assert runtime.submitter is None


def test_waiting_for_a_callback_needs_the_platform_api_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("VOLCANO_PLATFORM_API_URL", raising=False)
    runtime = RecordingContext()
    context = DurableContext(runtime, Engine())

    with pytest.raises(RuntimeError, match=r"^wait_for_callback\(\) needs VOLCANO"):
        _ = context.wait_for_callback("payment", Handoffs())
    assert runtime.submitter is None
