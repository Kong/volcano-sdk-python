from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.project_config_scheduler import ProjectConfigScheduler





T = TypeVar("T", bound="ProjectConfigFunction")



@_attrs_define
class ProjectConfigFunction:
    """ Configuration for an existing (deployed) function. Functions are never
    created or deleted through the manifest. When `schedulers` is declared
    it is fully synced (schedulers absent from the list are deleted);
    omitting `schedulers` leaves the function's schedulers untouched.

        Attributes:
            name (str):
            public (bool | Unset): Function visibility for anon-key invocation
            schedulers (list[ProjectConfigScheduler] | Unset):
     """

    name: str
    public: bool | Unset = UNSET
    schedulers: list[ProjectConfigScheduler] | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.project_config_scheduler import ProjectConfigScheduler
        name = self.name

        public = self.public

        schedulers: list[dict[str, Any]] | Unset = UNSET
        if not isinstance(self.schedulers, Unset):
            schedulers = []
            for schedulers_item_data in self.schedulers:
                schedulers_item = schedulers_item_data.to_dict()
                schedulers.append(schedulers_item)




        field_dict: dict[str, Any] = {}

        field_dict.update({
            "name": name,
        })
        if public is not UNSET:
            field_dict["public"] = public
        if schedulers is not UNSET:
            field_dict["schedulers"] = schedulers

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.project_config_scheduler import ProjectConfigScheduler
        d = dict(src_dict)
        name = d.pop("name")

        public = d.pop("public", UNSET)

        _schedulers = d.pop("schedulers", UNSET)
        schedulers: list[ProjectConfigScheduler] | Unset = UNSET
        if _schedulers is not UNSET:
            schedulers = []
            for schedulers_item_data in _schedulers:
                schedulers_item = ProjectConfigScheduler.from_dict(schedulers_item_data)



                schedulers.append(schedulers_item)


        project_config_function = cls(
            name=name,
            public=public,
            schedulers=schedulers,
        )

        return project_config_function

