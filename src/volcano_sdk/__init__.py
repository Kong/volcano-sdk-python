"""Public Volcano SDK facade."""

from .client import VolcanoClient
from .errors import (
    AuthenticationError,
    ConflictError,
    NotFoundError,
    RateLimitedError,
    ServerError,
    SessionChangedError,
    TransportError,
    ValidationError,
    VolcanoError,
)
from .models import (
    AuthSession,
    EmailChangeResult,
    LinkedOAuthProvider,
    LockLease,
    OAuthProviderName,
    Session,
    SessionPage,
    SignUpResult,
    User,
)

__all__ = [
    "AuthSession",
    "AuthenticationError",
    "ConflictError",
    "EmailChangeResult",
    "LinkedOAuthProvider",
    "LockLease",
    "NotFoundError",
    "OAuthProviderName",
    "RateLimitedError",
    "ServerError",
    "Session",
    "SessionChangedError",
    "SessionPage",
    "SignUpResult",
    "TransportError",
    "User",
    "ValidationError",
    "VolcanoClient",
    "VolcanoError",
]
