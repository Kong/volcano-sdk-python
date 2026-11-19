from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import httpx
import pytest

from volcano_sdk import VolcanoClient
from volcano_sdk._generated.api.sandboxes import list_sandbox_presets
from volcano_sdk._path_segments import check_request_path
from volcano_sdk._transport import GeneratedTransport
from volcano_sdk._transport_base import TransportBase
from volcano_sdk._transport_sandbox import SandboxRequest

from .test_facade import FakeTransport, anon_key_with_project_id, signed_in_client

if TYPE_CHECKING:
    from collections.abc import Callable

PROJECT = "00000000-0000-4000-8000-000000000001"
EXECUTION = "00000000-0000-4000-8000-0000000000e1"


def recording_transport() -> tuple[GeneratedTransport, list[httpx.Request]]:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev/base",
        httpx_transport=httpx.MockTransport(handle),
    )
    return transport, requests


@pytest.mark.parametrize(
    "path",
    [
        "/databases/../query/select",
        "/databases/./query/select",
        "/locks/%2E%2e/lease",
        "/locks/.%2e",
        "/storage/b/..%2F..%2Fprojects",
        "/storage/b/a%2f..%2f..",
        "/auth/user/sessions/",
        "/databases//query/select",
        "/storage/b/folder%2F",
    ],
)
def test_request_paths_that_leave_their_route_are_refused(path: str) -> None:
    with pytest.raises(ValueError, match="Request path cannot contain"):
        _ = check_request_path(path)


@pytest.mark.parametrize(
    "path",
    [
        "/storage/b/a..b.txt",
        "/storage/b/folder%2Fa.txt",
        "/storage/b/%252e%252e",
        "/storage/b/.hidden",
        "/functions/resolve?name=..",
    ],
)
def test_request_paths_inside_their_route_are_kept(path: str) -> None:
    assert check_request_path(path) == path


def database_dots(transport: GeneratedTransport) -> object:
    return transport.query_database_select(
        authorization="token", database_name="..", body={"table": "t"}
    )


def database_multiline(transport: GeneratedTransport) -> object:
    return transport.query_database_select(
        authorization="token", database_name="app\n..", body={"table": "t"}
    )


def database_too_long(transport: GeneratedTransport) -> object:
    return transport.query_database_select(
        authorization="token", database_name="a" * 65, body={"table": "t"}
    )


def lock_dots(transport: GeneratedTransport) -> object:
    return transport.get_project_lock(authorization="token", key="..")


def session_dots(transport: GeneratedTransport) -> object:
    return transport.auth_delete_my_session(authorization="token", session_id="..")


def session_empty(transport: GeneratedTransport) -> object:
    return transport.auth_delete_my_session(authorization="token", session_id="")


def durable_function_dots(transport: GeneratedTransport) -> object:
    return transport.get_durable_execution(
        authorization="token",
        project_id=PROJECT,
        function_id="..",
        execution_id=EXECUTION,
    )


def object_path_parent(transport: GeneratedTransport) -> object:
    return transport.download_storage_object(
        authorization="token", bucket_name="assets", path="../../a.txt"
    )


def object_path_nested_parent(transport: GeneratedTransport) -> object:
    return transport.download_storage_object(
        authorization="token", bucket_name="b", path="a/../../../b.txt"
    )


def bucket_dots(transport: GeneratedTransport) -> object:
    return transport.download_storage_object(
        authorization="token", bucket_name="..", path="a.txt"
    )


def bucket_slash(transport: GeneratedTransport) -> object:
    return transport.delete_storage_object(
        authorization="token", bucket_name="a/b", path="a.txt"
    )


