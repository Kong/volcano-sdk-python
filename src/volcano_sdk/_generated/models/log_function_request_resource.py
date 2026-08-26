from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.log_function_request_resource_type import check_log_function_request_resource_type
from ..models.log_function_request_resource_type import LogFunctionRequestResourceType
from ..types import UNSET, Unset
from typing import cast
from uuid import UUID

if TYPE_CHECKING:
  from ..models.log_deployment_request_selector import LogDeploymentRequestSelector





T = TypeVar("T", bound="LogFunctionRequestResource")



@_attrs_define
class LogFunctionRequestResource:
    """ Edge Function log resource selector.

        Attributes:
            type_ (LogFunctionRequestResourceType): Resource type to read logs for.
            ids (list[UUID] | Unset): Optional function identifiers. Omit or send an empty array to include every function
                in the project.
            deployments (LogDeploymentRequestSelector | Unset): Deployment log selector for deployable resources.
     """

    type_: LogFunctionRequestResourceType
    ids: list[UUID] | Unset = UNSET
    deployments: LogDeploymentRequestSelector | Unset = UNSET





    def to_dict(self) -> dict[str, Any]:
        from ..models.log_deployment_request_selector import LogDeploymentRequestSelector
        type_: str = self.type_

        ids: list[str] | Unset = UNSET
        if not isinstance(self.ids, Unset):
            ids = []
            for ids_item_data in self.ids:
                ids_item = str(ids_item_data)
                ids.append(ids_item)



        deployments: dict[str, Any] | Unset = UNSET
        if not isinstance(self.deployments, Unset):
            deployments = self.deployments.to_dict()


        field_dict: dict[str, Any] = {}

        field_dict.update({
            "type": type_,
        })
        if ids is not UNSET:
            field_dict["ids"] = ids
        if deployments is not UNSET:
            field_dict["deployments"] = deployments

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.log_deployment_request_selector import LogDeploymentRequestSelector
        d = dict(src_dict)
        type_ = check_log_function_request_resource_type(d.pop("type"))




        _ids = d.pop("ids", UNSET)
        ids: list[UUID] | Unset = UNSET
        if _ids is not UNSET:
            ids = []
            for ids_item_data in _ids:
                ids_item = UUID(ids_item_data)



                ids.append(ids_item)


        _deployments = d.pop("deployments", UNSET)
        deployments: LogDeploymentRequestSelector | Unset
        if isinstance(_deployments,  Unset):
            deployments = UNSET
        else:
            deployments = LogDeploymentRequestSelector.from_dict(_deployments)




        log_function_request_resource = cls(
            type_=type_,
            ids=ids,
            deployments=deployments,
        )

        return log_function_request_resource

