from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.verified_domain import VerifiedDomain





T = TypeVar("T", bound="VerifiedDomainsResponse")



@_attrs_define
class VerifiedDomainsResponse:
    """ 
        Attributes:
            domains (list[VerifiedDomain]):
     """

    domains: list[VerifiedDomain]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.verified_domain import VerifiedDomain # noqa: PLC0415
        domains = []
        for domains_item_data in self.domains:
            domains_item = domains_item_data.to_dict()
            domains.append(domains_item)




        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "domains": domains,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.verified_domain import VerifiedDomain # noqa: PLC0415
        d = dict(src_dict)
        domains = []
        _domains = d.pop("domains")
        for domains_item_data in (_domains):
            domains_item = VerifiedDomain.from_dict(domains_item_data)



            domains.append(domains_item)


        verified_domains_response = cls(
            domains=domains,
        )


        verified_domains_response.additional_properties = d
        return verified_domains_response

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
