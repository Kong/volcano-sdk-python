from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.auth_identity import AuthIdentity





T = TypeVar("T", bound="AuthIdentitiesResponse")



@_attrs_define
class AuthIdentitiesResponse:
    """ 
        Attributes:
            identities (list[AuthIdentity]):
     """

    identities: list[AuthIdentity]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_identity import AuthIdentity
        identities = []
        for identities_item_data in self.identities:
            identities_item = identities_item_data.to_dict()
            identities.append(identities_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "identities": identities,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_identity import AuthIdentity
        d = dict(src_dict)
        identities = []
        _identities = d.pop("identities")
        for identities_item_data in (_identities):
            identities_item = AuthIdentity.from_dict(identities_item_data)



            identities.append(identities_item)


        auth_identities_response = cls(
            identities=identities,
        )


        auth_identities_response.additional_properties = d
        return auth_identities_response

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
