from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthPasswordPolicy")



@_attrs_define
class AuthPasswordPolicy:
    """ Effective backend-enforced password policy.

        Attributes:
            effective_min_length (int): Effective minimum password length in Unicode characters.
            min_configurable_length (int): Lowest minimum password length accepted by the auth configuration endpoint.
            max_length (int): Maximum password length in Unicode characters.
            require_uppercase (bool): Whether passwords must contain an ASCII uppercase letter (A-Z).
            require_lowercase (bool): Whether passwords must contain an ASCII lowercase letter (a-z).
            require_numbers (bool): Whether passwords must contain an ASCII digit (0-9).
            require_special_chars (bool): Whether passwords must contain one of the backend-supported special characters.
            compromised_passwords_rejected (bool): Whether common and known-compromised passwords are rejected by the
                backend.
     """

    effective_min_length: int
    min_configurable_length: int
    max_length: int
    require_uppercase: bool
    require_lowercase: bool
    require_numbers: bool
    require_special_chars: bool
    compromised_passwords_rejected: bool





    def to_dict(self) -> dict[str, Any]:
        effective_min_length = self.effective_min_length

        min_configurable_length = self.min_configurable_length

        max_length = self.max_length

        require_uppercase = self.require_uppercase

        require_lowercase = self.require_lowercase

        require_numbers = self.require_numbers

        require_special_chars = self.require_special_chars

        compromised_passwords_rejected = self.compromised_passwords_rejected


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "effective_min_length": effective_min_length,
            "min_configurable_length": min_configurable_length,
            "max_length": max_length,
            "require_uppercase": require_uppercase,
            "require_lowercase": require_lowercase,
            "require_numbers": require_numbers,
            "require_special_chars": require_special_chars,
            "compromised_passwords_rejected": compromised_passwords_rejected,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        effective_min_length = d.pop("effective_min_length")

        min_configurable_length = d.pop("min_configurable_length")

        max_length = d.pop("max_length")

        require_uppercase = d.pop("require_uppercase")

        require_lowercase = d.pop("require_lowercase")

        require_numbers = d.pop("require_numbers")

        require_special_chars = d.pop("require_special_chars")

        compromised_passwords_rejected = d.pop("compromised_passwords_rejected")

        auth_password_policy = cls(
            effective_min_length=effective_min_length,
            min_configurable_length=min_configurable_length,
            max_length=max_length,
            require_uppercase=require_uppercase,
            require_lowercase=require_lowercase,
            require_numbers=require_numbers,
            require_special_chars=require_special_chars,
            compromised_passwords_rejected=compromised_passwords_rejected,
        )

        return auth_password_policy

