from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import BinaryIO

    from volcano_sdk.auth import Auth
    from volcano_sdk.logs import Logs
    from volcano_sdk.models import (
        JSONValue,
        LinkedOAuthProvider,
        OAuthProviderTokenStatus,
        SessionPage,
        SignUpResult,
        User,
    )
    from volcano_sdk.realtime import Channel, Realtime
    from volcano_sdk.storage import StorageBucket

# Each deliberate invalid call must retain its native mypy diagnostic.
# Unused-ignore checking rejects a public signature that becomes unchecked.


def non_session_adoption(auth: Auth) -> None:
    _ = auth.set_session(object())  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def non_string_content_type(bucket: StorageBucket, source: BinaryIO) -> None:
    _ = bucket.upload("payload.bin", source, content_type=1)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def fractional_fetch_window(realtime: Realtime) -> None:
    _ = realtime.channel(
        "public:messages",
        channel_type="postgres",
        fetch_batch_window_ms=1.5,  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    )


def bytes_storage_paths(bucket: StorageBucket) -> None:
    _ = bucket.remove(b"abc")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def multiple_public_url_paths(bucket: StorageBucket) -> object:
    return bucket.get_public_url(
        ["first.txt", "second.txt"]  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    )


def integer_visibility(bucket: StorageBucket) -> None:
    _ = bucket.update_visibility("avatars/a.png", is_public=1)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def string_visibility(bucket: StorageBucket) -> None:
    _ = bucket.update_visibility("avatars/a.png", is_public="true")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def non_mapping_log_request(logs: Logs) -> None:
    _ = logs.activity("project-1", [])  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def non_json_log_request(logs: Logs, request: object) -> None:
    _ = logs.search("project-1", request)  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def unknown_oauth_sign_in(auth: Auth) -> None:
    _ = auth.sign_in_with_oauth(
        provider="invalid",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        redirect_to="https://app.example/callback",
        state="state-value",
    )


def unknown_oauth_link(auth: Auth) -> None:
    _ = auth.link_oauth_provider(provider="invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def unknown_oauth_unlink(auth: Auth) -> None:
    auth.unlink_oauth_provider(provider="invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def unknown_oauth_token(auth: Auth) -> None:
    _ = auth.get_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def unknown_oauth_token_refresh(auth: Auth) -> None:
    _ = auth.refresh_oauth_provider_token(provider="invalid")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


def unknown_oauth_api_provider(auth: Auth) -> None:
    _ = auth.call_oauth_api(
        provider="invalid",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        endpoint="/user",
    )


def unsupported_oauth_api_method(auth: Auth) -> None:
    _ = auth.call_oauth_api(
        provider="github",
        endpoint="/user",
        method="DELETE",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    )


def unsupported_postgres_change_event(channel: Channel) -> None:
    _ = channel.on_postgres_changes(
        "UPSERT",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        schema="public",
        table="messages",
        callback=lambda _change: None,
    )


def unsupported_realtime_channel_type(realtime: Realtime) -> None:
    _ = realtime.channel("contract", channel_type="presense")  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]


async def remove_unsupported_realtime_channel_type(realtime: Realtime) -> None:
    await realtime.remove_channel(
        "contract",
        channel_type="presense",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
    )


def assign_session_page(page: SessionPage) -> None:
    page.page = 3  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def assign_linked_provider(provider: LinkedOAuthProvider) -> None:
    provider.provider = "github"  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def assign_provider_token(status: OAuthProviderTokenStatus) -> None:
    status.provider = "github"  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def assign_sign_up_message(result: SignUpResult) -> None:
    result.message = "changed"  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def assign_user_email(user: User) -> None:
    user.email = "changed@example.com"  # type: ignore[misc]  # pyright: ignore[reportAttributeAccessIssue]


def assign_snapshot_value(snapshot: Mapping[str, JSONValue]) -> None:
    snapshot["email"] = "changed"  # type: ignore[index]  # pyright: ignore[reportIndexIssue]


def assign_metadata_value(
    metadata: Mapping[str, JSONValue] | None, key: str, value: JSONValue
) -> None:
    assert metadata is not None
    metadata[key] = value  # type: ignore[index]  # pyright: ignore[reportIndexIssue]


def unsupported_hosted_auth_action(auth: Auth) -> None:
    _ = auth.get_hosted_auth_url(
        project_id="project-id",
        action="device",  # type: ignore[arg-type]  # pyright: ignore[reportArgumentType]
        state="state-value",
    )
