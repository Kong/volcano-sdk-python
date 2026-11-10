from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.lavaflow_involved_resource_roles_item import check_lavaflow_involved_resource_roles_item
from ..models.lavaflow_involved_resource_roles_item import LavaflowInvolvedResourceRolesItem
from typing import cast

if TYPE_CHECKING:
  from ..models.lavaflow_resource_reference import LavaflowResourceReference





T = TypeVar("T", bound="LavaflowInvolvedResource")



@_attrs_define
class LavaflowInvolvedResource:
    """ A resource a run involves, and how.

        Attributes:
            resource (LavaflowResourceReference): A function, durable function or frontend in the project, or the project of
                a user-reported problem.
            roles (list[LavaflowInvolvedResourceRolesItem]): `issue`: the issue came from it. `cause`: the issue came from
                it, or code the diagnosis cites as evidence is in its source. `fix`: the diagnosis proposes changing its source,
                or the fix changes it; a change to code that every function shares involves every function.
     """

    resource: LavaflowResourceReference
    roles: list[LavaflowInvolvedResourceRolesItem]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        resource = self.resource.to_dict()

        roles = []
        for roles_item_data in self.roles:
            roles_item: str = roles_item_data
            roles.append(roles_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "resource": resource,
            "roles": roles,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.lavaflow_resource_reference import LavaflowResourceReference # noqa: PLC0415
        d = dict(src_dict)
        resource = LavaflowResourceReference.from_dict(d.pop("resource"))




        roles = []
        _roles = d.pop("roles")
        for roles_item_data in (_roles):
            roles_item = check_lavaflow_involved_resource_roles_item(roles_item_data)



            roles.append(roles_item)


        lavaflow_involved_resource = cls(
            resource=resource,
            roles=roles,
        )


        lavaflow_involved_resource.additional_properties = d
        return lavaflow_involved_resource

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
