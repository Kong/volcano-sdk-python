"""Transport methods that fail if an unrelated facade reaches a test double."""

from __future__ import annotations

from typing_extensions import override

from volcano_sdk._transport import Transport

from .typing import Never


class RejectingTransport(Transport):
    """Provide the core transport interface without accepting unexpected calls."""

    @override
    def auth_signin(self, *, authorization: str, email: str, password: str) -> Never:
        del authorization, email, password
        raise AssertionError

    @override
    def query_database_select(
        self, *, authorization: str, database_name: str, body: dict[str, object]
    ) -> Never:
        del authorization, database_name, body
        raise AssertionError

    @override
    def query_database_insert(
        self, *, authorization: str, database_name: str, body: dict[str, object]
    ) -> Never:
        del authorization, database_name, body
        raise AssertionError

    @override
    def query_database_update(
        self, *, authorization: str, database_name: str, body: dict[str, object]
    ) -> Never:
        del authorization, database_name, body
        raise AssertionError

    @override
    def query_database_delete(
        self, *, authorization: str, database_name: str, body: dict[str, object]
    ) -> Never:
        del authorization, database_name, body
        raise AssertionError

    @override
    def upload_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> Never:
        del authorization, bucket_name, path, data, content_type
        raise AssertionError

    @override
    def download_storage_object(
        self,
        *,
        authorization: str,
        bucket_name: str,
        path: str,
        byte_range: str | None = None,
    ) -> Never:
        del authorization, bucket_name, path, byte_range
        raise AssertionError

    @override
    def acquire_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        ttl: int,
        token: str,
        request_id: str | None = None,
    ) -> Never:
        del authorization, key, ttl, token, request_id
        raise AssertionError

    @override
    def release_project_lock(
        self,
        *,
        authorization: str,
        key: str,
        token: str,
        request_id: str | None = None,
    ) -> Never:
        del authorization, key, token, request_id
        raise AssertionError
