from volcano_sdk import SignUpResult, VolcanoClient


def test_package_exports_client() -> None:
    assert VolcanoClient.__name__ == "VolcanoClient"


def test_package_exports_sign_up_result() -> None:
    result = SignUpResult(confirmation_required=True, message="Check your email")

    assert result.confirmation_required is True
    assert result.message == "Check your email"
