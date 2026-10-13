from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_message_sender_type import check_durable_message_sender_type
from ..models.durable_message_sender_type import DurableMessageSenderType
from typing import cast






T = TypeVar("T", bound="DurableMessageSender")



@_attrs_define
class DurableMessageSender:
    """ Who sent the message.

        Attributes:
            type_ (DurableMessageSenderType): The credential the message was sent with. `project` is the
                project's owner or one of its access tokens, and `execution` is the
                execution itself publishing.
            user_id (None | str): The auth user who sent it. Null unless `type` is `user`.
     """

    type_: DurableMessageSenderType
    user_id: None | str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        type_: str = self.type_

        user_id: None | str
        user_id = self.user_id


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "type": type_,
            "user_id": user_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        type_ = check_durable_message_sender_type(d.pop("type"))




        def _parse_user_id(data: object) -> None | str:
            if data is None:
                return data
            return cast(None | str, data)

        user_id = _parse_user_id(d.pop("user_id"))


        durable_message_sender = cls(
            type_=type_,
            user_id=user_id,
        )


        durable_message_sender.additional_properties = d
        return durable_message_sender

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
