from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import BinaryIO

    from volcano_sdk.auth import Auth
    from volcano_sdk.logs import Logs
    from volcano_sdk.models import (
        LinkedOAuthProvider,
        OAuthProviderTokenStatus,
        SessionPage,
    )
    from volcano_sdk.realtime import Channel, Realtime
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


def integer_visibility(bucket: StorageBucket) -> None:
    bucket.update_visibility("avatars/a.png", is_public=1)  # type: ignore[arg-type]


def string_visibility(bucket: StorageBucket) -> None:
    bucket.update_visibility("avatars/a.png", is_public="true")  # type: ignore[arg-type]


def non_mapping_log_request(logs: Logs) -> None:
    logs.activity("project-1", [])  # type: ignore[arg-type]


def unknown_oauth_sign_in(auth: Auth) -> None:
    auth.sign_in_with_oauth(
        provider="invalid",  # type: ignore[arg-type]
        redirect_to="https://app.example/callback",
        state="state-value",
    )


def unknown_oauth_link(auth: Auth) -> None:
    auth.link_oauth_provider(provider="invalid")  # type: ignore[arg-type]


def unknown_oauth_unlink(auth: Auth) -> None:
    auth.unlink_oauth_provider(provider="invalid")  # type: ignore[arg-type]


def unknown_oauth_token(auth: Auth) -> None:
    auth.get_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]


def unknown_oauth_token_refresh(auth: Auth) -> None:
    auth.refresh_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]


def unknown_oauth_api_provider(auth: Auth) -> None:
    auth.call_oauth_api(
        provider="invalid",  # type: ignore[arg-type]
        endpoint="/user",
    )


def unsupported_oauth_api_method(auth: Auth) -> None:
    auth.call_oauth_api(
        provider="github",
        endpoint="/user",
        method="DELETE",  # type: ignore[arg-type]
    )


def unsupported_postgres_change_event(channel: Channel) -> None:
    channel.on_postgres_changes(
        "UPSERT",  # type: ignore[arg-type]
        schema="public",
        table="messages",
        callback=lambda _change: None,
    )


def assign_session_page(page: SessionPage) -> None:
    page.page = 3  # type: ignore[misc]


def assign_linked_provider(provider: LinkedOAuthProvider) -> None:
    provider.provider = "github"  # type: ignore[misc]


def assign_provider_token(status: OAuthProviderTokenStatus) -> None:
    status.provider = "github"  # type: ignore[misc]
