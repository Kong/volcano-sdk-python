from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.auth_refresh_body_session_mode import AuthRefreshBodySessionMode
from ..models.auth_refresh_body_session_mode import check_auth_refresh_body_session_mode
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="AuthRefreshBody")



@_attrs_define
class AuthRefreshBody:
    """ 
        Attributes:
            refresh_token (str | Unset):
            session_mode (AuthRefreshBodySessionMode | Unset):
     """

    refresh_token: str | Unset = UNSET
    session_mode: AuthRefreshBodySessionMode | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        refresh_token = self.refresh_token

        session_mode: str | Unset = UNSET
        if not isinstance(self.session_mode, Unset):
            session_mode = self.session_mode



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
        })
        if refresh_token is not UNSET:
            field_dict["refresh_token"] = refresh_token
        if session_mode is not UNSET:
            field_dict["session_mode"] = session_mode

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        refresh_token = d.pop("refresh_token", UNSET)

        _session_mode = d.pop("session_mode", UNSET)
        session_mode: AuthRefreshBodySessionMode | Unset
        if isinstance(_session_mode,  Unset):
            session_mode = UNSET
        else:
            session_mode = check_auth_refresh_body_session_mode(_session_mode)




        auth_refresh_body = cls(
            refresh_token=refresh_token,
            session_mode=session_mode,
        )


        auth_refresh_body.additional_properties = d
        return auth_refresh_body

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
