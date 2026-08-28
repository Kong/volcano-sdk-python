import volcano_sdk
from volcano_sdk import VolcanoClient


def test_package_exports_client() -> None:
    assert VolcanoClient.__name__ == "VolcanoClient"


def test_package_exports_the_public_sdk_contract() -> None:
    assert volcano_sdk.__all__ == [
        "AuthSession",
        "AuthenticationError",
        "AuthorizationRequest",
        "ConflictError",
        "EmailChangeResult",
        "JSONValue",
        "LockLease",
        "MessageResult",
        "NotFoundError",
        "OAuthProvider",
        "OAuthProviderName",
        "OAuthTokenResult",
        "RateLimitedError",
        "ServerError",
        "Session",
        "SessionPage",
        "SignUpResult",
        "TransportError",
        "User",
        "ValidationError",
        "VolcanoClient",
        "VolcanoError",
    ]
