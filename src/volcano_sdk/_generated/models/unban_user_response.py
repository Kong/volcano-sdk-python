from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.unban_user_response_status import check_unban_user_response_status
from ..models.unban_user_response_status import UnbanUserResponseStatus
from typing import cast
from uuid import UUID






T = TypeVar("T", bound="UnbanUserResponse")



@_attrs_define
class UnbanUserResponse:
    """ Response when unbanning a user

        Attributes:
            message (str):  Example: User unbanned successfully.
            user_id (UUID):
            email (str):
            status (UnbanUserResponseStatus):
     """

    message: str
    user_id: UUID
    email: str
    status: UnbanUserResponseStatus
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        message = self.message

        user_id = str(self.user_id)

        email = self.email

        status: str = self.status


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "message": message,
            "user_id": user_id,
            "email": email,
            "status": status,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        message = d.pop("message")

        user_id = UUID(d.pop("user_id"))




        email = d.pop("email")

        status = check_unban_user_response_status(d.pop("status"))




        unban_user_response = cls(
            message=message,
            user_id=user_id,
            email=email,
            status=status,
        )


        unban_user_response.additional_properties = d
        return unban_user_response

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
