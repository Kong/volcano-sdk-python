from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_config_allowed_email_domains_mode import AuthConfigAllowedEmailDomainsMode
from ..models.auth_config_allowed_email_domains_mode import check_auth_config_allowed_email_domains_mode
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.auth_password_policy import AuthPasswordPolicy





T = TypeVar("T", bound="AuthConfig")



@_attrs_define
class AuthConfig:
    """ 
        Attributes:
            password_policy (AuthPasswordPolicy): Effective backend-enforced password policy.
            project_id (UUID | Unset):
            access_token_lifetime (int | Unset): Access token lifetime in seconds Default: 3600.
            refresh_token_lifetime (int | Unset): Refresh token lifetime in seconds Default: 2592000.
            inactivity_timeout (int | Unset): Force re-login after inactivity (seconds, 0=never) Default: 0.
            max_session_duration (int | Unset): Force re-login after duration (seconds, 0=never) Default: 0.
            min_password_length (int | Unset): Configured minimum password length in Unicode characters. Default: 15.
            require_uppercase (bool | Unset):  Default: False.
            require_lowercase (bool | Unset):  Default: False.
            require_numbers (bool | Unset):  Default: False.
            require_special_chars (bool | Unset):  Default: False.
            enable_signup (bool | Unset): Master switch - allow new user signups via ANY provider Default: True.
            enable_email_password (bool | Unset): Enable email/password authentication as a provider Default: True.
            rate_limit_signup (int | Unset): Signups per hour per IP Default: 100.
            rate_limit_signin (int | Unset): Signins per hour per IP Default: 100.
            rate_limit_token_refresh (int | Unset): Refreshes per hour per IP Default: 1000.
            cors_enabled (bool | Unset):  Default: False.
            cors_allowed_origins (list[str] | Unset):  Example: ['https://myapp.com', 'http://localhost:3000'].
            enable_anonymous_signins (bool | Unset): Allow creating users without email/password Default: False.
            allowed_email_domains (list[str] | Unset): Email domains allowed to create users in this project. Applies to
                email/password signup, OAuth/SSO signup, anonymous conversion, and
                email changes. Empty (the default) allows every domain.

                Entries are stored normalized (lowercase, no `@` prefix) and match
                the domain part exactly: `domain1.com` does not cover
                `mail.domain1.com`. Signups from other domains are rejected with
                403, and `allowed_email_domains_mode` decides whether sign-in is
                covered as well.

                The allowlist is a PRO feature to configure and to enforce. A
                downgrade parks it: the domains are still returned here and stop
                being applied until the project is back on PRO.
                 Example: ['domain1.com', 'domain2.com'].
            allowed_email_domains_mode (AuthConfigAllowedEmailDomainsMode | Unset): How far `allowed_email_domains` reaches.
                `signup` only gates account
                creation, so accounts that predate the list keep signing in.
                `signup_and_signin` also refuses to issue a session to an account
                whose domain is not listed. `disabled` keeps the list without
                enforcing it.
                 Default: 'signup'.
            platform_token_ttl (int | Unset): TTL in seconds for platform tokens minted via `/auth/platform/exchange`
                Default: 2592000.
            allow_password_reset (bool | Unset): Enable forgot password flow Default: True.
            password_reset_timeout (int | Unset): Recovery token expiry in seconds Default: 3600.
            max_password_history (int | Unset): Number of previous passwords to remember (0=disabled) Default: 0.
            cors_allow_credentials (bool | Unset): Allow credentials in CORS requests Default: True.
            cors_max_age (int | Unset): CORS preflight cache duration (seconds) Default: 86400.
            require_email_confirmation (bool | Unset): Require users to confirm email before sign-in. Can only be true when
                email_enabled is true. Default: False.
            email_confirmation_timeout (int | Unset): Email confirmation token expiry in seconds. Default: 86400.
            auto_link_verified_oauth (bool | Unset): Link a verified OAuth identity to an existing confirmed account with
                the same email instead of returning a conflict. Requires require_email_confirmation to be true. Default: False.
            email_enabled (bool | Unset): Enable transactional email sending (confirmation, reset, change notifications).
                Must be true when require_email_confirmation is true. Default: False.
            email_from_address (str | Unset):
            email_from_name (str | Unset):
            smtp_host (str | Unset):
            smtp_port (int | Unset):  Default: 587.
            smtp_username (str | Unset):
            smtp_password_configured (bool | Unset): Whether an SMTP password is configured. The password itself is never
                returned. Default: False.
            smtp_use_tls (bool | Unset):  Default: True.
            email_confirmation_subject (str | Unset):
            email_password_reset_subject (str | Unset):
            email_password_changed_subject (str | Unset):
            managed_auth_enabled (bool | Unset): Enables project-hosted managed auth pages. Default: False.
            post_auth_redirect_url (str | Unset): Default redirect target after successful hosted auth.
            allowed_redirect_urls (list[str] | Unset): Redirect allowlist used to validate post_auth_redirect_url and
                post_logout_redirect_url.
            post_logout_redirect_url (str | Unset): Redirect target after logout from hosted pages.
            device_verification_url (str | Unset): Optional override for the device-authorization verification page.
                When set, POST /auth/device/authorize returns this URL (with the
                user_code) as verification_uri/verification_uri_complete instead of
                the built-in managed device page. Lets a CLI surface the project's
                own RFC 8628 approval page. Empty falls back to the managed page.
                 Example: https://app.acme.com/device.
     """

    password_policy: AuthPasswordPolicy
    project_id: UUID | Unset = UNSET
    access_token_lifetime: int | Unset = 3600
    refresh_token_lifetime: int | Unset = 2592000
    inactivity_timeout: int | Unset = 0
    max_session_duration: int | Unset = 0
    min_password_length: int | Unset = 15
    require_uppercase: bool | Unset = False
    require_lowercase: bool | Unset = False
    require_numbers: bool | Unset = False
    require_special_chars: bool | Unset = False
    enable_signup: bool | Unset = True
    enable_email_password: bool | Unset = True
    rate_limit_signup: int | Unset = 100
    rate_limit_signin: int | Unset = 100
    rate_limit_token_refresh: int | Unset = 1000
    cors_enabled: bool | Unset = False
    cors_allowed_origins: list[str] | Unset = UNSET
    enable_anonymous_signins: bool | Unset = False
    allowed_email_domains: list[str] | Unset = UNSET
    allowed_email_domains_mode: AuthConfigAllowedEmailDomainsMode | Unset = 'signup'
    platform_token_ttl: int | Unset = 2592000
    allow_password_reset: bool | Unset = True
    password_reset_timeout: int | Unset = 3600
    max_password_history: int | Unset = 0
    cors_allow_credentials: bool | Unset = True
    cors_max_age: int | Unset = 86400
    require_email_confirmation: bool | Unset = False
    email_confirmation_timeout: int | Unset = 86400
    auto_link_verified_oauth: bool | Unset = False
    email_enabled: bool | Unset = False
    email_from_address: str | Unset = UNSET
    email_from_name: str | Unset = UNSET
    smtp_host: str | Unset = UNSET
    smtp_port: int | Unset = 587
    smtp_username: str | Unset = UNSET
    smtp_password_configured: bool | Unset = False
    smtp_use_tls: bool | Unset = True
    email_confirmation_subject: str | Unset = UNSET
    email_password_reset_subject: str | Unset = UNSET
    email_password_changed_subject: str | Unset = UNSET
    managed_auth_enabled: bool | Unset = False
    post_auth_redirect_url: str | Unset = UNSET
    allowed_redirect_urls: list[str] | Unset = UNSET
    post_logout_redirect_url: str | Unset = UNSET
    device_verification_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_password_policy import AuthPasswordPolicy
        password_policy = self.password_policy.to_dict()

        project_id: str | Unset = UNSET
        if not isinstance(self.project_id, Unset):
            project_id = str(self.project_id)

        access_token_lifetime = self.access_token_lifetime

        refresh_token_lifetime = self.refresh_token_lifetime

        inactivity_timeout = self.inactivity_timeout

        max_session_duration = self.max_session_duration

        min_password_length = self.min_password_length

        require_uppercase = self.require_uppercase

        require_lowercase = self.require_lowercase

        require_numbers = self.require_numbers

        require_special_chars = self.require_special_chars

        enable_signup = self.enable_signup

        enable_email_password = self.enable_email_password

        rate_limit_signup = self.rate_limit_signup

        rate_limit_signin = self.rate_limit_signin

        rate_limit_token_refresh = self.rate_limit_token_refresh

        cors_enabled = self.cors_enabled

        cors_allowed_origins: list[str] | Unset = UNSET
        if not isinstance(self.cors_allowed_origins, Unset):
            cors_allowed_origins = self.cors_allowed_origins



        enable_anonymous_signins = self.enable_anonymous_signins

        allowed_email_domains: list[str] | Unset = UNSET
        if not isinstance(self.allowed_email_domains, Unset):
            allowed_email_domains = self.allowed_email_domains



        allowed_email_domains_mode: str | Unset = UNSET
        if not isinstance(self.allowed_email_domains_mode, Unset):
            allowed_email_domains_mode = self.allowed_email_domains_mode


        platform_token_ttl = self.platform_token_ttl

        allow_password_reset = self.allow_password_reset

        password_reset_timeout = self.password_reset_timeout

        max_password_history = self.max_password_history

        cors_allow_credentials = self.cors_allow_credentials

        cors_max_age = self.cors_max_age

        require_email_confirmation = self.require_email_confirmation

        email_confirmation_timeout = self.email_confirmation_timeout

        auto_link_verified_oauth = self.auto_link_verified_oauth

        email_enabled = self.email_enabled

        email_from_address = self.email_from_address

        email_from_name = self.email_from_name

        smtp_host = self.smtp_host

        smtp_port = self.smtp_port

        smtp_username = self.smtp_username

        smtp_password_configured = self.smtp_password_configured

        smtp_use_tls = self.smtp_use_tls

        email_confirmation_subject = self.email_confirmation_subject

        email_password_reset_subject = self.email_password_reset_subject

        email_password_changed_subject = self.email_password_changed_subject

        managed_auth_enabled = self.managed_auth_enabled

        post_auth_redirect_url = self.post_auth_redirect_url

        allowed_redirect_urls: list[str] | Unset = UNSET
        if not isinstance(self.allowed_redirect_urls, Unset):
            allowed_redirect_urls = self.allowed_redirect_urls



        post_logout_redirect_url = self.post_logout_redirect_url

        device_verification_url = self.device_verification_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "password_policy": password_policy,
        })
        if project_id is not UNSET:
            field_dict["project_id"] = project_id
        if access_token_lifetime is not UNSET:
            field_dict["access_token_lifetime"] = access_token_lifetime
        if refresh_token_lifetime is not UNSET:
            field_dict["refresh_token_lifetime"] = refresh_token_lifetime
        if inactivity_timeout is not UNSET:
            field_dict["inactivity_timeout"] = inactivity_timeout
        if max_session_duration is not UNSET:
            field_dict["max_session_duration"] = max_session_duration
        if min_password_length is not UNSET:
            field_dict["min_password_length"] = min_password_length
        if require_uppercase is not UNSET:
            field_dict["require_uppercase"] = require_uppercase
        if require_lowercase is not UNSET:
            field_dict["require_lowercase"] = require_lowercase
        if require_numbers is not UNSET:
            field_dict["require_numbers"] = require_numbers
        if require_special_chars is not UNSET:
            field_dict["require_special_chars"] = require_special_chars
        if enable_signup is not UNSET:
            field_dict["enable_signup"] = enable_signup
        if enable_email_password is not UNSET:
            field_dict["enable_email_password"] = enable_email_password
        if rate_limit_signup is not UNSET:
            field_dict["rate_limit_signup"] = rate_limit_signup
        if rate_limit_signin is not UNSET:
            field_dict["rate_limit_signin"] = rate_limit_signin
        if rate_limit_token_refresh is not UNSET:
            field_dict["rate_limit_token_refresh"] = rate_limit_token_refresh
        if cors_enabled is not UNSET:
            field_dict["cors_enabled"] = cors_enabled
        if cors_allowed_origins is not UNSET:
            field_dict["cors_allowed_origins"] = cors_allowed_origins
        if enable_anonymous_signins is not UNSET:
            field_dict["enable_anonymous_signins"] = enable_anonymous_signins
        if allowed_email_domains is not UNSET:
            field_dict["allowed_email_domains"] = allowed_email_domains
        if allowed_email_domains_mode is not UNSET:
            field_dict["allowed_email_domains_mode"] = allowed_email_domains_mode
        if platform_token_ttl is not UNSET:
            field_dict["platform_token_ttl"] = platform_token_ttl
        if allow_password_reset is not UNSET:
            field_dict["allow_password_reset"] = allow_password_reset
        if password_reset_timeout is not UNSET:
            field_dict["password_reset_timeout"] = password_reset_timeout
        if max_password_history is not UNSET:
            field_dict["max_password_history"] = max_password_history
        if cors_allow_credentials is not UNSET:
            field_dict["cors_allow_credentials"] = cors_allow_credentials
        if cors_max_age is not UNSET:
            field_dict["cors_max_age"] = cors_max_age
        if require_email_confirmation is not UNSET:
            field_dict["require_email_confirmation"] = require_email_confirmation
        if email_confirmation_timeout is not UNSET:
            field_dict["email_confirmation_timeout"] = email_confirmation_timeout
        if auto_link_verified_oauth is not UNSET:
            field_dict["auto_link_verified_oauth"] = auto_link_verified_oauth
        if email_enabled is not UNSET:
            field_dict["email_enabled"] = email_enabled
        if email_from_address is not UNSET:
            field_dict["email_from_address"] = email_from_address
        if email_from_name is not UNSET:
            field_dict["email_from_name"] = email_from_name
        if smtp_host is not UNSET:
            field_dict["smtp_host"] = smtp_host
        if smtp_port is not UNSET:
            field_dict["smtp_port"] = smtp_port
        if smtp_username is not UNSET:
            field_dict["smtp_username"] = smtp_username
        if smtp_password_configured is not UNSET:
            field_dict["smtp_password_configured"] = smtp_password_configured
        if smtp_use_tls is not UNSET:
            field_dict["smtp_use_tls"] = smtp_use_tls
        if email_confirmation_subject is not UNSET:
            field_dict["email_confirmation_subject"] = email_confirmation_subject
        if email_password_reset_subject is not UNSET:
            field_dict["email_password_reset_subject"] = email_password_reset_subject
        if email_password_changed_subject is not UNSET:
            field_dict["email_password_changed_subject"] = email_password_changed_subject
        if managed_auth_enabled is not UNSET:
            field_dict["managed_auth_enabled"] = managed_auth_enabled
        if post_auth_redirect_url is not UNSET:
            field_dict["post_auth_redirect_url"] = post_auth_redirect_url
        if allowed_redirect_urls is not UNSET:
            field_dict["allowed_redirect_urls"] = allowed_redirect_urls
        if post_logout_redirect_url is not UNSET:
            field_dict["post_logout_redirect_url"] = post_logout_redirect_url
        if device_verification_url is not UNSET:
            field_dict["device_verification_url"] = device_verification_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_password_policy import AuthPasswordPolicy
        d = dict(src_dict)
        password_policy = AuthPasswordPolicy.from_dict(d.pop("password_policy"))




        _project_id = d.pop("project_id", UNSET)
        project_id: UUID | Unset
        if isinstance(_project_id,  Unset):
            project_id = UNSET
        else:
            project_id = UUID(_project_id)




        access_token_lifetime = d.pop("access_token_lifetime", UNSET)

        refresh_token_lifetime = d.pop("refresh_token_lifetime", UNSET)

        inactivity_timeout = d.pop("inactivity_timeout", UNSET)

        max_session_duration = d.pop("max_session_duration", UNSET)

        min_password_length = d.pop("min_password_length", UNSET)

        require_uppercase = d.pop("require_uppercase", UNSET)

        require_lowercase = d.pop("require_lowercase", UNSET)

        require_numbers = d.pop("require_numbers", UNSET)

        require_special_chars = d.pop("require_special_chars", UNSET)

        enable_signup = d.pop("enable_signup", UNSET)

        enable_email_password = d.pop("enable_email_password", UNSET)

        rate_limit_signup = d.pop("rate_limit_signup", UNSET)

        rate_limit_signin = d.pop("rate_limit_signin", UNSET)

        rate_limit_token_refresh = d.pop("rate_limit_token_refresh", UNSET)

        cors_enabled = d.pop("cors_enabled", UNSET)

        cors_allowed_origins = cast(list[str], d.pop("cors_allowed_origins", UNSET))


        enable_anonymous_signins = d.pop("enable_anonymous_signins", UNSET)

        allowed_email_domains = cast(list[str], d.pop("allowed_email_domains", UNSET))


        _allowed_email_domains_mode = d.pop("allowed_email_domains_mode", UNSET)
        allowed_email_domains_mode: AuthConfigAllowedEmailDomainsMode | Unset
        if isinstance(_allowed_email_domains_mode,  Unset):
            allowed_email_domains_mode = UNSET
        else:
            allowed_email_domains_mode = check_auth_config_allowed_email_domains_mode(_allowed_email_domains_mode)




        platform_token_ttl = d.pop("platform_token_ttl", UNSET)

        allow_password_reset = d.pop("allow_password_reset", UNSET)

        password_reset_timeout = d.pop("password_reset_timeout", UNSET)

        max_password_history = d.pop("max_password_history", UNSET)

        cors_allow_credentials = d.pop("cors_allow_credentials", UNSET)

        cors_max_age = d.pop("cors_max_age", UNSET)

        require_email_confirmation = d.pop("require_email_confirmation", UNSET)

        email_confirmation_timeout = d.pop("email_confirmation_timeout", UNSET)

        auto_link_verified_oauth = d.pop("auto_link_verified_oauth", UNSET)

        email_enabled = d.pop("email_enabled", UNSET)

        email_from_address = d.pop("email_from_address", UNSET)

        email_from_name = d.pop("email_from_name", UNSET)

        smtp_host = d.pop("smtp_host", UNSET)

        smtp_port = d.pop("smtp_port", UNSET)

        smtp_username = d.pop("smtp_username", UNSET)

        smtp_password_configured = d.pop("smtp_password_configured", UNSET)

        smtp_use_tls = d.pop("smtp_use_tls", UNSET)

        email_confirmation_subject = d.pop("email_confirmation_subject", UNSET)

        email_password_reset_subject = d.pop("email_password_reset_subject", UNSET)

        email_password_changed_subject = d.pop("email_password_changed_subject", UNSET)

        managed_auth_enabled = d.pop("managed_auth_enabled", UNSET)

        post_auth_redirect_url = d.pop("post_auth_redirect_url", UNSET)

        allowed_redirect_urls = cast(list[str], d.pop("allowed_redirect_urls", UNSET))


        post_logout_redirect_url = d.pop("post_logout_redirect_url", UNSET)

        device_verification_url = d.pop("device_verification_url", UNSET)

        auth_config = cls(
            password_policy=password_policy,
            project_id=project_id,
            access_token_lifetime=access_token_lifetime,
            refresh_token_lifetime=refresh_token_lifetime,
            inactivity_timeout=inactivity_timeout,
            max_session_duration=max_session_duration,
            min_password_length=min_password_length,
            require_uppercase=require_uppercase,
            require_lowercase=require_lowercase,
            require_numbers=require_numbers,
            require_special_chars=require_special_chars,
            enable_signup=enable_signup,
            enable_email_password=enable_email_password,
            rate_limit_signup=rate_limit_signup,
            rate_limit_signin=rate_limit_signin,
            rate_limit_token_refresh=rate_limit_token_refresh,
            cors_enabled=cors_enabled,
            cors_allowed_origins=cors_allowed_origins,
            enable_anonymous_signins=enable_anonymous_signins,
            allowed_email_domains=allowed_email_domains,
            allowed_email_domains_mode=allowed_email_domains_mode,
            platform_token_ttl=platform_token_ttl,
            allow_password_reset=allow_password_reset,
            password_reset_timeout=password_reset_timeout,
            max_password_history=max_password_history,
            cors_allow_credentials=cors_allow_credentials,
            cors_max_age=cors_max_age,
            require_email_confirmation=require_email_confirmation,
            email_confirmation_timeout=email_confirmation_timeout,
            auto_link_verified_oauth=auto_link_verified_oauth,
            email_enabled=email_enabled,
            email_from_address=email_from_address,
            email_from_name=email_from_name,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password_configured=smtp_password_configured,
            smtp_use_tls=smtp_use_tls,
            email_confirmation_subject=email_confirmation_subject,
            email_password_reset_subject=email_password_reset_subject,
            email_password_changed_subject=email_password_changed_subject,
            managed_auth_enabled=managed_auth_enabled,
            post_auth_redirect_url=post_auth_redirect_url,
            allowed_redirect_urls=allowed_redirect_urls,
            post_logout_redirect_url=post_logout_redirect_url,
            device_verification_url=device_verification_url,
        )


        auth_config.additional_properties = d
        return auth_config

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
