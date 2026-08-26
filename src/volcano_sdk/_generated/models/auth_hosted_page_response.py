from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.auth_hosted_page import AuthHostedPage
  from ..models.auth_hosted_page_defaults import AuthHostedPageDefaults
  from ..models.auth_hosted_page_runtime import AuthHostedPageRuntime





T = TypeVar("T", bound="AuthHostedPageResponse")



@_attrs_define
class AuthHostedPageResponse:
    """ 
        Attributes:
            page (AuthHostedPage | None): The saved page, or null when the project has not customized this page type yet.
            defaults (AuthHostedPageDefaults): The starting point for an unsaved page: the theme shell we render for the
                built-in page plus its stylesheet. Valid input to the update endpoint —
                it carries no script, meta, or link tags.
            runtime (AuthHostedPageRuntime): The server-owned behavior of a hosted page. Clients compose previews from
                this instead of reimplementing the page, so a preview cannot drift from
                what is actually served.
     """

    page: AuthHostedPage | None
    defaults: AuthHostedPageDefaults
    runtime: AuthHostedPageRuntime
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.auth_hosted_page import AuthHostedPage
        from ..models.auth_hosted_page_defaults import AuthHostedPageDefaults
        from ..models.auth_hosted_page_runtime import AuthHostedPageRuntime
        page: dict[str, Any] | None
        if isinstance(self.page, AuthHostedPage):
            page = self.page.to_dict()
        else:
            page = self.page

        defaults = self.defaults.to_dict()

        runtime = self.runtime.to_dict()


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "page": page,
            "defaults": defaults,
            "runtime": runtime,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.auth_hosted_page import AuthHostedPage
        from ..models.auth_hosted_page_defaults import AuthHostedPageDefaults
        from ..models.auth_hosted_page_runtime import AuthHostedPageRuntime
        d = dict(src_dict)
        def _parse_page(data: object) -> AuthHostedPage | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                page_type_1 = AuthHostedPage.from_dict(data)



                return page_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(AuthHostedPage | None, data)

        page = _parse_page(d.pop("page"))


        defaults = AuthHostedPageDefaults.from_dict(d.pop("defaults"))




        runtime = AuthHostedPageRuntime.from_dict(d.pop("runtime"))




        auth_hosted_page_response = cls(
            page=page,
            defaults=defaults,
            runtime=runtime,
        )


        auth_hosted_page_response.additional_properties = d
        return auth_hosted_page_response

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
