from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.durable_approval_status import check_durable_approval_status
from ..models.durable_approval_status import DurableApprovalStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime

if TYPE_CHECKING:
  from ..models.durable_approval_decision_type_0 import DurableApprovalDecisionType0
  from ..models.durable_approval_execution import DurableApprovalExecution
  from ..models.durable_approval_function import DurableApprovalFunction





T = TypeVar("T", bound="DurableApproval")



@_attrs_define
class DurableApproval:
    """ An approval a durable workflow requested.

        Attributes:
            id (UUID):
            status (DurableApprovalStatus): `pending` means the workflow is waiting for a decision. `approved` and
                `denied` are decisions a person made. `expired` means the workflow's
                approval timeout passed first, and `cancelled` means the execution
                ended while the approval was still pending. Every status but `pending`
                is final.
            name (str): The name the workflow gave the approval in `ctx.waitForApproval`.
            title (str):
            description (str):
            function (DurableApprovalFunction): The durable function that requested the approval. `id` is null once the
                function has been deleted; `name` is kept.
            execution (DurableApprovalExecution): The durable execution that requested the approval. `id` and `status`
                are null once the execution is no longer retained; `name` is kept.
            requested_at (datetime.datetime):
            expires_at (datetime.datetime | None): When the approval expires if nobody decides. Null when the
                workflow set no timeout; the approval then lasts as long as its
                execution.
            decision (DurableApprovalDecisionType0 | None): Who decided and when. Null unless the approval was approved or
                denied.
            details (Any | Unset): The JSON value the workflow attached for the person deciding, as
                given.
     """

    id: UUID
    status: DurableApprovalStatus
    name: str
    title: str
    description: str
    function: DurableApprovalFunction
    execution: DurableApprovalExecution
    requested_at: datetime.datetime
    expires_at: datetime.datetime | None
    decision: DurableApprovalDecisionType0 | None
    details: Any | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.durable_approval_decision_type_0 import DurableApprovalDecisionType0 # noqa: PLC0415
        from ..models.durable_approval_execution import DurableApprovalExecution # noqa: PLC0415
        from ..models.durable_approval_function import DurableApprovalFunction # noqa: PLC0415
        id = str(self.id)

        status: str = self.status

        name = self.name

        title = self.title

        description = self.description

        function = self.function.to_dict()

        execution = self.execution.to_dict()

        requested_at = self.requested_at.isoformat()

        expires_at: None | str
        if isinstance(self.expires_at, datetime.datetime):
            expires_at = self.expires_at.isoformat()
        else:
            expires_at = self.expires_at

        decision: dict[str, Any] | None
        if isinstance(self.decision, DurableApprovalDecisionType0):
            decision = self.decision.to_dict()
        else:
            decision = self.decision

        details = self.details


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "status": status,
            "name": name,
            "title": title,
            "description": description,
            "function": function,
            "execution": execution,
            "requested_at": requested_at,
            "expires_at": expires_at,
            "decision": decision,
        })
        if details is not UNSET:
            field_dict["details"] = details

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.durable_approval_decision_type_0 import DurableApprovalDecisionType0 # noqa: PLC0415
        from ..models.durable_approval_execution import DurableApprovalExecution # noqa: PLC0415
        from ..models.durable_approval_function import DurableApprovalFunction # noqa: PLC0415
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        status = check_durable_approval_status(d.pop("status"))




        name = d.pop("name")

        title = d.pop("title")

        description = d.pop("description")

        function = DurableApprovalFunction.from_dict(d.pop("function"))




        execution = DurableApprovalExecution.from_dict(d.pop("execution"))




        requested_at = datetime.datetime.fromisoformat(d.pop("requested_at"))




        def _parse_expires_at(data: object) -> datetime.datetime | None:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                expires_at_type_0 = datetime.datetime.fromisoformat(data)



                return expires_at_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(datetime.datetime | None, data)

        expires_at = _parse_expires_at(d.pop("expires_at"))


        def _parse_decision(data: object) -> DurableApprovalDecisionType0 | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                componentsschemas_durable_approval_decision_type_0 = DurableApprovalDecisionType0.from_dict(data)



                return componentsschemas_durable_approval_decision_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(DurableApprovalDecisionType0 | None, data)

        decision = _parse_decision(d.pop("decision"))


        details = d.pop("details", UNSET)

        durable_approval = cls(
            id=id,
            status=status,
            name=name,
            title=title,
            description=description,
            function=function,
            execution=execution,
            requested_at=requested_at,
            expires_at=expires_at,
            decision=decision,
            details=details,
        )


        durable_approval.additional_properties = d
        return durable_approval

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
