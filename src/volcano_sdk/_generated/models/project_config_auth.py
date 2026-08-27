from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_auth_cors import ProjectConfigAuthCORS
  from ..models.project_config_auth_email import ProjectConfigAuthEmail
  from ..models.project_config_auth_email_verification import ProjectConfigAuthEmailVerification
  from ..models.project_config_auth_managed_pages import ProjectConfigAuthManagedPages
  from ..models.project_config_auth_password import ProjectConfigAuthPassword
  from ..models.project_config_auth_password_reset import ProjectConfigAuthPasswordReset
  from ..models.project_config_auth_providers import ProjectConfigAuthProviders
  from ..models.project_config_auth_rate_limits import ProjectConfigAuthRateLimits
  from ..models.project_config_auth_sessions import ProjectConfigAuthSessions
  from ..models.project_config_auth_signup import ProjectConfigAuthSignup
  from ..models.project_config_auth_tokens import ProjectConfigAuthTokens





T = TypeVar("T", bound="ProjectConfigAuth")



@_attrs_define
class ProjectConfigAuth:
    """ Authentication settings, grouped like the dashboard auth-settings tabs.

        Attributes:
            tokens (ProjectConfigAuthTokens | Unset): Token lifetimes in seconds.
            sessions (ProjectConfigAuthSessions | Unset):
            signup (ProjectConfigAuthSignup | Unset):
            rate_limits (ProjectConfigAuthRateLimits | Unset): Rate limits per hour.
            password (ProjectConfigAuthPassword | Unset):
            password_reset (ProjectConfigAuthPasswordReset | Unset):
            email_verification (ProjectConfigAuthEmailVerification | Unset):
            cors (ProjectConfigAuthCORS | Unset):
            providers (ProjectConfigAuthProviders | Unset):
            email (ProjectConfigAuthEmail | Unset):
            managed_pages (ProjectConfigAuthManagedPages | Unset):
     """

    tokens: ProjectConfigAuthTokens | Unset = UNSET
    sessions: ProjectConfigAuthSessions | Unset = UNSET
    signup: ProjectConfigAuthSignup | Unset = UNSET
    rate_limits: ProjectConfigAuthRateLimits | Unset = UNSET
    password: ProjectConfigAuthPassword | Unset = UNSET
    password_reset: ProjectConfigAuthPasswordReset | Unset = UNSET
    email_verification: ProjectConfigAuthEmailVerification | Unset = UNSET
    cors: ProjectConfigAuthCORS | Unset = UNSET
    providers: ProjectConfigAuthProviders | Unset = UNSET
    email: ProjectConfigAuthEmail | Unset = UNSET
    managed_pages: ProjectConfigAuthManagedPages | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_auth_cors import ProjectConfigAuthCORS
        from ..models.project_config_auth_email import ProjectConfigAuthEmail
        from ..models.project_config_auth_email_verification import ProjectConfigAuthEmailVerification
        from ..models.project_config_auth_managed_pages import ProjectConfigAuthManagedPages
        from ..models.project_config_auth_password import ProjectConfigAuthPassword
        from ..models.project_config_auth_password_reset import ProjectConfigAuthPasswordReset
        from ..models.project_config_auth_providers import ProjectConfigAuthProviders
        from ..models.project_config_auth_rate_limits import ProjectConfigAuthRateLimits
        from ..models.project_config_auth_sessions import ProjectConfigAuthSessions
        from ..models.project_config_auth_signup import ProjectConfigAuthSignup
        from ..models.project_config_auth_tokens import ProjectConfigAuthTokens
        tokens: dict[str, Any] | Unset = UNSET
        if not isinstance(self.tokens, Unset):
            tokens = self.tokens.to_dict()

        sessions: dict[str, Any] | Unset = UNSET
        if not isinstance(self.sessions, Unset):
            sessions = self.sessions.to_dict()

        signup: dict[str, Any] | Unset = UNSET
        if not isinstance(self.signup, Unset):
            signup = self.signup.to_dict()

        rate_limits: dict[str, Any] | Unset = UNSET
        if not isinstance(self.rate_limits, Unset):
            rate_limits = self.rate_limits.to_dict()

        password: dict[str, Any] | Unset = UNSET
        if not isinstance(self.password, Unset):
            password = self.password.to_dict()

        password_reset: dict[str, Any] | Unset = UNSET
        if not isinstance(self.password_reset, Unset):
            password_reset = self.password_reset.to_dict()

        email_verification: dict[str, Any] | Unset = UNSET
        if not isinstance(self.email_verification, Unset):
            email_verification = self.email_verification.to_dict()

        cors: dict[str, Any] | Unset = UNSET
        if not isinstance(self.cors, Unset):
            cors = self.cors.to_dict()

        providers: dict[str, Any] | Unset = UNSET
        if not isinstance(self.providers, Unset):
            providers = self.providers.to_dict()

        email: dict[str, Any] | Unset = UNSET
        if not isinstance(self.email, Unset):
            email = self.email.to_dict()

        managed_pages: dict[str, Any] | Unset = UNSET
        if not isinstance(self.managed_pages, Unset):
            managed_pages = self.managed_pages.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
        })
        if tokens is not UNSET:
            field_dict["tokens"] = tokens
        if sessions is not UNSET:
            field_dict["sessions"] = sessions
        if signup is not UNSET:
            field_dict["signup"] = signup
        if rate_limits is not UNSET:
            field_dict["rate_limits"] = rate_limits
        if password is not UNSET:
            field_dict["password"] = password
        if password_reset is not UNSET:
            field_dict["password_reset"] = password_reset
        if email_verification is not UNSET:
            field_dict["email_verification"] = email_verification
        if cors is not UNSET:
            field_dict["cors"] = cors
        if providers is not UNSET:
            field_dict["providers"] = providers
        if email is not UNSET:
            field_dict["email"] = email
        if managed_pages is not UNSET:
            field_dict["managed_pages"] = managed_pages

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_auth_cors import ProjectConfigAuthCORS
        from ..models.project_config_auth_email import ProjectConfigAuthEmail
        from ..models.project_config_auth_email_verification import ProjectConfigAuthEmailVerification
        from ..models.project_config_auth_managed_pages import ProjectConfigAuthManagedPages
        from ..models.project_config_auth_password import ProjectConfigAuthPassword
        from ..models.project_config_auth_password_reset import ProjectConfigAuthPasswordReset
        from ..models.project_config_auth_providers import ProjectConfigAuthProviders
        from ..models.project_config_auth_rate_limits import ProjectConfigAuthRateLimits
        from ..models.project_config_auth_sessions import ProjectConfigAuthSessions
        from ..models.project_config_auth_signup import ProjectConfigAuthSignup
        from ..models.project_config_auth_tokens import ProjectConfigAuthTokens
        d = dict(src_dict)
        _tokens = d.pop("tokens", UNSET)
        tokens: ProjectConfigAuthTokens | Unset
        if isinstance(_tokens,  Unset):
            tokens = UNSET
        else:
            tokens = ProjectConfigAuthTokens.from_dict(_tokens)




        _sessions = d.pop("sessions", UNSET)
        sessions: ProjectConfigAuthSessions | Unset
        if isinstance(_sessions,  Unset):
            sessions = UNSET
        else:
            sessions = ProjectConfigAuthSessions.from_dict(_sessions)




        _signup = d.pop("signup", UNSET)
        signup: ProjectConfigAuthSignup | Unset
        if isinstance(_signup,  Unset):
            signup = UNSET
        else:
            signup = ProjectConfigAuthSignup.from_dict(_signup)




        _rate_limits = d.pop("rate_limits", UNSET)
        rate_limits: ProjectConfigAuthRateLimits | Unset
        if isinstance(_rate_limits,  Unset):
            rate_limits = UNSET
        else:
            rate_limits = ProjectConfigAuthRateLimits.from_dict(_rate_limits)




        _password = d.pop("password", UNSET)
        password: ProjectConfigAuthPassword | Unset
        if isinstance(_password,  Unset):
            password = UNSET
        else:
            password = ProjectConfigAuthPassword.from_dict(_password)




        _password_reset = d.pop("password_reset", UNSET)
        password_reset: ProjectConfigAuthPasswordReset | Unset
        if isinstance(_password_reset,  Unset):
            password_reset = UNSET
        else:
            password_reset = ProjectConfigAuthPasswordReset.from_dict(_password_reset)




        _email_verification = d.pop("email_verification", UNSET)
        email_verification: ProjectConfigAuthEmailVerification | Unset
        if isinstance(_email_verification,  Unset):
            email_verification = UNSET
        else:
            email_verification = ProjectConfigAuthEmailVerification.from_dict(_email_verification)




        _cors = d.pop("cors", UNSET)
        cors: ProjectConfigAuthCORS | Unset
        if isinstance(_cors,  Unset):
            cors = UNSET
        else:
            cors = ProjectConfigAuthCORS.from_dict(_cors)




        _providers = d.pop("providers", UNSET)
        providers: ProjectConfigAuthProviders | Unset
        if isinstance(_providers,  Unset):
            providers = UNSET
        else:
            providers = ProjectConfigAuthProviders.from_dict(_providers)




        _email = d.pop("email", UNSET)
        email: ProjectConfigAuthEmail | Unset
        if isinstance(_email,  Unset):
            email = UNSET
        else:
            email = ProjectConfigAuthEmail.from_dict(_email)




        _managed_pages = d.pop("managed_pages", UNSET)
        managed_pages: ProjectConfigAuthManagedPages | Unset
        if isinstance(_managed_pages,  Unset):
            managed_pages = UNSET
        else:
            managed_pages = ProjectConfigAuthManagedPages.from_dict(_managed_pages)




        project_config_auth = cls(
            tokens=tokens,
            sessions=sessions,
            signup=signup,
            rate_limits=rate_limits,
            password=password,
            password_reset=password_reset,
            email_verification=email_verification,
            cors=cors,
            providers=providers,
            email=email,
            managed_pages=managed_pages,
        )

        return project_config_auth

