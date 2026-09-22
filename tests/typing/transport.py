from __future__ import annotations

from typing import TYPE_CHECKING, assert_type

from volcano_sdk._transport import invoke, invoke_async, response_payload

if TYPE_CHECKING:
    from volcano_sdk._transport import TransportResponse

# These deliberate errors are checked by native mypy and its unused-ignore rule.
# They are never executed by pytest or shipped in the SDK.
response_payload(object(), 200)  # type: ignore[arg-type]


def unknown_response_payload(response: TransportResponse) -> None:
    assert_type(response.payload, object)


def operation(*, value: int) -> str:
    return str(value)


async def async_operation(*, value: int) -> str:
    return str(value)


def invalid_sync() -> None:
    invoke(operation, value="invalid")  # type: ignore[arg-type]
    invoke(operation, misspelled=1)  # type: ignore[call-arg]


async def invalid_async() -> None:
    await invoke_async(async_operation, value="invalid")  # type: ignore[arg-type]
    await invoke_async(async_operation, misspelled=1)  # type: ignore[call-arg]
