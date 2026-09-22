"""The public logger matches the optional runtime and checks consumer calls."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable

    from aws_durable_execution_sdk_python.logger import Logger

    from volcano_sdk.durable_authoring import DurableContext, DurableLogger, StepScope


def runtime_logger(logger: Logger) -> DurableLogger:
    return logger


def valid_messages(context: DurableContext, scope: StepScope) -> None:
    context.log.debug("starting %s", "order", extra={"order_id": 1})
    context.log.info({"status": "running"})
    context.log.warning("retrying")
    scope.log.error("step failed")


def valid_exception(scope: StepScope, operation: Callable[[], None]) -> None:
    try:
        operation()
    except ValueError:
        scope.log.exception("step failed with exception")


def invalid_messages(context: DurableContext, scope: StepScope) -> None:
    context.log.information("wrong method")  # type: ignore[attr-defined]
    scope.log.info("wrong option", extras={"operation": "charge"})  # type: ignore[call-arg]
