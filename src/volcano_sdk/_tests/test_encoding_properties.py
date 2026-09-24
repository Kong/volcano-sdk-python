from __future__ import annotations

import base64
import json
from urllib.parse import parse_qsl, unquote, urlsplit

import pytest
from hypothesis import given, seed

from volcano_sdk import VolcanoClient, database_connection_string

from .property_support import PROPERTY_SEED
from .typing import Literal

BASE = "postgresql://user:password@db.example.test/app?sslmode=require&application_name=old"


@seed(PROPERTY_SEED)
@given(...)
def test_database_scope_encodes_user_as_one_parameter(value: str) -> None:
    user_id = f"user-{value}"
    result = urlsplit(database_connection_string(BASE, user_id=user_id))
    assert (result.scheme, result.netloc, result.path, result.fragment) == (
        "postgresql",
        "user:password@db.example.test",
        "/app",
        "",
    )
    assert parse_qsl(result.query) == [
        ("sslmode", "require"),
        ("application_name", f"volcano_user_access:{user_id}"),
    ]


@seed(PROPERTY_SEED)
@given(...)
def test_database_scope_replacement_keeps_only_the_latest_user(
    first: str, second: str
) -> None:
    initial = database_connection_string(BASE, user_id=f"first-{first}")
    assert database_connection_string(
        initial, user_id=f"second-{second}"
    ) == database_connection_string(BASE, user_id=f"second-{second}")


def public_url_client() -> VolcanoClient:
    payload = (
        base64.urlsafe_b64encode(json.dumps({"project_id": "project-123"}).encode())
        .decode()
        .rstrip("=")
    )
    return VolcanoClient(
        api_url="https://api.example.test", anon_key=f"header.{payload}.signature"
    )


@seed(PROPERTY_SEED)
@given(...)
def test_storage_path_encoding_preserves_every_character(value: str) -> None:
    path = f"folder/{value.replace('/', '_')} name"
    result = urlsplit(
        public_url_client().storage.from_("bucket &+#?%").get_public_url(path)
    )
    assert (result.scheme, result.netloc, result.query, result.fragment) == (
        "https",
        "api.example.test",
        "",
        "",
    )
    assert [unquote(part) for part in result.path.split("/")] == [
        "",
        "public",
        "project-123",
        "bucket &+#?%",
        *path.split("/"),
    ]


@seed(PROPERTY_SEED)
@given(...)
def test_storage_path_rejects_dot_segments(
    value: str, segment: Literal[".", ".."]
) -> None:
    path = f"folder-{value.replace('/', '_')}/{segment}/file"
    with pytest.raises(ValueError, match="dot segments"):
        _ = public_url_client().storage.from_("assets").get_public_url(path)
