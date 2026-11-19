"""The User-Agent every request sends, so Volcano can count SDK use by version."""

from __future__ import annotations

import platform
import sys
from importlib import metadata
from typing import Final

_DISTRIBUTION = "volcano-sdk-python"
_UNKNOWN = "unknown"
_PLATFORMS = {"win32": "windows"}


def sdk_version() -> str:
    """Read the installed SDK version.

    Returns:
        The distribution's version, or ``unknown`` when it is not installed.

    """
    try:
        version: str | None = metadata.version(_DISTRIBUTION)
    except metadata.PackageNotFoundError:
        return _UNKNOWN
    return version or _UNKNOWN


def build_user_agent(
    *,
    version: str,
    implementation: str,
    python_version: str,
    system: str,
    machine: str,
) -> str:
    """Format the SDK, its version, and its runtime as a User-Agent value.

    Returns:
        ``volcano-sdk-python/<version> (<implementation>/<python>; <os>/<arch>)``.

    """
    os_name = _PLATFORMS.get(system, system)
    arch = machine.lower() or _UNKNOWN
    value = (
        f"{_DISTRIBUTION}/{version} "
        f"({implementation}/{python_version}; {os_name}/{arch})"
    )
    # HTTP clients encode header values as ASCII and raise on anything else.
    return "".join(char if char.isascii() else "?" for char in value)


USER_AGENT: Final = build_user_agent(
    version=sdk_version(),
    implementation=sys.implementation.name,
    python_version=platform.python_version(),
    system=sys.platform,
    machine=platform.machine(),
)


def user_agent_headers() -> dict[str, str]:
    """Return a fresh header mapping, since HTTP clients may add to it.

    Returns:
        The ``User-Agent`` header.

    """
    return {"User-Agent": USER_AGENT}
