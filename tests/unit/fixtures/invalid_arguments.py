from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import BinaryIO

    from volcano_sdk.auth import Auth
    from volcano_sdk.realtime import Realtime
    from volcano_sdk.storage import StorageBucket

# Each deliberate invalid call must retain its native mypy diagnostic.
# Unused-ignore checking rejects a public signature that becomes unchecked.


def non_session_adoption(auth: Auth) -> None:
    auth.set_session(object())  # type: ignore[arg-type]


def non_string_content_type(bucket: StorageBucket, source: BinaryIO) -> None:
    bucket.upload("payload.bin", source, content_type=1)  # type: ignore[arg-type]


def fractional_fetch_window(realtime: Realtime) -> None:
    realtime.channel(
        "public:messages",
        channel_type="postgres",
        fetch_batch_window_ms=1.5,  # type: ignore[arg-type]
    )


def bytes_storage_paths(bucket: StorageBucket) -> None:
    bucket.remove(b"abc")  # type: ignore[arg-type]


def non_boolean_visibility(bucket: StorageBucket, value: int | str) -> None:
    bucket.update_visibility("avatars/a.png", is_public=value)  # type: ignore[arg-type]
