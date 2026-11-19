from __future__ import annotations

import re
from importlib import metadata

_VERSION = re.escape(metadata.version("volcano-sdk-python"))
_RUNTIME = r"[a-z][a-z0-9_]*/\d+\.\d+\.\d+[a-z0-9+]*"
_PLATFORM = r"[a-z][a-z0-9]*/[a-z0-9_]+"
USER_AGENT_PATTERN = re.compile(
    rf"volcano-sdk-python/{_VERSION} \({_RUNTIME}; {_PLATFORM}\)"
)
