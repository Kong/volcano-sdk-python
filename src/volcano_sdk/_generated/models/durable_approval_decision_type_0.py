from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
import datetime

if TYPE_CHECKING:
  from ..models.durable_approval_decider_type_0 import DurableApprovalDeciderType0





T = TypeVar("T", bound="DurableApprovalDecisionType0")



@_attrs_define
class DurableApprovalDecisionType0:
    """ Who decided and when. Null unless the approval was approved or denied.

        Attributes:
            comment (str):
            decided_by (DurableApprovalDeciderType0 | None): The person who decided. Null once their account is deleted.
            decided_at (datetime.datetime):
     """

    comment: str
    decided_by: DurableApprovalDeciderType0 | None
    decided_at: datetime.datetime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_approval_decider_type_0 import DurableApprovalDeciderType0 # noqa: PLC0415
        comment = self.comment

        decided_by: dict[str, Any] | None
        if isinstance(self.decided_by, DurableApprovalDeciderType0):
            decided_by = self.decided_by.to_dict()
        else:
            decided_by = self.decided_by

        decided_at = self.decided_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "comment": comment,
            "decided_by": decided_by,
            "decided_at": decided_at,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_approval_decider_type_0 import DurableApprovalDeciderType0 # noqa: PLC0415
        d = dict(src_dict)
        comment = d.pop("comment")

        def _parse_decided_by(data: object) -> DurableApprovalDeciderType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_durable_approval_decider_type_0 = DurableApprovalDeciderType0.from_dict(data)



                return componentsschemas_durable_approval_decider_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DurableApprovalDeciderType0 | None, data)

        decided_by = _parse_decided_by(d.pop("decided_by"))


        decided_at = datetime.datetime.fromisoformat(d.pop("decided_at"))




        durable_approval_decision_type_0 = cls(
            comment=comment,
            decided_by=decided_by,
            decided_at=decided_at,
        )


        durable_approval_decision_type_0.additional_properties = d
        return durable_approval_decision_type_0

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
