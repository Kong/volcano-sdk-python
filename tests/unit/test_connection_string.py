import pytest

from volcano_sdk import database_connection_string


def test_database_connection_string_selects_full_access() -> None:
    base = (
        "postgresql://user:p%40ss@db.example.com/app?"
        "sslmode=require&application_name=old#target"
    )

    assert database_connection_string(base) == (
        "postgresql://user:p%40ss@db.example.com/app?"
        "sslmode=require&application_name=volcano_full_access#target"
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


@pytest.mark.parametrize("value", ["databases/app", "postgres://db.example.com/%"])
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
