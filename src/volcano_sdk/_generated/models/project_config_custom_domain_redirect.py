from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.project_config_custom_domain_redirect_status import check_project_config_custom_domain_redirect_status
from ..models.project_config_custom_domain_redirect_status import ProjectConfigCustomDomainRedirectStatus
from ..types import UNSET, Unset
from typing import cast






T = TypeVar("T", bound="ProjectConfigCustomDomainRedirect")



@_attrs_define
class ProjectConfigCustomDomainRedirect:
    """ 
        Attributes:
            to (str): Another domain in the same `custom_domains` list, without `redirect`.
            status (ProjectConfigCustomDomainRedirectStatus | Unset):  Default: 308.
     """

    to: str
    status: ProjectConfigCustomDomainRedirectStatus | Unset = 308





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
        status: ProjectConfigCustomDomainRedirectStatus | Unset
        if isinstance(_status,  Unset):
            status = UNSET
        else:
            status = check_project_config_custom_domain_redirect_status(_status)




        project_config_custom_domain_redirect = cls(
            to=to,
            status=status,
        )

        return project_config_custom_domain_redirect

