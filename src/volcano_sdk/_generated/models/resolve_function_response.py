from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..types import UNSET, Unset
from uuid import UUID






T = TypeVar("T", bound="ResolveFunctionResponse")



@_attrs_define
class ResolveFunctionResponse:
    """ 
        Attributes:
            name (str): DNS-safe function name
            function_id (UUID): Canonical function ID used for invocation routing
            cache_ttl_seconds (int): Suggested SDK cache TTL for this name-to-ID mapping
            invoke_url (str | Unset): Canonical HTTPS endpoint for invoking this function. Use it as-is: it does not share a
                domain with the API, so a host derived from the API URL will not reach the function. Omitted when the deployment
                serves no public invocation domain, as in local development; invoke through POST /functions/{functionId}/invoke
                instead.
     """

    name: str
    function_id: UUID
    cache_ttl_seconds: int
    invoke_url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        name = self.name

        function_id = str(self.function_id)

        cache_ttl_seconds = self.cache_ttl_seconds

        invoke_url = self.invoke_url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "name": name,
            "function_id": function_id,
            "cache_ttl_seconds": cache_ttl_seconds,
        })
        if invoke_url is not UNSET:
            field_dict["invoke_url"] = invoke_url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        name = d.pop("name")

        function_id = UUID(d.pop("function_id"))




        cache_ttl_seconds = d.pop("cache_ttl_seconds")

        invoke_url = d.pop("invoke_url", UNSET)

        resolve_function_response = cls(
            name=name,
            function_id=function_id,
            cache_ttl_seconds=cache_ttl_seconds,
            invoke_url=invoke_url,
        )


        resolve_function_response.additional_properties = d
        return resolve_function_response

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
