from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset







T = TypeVar("T", bound="AuthHostedPageRuntime")



@_attrs_define
class AuthHostedPageRuntime:
    """ The server-owned behavior of a hosted page. Clients compose previews from
    this instead of reimplementing the page, so a preview cannot drift from
    what is actually served.

        Attributes:
            root_id (str): Element id the runtime script renders into. Markup carrying it opts into the theme-shell
                contract.
            script (str): The runtime script injected into the rendered page.
            mock_prelude (str): Preview harness that supplies request params and stubs the hosted-auth API. Never served on
                a real page.
     """

    root_id: str
    script: str
    mock_prelude: str
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        root_id = self.root_id

        script = self.script

        mock_prelude = self.mock_prelude


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "root_id": root_id,
            "script": script,
            "mock_prelude": mock_prelude,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        root_id = d.pop("root_id")

        script = d.pop("script")

        mock_prelude = d.pop("mock_prelude")

        auth_hosted_page_runtime = cls(
            root_id=root_id,
            script=script,
            mock_prelude=mock_prelude,
        )


        auth_hosted_page_runtime.additional_properties = d
        return auth_hosted_page_runtime

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
