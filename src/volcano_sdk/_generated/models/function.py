from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.function_status import check_function_status
from ..models.function_status import FunctionStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="Function")



@_attrs_define
class Function:
    """ 
        Attributes:
            id (UUID):
            project_id (UUID):
            name (str):
            status (FunctionStatus):
            is_public (bool): Function visibility for anon-key invocation.
                - `false` (default): only auth user tokens and service keys can invoke
                - `true`: anon keys with `functions.invoke` can invoke
            deployed_regions (list[str]): Regions where this function is currently deployed
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            provisioning_started_at (datetime.datetime | Unset): Timestamp when the current provisioning phase started
            aws_function_arn (str | Unset):
            invoke_url (str | Unset): Canonical GeoDNS endpoint URL for invoking this function (always HTTPS)
            runtime (str | Unset):
            handler (str | Unset):
            current_deployment_id (UUID | Unset): Identifier of the latest function deployment operation
            pending_deployment_id (UUID | Unset): Newest queued deployment that will run after the current operation
            last_invoked_at (datetime.datetime | Unset): Most recent successful invocation timestamp
     """

    id: UUID
    project_id: UUID
    name: str
    status: FunctionStatus
    is_public: bool
    deployed_regions: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    provisioning_started_at: datetime.datetime | Unset = UNSET
    aws_function_arn: str | Unset = UNSET
    invoke_url: str | Unset = UNSET
    runtime: str | Unset = UNSET
    handler: str | Unset = UNSET
    current_deployment_id: UUID | Unset = UNSET
    pending_deployment_id: UUID | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        project_id = str(self.project_id)

        name = self.name

        status: str = self.status

        is_public = self.is_public

        deployed_regions = self.deployed_regions



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        provisioning_started_at: str | Unset = UNSET
        if not isinstance(self.provisioning_started_at, Unset):
            provisioning_started_at = self.provisioning_started_at.isoformat()

        aws_function_arn = self.aws_function_arn

        invoke_url = self.invoke_url

        runtime = self.runtime

        handler = self.handler

        current_deployment_id: str | Unset = UNSET
        if not isinstance(self.current_deployment_id, Unset):
            current_deployment_id = str(self.current_deployment_id)

        pending_deployment_id: str | Unset = UNSET
        if not isinstance(self.pending_deployment_id, Unset):
            pending_deployment_id = str(self.pending_deployment_id)

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "project_id": project_id,
            "name": name,
            "status": status,
            "is_public": is_public,
            "deployed_regions": deployed_regions,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if provisioning_started_at is not UNSET:
            field_dict["provisioning_started_at"] = provisioning_started_at
        if aws_function_arn is not UNSET:
            field_dict["aws_function_arn"] = aws_function_arn
        if invoke_url is not UNSET:
            field_dict["invoke_url"] = invoke_url
        if runtime is not UNSET:
            field_dict["runtime"] = runtime
        if handler is not UNSET:
            field_dict["handler"] = handler
        if current_deployment_id is not UNSET:
            field_dict["current_deployment_id"] = current_deployment_id
        if pending_deployment_id is not UNSET:
            field_dict["pending_deployment_id"] = pending_deployment_id
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        project_id = UUID(d.pop("project_id"))




        name = d.pop("name")

        status = check_function_status(d.pop("status"))




        is_public = d.pop("is_public")

        deployed_regions = cast(list[str], d.pop("deployed_regions"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _provisioning_started_at = d.pop("provisioning_started_at", UNSET)
        provisioning_started_at: datetime.datetime | Unset
        if isinstance(_provisioning_started_at,  Unset):
            provisioning_started_at = UNSET
        else:
            provisioning_started_at = datetime.datetime.fromisoformat(_provisioning_started_at)




        aws_function_arn = d.pop("aws_function_arn", UNSET)

        invoke_url = d.pop("invoke_url", UNSET)

        runtime = d.pop("runtime", UNSET)

        handler = d.pop("handler", UNSET)

        _current_deployment_id = d.pop("current_deployment_id", UNSET)
        current_deployment_id: UUID | Unset
        if isinstance(_current_deployment_id,  Unset):
            current_deployment_id = UNSET
        else:
            current_deployment_id = UUID(_current_deployment_id)




        _pending_deployment_id = d.pop("pending_deployment_id", UNSET)
        pending_deployment_id: UUID | Unset
        if isinstance(_pending_deployment_id,  Unset):
            pending_deployment_id = UNSET
        else:
            pending_deployment_id = UUID(_pending_deployment_id)




        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        function = cls(
            id=id,
            project_id=project_id,
            name=name,
            status=status,
            is_public=is_public,
            deployed_regions=deployed_regions,
            created_at=created_at,
            updated_at=updated_at,
            provisioning_started_at=provisioning_started_at,
            aws_function_arn=aws_function_arn,
            invoke_url=invoke_url,
            runtime=runtime,
            handler=handler,
            current_deployment_id=current_deployment_id,
            pending_deployment_id=pending_deployment_id,
            last_invoked_at=last_invoked_at,
        )


        function.additional_properties = d
        return function

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
