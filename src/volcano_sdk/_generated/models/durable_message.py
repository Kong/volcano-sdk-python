from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_message_direction import check_durable_message_direction
from ..models.durable_message_direction import DurableMessageDirection
from ..models.durable_message_status import check_durable_message_status
from ..models.durable_message_status import DurableMessageStatus
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.durable_message_sender import DurableMessageSender





T = TypeVar("T", bound="DurableMessage")



@_attrs_define
class DurableMessage:
    """ A message sent to, or published by, a durable execution.

        Attributes:
            id (UUID):
            execution_id (UUID):
            direction (DurableMessageDirection): `in` is a message sent to the execution. `out` is one the execution
                published.
            seq (int): Orders the execution's messages in both directions. It increases
                with every message but can skip numbers. Pass the last one you read
                as `after` to read what came next.
            name (str):
            data (Any): The JSON value sent or published, or null.
            sender (DurableMessageSender): Who sent the message.
            status (DurableMessageStatus): An `in` message is `queued` until a wait for its name takes it,
                `delivering` while it is handed over, and `delivered` once the
                execution has it. It is `dropped` if the execution ended before any
                wait took it. Every `out` message is `published`.
            delivered_at (datetime.datetime | None): When the execution received the message. Null until then, and for `out`
                messages.
            sent_at (datetime.datetime):
     """

    id: UUID
    execution_id: UUID
    direction: DurableMessageDirection
    seq: int
    name: str
    data: Any
    sender: DurableMessageSender
    status: DurableMessageStatus
    delivered_at: datetime.datetime | None
    sent_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_message_sender import DurableMessageSender # noqa: PLC0415
        id = str(self.id)

        execution_id = str(self.execution_id)

        direction: str = self.direction

        seq = self.seq

        name = self.name

        data = self.data

        sender = self.sender.to_dict()

        status: str = self.status

        delivered_at: None | str
        if isinstance(self.delivered_at, datetime.datetime):
            delivered_at = self.delivered_at.isoformat()
        else:
            delivered_at = self.delivered_at

        sent_at = self.sent_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "execution_id": execution_id,
            "direction": direction,
            "seq": seq,
            "name": name,
            "data": data,
            "sender": sender,
            "status": status,
            "delivered_at": delivered_at,
            "sent_at": sent_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_message_sender import DurableMessageSender # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        execution_id = UUID(d.pop("execution_id"))




        direction = check_durable_message_direction(d.pop("direction"))




        seq = d.pop("seq")

        name = d.pop("name")

        data = d.pop("data")

        sender = DurableMessageSender.from_dict(d.pop("sender"))




        status = check_durable_message_status(d.pop("status"))




        def _parse_delivered_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                delivered_at_type_0 = datetime.datetime.fromisoformat(data)



                return delivered_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        delivered_at = _parse_delivered_at(d.pop("delivered_at"))


        sent_at = datetime.datetime.fromisoformat(d.pop("sent_at"))




        durable_message = cls(
            id=id,
            execution_id=execution_id,
            direction=direction,
            seq=seq,
            name=name,
            data=data,
            sender=sender,
            status=status,
            delivered_at=delivered_at,
            sent_at=sent_at,
        )


        durable_message.additional_properties = d
        return durable_message

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
