from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from uuid import UUID






T = TypeVar("T", bound="CreateFrontendDeploymentRequest")



@_attrs_define
class CreateFrontendDeploymentRequest:
    """ Deploys the build of an existing deployment instead of compiling the frontend's source.

        Attributes:
            source_deployment_id (UUID): An `active` or `degraded` deployment of another frontend in the same project. Its
                build is copied to this frontend and published without compiling it again.
     """

    source_deployment_id: UUID





    def to_dict(self) -> dict[str, Any]:
        source_deployment_id = str(self.source_deployment_id)


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "source_deployment_id": source_deployment_id,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        source_deployment_id = UUID(d.pop("source_deployment_id"))




        create_frontend_deployment_request = cls(
            source_deployment_id=source_deployment_id,
        )

        return create_frontend_deployment_request

