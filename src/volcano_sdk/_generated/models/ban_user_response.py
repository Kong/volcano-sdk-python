from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.ban_user_response_status import BanUserResponseStatus
from ..models.ban_user_response_status import check_ban_user_response_status
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="BanUserResponse")



@_attrs_define
class BanUserResponse:
    """ Response when banning a user

        Attributes:
            message (str):  Example: User banned until 2026-12-31T23:59:59Z.
            user_id (UUID):
            email (str):
            status (BanUserResponseStatus):
            banned_until (datetime.datetime | None | Unset): When the ban expires (null for permanent ban)
     """

    message: str
    user_id: UUID
    email: str
    status: BanUserResponseStatus
    banned_until: datetime.datetime | None | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message = self.message

        user_id = str(self.user_id)

        email = self.email

        status: str = self.status

        banned_until: None | str | Unset
        if isinstance(self.banned_until, Unset):
            banned_until = UNSET
        elif isinstance(self.banned_until, datetime.datetime):
            banned_until = self.banned_until.isoformat()
        else:
            banned_until = self.banned_until


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "message": message,
            "user_id": user_id,
            "email": email,
            "status": status,
        })
        if banned_until is not UNSET:
            field_dict["banned_until"] = banned_until

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        user_id = UUID(d.pop("user_id"))




        email = d.pop("email")

        status = check_ban_user_response_status(d.pop("status"))




        def _parse_banned_until(data: object) -> datetime.datetime | None | Unset:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                banned_until_type_0 = datetime.datetime.fromisoformat(data)



                return banned_until_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None | Unset, data)

        banned_until = _parse_banned_until(d.pop("banned_until", UNSET))


        ban_user_response = cls(
            message=message,
            user_id=user_id,
            email=email,
            status=status,
            banned_until=banned_until,
        )


        ban_user_response.additional_properties = d
        return ban_user_response

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