@pytest.mark.parametrize(
    "send",
    [
        database_dots,
        database_multiline,
        database_too_long,
        lock_dots,
        session_dots,
        session_empty,
        durable_function_dots,
        object_path_parent,
        object_path_nested_parent,
        bucket_dots,
        bucket_slash,
    ],
    ids=[
        "database_dots",
        "database_multiline",
        "database_too_long",
        "lock_dots",
        "session_dots",
        "session_empty",
        "durable_function_dots",
        "object_path_parent",
        "object_path_nested_parent",
        "bucket_dots",
        "bucket_slash",
    ],
)
def test_generated_transport_refuses_values_that_leave_their_route(
    send: Callable[[GeneratedTransport], object],
) -> None:
    transport, requests = recording_transport()

    with pytest.raises(ValueError, match=r"cannot contain|must"):
        _ = send(transport)

    assert requests == []


def test_async_generated_requests_are_checked_too() -> None:
    transport, requests = recording_transport()

    async def query() -> object:
        return await transport.query_database_select_async(
            authorization="token", database_name="..", body={"table": "t"}
        )

    with pytest.raises(ValueError, match="Database name"):
        _ = asyncio.run(query())

    assert requests == []


def test_generated_transport_sends_a_leading_slash_path_relative_to_its_bucket() -> (
    None
):
    transport, requests = recording_transport()

    _ = transport.download_storage_object(
        authorization="token", bucket_name="assets", path="/folder/a..b.txt"
    )

    assert requests[0].url.raw_path == b"/base/storage/assets/folder%2Fa..b.txt"
    assert requests[0].headers["authorization"] == "Bearer token"


def download(client: VolcanoClient) -> object:
    return client.storage.from_("assets").download("a/1/../../b/2/x.txt")


def upload(client: VolcanoClient) -> object:
    return client.storage.from_("assets").upload("a/../../../b.txt", b"x")


def remove(client: VolcanoClient) -> object:
    return client.storage.from_("assets").remove(["ok.txt", "a//b"])


def move(client: VolcanoClient) -> object:
    return client.storage.from_("assets").move("a.txt", "..")


def copy(client: VolcanoClient) -> object:
    return client.storage.from_("assets").copy("./a.txt", "b.txt")


def visibility(client: VolcanoClient) -> object:
    return client.storage.from_("assets").update_visibility("x/", is_public=True)


def upload_session(client: VolcanoClient) -> object:
    return client.storage.from_("assets").create_upload_session("../x", total_size=1)


@pytest.mark.parametrize(
    "attempt",
    [download, upload, remove, move, copy, visibility, upload_session],
    ids=["download", "upload", "remove", "move", "copy", "visibility", "session"],
)
def test_storage_facade_refuses_paths_with_dot_or_empty_segments(
    attempt: Callable[[VolcanoClient], object],
) -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    calls = list(transport.calls)

    with pytest.raises(ValueError, match="cannot contain"):
        _ = attempt(client)

    assert transport.calls == calls


@pytest.mark.parametrize("bucket", ["..", "a/b", "assets\n..", "a" * 65])
def test_storage_facade_refuses_invalid_bucket_names(bucket: str) -> None:
    transport = FakeTransport()
    client = signed_in_client(transport)
    calls = list(transport.calls)

    with pytest.raises(ValueError, match="Bucket name"):
        _ = client.storage.from_(bucket).download("a.txt")

    assert transport.calls == calls


@pytest.mark.parametrize("function_name", ["..", ".", "a/b"])
def test_durable_facade_refuses_identifiers_that_are_not_one_segment(
    function_name: str,
) -> None:
    transport = FakeTransport()
    client = VolcanoClient(anon_key="anon-key", _transport=transport)

    with pytest.raises(ValueError, match="function_name"):
        _ = client.durable.get(PROJECT, function_name, EXECUTION)

    assert transport.calls == []


@pytest.mark.parametrize("project_id", ["..", ".", "a/b"])
def test_hosted_auth_url_refuses_project_ids_that_are_not_one_segment(
    project_id: str,
) -> None:
    client = VolcanoClient(anon_key="anon-key")

    with pytest.raises(
        ValueError, match=r'^project_id cannot contain "/" or be "\." or "\.\."$'
    ):
        _ = client.auth.get_hosted_auth_url(project_id=project_id, state="s")


