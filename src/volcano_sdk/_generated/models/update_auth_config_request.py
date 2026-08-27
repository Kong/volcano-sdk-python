from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.update_auth_config_request_allowed_email_domains_mode import check_update_auth_config_request_allowed_email_domains_mode
from ..models.update_auth_config_request_allowed_email_domains_mode import UpdateAuthConfigRequestAllowedEmailDomainsMode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="UpdateAuthConfigRequest")



@_attrs_define
class UpdateAuthConfigRequest:
    """ All fields optional - only include fields you want to update. Validation rule: require_email_confirmation=true
    requires email_enabled=true.

        Attributes:
            access_token_lifetime (int | Unset):
            refresh_token_lifetime (int | Unset):
            inactivity_timeout (int | Unset):
            max_session_duration (int | Unset):
            min_password_length (int | Unset):
            require_uppercase (bool | Unset):
            require_lowercase (bool | Unset):
            require_numbers (bool | Unset):
            require_special_chars (bool | Unset):
            enable_signup (bool | Unset): Master switch for signups across ALL providers
            enable_email_password (bool | Unset): Enable/disable email/password provider
            rate_limit_signup (int | Unset):
            rate_limit_signin (int | Unset):
            rate_limit_token_refresh (int | Unset):
            cors_allow_credentials (bool | Unset):
            cors_max_age (int | Unset):
            enable_anonymous_signins (bool | Unset):
            allowed_email_domains (list[str] | Unset): Replaces the email domain allowlist. Empty array removes the
                restriction so any domain can sign up. Entries must be bare domains
                such as `domain1.com` and are stored normalized (lowercase, no `@`
                prefix); matching is exact, so subdomains need their own entry. At
                most 100 entries.

                Restricting signups is a PRO feature to configure and to enforce: a
                FREE project can only remove the restriction and gets 403 for any
                other change, and the list it keeps is parked until it upgrades.
                 Example: ['domain1.com', 'domain2.com'].
            allowed_email_domains_mode (UpdateAuthConfigRequestAllowedEmailDomainsMode | Unset): How far
                `allowed_email_domains` reaches. `signup` gates account
                creation only. `signup_and_signin` also blocks sign-in for accounts
                outside the list; switching to it, or narrowing the list while in
                it, deletes the sessions of every account it locks out. `disabled`
                keeps the list without enforcing it.
            allow_password_reset (bool | Unset):
            password_reset_timeout (int | Unset):
            max_password_history (int | Unset):
            require_email_confirmation (bool | Unset): Require users to confirm email before sign-in. Can only be true when
                email_enabled is true.
            email_confirmation_timeout (int | Unset): Email confirmation token expiry in seconds.
            auto_link_verified_oauth (bool | Unset): Link a verified OAuth identity to an existing confirmed account with
                the same email instead of returning a conflict. Requires require_email_confirmation to be true.
            email_enabled (bool | Unset): Enable transactional email sending. Cannot be false while
                require_email_confirmation is true.
            email_from_address (str | Unset):
            email_from_name (str | Unset):
            smtp_host (str | Unset):
            smtp_port (int | Unset):
            smtp_username (str | Unset):
            smtp_password (str | Unset): Replacement SMTP password. Omit this field to preserve the configured password. The
                value is encrypted at rest and never returned.
            smtp_use_tls (bool | Unset):
            email_confirmation_subject (str | Unset):
            email_password_reset_subject (str | Unset):
            email_password_changed_subject (str | Unset):
            managed_auth_enabled (bool | Unset): Enable or disable managed auth hosted pages for the project.
            post_auth_redirect_url (str | Unset): Must be included in allowed_redirect_urls when set.
            allowed_redirect_urls (list[str] | Unset): Redirect allowlist. Every entry must be a valid http/https URL.
            post_logout_redirect_url (str | Unset): Must be included in allowed_redirect_urls when set.
            device_verification_url (str | Unset): Optional custom device-authorization verification page. Must be a
                valid http/https URL (not tied to allowed_redirect_urls). When set,
                device-code logins return this URL (with user_code) instead of the
                managed device page. Send an empty string to clear the override.
     """

    access_token_lifetime: int | Unset = UNSET
    refresh_token_lifetime: int | Unset = UNSET
    inactivity_timeout: int | Unset = UNSET
    max_session_duration: int | Unset = UNSET
    min_password_length: int | Unset = UNSET
    require_uppercase: bool | Unset = UNSET
    require_lowercase: bool | Unset = UNSET
    require_numbers: bool | Unset = UNSET
    require_special_chars: bool | Unset = UNSET
    enable_signup: bool | Unset = UNSET
    enable_email_password: bool | Unset = UNSET
    rate_limit_signup: int | Unset = UNSET
    rate_limit_signin: int | Unset = UNSET
    rate_limit_token_refresh: int | Unset = UNSET
    cors_allow_credentials: bool | Unset = UNSET
    cors_max_age: int | Unset = UNSET
    enable_anonymous_signins: bool | Unset = UNSET
    allowed_email_domains: list[str] | Unset = UNSET
    allowed_email_domains_mode: UpdateAuthConfigRequestAllowedEmailDomainsMode | Unset = UNSET
    allow_password_reset: bool | Unset = UNSET
    password_reset_timeout: int | Unset = UNSET
    max_password_history: int | Unset = UNSET
    require_email_confirmation: bool | Unset = UNSET
    email_confirmation_timeout: int | Unset = UNSET
    auto_link_verified_oauth: bool | Unset = UNSET
    email_enabled: bool | Unset = UNSET
    email_from_address: str | Unset = UNSET
    email_from_name: str | Unset = UNSET
    smtp_host: str | Unset = UNSET
    smtp_port: int | Unset = UNSET
    smtp_username: str | Unset = UNSET
    smtp_password: str | Unset = UNSET
    smtp_use_tls: bool | Unset = UNSET
    email_confirmation_subject: str | Unset = UNSET
    email_password_reset_subject: str | Unset = UNSET
    email_password_changed_subject: str | Unset = UNSET
    managed_auth_enabled: bool | Unset = UNSET
    post_auth_redirect_url: str | Unset = UNSET
    allowed_redirect_urls: list[str] | Unset = UNSET
    post_logout_redirect_url: str | Unset = UNSET
    device_verification_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
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

        cors_allow_credentials = self.cors_allow_credentials

        cors_max_age = self.cors_max_age

        enable_anonymous_signins = self.enable_anonymous_signins

        allowed_email_domains: list[str] | Unset = UNSET
        if not isinstance(self.allowed_email_domains, Unset):
            allowed_email_domains = self.allowed_email_domains



        allowed_email_domains_mode: str | Unset = UNSET
        if not isinstance(self.allowed_email_domains_mode, Unset):
            allowed_email_domains_mode = self.allowed_email_domains_mode


        allow_password_reset = self.allow_password_reset

        password_reset_timeout = self.password_reset_timeout

        max_password_history = self.max_password_history

        require_email_confirmation = self.require_email_confirmation

        email_confirmation_timeout = self.email_confirmation_timeout

        auto_link_verified_oauth = self.auto_link_verified_oauth

        email_enabled = self.email_enabled

        email_from_address = self.email_from_address

        email_from_name = self.email_from_name

        smtp_host = self.smtp_host

        smtp_port = self.smtp_port

        smtp_username = self.smtp_username

        smtp_password = self.smtp_password

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
        })
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
        if cors_allow_credentials is not UNSET:
            field_dict["cors_allow_credentials"] = cors_allow_credentials
        if cors_max_age is not UNSET:
            field_dict["cors_max_age"] = cors_max_age
        if enable_anonymous_signins is not UNSET:
            field_dict["enable_anonymous_signins"] = enable_anonymous_signins
        if allowed_email_domains is not UNSET:
            field_dict["allowed_email_domains"] = allowed_email_domains
        if allowed_email_domains_mode is not UNSET:
            field_dict["allowed_email_domains_mode"] = allowed_email_domains_mode
        if allow_password_reset is not UNSET:
            field_dict["allow_password_reset"] = allow_password_reset
        if password_reset_timeout is not UNSET:
            field_dict["password_reset_timeout"] = password_reset_timeout
        if max_password_history is not UNSET:
            field_dict["max_password_history"] = max_password_history
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
        if smtp_password is not UNSET:
            field_dict["smtp_password"] = smtp_password
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
        d = dict(src_dict)
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

        cors_allow_credentials = d.pop("cors_allow_credentials", UNSET)

        cors_max_age = d.pop("cors_max_age", UNSET)

        enable_anonymous_signins = d.pop("enable_anonymous_signins", UNSET)

        allowed_email_domains = cast(list[str], d.pop("allowed_email_domains", UNSET))


        _allowed_email_domains_mode = d.pop("allowed_email_domains_mode", UNSET)
        allowed_email_domains_mode: UpdateAuthConfigRequestAllowedEmailDomainsMode | Unset
        if isinstance(_allowed_email_domains_mode,  Unset):
            allowed_email_domains_mode = UNSET
        else:
            allowed_email_domains_mode = check_update_auth_config_request_allowed_email_domains_mode(_allowed_email_domains_mode)




        allow_password_reset = d.pop("allow_password_reset", UNSET)

        password_reset_timeout = d.pop("password_reset_timeout", UNSET)

        max_password_history = d.pop("max_password_history", UNSET)

        require_email_confirmation = d.pop("require_email_confirmation", UNSET)

        email_confirmation_timeout = d.pop("email_confirmation_timeout", UNSET)

        auto_link_verified_oauth = d.pop("auto_link_verified_oauth", UNSET)

        email_enabled = d.pop("email_enabled", UNSET)

        email_from_address = d.pop("email_from_address", UNSET)

        email_from_name = d.pop("email_from_name", UNSET)

        smtp_host = d.pop("smtp_host", UNSET)

        smtp_port = d.pop("smtp_port", UNSET)

        smtp_username = d.pop("smtp_username", UNSET)

        smtp_password = d.pop("smtp_password", UNSET)

        smtp_use_tls = d.pop("smtp_use_tls", UNSET)

        email_confirmation_subject = d.pop("email_confirmation_subject", UNSET)

        email_password_reset_subject = d.pop("email_password_reset_subject", UNSET)

        email_password_changed_subject = d.pop("email_password_changed_subject", UNSET)

        managed_auth_enabled = d.pop("managed_auth_enabled", UNSET)

        post_auth_redirect_url = d.pop("post_auth_redirect_url", UNSET)

        allowed_redirect_urls = cast(list[str], d.pop("allowed_redirect_urls", UNSET))


        post_logout_redirect_url = d.pop("post_logout_redirect_url", UNSET)

        device_verification_url = d.pop("device_verification_url", UNSET)

        update_auth_config_request = cls(
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
            cors_allow_credentials=cors_allow_credentials,
            cors_max_age=cors_max_age,
            enable_anonymous_signins=enable_anonymous_signins,
            allowed_email_domains=allowed_email_domains,
            allowed_email_domains_mode=allowed_email_domains_mode,
            allow_password_reset=allow_password_reset,
            password_reset_timeout=password_reset_timeout,
            max_password_history=max_password_history,
            require_email_confirmation=require_email_confirmation,
            email_confirmation_timeout=email_confirmation_timeout,
            auto_link_verified_oauth=auto_link_verified_oauth,
            email_enabled=email_enabled,
            email_from_address=email_from_address,
            email_from_name=email_from_name,
            smtp_host=smtp_host,
            smtp_port=smtp_port,
            smtp_username=smtp_username,
            smtp_password=smtp_password,
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


        update_auth_config_request.additional_properties = d
        return update_auth_config_request

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
