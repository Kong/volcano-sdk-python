from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.frontend_custom_domain_redirect_request_status import check_frontend_custom_domain_redirect_request_status
from ..models.frontend_custom_domain_redirect_request_status import FrontendCustomDomainRedirectRequestStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="FrontendCustomDomainRedirectRequest")



@_attrs_define
class FrontendCustomDomainRedirectRequest:
    """ Redirects every request for the domain to `to`, another active domain of the same frontend that serves it, keeping
    the path and query string.

        Attributes:
            to (str): Hostname of an active domain of the same frontend that serves it. Example: www.example.com.
            status (FrontendCustomDomainRedirectRequestStatus | Unset): Redirect status. 301 and 308 are permanent, 302 and
                307 temporary; 307 and 308 keep the request method and body. Default: 308.
     """

    to: str
    status: FrontendCustomDomainRedirectRequestStatus | Unset = 308





    def to_dict(self) -> dict[str, Any]:
        to = self.to

        status: int | Unset = UNSET
        if not isinstance(self.status, Unset):
            status = self.status



        field_dict: dict[str, Any] = {}

        field_dict.update({
            "to": to,
        })
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        to = d.pop("to")

        _status = d.pop("status", UNSET)
        status: FrontendCustomDomainRedirectRequestStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_frontend_custom_domain_redirect_request_status(_status)




        frontend_custom_domain_redirect_request = cls(
            to=to,
            status=status,
        )

        return frontend_custom_domain_redirect_request

