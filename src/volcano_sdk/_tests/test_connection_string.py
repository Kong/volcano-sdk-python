import pytest

from volcano_sdk import database_connection_string


def test_database_connection_string_selects_full_access() -> None:
    base = (
        "postgresql://user:p%40ss@db.example.com/app?"
        "sslmode=require&application_name=old"
    )

    assert database_connection_string(base) == (
        "postgresql://user:p%40ss@db.example.com/app?"
        "sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_preserves_unrelated_query_encoding() -> None:
    base = (
        "postgresql://db.example.com/app?"
        "options=-c+search_path%3Dapp&application_name=old"
    )

    assert database_connection_string(base) == (
        "postgresql://db.example.com/app?"
        "options=-c+search_path%3Dapp&application_name=volcano_full_access"
    )


def test_database_connection_string_selects_encoded_user_access() -> None:
    assert database_connection_string(
        "postgres://user:password@db.example.com/app",
        user_id="user + one",
    ) == (
        "postgres://user:password@db.example.com/app?"
        "application_name=volcano_user_access%3Auser%20%2B%20one"
    )


def test_database_connection_string_escapes_slashes_in_user_scope() -> None:
    assert (
        database_connection_string("postgres://host/app", user_id="tenant/child")
        == "postgres://host/app?application_name=volcano_user_access%3Atenant%2Fchild"
    )


def test_database_connection_string_treats_empty_user_id_as_full_access() -> None:
    result = database_connection_string(
        "postgres://user:password@db.example.com/app",
        user_id="",
    )

    assert result.endswith("application_name=volcano_full_access")


def test_database_connection_string_preserves_hostless_uri_authority() -> None:
    assert database_connection_string("postgresql:///app") == (
        "postgresql:///app?application_name=volcano_full_access"
    )


def test_database_connection_string_preserves_libpq_credentials() -> None:
    assert database_connection_string("postgres://u:pa?ss#word@host/db") == (
        "postgres://u:pa?ss#word@host/db?application_name=volcano_full_access"
    )


def test_database_connection_string_accepts_multi_host_ipv6_uri() -> None:
    assert database_connection_string("postgresql://[::1],[::2]/db") == (
        "postgresql://[::1],[::2]/db?application_name=volcano_full_access"
    )


def test_database_connection_string_drops_trailing_query_separator() -> None:
    assert database_connection_string("postgresql://host/db?sslmode=require&") == (
        "postgresql://host/db?sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_drops_repeated_trailing_separators() -> None:
    assert database_connection_string("postgresql://host/db?sslmode=require&&&") == (
        "postgresql://host/db?sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_drops_only_empty_parameters() -> None:
    assert database_connection_string("postgresql://host/db?&&") == (
        "postgresql://host/db?application_name=volcano_full_access"
    )


@pytest.mark.parametrize(
    "query", ["mode=X", "mode=with space", "mode=XX&XX", "mode=x&&other=y"]
)
def test_database_connection_string_preserves_unrelated_query_fields(
    query: str,
) -> None:
    base = f"postgresql://host/db?{query}"

    assert database_connection_string(base) == (
        f"{base}&application_name=volcano_full_access"
    )


def test_database_connection_string_ignores_at_sign_in_query_value() -> None:
    assert database_connection_string("postgresql://host/db?options=foo@bar") == (
        "postgresql://host/db?options=foo@bar&application_name=volcano_full_access"
    )


def test_database_connection_string_keeps_at_sign_in_query_before_a_slash() -> None:
    assert database_connection_string("postgresql://host/db?options=foo@bar/path") == (
        "postgresql://host/db?options=foo@bar/path&application_name=volcano_full_access"
    )


def test_database_connection_string_keeps_credential_question_mark() -> None:
    base = "postgres://u:p?@host?application_name=old&sslmode=require"

    assert database_connection_string(base) == (
        "postgres://u:p?@host?sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_finds_query_immediately_after_userinfo() -> None:
    assert database_connection_string("postgres://u@?sslmode=require") == (
        "postgres://u@?sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_ignores_later_at_sign_in_query() -> None:
    base = "postgres://u@host?options=a@b"

    assert database_connection_string(base) == (
        f"{base}&application_name=volcano_full_access"
    )


def test_database_connection_string_keeps_question_mark_in_query_value() -> None:
    base = "postgres://host/db?application_name=old?mode&sslmode=require"

    assert database_connection_string(base) == (
        "postgres://host/db?sslmode=require&application_name=volcano_full_access"
    )


def test_database_connection_string_replaces_name_containing_equals() -> None:
    assert database_connection_string(
        "postgres://host/db?application_name=old=more&sslmode=require"
    ) == ("postgres://host/db?sslmode=require&application_name=volcano_full_access")


@pytest.mark.parametrize(
    "value",
    [
        "databases/app",
        "https://db.example.com/app",
        "postgres://db.example.com/%",
    ],
)
def test_database_connection_string_rejects_invalid_url(value: str) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "database_connection_string: base_connection_string is not a valid "
            "connection URL"
        ),
    ):
        _ = database_connection_string(value)


def test_database_connection_string_requires_a_value() -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"database_connection_string: base_connection_string \(DATABASE_URL\) "
            "is required"
        ),
    ):
        _ = database_connection_string("")
