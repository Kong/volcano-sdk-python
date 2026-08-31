from volcano_sdk import SignUpResult, User, VolcanoClient


def test_package_exports_client() -> None:
    assert VolcanoClient.__name__ == "VolcanoClient"


def test_package_exports_sign_up_result() -> None:
    result = SignUpResult(confirmation_required=True, message="Check your email")

    assert result.confirmation_required is True
    assert result.message == "Check your email"


def test_package_exports_user() -> None:
    user = User(id="user-123", email="user@example.com", status="active")

    assert user.id == "user-123"


def test_user_preserves_the_existing_positional_constructor() -> None:
    confirmed = True
    user = User(
        "user-123",
        "user@example.com",
        "active",
        confirmed,
        {"role": "admin"},
    )

    assert user.email_confirmed is True
    assert user.user_metadata == {"role": "admin"}