@pytest.mark.parametrize("project_id", ["..", "a/b"])
def test_public_url_refuses_an_anon_key_project_that_is_not_one_segment(
    project_id: str,
) -> None:
    client = VolcanoClient(anon_key=anon_key_with_project_id(project_id))

    with pytest.raises(
        ValueError,
        match=r'^Project ID in anon key cannot contain "/" or be "\." or "\.\."$',
    ):
        _ = client.storage.from_("assets").get_public_url("a.txt")


def test_realtime_refuses_an_invalid_database_name_when_it_is_set() -> None:
    client = VolcanoClient(anon_key="anon-key")

    with pytest.raises(ValueError, match="Database name"):
        client.realtime.set_database_name("..")
    client.realtime.set_database_name(None)
    assert client.realtime.database_name is None


def test_function_urls_resolved_off_the_api_host_are_not_route_checked() -> None:
    transport, requests = recording_transport()

    _ = transport.invoke_function_url(
        authorization="token", invoke_url="https://fn.example/", payload={}
    )

    assert str(requests[0].url) == "https://fn.example/"


def test_route_checked_clients_keep_the_configured_timeouts() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": []})

    transport = GeneratedTransport(
        api_url="https://api.test.volcano.dev",
        timeout=7,
        httpx_transport=httpx.MockTransport(handle),
    )

    _ = transport.download_storage_object(
        authorization="token", bucket_name="assets", path="a.txt"
    )
    _ = transport.sandbox_request(
        authorization="token",
        request=SandboxRequest("get_sandbox_session", PROJECT, timeout=300),
    )
    _ = transport.sandbox_request(
        authorization=None, request=SandboxRequest("list_sandbox_presets", timeout=3)
    )
    _ = transport.sandbox_request(
        authorization=None, request=SandboxRequest("list_sandbox_presets", timeout=30)
    )

    async def query() -> object:
        return await transport.query_database_select_async(
            authorization="token", database_name="app", body={"table": "t"}
        )

    _ = asyncio.run(query())

    for request, limit in zip(requests, (7, 300, 7, 30, 7), strict=True):
        assert request.extensions["timeout"] == dict.fromkeys(
            ("connect", "read", "write", "pool"), limit
        )


def test_a_64_character_database_name_is_sent() -> None:
    transport, requests = recording_transport()

    _ = transport.query_database_select(
        authorization="token", database_name="a" * 64, body={"table": "t"}
    )

    assert requests[0].url.path == f"/base/databases/{'a' * 64}/query/select"


class AsyncPublicTransport(TransportBase):
    async def presets(self, path: str = "") -> object:
        async with self._public_client(timeout=9) as client:
            if path:
                return await client.get_async_httpx_client().get(path)
            return await list_sandbox_presets.asyncio_detailed(client=client)


def test_asynchronous_public_requests_are_route_checked() -> None:
    requests: list[httpx.Request] = []

    def handle(request: httpx.Request) -> httpx.Response:
        requests.append(request)
        return httpx.Response(200, json={"data": []})

    transport = AsyncPublicTransport(
        api_url="https://api.test.volcano.dev/base",
        httpx_transport=httpx.MockTransport(handle),
    )

    _ = asyncio.run(transport.presets())
    with pytest.raises(ValueError, match="Request path cannot contain"):
        _ = asyncio.run(transport.presets("/sandboxes/../projects"))

    assert len(requests) == 1
    assert requests[0].url.path.startswith("/base/")
    assert requests[0].headers["user-agent"].startswith("volcano-sdk-python/")
    assert "authorization" not in requests[0].headers
    assert requests[0].extensions["timeout"] == dict.fromkeys(
        ("connect", "read", "write", "pool"), 9
    )
