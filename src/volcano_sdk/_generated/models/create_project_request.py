from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="CreateProjectRequest")



@_attrs_define
class CreateProjectRequest:
    """ Request to create a new project

        Attributes:
            name (str): Project name (must be unique).
                Can only contain letters, numbers, underscores, and hyphens.
                 Example: my-awesome-app.
            all_regions (bool | Unset): Optional region policy.
                - `true` (default): project functions deploy to all configured regions
                - `false`: project deploys only to `selected_regions`
                 Default: True.
            selected_regions (list[str] | Unset): Optional region subset. Requires `all_regions=false`.
                Region names must be a subset of platform `AWS_REGIONS`.
                 Example: ['us-east-1', 'us-west-2'].
     """

    name: str
    all_regions: bool | Unset = True
    selected_regions: list[str] | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        all_regions = self.all_regions

        selected_regions: list[str] | Unset = UNSET
        if not isinstance(self.selected_regions, Unset):
            selected_regions = self.selected_regions




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
        })
        if all_regions is not UNSET:
            field_dict["all_regions"] = all_regions
        if selected_regions is not UNSET:
            field_dict["selected_regions"] = selected_regions

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        all_regions = d.pop("all_regions", UNSET)

        selected_regions = cast(list[str], d.pop("selected_regions", UNSET))


        create_project_request = cls(
            name=name,
            all_regions=all_regions,
            selected_regions=selected_regions,
        )


        create_project_request.additional_properties = d
        return create_project_request

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
