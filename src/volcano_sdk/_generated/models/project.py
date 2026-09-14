from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_plan import check_project_plan
from ..models.project_plan import ProjectPlan
from ..models.project_status import check_project_status
from ..models.project_status import ProjectStatus
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime






T = TypeVar("T", bound="Project")



@_attrs_define
class Project:
    """ 
        Attributes:
            id (UUID):
            name (str):
            status (ProjectStatus):
            all_regions (bool): Region policy for function deployment.
                - `true`: deploy functions to all configured platform regions
                - `false`: deploy only to `selected_regions`
            selected_regions (list[str]): Effective region set for this project (normalized and deduplicated)
            created_at (datetime.datetime):
            updated_at (datetime.datetime):
            plan (ProjectPlan | Unset): Platform plan applied to the project when available
            aws_application_name (str | Unset):
            last_invoked_at (datetime.datetime | Unset): Most recent activity timestamp across project resources
            logo_url (str | Unset): Relative API path that serves the project logo when one has been
                uploaded. The path is versioned with a `?v=` cache-busting query
                param that changes on each upload. Absent when the project has no
                logo. The logo image is stored in the project's storage folder.
                 Example: /projects/3fa85f64-5717-4562-b3fc-2c963f66afa6/logo?v=1718524800.
     """

    id: UUID
    name: str
    status: ProjectStatus
    all_regions: bool
    selected_regions: list[str]
    created_at: datetime.datetime
    updated_at: datetime.datetime
    plan: ProjectPlan | Unset = UNSET
    aws_application_name: str | Unset = UNSET
    last_invoked_at: datetime.datetime | Unset = UNSET
    logo_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        name = self.name

        status: str = self.status

        all_regions = self.all_regions

        selected_regions = self.selected_regions



        created_at = self.created_at.isoformat()

        updated_at = self.updated_at.isoformat()

        plan: str | Unset = UNSET
        if not isinstance(self.plan, Unset):
            plan = self.plan


        aws_application_name = self.aws_application_name

        last_invoked_at: str | Unset = UNSET
        if not isinstance(self.last_invoked_at, Unset):
            last_invoked_at = self.last_invoked_at.isoformat()

        logo_url = self.logo_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "id": id,
            "name": name,
            "status": status,
            "all_regions": all_regions,
            "selected_regions": selected_regions,
            "created_at": created_at,
            "updated_at": updated_at,
        })
        if plan is not UNSET:
            field_dict["plan"] = plan
        if aws_application_name is not UNSET:
            field_dict["aws_application_name"] = aws_application_name
        if last_invoked_at is not UNSET:
            field_dict["last_invoked_at"] = last_invoked_at
        if logo_url is not UNSET:
            field_dict["logo_url"] = logo_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))




        name = d.pop("name")

        status = check_project_status(d.pop("status"))




        all_regions = d.pop("all_regions")

        selected_regions = cast(list[str], d.pop("selected_regions"))


        created_at = datetime.datetime.fromisoformat(d.pop("created_at"))




        updated_at = datetime.datetime.fromisoformat(d.pop("updated_at"))




        _plan = d.pop("plan", UNSET)
        plan: ProjectPlan | Unset
        if isinstance(_plan,  Unset):
            plan = UNSET
        else:
            plan = check_project_plan(_plan)




        aws_application_name = d.pop("aws_application_name", UNSET)

        _last_invoked_at = d.pop("last_invoked_at", UNSET)
        last_invoked_at: datetime.datetime | Unset
        if isinstance(_last_invoked_at,  Unset):
            last_invoked_at = UNSET
        else:
            last_invoked_at = datetime.datetime.fromisoformat(_last_invoked_at)




        logo_url = d.pop("logo_url", UNSET)

        project = cls(
            id=id,
            name=name,
            status=status,
            all_regions=all_regions,
            selected_regions=selected_regions,
            created_at=created_at,
            updated_at=updated_at,
            plan=plan,
            aws_application_name=aws_application_name,
            last_invoked_at=last_invoked_at,
            logo_url=logo_url,
        )


        project.additional_properties = d
        return project

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
