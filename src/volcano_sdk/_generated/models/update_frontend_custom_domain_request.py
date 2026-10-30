from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest





T = TypeVar("T", bound="UpdateFrontendCustomDomainRequest")



@_attrs_define
class UpdateFrontendCustomDomainRequest:
    """ 
        Attributes:
            redirect (FrontendCustomDomainRedirectRequest | None): The redirect to set, or null to make the domain serve the
                frontend.
     """

    redirect: FrontendCustomDomainRedirectRequest | None





    def to_dict(self) -> dict[str, Any]:
        from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest # noqa: PLC0415
        redirect: dict[str, Any] | None
        if isinstance(self.redirect, FrontendCustomDomainRedirectRequest):
            redirect = self.redirect.to_dict()
        else:
            redirect = self.redirect


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "redirect": redirect,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.frontend_custom_domain_redirect_request import FrontendCustomDomainRedirectRequest # noqa: PLC0415
        d = dict(src_dict)
        def _parse_redirect(data: object) -> FrontendCustomDomainRedirectRequest | None:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                redirect_type_1 = FrontendCustomDomainRedirectRequest.from_dict(data)



                return redirect_type_1
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(FrontendCustomDomainRedirectRequest | None, data)

        redirect = _parse_redirect(d.pop("redirect"))


        update_frontend_custom_domain_request = cls(
            redirect=redirect,
        )

        return update_frontend_custom_domain_request

