from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.variable_deploy_source import check_variable_deploy_source
from ..models.variable_deploy_source import VariableDeploySource
from ..models.variable_status import check_variable_status
from ..models.variable_status import VariableStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="Variable")



@_attrs_define
class Variable:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            value (str):
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            status (VariableStatus | Unset): Latest project variable propagation status, when a sync has run.
            current_sync_id (UUID | Unset): Identifier of the latest variable propagation sync.
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current variable propagation phase
                started.
            deploy_source (VariableDeploySource | Unset): What initiated the latest variable propagation sync, when one has
                run.
     """

    id: UUID
    project_id: UUID
    name: str
    value: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    status: VariableStatus | Unset = UNSET
    current_sync_id: UUID | Unset = UNSET
    provisioning_started_at: datetime.datetime | Unset = UNSET
    deploy_source: VariableDeploySource | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        value = self.value

        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        status: str | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status


        current_sync_id: str | Unset = UNSET
        if not isinstance(self.current_sync_id, Unset):
            current_sync_id = str(self.current_sync_id)

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()

        deploy_source: str | Unset = UNSET
        if not isinstance(self.deploy_source, Unset):
            deploy_source = self.deploy_source



        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "value": value,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if status is not UNSET:
            field_dict["status"] = status
        if current_sync_id is not UNSET:
            field_dict["current_sync_id"] = current_sync_id
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at
        if deploy_source is not UNSET:
            field_dict["deploy_source"] = deploy_source

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        value = d.pop("value")

        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _status = d.pop("status", UNSET)
        status: VariableStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_variable_status(_status)




        _current_sync_id = d.pop("current_sync_id", UNSET)
        current_sync_id: UUID | Unset
        if isinstance(_current_sync_id,  Unset):
            current_sync_id = UNSET
        else:
            current_sync_id = UUID(_current_sync_id)




        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        _deploy_source = d.pop("deploy_source", UNSET)
        deploy_source: VariableDeploySource | Unset
        if isinstance(_deploy_source,  Unset):
            deploy_source = UNSET
        else:
            deploy_source = check_variable_deploy_source(_deploy_source)




        variable = cls(
            id=id,
            project_id=project_id,
            name=name,
            value=value,
            created_at=created_at,
            updated_at=updated_at,
            status=status,
            current_sync_id=current_sync_id,
            provisioning_started_at=provisioning_started_at,
            deploy_source=deploy_source,
        )


        variable.additional_properties = d
        return variable

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
