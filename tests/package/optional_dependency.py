"""Check the installed wheel with and without its durable extra."""

from __future__ import annotations

import sys
from importlib.util import find_spec

from volcano_sdk.durable_authoring import _Engine, durable


def main() -> None:
    """Exercise the optional runtime in a package environment managed by tox."""
    assert callable(durable)
    installed = find_spec("aws_durable_execution_sdk_python") is not None
    if sys.argv[1] == "base":
        assert not installed
    elif sys.argv[1] == "durable":
        assert installed
        _Engine.load()
    else:
        raise ValueError(sys.argv[1])


if __name__ == "__main__":
    main()
