"""Check the installed wheel with and without its durable extra."""

from __future__ import annotations

import sys
from importlib import import_module
from importlib.util import find_spec
from typing import cast

from volcano_sdk.durable_authoring import DurableContext, durable


def _handler(event: object, _context: DurableContext) -> object:
    return event


def main() -> None:
    """Exercise the optional runtime in a package environment managed by tox.

    Raises:
        AssertionError: The durable runtime does not reject invalid input.
        ValueError: The requested package scenario is not supported.

    """
    assert callable(durable)
    installed = find_spec("aws_durable_execution_sdk_python") is not None
    if sys.argv[1] == "base":
        assert not installed
    elif sys.argv[1] == "durable":
        assert installed
        exceptions = import_module("aws_durable_execution_sdk_python.exceptions")
        expected = cast("object", getattr(exceptions, "ExecutionError", None))
        assert isinstance(expected, type)
        assert issubclass(expected, BaseException)
        wrapped = durable(_handler)
        try:
            _ = wrapped({}, object())
        except expected:
            pass
        else:
            message = "invalid durable invocation unexpectedly succeeded"
            raise AssertionError(message)
    else:
        raise ValueError(sys.argv[1])


if __name__ == "__main__":
    main()
