from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from volcano_sdk.realtime import Realtime


def register_non_callable(realtime: Realtime) -> None:
    # Native mypy must report arg-type; unused-ignore rejects a missing diagnostic.
    realtime.on_connect(None)  # type: ignore[arg-type]
