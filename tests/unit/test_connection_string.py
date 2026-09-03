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


def test_database_connection_string_ignores_at_sign_in_query_value() -> None:
    assert database_connection_string("postgresql://host/db?options=foo@bar") == (
        "postgresql://host/db?options=foo@bar&application_name=volcano_full_access"
    )


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
        database_connection_string(value)


def test_database_connection_string_requires_a_value() -> None:
    with pytest.raises(
        ValueError,
        match=(
            r"database_connection_string: base_connection_string \(DATABASE_URL\) "
            "is required"
        ),
    ):
        database_connection_string("")
